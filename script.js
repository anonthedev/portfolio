const socialsEl = document.querySelector("#socials");
const projectsEl = document.querySelector("#projects");
const experienceEl = document.querySelector("#experience");

const socialHandles = [
  {
    Link: "https://twitter.com/anonthedev",
    // imgSrc: "images/twitter-logo.webp",
    platform: "twitter",
  },
  {
    Link: "https://github.com/anonthedev",
    platform: "github",
  },
  {
    Link: "https://peerlist.io/anonthedev",
    platform: "peerlist",
  },
  {
    Link: "https://anontheblogger.medium.com/",
    platform: "medium",
  },
];

const projectsArray = [
  {
    title: "Slayshot",
    techStack: "Next.js, Tailwind, TypeScript, Supabase, Python, OpenAI, Modal, Inngest",
    imgSrc: "/resources/img/slayshot.png",
    desc: "An AI-powered SaaS for generating short-form videos from long podcasts, automating clip extraction, captioning, and vertical formatting.",
    githubLink: "",
    demoLink: "https://slayshot.xyz",
  },
  {
    title: "Readica",
    techStack: "Next.js, Supabase, Node.js, PDF-lib, Tiptap",
    imgSrc: "/resources/img/readica.png",
    desc: "A research paper management platform for discovering, organizing, and annotating academic PDFs.",
    githubLink: "",
    demoLink: "https://readica.pro/",
  },
  {
    title: "Booksuno (1000+ users)",
    techStack: "Next.js, Tailwind, TypeScript, Zustand",
    imgSrc: "/resources/img/booksuno.webp",
    desc: "An audiobook platform leveraging LibriVox API for extensive content.",
    githubLink: "https://github.com/anonthedev/booksuno",
    demoLink: "https://booksuno.xyz",
  },
  {
    title: "Youify (50+ MAUs)",
    techStack: "Next.js, Tailwind, TypeScript, ContextAPI",
    imgSrc: "/resources/img/youify.webp",
    desc: "A service website for migrating playlists between YouTube and Spotify.",
    githubLink: "https://github.com/anonthedev/youify",
    demoLink: "https://youify.xyz/",
  },
];

socialHandles.forEach((social, index) => {
  const a = document.createElement("a");
  a.href = social.Link;
  a.textContent = social.platform;
  a.target = "_blank";

  socialsEl.appendChild(a);
});

const experienceArray = [
  {
    role: "Contractor",
    company: "Unusals",
    duration: "Jul 2025",
    techStack: "NestJS, React (Electron), OpenAI Agents SDK",
    responsibilities: [
      "Built end-to-end AI-driven video generation workflows in NestJS, achieving ~50% performance improvements through optimized pipeline design and caching strategies.",
      "Developed a flow editor in React (Electron), enabling interactive workflow creation with real-time updates and TypeScript-based extensibility.",
      "Integrated OpenAI Agents SDK to orchestrate modular AI agents, streamlining video generation and automation tasks."
    ]
  },
  {
    role: "Frontend Intern",
    company: "1811 Labs",
    duration: "May 2025 – Jun 2025",
    techStack: "Next.js, TypeScript, Tailwind CSS, Supabase, Tanstack Query, Plasmo",
    responsibilities: [
      "Developed a full-featured YouTube transcription browser extension with seamless authentication via the main platform and a pixel-perfect, responsive UI using Plasmo.",
      "Implemented optimized frontend flows for image generation, leveraging Tanstack Query for caching and Supabase Realtime for dynamic cache invalidation.",
      "Built efficient frontend workflows for video generation, integrating real-time updates and performance-focused data fetching strategies."
    ]
  },
  {
    role: "Software Development Engineer Intern",
    company: "Composio",
    duration: "Apr 2024 - Aug 2024",
    techStack: "TypeScript, Next.js, Python, Tailwind CSS",
    responsibilities: [
      "Integrated Cloudflare AI and Vercel AI SDK into Composio's JavaScript SDK, including comprehensive documentation.",
      "Implemented a robust design system in Next.js with Storybook for improved component development and testing.",
      "Developed multiple small projects and examples with Composio's Python and JavaScript SDK."
    ]
  }
];

projectsArray.forEach((project, index) => {
  const div = document.createElement("div");
  div.className = "project-div";

  const imgDiv = document.createElement("div");
  const img = document.createElement("img");
  img.className = "project-img";
  img.src = project.imgSrc;
  img.loading = "lazy";

  imgDiv.append(img);

  const detailsDiv = document.createElement("div");
  detailsDiv.className = "project-details"
  const h3 = document.createElement("h3");
  h3.className = "project-title";
  h3.textContent = `${project.title}`;

  const span = document.createElement("span")
  span.className = "project-tech-stack"
  span.textContent = `${project.techStack}`

  const p = document.createElement("p");
  p.textContent = project.desc;
  p.className = "project-desc";

  const links = document.createElement("div");
  links.className = "links";
  const githubLink = document.createElement("a");
  githubLink.target = "_blank";
  githubLink.href = project.githubLink;
  githubLink.textContent = "github";
  githubLink.style.display = project.githubLink ? "block" : "none";
  const demoLink = document.createElement("a");
  demoLink.target = "_blank";
  demoLink.href = project.demoLink;
  demoLink.textContent = "demo";
  demoLink.style.display = project.demoLink ? "block" : "none";

  links.append(githubLink, demoLink);

  detailsDiv.append(h3, span, p, links);

  div.append(imgDiv, detailsDiv);

  projectsEl.appendChild(div);
});

experienceArray.forEach((exp) => {
  const timelineItem = document.createElement("div");
  timelineItem.className = "timeline-item";

  const content = document.createElement("div");
  content.className = "timeline-content";

  const role = document.createElement("h3");
  role.textContent = exp.role;

  const companyDuration = document.createElement("div");
  companyDuration.className = "company-duration";

  const company = document.createElement("span");
  company.className = "company";
  company.textContent = exp.company;

  const duration = document.createElement("span");
  duration.className = "duration";
  duration.textContent = exp.duration;

  companyDuration.append(company, duration);

  const techStack = document.createElement("div");
  techStack.className = "tech-stack";
  techStack.textContent = `Tech Stack: ${exp.techStack}`;

  const responsibilities = document.createElement("ul");
  responsibilities.className = "responsibilities";

  exp.responsibilities.forEach((resp) => {
    const li = document.createElement("li");
    li.textContent = resp;
    responsibilities.appendChild(li);
  });

  content.append(role, companyDuration, techStack, responsibilities);
  timelineItem.appendChild(content);
  experienceEl.appendChild(timelineItem);
});
