"""PWA routes for a Flask app.

Register once in your app factory:

    from pwa import pwa
    app.register_blueprint(pwa)

The only non-obvious part is /sw.js. A service worker can only control URLs at
or below its own path, so one served from /static/sw.js would control nothing
but /static/*. It has to be served from the site root to control the whole app.
"""

from flask import Blueprint, current_app, render_template, send_from_directory

pwa = Blueprint("pwa", __name__)


@pwa.route("/sw.js")
def service_worker():
    response = send_from_directory(
        current_app.static_folder, "sw.js", mimetype="application/javascript"
    )
    # Without this the browser can serve a stale worker for up to 24h, which
    # makes shipping a cache-version bump unreliable.
    response.headers["Cache-Control"] = "no-cache"
    return response


@pwa.route("/manifest.json")
def manifest():
    return send_from_directory(
        current_app.static_folder, "manifest.json", mimetype="application/manifest+json"
    )


@pwa.route("/offline")
def offline():
    """Shown only when the device has no connection. Must not require a DB
    query or a logged-in user — it is precached at install time."""
    return render_template("offline.html")
