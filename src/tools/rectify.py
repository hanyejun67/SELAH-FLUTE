import sys, cv2, numpy as np
src, out = sys.argv[1], sys.argv[2]
im = cv2.imread(src)
W, H = 2000, 940
quad = np.float32([[0, 425], [2000, 270], [2000, 1300], [0, 1170]])
rect = np.float32([[0, 0], [W, 0], [W, H], [0, H]])
M = cv2.getPerspectiveTransform(quad, rect)
warped = cv2.warpPerspective(im, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
cv2.imwrite(out, warped, [cv2.IMWRITE_JPEG_QUALITY, 95])
g = warped.copy()
for y in range(0, H, 50):
    cv2.line(g, (0, y), (W, y), (0, 255, 0) if y % 250 else (0, 255, 255), 1)
for x in range(0, W, 100):
    cv2.line(g, (x, 0), (x, H), (0, 255, 0) if x % 500 else (0, 255, 255), 1)
cv2.imwrite(out.replace('.jpg', '-grid.jpg'), cv2.resize(g, (1500, 705)), [cv2.IMWRITE_JPEG_QUALITY, 85])
print('ok')
