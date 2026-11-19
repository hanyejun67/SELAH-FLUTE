"""WebP copies of the page photos at the widths the layout asks for (srcset). Pixels are only resized, never altered.
Usage: python3 tools/webp.py img"""
import os, sys
from PIL import Image

D = sys.argv[1]
SETS = {
    "keys": [640, 960, 1200], "lip": [640, 960, 1200], "latch": [640, 960, 1200],
    "cups": [640, 1000], "badge-c": [640, 1000],
    "case-lid": [800, 1200, 1600], "case-base": [800, 1200, 1600],
    "case-silver": [640, 1000], "case-gold": [640, 1000],
    "case-full": [2000],
}
for name, widths in SETS.items():
    im = Image.open(os.path.join(D, name + ".jpg")).convert("RGB")
    for w in widths:
        r = im if w == im.width else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        out = os.path.join(D, f"{name}-{w}.webp")
        r.save(out, "WEBP", quality=80, method=6)
        print(out, r.size, os.path.getsize(out) // 1024, "KB")
