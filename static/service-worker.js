const CACHE_NAME = "bingoai-cache-v2";

// Files to cache for offline use
const URLS_TO_CACHE = [
    "/",
    "/static/css/style.css",
    "/static/js/script.js",
    "/static/images/robot.png",
    "/static/images/universe.jpg",
    "/static/images/icon-192.png",
    "/static/images/icon-512.png",
    "/static/images/desktop.png",
    "/static/images/mobile.png",
    "/static/manifest.json"
];

// Install Event: Cache essential assets
self.addEventListener("install", event => {
    console.log("Service Worker: Installing...");
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log("Service Worker: Caching files");
                return cache.addAll(URLS_TO_CACHE);
            })
            .then(() => self.skipWaiting())
    );
});

// Activate Event: Remove old caches
self.addEventListener("activate", event => {
    console.log("Service Worker: Activating...");
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cache => {
                    if (cache !== CACHE_NAME) {
                        console.log("Service Worker: Deleting old cache:", cache);
                        return caches.delete(cache);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch Event: Serve cached files when offline
self.addEventListener("fetch", event => {
    // Ignore non-GET requests (e.g., POST requests to /chat)
    if (event.request.method !== "GET") {
        return;
    }

    event.respondWith(
        caches.match(event.request).then(cachedResponse => {
            // Return cached file if available
            if (cachedResponse) {
                return cachedResponse;
            }

            // Otherwise fetch from the network
            return fetch(event.request)
                .then(networkResponse => {
                    return caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, networkResponse.clone());
                        return networkResponse;
                    });
                })
                .catch(() => {
                    // Fallback response when offline
                    if (event.request.headers.get("accept").includes("text/html")) {
                        return caches.match("/");
                    }
                });
        })
    );
});