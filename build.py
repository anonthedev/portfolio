#!/usr/bin/env python3
"""Build the blog from markdown files in posts/.

Add a note:

    posts/my-note.md

    ---
    title: my note
    date: 2026-11-23
    description: one line on what this is.
    ---

    The note, in markdown.

Then run:

    python3 build.py

The filename is the URL: posts/my-note.md becomes /blog/my-note/.
Files named _*.md, and posts with `draft: true`, are not published.
Each post gets its own share image at /blog/<slug>/og.png.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://anonthedev.xyz"
POSTS = ROOT / "posts"
BLOG = ROOT / "blog"
RESUME = "https://drive.google.com/file/d/19a5pm2cy9TrVS72FmJt1GjBqxsj1Bj41/view?usp=sharing"
OG_ALT = "Pranav Kumar. hey, i'm pranav. i engineer applied ai systems."
FOOTER = "© 2026 pranav kumar · built in india · updated november 2026"
MONTHS = "jan feb mar apr may jun jul aug sep oct nov dec".split()

LIST_RE = re.compile(r"^( *)([-*]|\d+\.)\s+(\S.*)$")
HEADING_RE = re.compile(r"^(#{1,4})\s+(\S.*)$")
HR_RE = re.compile(r"^(\*\*\*|---|___)\s*$")
SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
FENCE_RE = re.compile(r"^(```|~~~)")


@dataclass
class Post:
    slug: str
    title: str
    description: str
    date: dt.date
    body_html: str
    image: str | None
    source: str

    @property
    def date_label(self) -> str:
        return f"{self.date.day} {MONTHS[self.date.month - 1]} {self.date.year}"

    @property
    def url(self) -> str:
        return f"{SITE}/blog/{self.slug}/"

    @property
    def image_url(self) -> str:
        return f"{SITE}/blog/{self.slug}/og.png"

    @property
    def image_alt(self) -> str:
        return f"{self.title} — Pranav Kumar, {self.date_label}"


def esc(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_inline(text: str) -> str:
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "\\" and i + 1 < n:
            out.append(esc(text[i + 1]))
            i += 2
            continue
        if ch == "`":
            j = text.find("`", i + 1)
            if j != -1:
                out.append(f"<code>{esc(text[i + 1 : j])}</code>")
                i = j + 1
                continue
        if text.startswith("***", i):
            j = text.find("***", i + 3)
            if j != -1 and j > i + 3:
                out.append(f"<strong><em>{render_inline(text[i + 3 : j])}</em></strong>")
                i = j + 3
                continue
        if text.startswith(("**", "__"), i):
            delim = text[i : i + 2]
            j = text.find(delim, i + 2)
            if j != -1 and j > i + 2:
                out.append(f"<strong>{render_inline(text[i + 2 : j])}</strong>")
                i = j + 2
                continue
        if ch == "[":
            html, nxt = try_link(text, i, image=False)
            if html is not None:
                out.append(html)
                i = nxt
                continue
        if ch == "!" and i + 1 < n and text[i + 1] == "[":
            html, nxt = try_link(text, i + 1, image=True)
            if html is not None:
                out.append(html)
                i = nxt
                continue
        if ch == "*" or (ch == "_" and (i == 0 or not text[i - 1].isalnum())):
            j = find_emph_closer(text, i, ch)
            if j is not None:
                out.append(f"<em>{render_inline(text[i + 1 : j])}</em>")
                i = j + 1
                continue
        out.append(esc(ch))
        i += 1
    return "".join(out)


def find_emph_closer(text: str, start: int, delim: str) -> int | None:
    j = start + 1
    n = len(text)
    while j < n:
        if text[j] == "\\":
            j += 2
            continue
        if text[j] == "\n":
            return None
        if text[j] == delim:
            if delim == "*" and j + 1 < n and text[j + 1] == "*":
                j += 2
                continue
            if delim == "_" and j + 1 < n and text[j + 1].isalnum():
                j += 1
                continue
            if j == start + 1:
                return None
            return j
        j += 1
    return None


def try_link(text: str, start: int, image: bool) -> tuple[str | None, int]:
    if start >= len(text) or text[start] != "[":
        return None, start
    j = start + 1
    while j < len(text):
        if text[j] == "\\":
            j += 2
            continue
        if text[j] == "\n":
            return None, start
        if text[j] == "]":
            break
        j += 1
    else:
        return None, start
    if j + 1 >= len(text) or text[j + 1] != "(":
        return None, start
    k = text.find(")", j + 2)
    if k == -1:
        return None, start
    label = text[start + 1 : j]
    href = text[j + 2 : k].strip()
    if " " in href:
        href = href.split()[0]
    if not href or href.lower().startswith(("javascript:", "data:", "vbscript:")):
        return None, start
    if image:
        return f'<img src="{esc(href)}" alt="{esc(label)}">', k + 1
    external = href.lower().startswith(("http://", "https://", "//"))
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ""
    return f'<a href="{esc(href)}"{attrs}>{render_inline(label)}</a>', k + 1


def is_boundary(line: str) -> bool:
    if line.strip() == "":
        return True
    if FENCE_RE.match(line):
        return True
    if HEADING_RE.match(line):
        return True
    if LIST_RE.match(line) and len(LIST_RE.match(line).group(1)) == 0:
        return True
    if line.lstrip().startswith(">"):
        return True
    if HR_RE.match(line):
        return True
    return False


def render_markdown(source: str) -> str:
    lines = source.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return render_blocks(lines).strip()


def render_blocks(lines: list[str]) -> str:
    html: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.strip() == "":
            i += 1
            continue
        fence = FENCE_RE.match(line)
        if fence:
            token = fence.group(1)
            info = line[len(token) :].strip().split()
            lang = info[0] if info and re.fullmatch(r"[A-Za-z0-9_+-]+", info[0]) else ""
            i += 1
            buf: list[str] = []
            while i < n and not lines[i].startswith(token):
                buf.append(lines[i])
                i += 1
            if i < n:
                i += 1
            klass = f' class="language-{lang}"' if lang else ""
            html.append(f"<pre><code{klass}>{esc(chr(10).join(buf))}</code></pre>")
            continue
        heading = HEADING_RE.match(line)
        if heading:
            level = 2 if len(heading.group(1)) <= 2 else 3
            html.append(f"<h{level}>{render_inline(heading.group(2).strip())}</h{level}>")
            i += 1
            continue
        if LIST_RE.match(line) and len(LIST_RE.match(line).group(1)) == 0:
            block, i = parse_list(lines, i, 0)
            html.append(block)
            continue
        if line.lstrip().startswith(">"):
            quoted: list[str] = []
            while i < n and lines[i].lstrip().startswith(">"):
                quoted.append(re.sub(r"^\s*>\s?", "", lines[i], count=1))
                i += 1
            html.append(f"<blockquote>\n{render_blocks(quoted)}\n</blockquote>")
            continue
        if HR_RE.match(line):
            html.append("<hr>")
            i += 1
            continue
        chunk = [line]
        i += 1
        while i < n and not is_boundary(lines[i]):
            chunk.append(lines[i])
            i += 1
        pieces: list[str] = []
        for idx, part in enumerate(chunk):
            pieces.append(render_inline(part.strip()))
            if idx != len(chunk) - 1:
                pieces.append("<br>" if part.endswith("  ") else " ")
        html.append(f"<p>{''.join(pieces)}</p>")
    return "\n".join(html)


def parse_list(lines: list[str], i: int, indent: int) -> tuple[str, int]:
    items: list[str] = []
    kind: str | None = None
    n = len(lines)
    while i < n:
        if lines[i].strip() == "":
            j = i + 1
            while j < n and lines[j].strip() == "":
                j += 1
            nxt = LIST_RE.match(lines[j]) if j < n else None
            if nxt and len(nxt.group(1)) == indent:
                i = j
            else:
                break
        if i >= n:
            break
        match = LIST_RE.match(lines[i])
        if not match or len(match.group(1)) != indent:
            break
        this = "ol" if match.group(2)[0].isdigit() else "ul"
        if kind is None:
            kind = this
        elif this != kind:
            break
        parts = [match.group(3).strip()]
        i += 1
        nested = ""
        while i < n and lines[i].strip() != "":
            child = LIST_RE.match(lines[i])
            if child and len(child.group(1)) > indent:
                nested_html, i = parse_list(lines, i, len(child.group(1)))
                nested += nested_html
                continue
            if child and len(child.group(1)) <= indent:
                break
            if is_boundary(lines[i]) and not lines[i].startswith(" "):
                break
            parts.append(lines[i].strip())
            i += 1
        items.append(f"<li>{render_inline(' '.join(parts))}{nested}</li>")
    tag = kind or "ul"
    return f"<{tag}>{''.join(items)}</{tag}>", i


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    text = text.lstrip("\ufeff")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("frontmatter must start with ---")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise ValueError("frontmatter is missing a closing ---")
    meta: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"bad frontmatter line: {line}")
        key, value = line.split(":", 1)
        meta[key.strip().lower()] = value.strip().strip('"').strip("'")
    body = "\n".join(lines[end + 1 :]).lstrip("\n")
    return meta, body


def load_posts() -> list[Post]:
    if not POSTS.exists():
        return []
    posts: list[Post] = []
    seen: set[str] = set()
    for path in sorted(POSTS.glob("*.md")):
        if path.name.startswith("_") or path.name.lower() == "readme.md":
            print(f"skip {path.relative_to(ROOT)}")
            continue
        try:
            meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            raise SystemExit(f"{path.relative_to(ROOT)}: {exc}") from exc
        if meta.get("draft", "").lower() in {"true", "yes", "1"}:
            print(f"skip draft {path.relative_to(ROOT)}")
            continue
        slug = path.stem
        if not SLUG_RE.fullmatch(slug) or slug in {"index", "feed"}:
            raise SystemExit(
                f"{path.name}: rename to lowercase words separated by hyphens"
            )
        if slug in seen:
            raise SystemExit(f"duplicate slug: {slug}")
        seen.add(slug)
        missing = [key for key in ("title", "date", "description") if not meta.get(key)]
        if missing:
            raise SystemExit(f"{path.name}: missing {', '.join(missing)}")
        try:
            date = dt.date.fromisoformat(meta["date"])
        except ValueError as exc:
            raise SystemExit(f"{path.name}: date must be YYYY-MM-DD") from exc
        posts.append(
            Post(
                slug=slug,
                title=meta["title"],
                description=meta["description"],
                date=date,
                body_html=render_markdown(body),
                image=meta.get("image") or None,
                source=path.name,
            )
        )
    posts.sort(key=lambda post: post.slug)
    posts.sort(key=lambda post: post.date, reverse=True)
    return posts


def write_if_changed(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return
    path.write_text(content, encoding="utf-8")


def replace_block(path: Path, pattern: str, replacement: str) -> None:
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"{path.name}: missing marker for {pattern}")
    write_if_changed(path, updated)


def update_home(posts: list[Post]) -> None:
    if posts:
        items = []
        for post in posts[:4]:
            items.append(
                "\n".join(
                    [
                        "          <li>",
                        f'            <a href="/blog/{post.slug}/">',
                        f'              <p class="post-kicker"><time datetime="{post.date.isoformat()}">{esc(post.date_label)}</time></p>',
                        f'              <h3 class="post-title">{esc(post.title)}</h3>',
                        f'              <p class="post-desc">{esc(post.description)}</p>',
                        "            </a>",
                        "          </li>",
                    ]
                )
            )
        block = "\n".join(
            [
                "<!-- writing:start -->",
                '      <section id="writing" class="section" aria-labelledby="writing-heading">',
                '        <p class="section-label">04 · writing</p>',
                '        <h2 id="writing-heading" class="section-title">notes from the work.</h2>',
                '        <ol class="writing-list">',
                *items,
                "        </ol>",
                '        <p class="links"><a href="/blog/">all writing</a></p>',
                "      </section>",
                "      <!-- writing:end -->",
            ]
        )
        hello_num = "05"
    else:
        block = "<!-- writing:start -->\n      <!-- writing:end -->"
        hello_num = "04"
    index = ROOT / "index.html"
    text = index.read_text(encoding="utf-8")
    text, count = re.subn(
        r"<!-- writing:start -->.*?<!-- writing:end -->",
        block,
        text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit("index.html: missing writing markers")
    text, count = re.subn(
        r'(id="hello-label">)\d+( · hello)',
        rf"\g<1>{hello_num}\2",
        text,
        count=1,
    )
    if count != 1:
        raise SystemExit("index.html: missing hello label")
    write_if_changed(index, text)


def update_llms(posts: list[Post]) -> None:
    if posts:
        lines = ["<!-- writing-posts:start -->"]
        for post in posts:
            lines.append(f"- [{post.title}]({post.url}): {post.description}")
        lines.append("<!-- writing-posts:end -->")
        block = "\n".join(lines)
    else:
        block = "<!-- writing-posts:start -->\n<!-- writing-posts:end -->"
    replace_block(
        ROOT / "llms.txt",
        r"<!-- writing-posts:start -->.*?<!-- writing-posts:end -->",
        block,
    )


def nav(current: str | None) -> str:
    def item(href: str, label: str, key: str) -> str:
        current_attr = ' aria-current="page"' if current == key else ""
        return f'<li><a href="{href}"{current_attr}>{label}</a></li>'

    return f"""<header class="site-header">
      <nav class="nav" aria-label="Primary">
        <a class="nav-brand" href="/">pranav</a>
        <ul class="nav-items">
          {item("/#work", "work", "work")}
          {item("/#experience", "experience", "experience")}
          {item("/#toolkit", "toolkit", "toolkit")}
          {item("/blog/", "writing", "writing")}
          {item("/#hello", "hello", "hello")}
          <li>
            <a class="nav-resume" target="_blank" rel="noopener noreferrer" href="{RESUME}">resume</a>
          </li>
        </ul>
      </nav>
    </header>"""


def page(
    *,
    title: str,
    description: str,
    canonical: str,
    body: str,
    og_type: str,
    image: str,
    image_alt: str,
    json_ld: dict,
    extra_meta: str = "",
) -> str:
    dims = ""
    if image.startswith(f"{SITE}/") and image.endswith(".png"):
        dims = """
    <meta property="og:image:type" content="image/png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />"""
    payload = json.dumps(json_ld, ensure_ascii=False, indent=2).replace("<", "\\u003c")
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(description)}" />
    <meta name="author" content="Pranav Kumar" />
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />
    <meta name="theme-color" content="#121212" />
    <link rel="canonical" href="{esc(canonical)}" />
    <link rel="alternate" type="application/rss+xml" title="Writing" href="/blog/feed.xml" />
    <meta property="og:type" content="{esc(og_type)}" />
    <meta property="og:site_name" content="Pranav Kumar" />
    <meta property="og:title" content="{esc(title)}" />
    <meta property="og:description" content="{esc(description)}" />
    <meta property="og:url" content="{esc(canonical)}" />
    <meta property="og:locale" content="en_IN" />
    <meta property="og:image" content="{esc(image)}" />{dims}
    <meta property="og:image:alt" content="{esc(image_alt)}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:creator" content="@anonthedev" />
    <meta name="twitter:title" content="{esc(title)}" />
    <meta name="twitter:description" content="{esc(description)}" />
    <meta name="twitter:image" content="{esc(image)}" />
    <meta name="twitter:image:alt" content="{esc(image_alt)}" />{extra_meta}
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
    <link rel="manifest" href="/site.webmanifest" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="/style.css" />
    <script type="application/ld+json">
{payload}
    </script>
  </head>
  <body>
    <a class="skip-link" href="#top">Skip to content</a>
    {nav("writing")}
    <main id="top" class="main-content">
{body}
    </main>
    <footer class="site-footer">
      <p>{FOOTER}</p>
    </footer>
  </body>
</html>
"""


def font_file(name: str) -> Path:
    cache = Path("/tmp/poppins")
    cache.mkdir(exist_ok=True)
    path = cache / name
    if path.exists() and path.stat().st_size > 1000:
        return path
    url = f"https://github.com/google/fonts/raw/main/ofl/poppins/{name}"
    import urllib.request

    urllib.request.urlretrieve(url, path)
    return path


def render_post_og(post: Post, dest: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    width, height = 1200, 630
    scale = 2
    image = Image.new("RGB", (width * scale, height * scale), "#121212")
    draw = ImageDraw.Draw(image)
    text = "#e0e2dc"
    muted = "#a3a3a3"
    accent = "#ffc42c"
    pad = 84 * scale
    max_width = (width - 168) * scale

    def measure(font, value: str) -> int:
        box = draw.textbbox((0, 0), value, font=font)
        return box[2] - box[0]

    def wrap(value: str, font) -> list[str]:
        lines: list[str] = []
        current = ""
        for word in value.split():
            trial = word if not current else f"{current} {word}"
            if measure(font, trial) <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines or [""]

    size = 72
    title_font = ImageFont.truetype(font_file("Poppins-Medium.ttf"), size * scale)
    lines = wrap(post.title, title_font)
    while (len(lines) > 3 or any(measure(title_font, line) > max_width for line in lines)) and size > 46:
        size -= 4
        title_font = ImageFont.truetype(font_file("Poppins-Medium.ttf"), size * scale)
        lines = wrap(post.title, title_font)

    meta_font = ImageFont.truetype(font_file("Poppins-Regular.ttf"), 24 * scale)
    domain_font = ImageFont.truetype(font_file("Poppins-Regular.ttf"), 22 * scale)

    meta_y = 92 * scale
    draw.text((pad, meta_y), "Pranav Kumar", font=meta_font, fill=muted)
    date = post.date_label
    draw.text((width * scale - pad - measure(meta_font, date), meta_y), date, font=meta_font, fill=muted)

    rule_y = meta_y + 24 * scale + 26 * scale
    draw.rectangle((pad, rule_y, pad + 42 * scale, rule_y + 4 * scale), fill=accent)

    line_height = int(size * scale * 1.16)
    title_y = rule_y + 4 * scale + 32 * scale
    for index, line in enumerate(lines[:4]):
        draw.text((pad, title_y + index * line_height), line, font=title_font, fill=text)

    domain = "anonthedev.xyz"
    draw.text((pad, height * scale - 72 * scale - 22 * scale), domain, font=domain_font, fill=muted)

    dest.parent.mkdir(parents=True, exist_ok=True)
    image.resize((width, height), Image.Resampling.LANCZOS).save(dest, "PNG", optimize=True)


def write_blog(posts: list[Post]) -> None:
    BLOG.mkdir(exist_ok=True)
    live = {post.slug for post in posts}
    for child in BLOG.iterdir():
        if child.is_dir() and child.name not in live:
            shutil.rmtree(child)

    if posts:
        items = []
        for post in posts:
            items.append(
                "\n".join(
                    [
                        "          <li>",
                        f'            <a href="/blog/{post.slug}/">',
                        f'              <p class="post-kicker"><time datetime="{post.date.isoformat()}">{esc(post.date_label)}</time></p>',
                        f'              <h2 class="post-title">{esc(post.title)}</h2>',
                        f'              <p class="post-desc">{esc(post.description)}</p>',
                        "            </a>",
                        "          </li>",
                    ]
                )
            )
        listing = (
            '        <ol class="writing-list">\n'
            + "\n".join(items)
            + "\n        </ol>"
        )
    else:
        listing = '        <p class="empty-note">nothing posted yet.</p>'

    description = "Notes on retrieval, queues, and the infrastructure under LLMs."
    graph: dict = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "@id": f"{SITE}/blog/#blog",
        "url": f"{SITE}/blog/",
        "name": "Writing by Pranav Kumar",
        "description": description,
        "inLanguage": "en",
        "author": {"@id": f"{SITE}/#pranav"},
        "image": f"{SITE}/og.png",
    }
    if posts:
        graph["blogPost"] = [
            {"@type": "BlogPosting", "headline": post.title, "url": post.url, "datePublished": post.date.isoformat()}
            for post in posts
        ]
    body = f"""      <section class="hero" aria-labelledby="writing-heading">
        <p class="eyebrow">pranav kumar · notes</p>
        <h1 id="writing-heading">writing.</h1>
        <p class="lede">notes on retrieval, queues, and the infrastructure under llms.</p>
{listing}
      </section>"""
    write_if_changed(
        BLOG / "index.html",
        page(
            title="Writing | Pranav Kumar",
            description=description,
            canonical=f"{SITE}/blog/",
            body=body,
            og_type="website",
            image=f"{SITE}/og.png",
            image_alt=OG_ALT,
            json_ld=graph,
        ),
    )

    for post in posts:
        render_post_og(post, BLOG / post.slug / "og.png")
        extra = f'\n    <meta property="article:published_time" content="{post.date.isoformat()}" />'
        body = f"""      <article class="post">
        <p class="post-kicker"><a href="/blog/">writing</a> · <time datetime="{post.date.isoformat()}">{esc(post.date_label)}</time></p>
        <h1>{esc(post.title)}</h1>
        <p class="lede">{esc(post.description)}</p>
        <div class="prose">
{post.body_html}
        </div>
      </article>"""
        write_if_changed(
            BLOG / post.slug / "index.html",
            page(
                title=f"{post.title} | Pranav Kumar",
                description=post.description,
                canonical=post.url,
                body=body,
                og_type="article",
                image=post.image_url,
                image_alt=post.image_alt,
                json_ld={
                    "@context": "https://schema.org",
                    "@type": "BlogPosting",
                    "headline": post.title,
                    "description": post.description,
                    "datePublished": post.date.isoformat(),
                    "url": post.url,
                    "image": post.image_url,
                    "inLanguage": "en",
                    "author": {"@id": f"{SITE}/#pranav"},
                    "mainEntityOfPage": post.url,
                },
                extra_meta=extra,
            ),
        )


def write_feed(posts: list[Post]) -> None:
    items = []
    for post in posts:
        pub = dt.datetime(post.date.year, post.date.month, post.date.day, tzinfo=dt.timezone.utc)
        items.append(
            "\n".join(
                [
                    "    <item>",
                    f"      <title>{esc(post.title)}</title>",
                    f"      <link>{post.url}</link>",
                    f"      <guid>{post.url}</guid>",
                    f"      <pubDate>{pub.strftime('%a, %d %b %Y 00:00:00 +0000')}</pubDate>",
                    f"      <description>{esc(post.description)}</description>",
                    "    </item>",
                ]
            )
        )
    last = ""
    if posts:
        newest = posts[0].date
        stamp = dt.datetime(newest.year, newest.month, newest.day, tzinfo=dt.timezone.utc)
        last = f"    <lastBuildDate>{stamp.strftime('%a, %d %b %Y 00:00:00 +0000')}</lastBuildDate>\n"
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Pranav Kumar</title>
    <link>{SITE}/blog/</link>
    <description>Notes on retrieval, queues, and the infrastructure under LLMs.</description>
    <language>en</language>
{last}{chr(10).join(items)}
  </channel>
</rss>
"""
    write_if_changed(BLOG / "feed.xml", xml)


def write_sitemap(posts: list[Post]) -> None:
    home_mtime = dt.date.fromtimestamp((ROOT / "index.html").stat().st_mtime).isoformat()
    blog_last = posts[0].date.isoformat() if posts else home_mtime
    urls = [
        (f"{SITE}/", home_mtime, "monthly", "1.0"),
        (f"{SITE}/blog/", blog_last, "weekly", "0.8"),
    ]
    for post in posts:
        urls.append((post.url, post.date.isoformat(), "monthly", "0.6"))
    body = "\n".join(
        f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>"""
        for loc, lastmod, freq, priority in urls
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
"""
    write_if_changed(ROOT / "sitemap.xml", xml)


def main() -> None:
    posts = load_posts()
    update_home(posts)
    update_llms(posts)
    write_blog(posts)
    write_feed(posts)
    write_sitemap(posts)
    label = "post" if len(posts) == 1 else "posts"
    print(f"built {len(posts)} {label}")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
