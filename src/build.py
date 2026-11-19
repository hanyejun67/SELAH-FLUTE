"""Subset the page fonts (Korean and Latin) to the characters the page uses and inline them as data URIs."""
import base64, io, sys
from fontTools import subset
from fontTools.ttLib import TTFont

src, out, pre, maru, latin = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
html = open(src, encoding="utf-8").read()

chars = set(html)
chars |= set(chr(c) for c in range(0x20, 0x7F))
chars |= set("①②③·…“”‘’—–")
text = "".join(sorted(ch for ch in chars if ch.isprintable()))

# only the weights the page actually uses
faces = [
    ("Pretendard", 400, f"{pre}/Pretendard-Regular.woff2"),
    ("Pretendard", 600, f"{pre}/Pretendard-SemiBold.woff2"),
    ("MaruBuri", 300, f"{maru}/MaruBuri-Light.woff2"),
    ("MaruBuri", 600, f"{maru}/MaruBuri-SemiBold.woff2"),
    ("Cinzel", 500, f"{latin}/cinzel/package/files/cinzel-latin-500-normal.woff2"),
    ("Cormorant Garamond", 500, f"{latin}/cormorant/package/files/cormorant-garamond-latin-500-normal.woff2"),
]

css = []
total = 0
for fam, wt, path in faces:
    font = TTFont(path)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    sub = subset.Subsetter(opts)
    sub.populate(text=text)
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    data = buf.getvalue()
    total += len(data)
    b64 = base64.b64encode(data).decode()
    css.append(
        f'@font-face{{font-family:"{fam}";font-weight:{wt};font-style:normal;font-display:swap;'
        f'src:url(data:font/woff2;base64,{b64}) format("woff2");}}'
    )
    print(fam, wt, len(data), "bytes")

html = html.replace("/*@FONTFACES@*/", "\n".join(css), 1)
open(out, "w", encoding="utf-8").write(html)
print("chars", len(text), "fonts total", total, "html", len(html.encode()))
