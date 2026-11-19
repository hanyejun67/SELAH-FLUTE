#!/bin/bash
# page.html -> ../dist (index.html with subset fonts inlined, og.jpg, img/)
set -e
cd "$(dirname "$0")"
[ -d fontpkgs/pretendard ] && [ -d fontpkgs/cinzel ] || ./setup_fonts.sh
python3 -c "import fontTools, brotli" 2>/dev/null || pip install --quiet fonttools brotli
rm -rf ../dist
python3 build.py page.html built.html fontpkgs/pretendard/package/dist/web/static/woff2 fontpkgs/maruburi/package fontpkgs
python3 wrap.py built.html img ../dist https://selah-muramatsu.vercel.app
rm -f built.html
