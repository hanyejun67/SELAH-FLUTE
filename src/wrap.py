"""Turn the built artifact page into a standalone website (full HTML document, share preview tags, OG image)."""
import shutil, sys, os
from PIL import Image

built, imgdir, outdir, base_url = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].rstrip("/")
html = open(built, encoding="utf-8").read()

html = html.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
cut = html.index('<div class="wrap">')
head_part, body_part = html[:cut], html[cut:]

title = "국내 단 한 대 · 무라마츠 14K+9K 풀옵션 | 셀라플루트"
desc = "5년을 기다린 풀옵션 무라마츠 올골드 14K, 9K. 12월 5일에 도착합니다. 14K 관체 · 9K 금 키 · 전체 수공 각인 · 츠바사 립. 11월 30일 예약 마감."
favicon = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Crect width='64' height='64' rx='14' fill='%230E0508'/%3E"
           "%3Cpath d='M32 10l20 22-20 22-20-22z' fill='%23D6AC68'/%3E%3C/svg%3E")

head = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0E0508">
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="셀라플루트 Selah Flute">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{base_url}/">
<meta property="og:image" content="{base_url}/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
<meta name="color-scheme" content="dark">
<link rel="icon" type="image/svg+xml" href="{favicon}">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<style>html{{-webkit-text-size-adjust:100%;background:#0E0508}}body{{margin:0}}[hidden]{{display:none!important}}img{{max-width:100%}}</style>
"""
doc = head + head_part.replace("<title>무라마츠 14K+9K 풀각인</title>", f"<title>{title}</title>") + "</head>\n<body>\n" + body_part + "\n</body>\n</html>\n"

os.makedirs(os.path.join(outdir, "img"), exist_ok=True)
open(os.path.join(outdir, "index.html"), "w", encoding="utf-8").write(doc)
for f in os.listdir(imgdir):
    if f.endswith((".jpg", ".png", ".webp")):
        shutil.copy(os.path.join(imgdir, f), os.path.join(outdir, "img", f))

icondir = os.path.join(os.path.dirname(os.path.abspath(imgdir)), "icons")
for f in os.listdir(icondir):
    shutil.copy(os.path.join(icondir, f), os.path.join(outdir, f))

# 1200x630 share image, rendered separately from the real case photo
shutil.copy(os.path.join(os.path.dirname(os.path.abspath(imgdir)), "og-real.jpg"), os.path.join(outdir, "og.jpg"))
print("site written", sorted(os.listdir(outdir)), len(doc.encode()), "bytes html")
