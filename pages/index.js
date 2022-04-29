import "aos/dist/aos.css";
import AOS from "aos";
import Head from "next/head";

if (typeof window === "object") {
  AOS.init();
}

export default function Home() {
  return (
    <main className="text-gray-600 body-font bg-slate-900">
      <Head>
        <title>Anon</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      <div
        className="container mx-auto flex px-5 py-24 md:flex-row flex-col items-center "
        data-aos="fade-in"
      >
        <div className="lg:max-w-lg lg:w-full md:w-1/2 w-5/6 mb-10 md:mb-0">
          <img
            className="object-cover object-center rounded-full  shadow-2xl shadow-black"
            alt="hero"
            src="images/hero-img.png"
          />
        </div>
        <div className="lg:flex-grow md:w-1/2 lg:pl-24 md:pl-16 flex flex-col md:items-start md:text-left items-center text-center">
          <h1 className="title-font sm:text-4xl text-3xl mb-4 font-bold text-white">
            Heyy 👋,
            <br className="hidden lg:inline-block" /> Anon here
          </h1>
          <h2 className="title-font sm:text-4xl text-3xl mb-4 font-medium text-white">
            A High School Student
            <br className="hidden lg:inline-block" /> and Fronted Developer 👨‍💻
          </h2>
          <p className="mb-8 leading-relaxed text-xl text-slate-400">
            I love Coding, Physics and Mythologies too.
          </p>
          <div className="flex justify-center">
            <a
              rel="noreferrer"
              target="_blank"
              href="https://twitter.com/Anonthedev"
              className="w-8 mr-5"
            >
              <img
                className="rounded-full"
                src="images/twitter-logo.png"
                alt=""
              />
            </a>
            <a
              rel="noreferrer"
              href="https://github.com/anonthedev"
              target="_blank"
              className="w-8 mr-5"
            >
              <img
                className="rounded-full"
                src="images/github-logo.png"
                alt=""
              />
            </a>
            <a
              rel="noreferrer"
              href="https://anondevblog.hashnode.dev"
              target="_blank"
              className="w-8 mr-5"
            >
              <img
                className="rounded-full"
                src="images/hashnode-logo.png"
                alt=""
              />
            </a>
          </div>
        </div>
      </div>

      <div className="flex flex-col items-center justify-center">
        <h2
          className="title-font sm:text-4xl text-3xl mb-4 font-medium text-white text-center"
          data-aos="fade-up-left"
        >
          Tools in my Tech Workshop ⚒
        </h2>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-3 gap-4">
          <img
            data-aos="fade-up-left"
            className="mx-auto object-cover h-16 mt-12 mr-12"
            src="images/html-logo.png"
            alt=""
          />
          <img
            data-aos="fade-up-left"
            className="mx-auto object-cover h-16 mt-12 mr-12"
            src="images/css-logo.png"
            alt=""
          />
          <img
            data-aos="fade-up-left"
            className="mx-auto object-cover h-16 mt-12"
            src="images/js-logo.png"
            alt=""
          />
          <img
            data-aos="fade-up-left"
            className="mx-auto object-cover h-16 mt-12 mr-12"
            src="images/react-logo.png"
            alt=""
          />
          <img
            data-aos="fade-up-left"
            className="mx-auto object-cover h-16 mt-12 mr-12 bg-white rounded-full border-none"
            src="images/next-logo.png"
            alt=""
          />
          <img
            data-aos="fade-up-left"
            className="mx-auto object-cover h-16 mt-12"
            src="images/tailwind-logo.png"
            alt=""
          />
          <img
            data-aos="fade-up-left"
            className="mx-auto object-cover h-16 mt-12 mr-12"
            src="images/bootstrap-logo.png"
            alt=""
          />
          <img
            data-aos="fade-up-left"
            className="mx-auto object-cover h-16 mt-12 mr-12"
            src="images/firebase-logo.png"
            alt=""
          />
        </div>
      </div>

      <div className="mt-32">
        <h2
          className="title-font sm:text-4xl text-4xl mb-4 font-medium text-white text-center"
          data-aos="fade-up-right"
        >
          A few projects of mine 📽
        </h2>

        <div className="w-full p-12">
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-12">
            <div
              className="overflow-hidden rounded-lg h-90 w-60 md:w-80 cursor-pointer m-auto"
              data-aos="fade-up-right"
            >
              <a
                rel="noreferrer"
                target="_blank"
                href="https://vikings-mythbuster.netlify.app/"
                className="w-full block h-full shadow-lg"
              >
                <img
                  alt="blog photo"
                  src="/images/viking-mythbuster.png"
                  className="max-h-40 w-full object-cover"
                />
                <div className="bg-white dark:bg-gray-800 w-full p-4 rounded-br-lg rounded-bl-lg">
                  <p className="text-gray-800 dark:text-white text-xl font-medium mb-2">
                    Viking Mythbuster
                  </p>
                  <p className="text-gray-400 dark:text-gray-300 font-light text-md">
                    There are many misconceptions on Vikings so this is a small
                    project I made when I started learning React.
                  </p>
                </div>
              </a>
              <a
              rel="noreferrer"
                target="_blank"
                href="https://github.com/anonthedev/vikings-mythbuster"
              >
                <p className="pt-4 text-gray-400">Code</p>
              </a>
            </div>
            <div
              className="overflow-hidden rounded-lg h-90 w-60 md:w-80 cursor-pointer m-auto"
              data-aos="fade-up-right"
            >
              <a
                rel="noreferrer"
                target="_blank"
                href="https://anon-netflix-clone.netlify.app/"
                className="w-full block h-full shadow-lg"
              >
                <img
                  alt="blog photo"
                  src="/images/netflix-clone.png"
                  className="max-h-40 w-full object-cover"
                />
                <div className="bg-white dark:bg-gray-800 w-full p-4 rounded-br-lg rounded-bl-lg">
                  <p className="text-gray-800 dark:text-white text-xl font-medium mb-2">
                    Netflix Clone
                  </p>
                  <p className="text-gray-400 dark:text-gray-300 font-light text-md">
                    This is clone project I made after learning React. It uses
                    TMDB API to get movies and this is majorly made without any
                    tutorials.
                  </p>
                </div>
              </a>
              <a
              rel="noreferrer"
                target="_blank"
                href="https://github.com/anonthedev/netflix-clone"
              >
                <p className="pt-4 text-gray-400">Code</p>
              </a>
            </div>
            <div
              className="overflow-hidden rounded-lg h-90 w-60 md:w-80 cursor-pointer m-auto"
              data-aos="fade-up-right"
            >
              <a
                rel="noreferrer"
                target="_blank"
                href="https://anon-weather-app.netlify.app/"
                className="w-full block h-full shadow-lg"
              >
                <img
                  alt="blog photo"
                  src="/images/weather-app.png"
                  className="max-h-40 w-full object-cover"
                />
                <div className="bg-white dark:bg-gray-800 w-full p-4 rounded-br-lg rounded-bl-lg">
                  <p className="text-gray-800 dark:text-white text-xl font-medium mb-2">
                    Weather App
                  </p>
                  <p className="text-gray-400 dark:text-gray-300 font-light text-md">
                    This weather app is made with pure HTML, CSS and JS uses an
                    API to fetch data and one to get location automatically.
                  </p>
                </div>
              </a>
              <a
              rel="noreferrer"
                target="_blank"
                href="https://github.com/anonthedev/weather-app"
              >
                <p className="pt-4 text-gray-400">Code</p>
              </a>
            </div>
            <div
              className="overflow-hidden rounded-lg h-90 w-60 md:w-80 cursor-pointer m-auto"
              data-aos="fade-up-right"
            >
              <a
                rel="noreferrer"
                target="_blank"
                href="https://text-speech-webapi.netlify.app/"
                className="w-full block h-full shadow-lg"
              >
                <img
                  alt="blog photo"
                  src="/images/text-speech.png"
                  className="max-h-40 w-full object-cover"
                />
                <div className="bg-white dark:bg-gray-800 w-full p-4 rounded-br-lg rounded-bl-lg">
                  <p className="text-indigo-500 text-md font-medium"></p>
                  <p className="text-gray-800 dark:text-white text-xl font-medium mb-2">
                    Text-to-Speech
                  </p>
                  <p className="text-gray-400 dark:text-gray-300 font-light text-md">
                    A web app that uses Web Speech API to convert text to
                    speech. You can customize the voice, speed and pitch.
                  </p>
                </div>
              </a>
              <a
                rel="noreferrer"
                target="_blank"
                href="https://github.com/anonthedev/text-to-speech-webAPI"
              >
                <p className="pt-4 text-gray-400">Code</p>
              </a>
            </div>
            <div
              className="overflow-hidden rounded-lg h-90 w-60 md:w-80 cursor-pointer m-auto"
              data-aos="fade-up-right"
            >
              <a
                rel="noreferrer"
                target="_blank"
                href="https://chrome.google.com/webstore/detail/nordic-homepage/mnejdficbihlkhinkhfmdelhniemidff"
                className="w-full block h-full shadow-lg"
              >
                <img
                  alt="blog photo"
                  src="/images/nordic-homepage-extension.png"
                  className="max-h-40 w-full object-cover"
                />
                <div className="bg-white dark:bg-gray-800 w-full p-4 rounded-br-lg rounded-bl-lg">
                  <p className="text-indigo-500 text-md font-medium"></p>
                  <p className="text-gray-800 dark:text-white text-xl font-medium mb-2">
                    Nordic Homepage Extension
                  </p>
                  <p className="text-gray-400 dark:text-gray-300 font-light text-md">
                    A chrome extension that changes your homepage and gives it a
                    Nordic Vibe. Made on HTML, CSS and JS.
                  </p>
                </div>
              </a>
              <a
                rel="noreferrer"
                target="_blank"
                href="https://github.com/anonthedev/nordic-homepage"
              >
                <p className="pt-4 text-gray-400">Code</p>
              </a>
            </div>
            <div
              className="overflow-hidden rounded-lg h-90 w-60 md:w-80 cursor-pointer m-auto"
              data-aos="fade-up-right"
            >
              <a
                rel="noreferrer"
                target="_blank"
                href="https://github.com/anonthedev/newslit"
                className="w-full block h-full shadow-lg"
              >
                <img
                  alt="blog photo"
                  src="/images/newslit.png"
                  className="max-h-40 w-full object-cover"
                />
                <div className="bg-white dark:bg-gray-800 w-full p-4  rounded-br-lg rounded-bl-lg">
                  <p className="text-gray-800 dark:text-white text-xl font-medium mb-2">
                    NewsLit - News App
                  </p>
                  <p className="text-gray-400 dark:text-gray-300 font-light text-md">
                    A React app made using News API. I made this following a
                    tutorial to learn React. Unfortunetly, I couldn't deploy
                    this.
                  </p>
                </div>
              </a>
              <a
                rel="noreferrer"
                target="_blank"
                href="https://github.com/anonthedev/newslit"
              >
                <p className="pt-4 text-gray-400">Code</p>
              </a>
            </div>
          </div>
        </div>
      </div>

      <footer>
        <p></p>
        <p className="text-slate-400 text-right mr-20 pb-4">
          Made with NextJS, Tailwind and 🎵
        </p>
      </footer>
    </main>
  );
}
