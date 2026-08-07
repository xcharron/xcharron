"""Generate every PWA icon size from one source image.

    pip install pillow
    python make_icons.py logo.png static/icons

Produces the four sizes the manifest expects plus the 180px apple-touch-icon.
The "maskable" variants are padded to 80% of the canvas because Android crops
icons to a circle or squircle depending on the launcher — an unpadded logo
loses its edges.
"""

import os
import sys

from PIL import Image

SIZES = [
    # (filename, pixel size, scale of logo within the canvas)
    ("icon-192.png", 192, 1.0),
    ("icon-512.png", 512, 1.0),
    ("icon-192-maskable.png", 192, 0.8),
    ("icon-512-maskable.png", 512, 0.8),
    ("icon-180.png", 180, 1.0),  # apple-touch-icon
]

# Shows through wherever the source image is transparent. iOS does not support
# transparency in home-screen icons, so a solid background avoids a black box.
BACKGROUND = (11, 11, 11, 255)


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: python make_icons.py <source-image> <output-dir>")

    source_path, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)

    source = Image.open(source_path).convert("RGBA")

    for filename, size, scale in SIZES:
        canvas = Image.new("RGBA", (size, size), BACKGROUND)

        inner = int(size * scale)
        logo = source.copy()
        logo.thumbnail((inner, inner), Image.LANCZOS)

        offset = ((size - logo.width) // 2, (size - logo.height) // 2)
        canvas.paste(logo, offset, logo)

        out_path = os.path.join(out_dir, filename)
        canvas.convert("RGB").save(out_path, "PNG", optimize=True)
        print(f"wrote {out_path} ({size}x{size})")


if __name__ == "__main__":
    main()
