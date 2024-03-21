const socialsEl = document.querySelector("#socials");
const projectsEl = document.querySelector("#projects");

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
    title: "Youify (50+ MAUs)",
    techStack: "Next.js, Tailwind, TS, ContextAPI",
    imgSrc: "/resources/img/youify.webp",
    desc: "A website where you can convert your YouTube playlist to Spotify and vice versa.",
    githubLink: "https://github.com/anonthedev/youify",
    demoLink: "https://youify.xyz/",
  },
  {
    title: "booksuno (300+ users)",
    techStack: "Next.js, Tailwind, TS, Zustand",
    imgSrc: "/resources/img/booksuno.webp",
    desc: "A webapp that let's you listen to audiobooks for free.",
    demoLink: "https://booksuno.xyz",
  },
  {
    title: "Rush My Flight",
    techStack: "Next.js, Tailwind, TS, ContextAPI",
    imgSrc: "/resources/img/rush-my-flight.webp",
    desc: "A freelance project wesbite where you can book flights, I handled the frontend on this project.",
    demoLink: "https://rushmyflight.com/",
  },
  {
    title: "3D renderer",
    techStack: "HTML, CSS, TS, BABYLON",
    imgSrc: "/resources/img/3d-renderer.webp",
    desc: "A 3D renderer made in TS, it can render simple 3D objects in the HTML Canvas.",
    githubLink: "https://github.com/anonthedev/soft3Dengine",
    // demoLink: "https://blog-thumbnail-generator.netlify.app",
  },
  {
    title: "focustunes (200+ users)",
    techStack: "Next.js, Tailwind, TS, Zustand",
    imgSrc: "/resources/img/focustunes.webp",
    desc: "focustunes is a website where you can mix different sounds at different volumes to find the perfect sweet spot for yourself.",
    githubLink: "https://github.com/anonthedev/soft3Dengine",
    demoLink: "https://focustunes.vercel.app",
  },
  {
    title: "Likify",
    imgSrc: "/resources/img/likify.webp",
    techStack: "Next.js, Tailwind, TS",
    desc: "A website where you can convert your liked songs collection to a shareable spotify playlist.",
    githubLink: "https://github.com/anonthedev/Likify",
    demoLink: "https://likify.vercel.app/",
  },
  {
    title: "Screen Recorder",
    techStack: "HTML, CSS, JS",
    imgSrc: "/resources/img/screen-recorder.webp",
    desc: "A web based screen recorder that lets you record your screen and download it without having to create an account.",
    githubLink: "https://github.com/anonthedev/screen-recorder",
    demoLink: "https://anon-screen-recorder.netlify.app/",
  },
];

socialHandles.forEach((social, index) => {
  const a = document.createElement("a");
  a.href = social.Link;
  a.textContent = social.platform;
  a.target = "_blank";

  socialsEl.appendChild(a);
});

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
