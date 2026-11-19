"""Hide the engraved serial number in the case photo (owner's request: the serial must never be published).
Works on the original shot, so every derived image is clean. Only the serial line on the barrel is touched.
Usage: python3 tools/redact.py raw/1289e12a-image.jpg"""
import sys, cv2, numpy as np

path = sys.argv[1]
im = cv2.imread(path).astype(np.float32)

# The serial is a narrow column across the tube. Each row is refilled from the clean metal just left
# and right of it, so the tube's own horizontal reflections carry straight through the gap.
x0, x1, y0, y1 = 1738, 1767, 876, 980
left = im[y0:y1, x0 - 4:x0].mean(axis=1, keepdims=True)
right = im[y0:y1, x1:x1 + 3].mean(axis=1, keepdims=True)
t = np.linspace(0, 1, x1 - x0, dtype=np.float32)[None, :, None]
fill = left * (1 - t) + right * t
fill = cv2.GaussianBlur(fill, (0, 0), sigmaX=0.1, sigmaY=1.2)
fill += np.random.default_rng(7).normal(0, 1.6, fill.shape).astype(np.float32)   # match the photo's grain
im[y0:y1, x0:x1] = fill

cv2.imwrite(path, np.clip(im, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 96])
print("redacted", path)
