/*
 * Service worker for a server-rendered Flask app.
 *
 * Design rule: this worker NEVER stores HTML responses. Pages rendered for a
 * logged-in user would otherwise sit in the cache and could be served to a
 * different account on a shared device. Only fingerprint-safe static assets
 * are cached; navigations go to the network and fall back to a static offline
 * page when there is no connection.
 *
 * Bump CACHE_VERSION on every deploy that changes static assets, or clients
 * will keep serving the old CSS/JS indefinitely.
 */

const CACHE_VERSION = 'v1';
const CACHE_NAME = `app-static-${CACHE_VERSION}`;
const OFFLINE_URL = '/offline';

// Static assets worth having available immediately on first load.
// Keep this list short — anything missing at install time fails the whole
// install, and the worker never activates.
const PRECACHE_URLS = [
  OFFLINE_URL,
  '/static/icons/icon-192.png',
];

// Anything under these prefixes always goes straight to the network.
// Auth, payments, and API traffic must never be intercepted.
const NETWORK_ONLY_PREFIXES = [
  '/api/',
  '/auth/',
  '/login',
  '/logout',
  '/admin',
  '/webhook',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
        )
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Never touch anything but same-origin GETs. This single check rules out
  // every POST, PUT and DELETE, so form submissions and API writes are safe.
  if (request.method !== 'GET' || url.origin !== self.location.origin) {
    return;
  }

  if (NETWORK_ONLY_PREFIXES.some((prefix) => url.pathname.startsWith(prefix))) {
    return;
  }

  // Page loads: always hit the network so the user sees live data. The offline
  // page is only a fallback — the response itself is never cached.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() => caches.match(OFFLINE_URL))
    );
    return;
  }

  // Static assets: serve from cache immediately, then refresh in the
  // background so the next load picks up any change.
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.open(CACHE_NAME).then(async (cache) => {
        const cached = await cache.match(request);
        const network = fetch(request)
          .then((response) => {
            if (response.ok) {
              cache.put(request, response.clone());
            }
            return response;
          })
          .catch(() => cached);

        return cached || network;
      })
    );
  }
});
