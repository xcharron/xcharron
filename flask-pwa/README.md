# Flask PWA kit

Turns a server-rendered Flask app into an installable PWA that launches
chromeless from the home screen. Every file here was run and verified, not
sketched.

## What's in here

| File | Goes to | Purpose |
|---|---|---|
| `pwa.py` | project root (or `app/`) | Blueprint serving `/sw.js`, `/manifest.json`, `/offline` |
| `static/sw.js` | `static/` | Service worker — caches static assets only |
| `static/manifest.json` | `static/` | Web app manifest |
| `templates/offline.html` | `templates/` | Fallback page shown with no connection |
| `templates/_pwa_head.html` | `templates/` | Snippet to paste into your base template's `<head>` |
| `make_icons.py` | anywhere | Generates all five icon sizes from one source image |

## Setup

**1. Icons.** From any square logo, ideally 512px or larger:

```bash
pip install pillow
python make_icons.py logo.png static/icons
```

Writes `icon-192`, `icon-512`, both maskable variants, and `icon-180`.

**2. Register the blueprint** in your app factory:

```python
from pwa import pwa
app.register_blueprint(pwa)
```

**3. Add the head snippet.** Paste the contents of `templates/_pwa_head.html`
into your base template's `<head>`, or include it:

```jinja
{% include '_pwa_head.html' %}
```

**4. Edit `static/manifest.json`** — set `name`, `short_name`, `description`,
and the two colors. Set `apple-mobile-web-app-title` in the head snippet to
match `short_name`; that's the label under the icon on iOS.

**5. Confirm HTTPS.** Service workers only run on HTTPS or `localhost`. A plain
HTTP staging server will silently fail to register.

## Two things that will bite you

**Bump `CACHE_VERSION` in `sw.js` on every deploy that changes static assets.**
Otherwise installed clients keep serving the old CSS and JS with no way to
recover short of clearing site data. This is the single most common way to ship
a broken PWA.

**Check `NETWORK_ONLY_PREFIXES` in `sw.js` against your real routes.** It
currently lists `/api/`, `/auth/`, `/login`, `/logout`, `/admin`, `/webhook`.
If your app uses different paths for auth or payments, add them. The worker
already skips every non-GET request, so form posts are safe regardless — this
list is the second layer.

## Verifying it worked

**Android/Chrome:** DevTools → Application → Manifest. It lists any
installability failure explicitly. Then Lighthouse → Progressive Web App.

**iOS:** Safari only — an icon added from Chrome on iOS is always a plain
bookmark that opens the browser. Share → Add to Home Screen, then launch it.
No URL bar means it worked.

**Anyone with the old icon must delete and re-add it.** iOS caches the
bookmark and won't pick up the manifest on its own. This is usually why "it
still opens the browser" after a correct fix.

## What this does not do

No offline reads or writes. Pages need a connection; without one the user gets
`offline.html` instead of a browser error. Real offline means caching data in
IndexedDB, queueing mutations, and resolving sync conflicts — a separate
project, and worth doing only if people actually use the app without signal.
