"""Less-zoomed close-ups: level crop widened a little; the few corner pixels outside the photo fade into the page's dark vignette."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import cv2, numpy as np
from fitcrop import best_crop, rot_matrix
from grade import grade
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'raw') + '/'
BG = np.array([8, 5, 14], np.float32)  # page background (BGR of #0E0508)
def wide(f, ang, cx, cy, asp, k, ow):
    im = cv2.imread(A + f)
    _, (x, y, w, h) = best_crop(im.shape, ang, cx, cy, asp)
    W2, H2 = w * k, h * k
    M, nW, nH = rot_matrix(im.shape, ang)
    M2 = M.copy(); M2[0, 2] -= cx - W2 / 2; M2[1, 2] -= cy - H2 / 2
    s = ow / W2; M2 *= s; oh = int(round(H2 * s))
    out = cv2.warpAffine(im, M2, (ow, oh), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    valid = cv2.warpAffine(np.full(im.shape[:2], 255, np.uint8), M2, (ow, oh), flags=cv2.INTER_NEAREST, borderValue=0)
    hole = (255 - valid).astype(np.float32) / 255
    a = np.clip(cv2.GaussianBlur(hole, (0, 0), 28) * 1.8, 0, 1)[..., None]
    blur = cv2.GaussianBlur(out, (0, 0), 30).astype(np.float32)
    dark = blur * 0.35 + BG * 0.65
    return (out.astype(np.float32) * (1 - a) + dark * a).astype(np.uint8)
jobs = [('keys', 'ecfd4df7-image.jpg', 25.2, 1150, 1180, 4/3, 1.2, 1200),
        ('cups', '9e120638-image.jpg', 19.1, 860, 610, 4/3, 1.22, 1000),
        ('lip',  '9e120638-image.jpg', 19.1, 1150, 1610, 4/3, 1.18, 1200)]
out_dir = sys.argv[1]
row = []
for k, f, ang, cx, cy, asp, z, ow in jobs:
    r = wide(f, ang, cx, cy, asp, z, ow)
    r = grade(r, wb=(1.035, 1.0, 0.95), gamma=1.05, contrast=0.14, sat=1.06, clahe=0.35, sharpen=0.4)
    cv2.imwrite(os.path.join(out_dir, k + '.jpg'), r, [cv2.IMWRITE_JPEG_QUALITY, 86, cv2.IMWRITE_JPEG_PROGRESSIVE, 1])
    row.append(cv2.resize(r, (520, 390)))
cv2.imwrite('real/wide-sheet.jpg', np.hstack(row), [cv2.IMWRITE_JPEG_QUALITY, 85])
