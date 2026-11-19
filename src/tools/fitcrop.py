import cv2, numpy as np
def rot_matrix(shape, ang):
    H, W = shape[:2]
    M = cv2.getRotationMatrix2D((W/2, H/2), ang, 1.0)
    c, s = abs(M[0,0]), abs(M[0,1]); nW = int(H*s + W*c); nH = int(H*c + W*s)
    M[0,2] += nW/2 - W/2; M[1,2] += nH/2 - H/2
    return M, nW, nH
def inside(shape, M, pts):
    H, W = shape[:2]
    Mi = cv2.invertAffineTransform(M)
    src = (Mi[:, :2] @ np.array(pts, float).T).T + Mi[:, 2]
    return np.all((src[:,0] >= 0) & (src[:,0] <= W-1) & (src[:,1] >= 0) & (src[:,1] <= H-1))
def best_crop(shape, ang, cx, cy, aspect, maxw=4000):
    M, nW, nH = rot_matrix(shape, ang)
    lo, hi = 10, maxw
    while hi - lo > 2:
        w = (lo + hi) / 2; h = w / aspect
        pts = [[cx-w/2, cy-h/2], [cx+w/2, cy-h/2], [cx+w/2, cy+h/2], [cx-w/2, cy+h/2]]
        if inside(shape, M, pts): lo = w
        else: hi = w
    w = lo; h = w / aspect
    return M, (int(cx-w/2), int(cy-h/2), int(w), int(h))
def render(im, ang, box, out_w=None):
    M, nW, nH = rot_matrix(im.shape, ang)
    x, y, w, h = box
    M2 = M.copy(); M2[0,2] -= x; M2[1,2] -= y
    if out_w:
        s = out_w / w; M2 *= s; w2, h2 = out_w, int(round(h*s))
    else: w2, h2 = w, h
    return cv2.warpAffine(im, M2, (int(w2), int(h2)), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
