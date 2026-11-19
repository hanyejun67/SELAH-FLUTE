"""Real photos -> site assets. Case: straightened, warm-graded, split at the hinge, ends finished with the case's own leather."""
import sys, os, cv2, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from grade import grade
from fitcrop import best_crop, render

A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw') + '/'
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
Q = [cv2.IMWRITE_JPEG_QUALITY, 86, cv2.IMWRITE_JPEG_PROGRESSIVE, 1, cv2.IMWRITE_JPEG_OPTIMIZE, 1]

case = grade(cv2.imread('real/case-rect.jpg'), wb=(1.05, 1.0, 0.91))
cv2.imwrite(os.path.join(OUT, 'case-full.jpg'), case, Q)

HINGE = 440
lid, base = case[:HINGE].copy(), case[HINGE:].copy()

# leather strip from the lid's own left wall (real grain), used to close the cut ends
strip = case[60:380, 2:46].astype(np.float32)
rim = case[8:38, 400:1500].reshape(-1, 3).astype(np.float32)
strip = (strip - strip.reshape(-1, 3).mean(0)) * 0.7 + rim.mean(0) * 0.96
SW = 46
def finish_ends(part):
    h, w = part.shape[:2]
    p = part.astype(np.float32)
    tex = cv2.resize(strip, (SW, h), interpolation=cv2.INTER_CUBIC)
    for side in ('l', 'r'):
        t = tex if side == 'l' else tex[:, ::-1]
        a = np.ones((h, SW), np.float32)
        ramp = np.linspace(1, 0, 8)
        if side == 'l': a[:, SW-8:] = ramp
        else: a[:, :8] = ramp[::-1]
        a = a[..., None]
        sl = slice(0, SW) if side == 'l' else slice(w - SW, w)
        p[:, sl] = t * a + p[:, sl] * (1 - a)
        # soft shadow the rim casts into the compartment
        sh = np.linspace(0.62, 1.0, 22)[None, :, None]
        if side == 'l': p[:, SW-4:SW+18] *= sh
        else: p[:, w-SW-18:w-SW+4] *= sh[:, ::-1]
    return np.clip(p, 0, 255).astype(np.uint8)

lid, base = finish_ends(lid), finish_ends(base)
# 2000px halves for large retina screens: the base is native at this size (the source photo is 2000px wide)
for name, part in (('case-lid', lid), ('case-base', base)):
    cv2.imwrite(os.path.join(OUT, name + '-2000.webp'), cv2.resize(part, (2000, 500), interpolation=cv2.INTER_LANCZOS4), [cv2.IMWRITE_WEBP_QUALITY, 82])
W2, H2 = 1600, 400
lid = cv2.resize(lid, (W2, H2), interpolation=cv2.INTER_AREA)       # lid is foreshortened in the shot; matched to the base
base = cv2.resize(base, (W2, H2), interpolation=cv2.INTER_AREA)
cv2.imwrite(os.path.join(OUT, 'case-lid.jpg'), lid, Q)
cv2.imwrite(os.path.join(OUT, 'case-base.jpg'), base, Q)
cv2.imwrite('real/case-open-preview.jpg', np.vstack([lid, base]), Q)

# close-ups: level, then crop
close = [
    ('keys',  'ecfd4df7-image.jpg', 25.2, 1150, 1180, 4/3, 1200),
    ('cups',  '9e120638-image.jpg', 19.1, 860,  580,  4/3, 1000),
    ('lip',   '9e120638-image.jpg', 19.1, 1150, 1640, 4/3, 1200),
    ('badge', '32a4778b-image.jpg', 10.5, 830,  900,  4/3, 1200),
    ('latch', 'd751cb7b-image.jpg', 10.5, 930,  950, 4/3, 1200),
]
for k, f, ang, cx, cy, asp, ow in close:
    im = cv2.imread(A + f)
    _, box = best_crop(im.shape, ang, cx, cy, asp)
    r = render(im, ang, box, out_w=ow)
    leather = k in ('badge', 'latch')
    r = grade(r, wb=(1.05, 1.0, 0.91) if leather else (1.035, 1.0, 0.95), gamma=1.18 if leather else 1.05,
              contrast=0.14, sat=1.06, clahe=0.25 if leather else 0.35, sharpen=0.4)
    cv2.imwrite(os.path.join(OUT, k + '.jpg'), r, Q)
    print(k, box, r.shape)

# leather texture (real lid top) and the brass name plate, for the closed case in the intro
b = cv2.imread(os.path.join(OUT, 'badge.jpg'))
leather = b[30:470, 40:1160]
cv2.imwrite(os.path.join(OUT, 'leather.jpg'), cv2.resize(leather, (1000, 393), interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 80, cv2.IMWRITE_JPEG_PROGRESSIVE, 1])
print('leather mean', leather.reshape(-1,3).mean(0)[::-1].round(1))
