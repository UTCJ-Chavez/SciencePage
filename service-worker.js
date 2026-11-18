const CACHE_NAME = "sciencepage-v2";

const FILES_TO_CACHE = [
  "./",
  "./index.html",
  "./about.html",
  "./blog.html",
  "./contact.html",
  "./projects.html",
  "./proj1.html",
  "./singlepost.html",

  "./manifest.json",

  "./css/style.css",
  "./css/mobile.css",

  "./js/mobile.js",

  "./images/pwa-icon.svg",
  "./images/logo.png",
  "./images/icons.png",
  "./images/alien-life.jpg",
  "./images/astronaut.jpg",
  "./images/bg-about.jpg",
  "./images/bg-home.jpg",
  "./images/bg-transparent1.png",
  "./images/curious-rover.jpg",
  "./images/earth-satellite.jpg",
  "./images/finding-planet.jpg",
  "./images/galaxy.jpg",
  "./images/mars-rover.jpg",
  "./images/martianrover-journey.jpg",
  "./images/moon-landing.jpg",
  "./images/moon-satellite.jpg",
  "./images/new-satellitedish.jpg",
  "./images/project-image1.jpg",
  "./images/project-image2.jpg",
  "./images/project-image3.jpg",
  "./images/project-image4.jpg",
  "./images/satellite-dish.jpg",
  "./images/satellite.png",
  "./images/space-shuttle.png",
  "./images/space-station.jpg",

  "./fonts/audiowide-regular-webfont.eot",
  "./fonts/audiowide-regular-webfont.svg",
  "./fonts/audiowide-regular-webfont.ttf",
  "./fonts/audiowide-regular-webfont.woff"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(FILES_TO_CACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(cacheNames =>
        Promise.all(
          cacheNames
            .filter(name =>
              name.startsWith("sciencepage-") &&
              name !== CACHE_NAME
            )
            .map(name => caches.delete(name))
        )
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  if (event.request.method !== "GET") return;

  const url = new URL(event.request.url);

  if (url.origin !== self.location.origin) return;

  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        if (cachedResponse) {
          return cachedResponse;
        }

        return fetch(event.request);
      })
      .catch(() => {
        if (event.request.mode === "navigate") {
          return caches.match("./index.html");
        }
      })
  );
});
