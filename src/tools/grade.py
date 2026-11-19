import cv2, numpy as np

def grade(bgr, wb=(1.06, 1.0, 0.90), gamma=1.12, contrast=0.16, sat=1.10, clahe=0.45, sharpen=0.55):
    """Warm the store fluorescent light, deepen the leather, keep gold highlights crisp."""
    im = bgr.astype(np.float32) / 255.0
    b, g, r = cv2.split(im)
    r *= wb[0]; g *= wb[1]; b *= wb[2]
    im = np.clip(cv2.merge([b, g, r]), 0, 1)
    im = im ** gamma
    # gentle S-curve around mid grey
    im = np.clip(im + contrast * (im - 0.5) * (1 - np.abs(2 * im - 1)) * 2, 0, 1)
    # local contrast on lightness for engraving detail
    lab = cv2.cvtColor((im * 255).astype(np.uint8), cv2.COLOR_BGR2LAB)
    L, A, B = cv2.split(lab)
    if clahe > 0:
        cl = cv2.createCLAHE(clipLimit=1.8, tileGridSize=(8, 8)).apply(L)
        L = cv2.addWeighted(L, 1 - clahe, cl, clahe, 0)
    lab = cv2.merge([L, A, B])
    out = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR).astype(np.float32) / 255
    # saturation
    hsv = cv2.cvtColor(out, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * sat, 0, 1)
    out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    if sharpen > 0:
        bl = cv2.GaussianBlur(out, (0, 0), 1.3)
        out = np.clip(out + sharpen * (out - bl), 0, 1)
    return (out * 255 + 0.5).astype(np.uint8)

def rotate_crop(bgr, angle, cx, cy, w, h):
    """Rotate about (cx, cy) so the given angle becomes level, then cut a w x h box centered there."""
    M = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)
    M[0, 2] += w / 2 - cx
    M[1, 2] += h / 2 - cy
    return cv2.warpAffine(bgr, M, (int(w), int(h)), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 255))

def valid(shape, angle, cx, cy, w, h):
    H, W = shape[:2]
    M = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)
    Mi = cv2.invertAffineTransform(M)
    pts = np.array([[cx - w/2, cy - h/2], [cx + w/2, cy - h/2], [cx + w/2, cy + h/2], [cx - w/2, cy + h/2]])
    src = (Mi[:, :2] @ pts.T).T + Mi[:, 2]
    return bool(np.all(src[:, 0] >= 0) and np.all(src[:, 0] <= W) and np.all(src[:, 1] >= 0) and np.all(src[:, 1] <= H)), src.round(0).tolist()
