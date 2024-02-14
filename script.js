const socialsEl = document.querySelector("#socials");
const projectsEl = document.querySelector("#projects");

const socialHandles = [
  {
    Link: "https://twitter.com/anonthedev",
    // imgSrc: "images/twitter-logo.png",
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
    title: "youify",
    desc: "A website where you can convert your YouTube playlist to Spotify and vice versa.",
    githubLink: "https://github.com/anonthedev/youify",
    demoLink: "https://youify.xyz/",
  },
  {
    title: "3D Renderer",
    desc: "A 3D renderer made in vanilla JS and HTML Canvas API.",
    githubLink: "https://github.com/anonthedev/soft3Dengine",
    demoLink: "https://twitter.com/anonthedev/status/1753402885961093391",
  },
  {
    title: "youdio",
    desc: "A webapp that let's you convert youtube to an online audio jukebox. Supabase took it down due to no interactivity.",
    demoLink:
      "https://youdio.xyz",
  },
  {
    title: "Rush My Flight",
    desc: "A freelance project wesbite where you can book flights, I handled the frontend on this project. Frontend built on Next & TS. [Project got abandoned]",
    demoLink: "https://rushmyflight.com/",
  },
  {
    title: "Particle Simulation in JS",
    desc: "A particle simulation made in vanilla JS & HTML Canvas",
    githubLink: "https://github.com/anonthedev/particleLife",
    demoLink: "https://particle-simulation.vercel.app/"
  },
  {
    title: "Likify",
    desc: "A website where you can convert your liked songs collection to a shareable spotify playlist.",
    githubLink: "https://github.com/anonthedev/Likify",
    demoLink: "https://likify.vercel.app/",
  },
  {
    title: "Screen Recorder",
    desc: "A web based screen recorder made using webRTC API, HTML, CSS & JS.",
    githubLink: "https://github.com/anonthedev/screen-recorder",
    demoLink: "https://anon-screen-recorder.netlify.app/",
  },
  {
    title: "Blog Thumbnail Generator",
    desc: "Just a tool made to make blog thumbnails using HTML, CSS, JS (Canvas API).",
    githubLink: "https://github.com/anonthedev/blog-thumbnail-generator",
    demoLink: "https://blog-thumbnail-generator.netlify.app",
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
  div.style.display = "flex"
  div.style.flexDirection = "column"
  div.style.gap = "10px"
  div.style.marginLeft = "15px"
  div.style.color = "rgb(229, 231, 235)"
  const h3 = document.createElement("h3");
  h3.className = "project-title";
  h3.textContent = `- ${project.title}`;
  h3.style.marginLeft = "-15px"
  const p = document.createElement("p");
  p.textContent = project.desc;
  const links = document.createElement("div")
  links.className = "links"
  const githubLink = document.createElement("a");
  githubLink.target = "_blank";
  githubLink.href = project.githubLink;
  githubLink.textContent = "github";
  githubLink.style.display = project.githubLink ? "block" : "none"
  const demoLink = document.createElement("a");
  demoLink.target = "_blank";
  demoLink.href = project.demoLink;
  demoLink.textContent = "demo";

  links.append(githubLink, demoLink);

  div.append(h3, p, links);

  projectsEl.appendChild(div);
});
