#!/usr/bin/env python3
"""Generate the extension toolbar icons.

Draws at 8x supersample (1024px) on a 128-unit grid, then downscales with
LANCZOS to 16/32/48/128 px so edges stay crisp at every size.

Requires Pillow:  pip install Pillow
Run from anywhere:  python3 tools/generate-icons.py
Output: icons/icon{16,32,48,128}.png
"""
import os
from PIL import Image, ImageDraw

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "icons")
os.makedirs(OUT_DIR, exist_ok=True)

S = 8            # supersample: 128 units -> 1024 px
BIG = 128 * S

BLUE = (37, 99, 235, 255)     # #2563EB tile
WHITE = (255, 255, 255, 255)
RED = (220, 38, 38, 255)      # #DC2626 prohibition


def u(v):
    """128-unit coordinate -> supersampled pixel."""
    return round(v * S)


def draw_icon():
    img = Image.new("RGBA", (BIG, BIG), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Rounded blue tile (own contrast on light & dark toolbars)
    d.rounded_rectangle([u(6), u(6), u(122), u(122)], radius=u(26), fill=BLUE)

    # White mouse body
    d.rounded_rectangle([u(43), u(30), u(85), u(98)], radius=u(21), fill=WHITE)

    # Button gaps in the tile color, plus the scroll-wheel slot
    d.line([u(64), u(32), u(64), u(56)], fill=BLUE, width=u(2.2))   # left/right split
    d.line([u(45), u(56), u(83), u(56)], fill=BLUE, width=u(2.2))   # buttons/body split
    d.rounded_rectangle([u(61), u(35), u(67), u(52)], radius=u(3), fill=BLUE)  # wheel

    # Red "no" ring + slash over the middle-button area, with a white halo
    cx, cy, r = 64, 43, 18
    ring = [u(cx - r), u(cy - r), u(cx + r), u(cy + r)]
    off = r * 0.7071  # 45-degree endpoints inside the ring
    slash = [u(cx - off), u(cy - off), u(cx + off), u(cy + off)]

    d.ellipse(ring, outline=WHITE, width=u(7))     # halo
    d.line(slash, fill=WHITE, width=u(7))
    d.ellipse(ring, outline=RED, width=u(4.5))     # prohibition
    d.line(slash, fill=RED, width=u(4.5))

    return img


def main():
    master = draw_icon()
    for size in (16, 32, 48, 128):
        master.resize((size, size), Image.LANCZOS).save(
            os.path.join(OUT_DIR, f"icon{size}.png")
        )
    print("wrote icons to", OUT_DIR)


if __name__ == "__main__":
    main()
