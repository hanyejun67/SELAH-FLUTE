#!/bin/bash
# Web fonts used by the page (subset and inlined at build time)
set -e
cd "$(dirname "$0")"
mkdir -p fontpkgs && cd fontpkgs
npm pack --silent pretendard@1.3.9 @kfonts/maruburi@0.1.0 @fontsource/cinzel@5.3.0 @fontsource/cormorant-garamond@5.3.0 >/dev/null
mkdir -p pretendard maruburi cinzel cormorant
tar xzf pretendard-1.3.9.tgz -C pretendard
tar xzf kfonts-maruburi-0.1.0.tgz -C maruburi
tar xzf fontsource-cinzel-5.3.0.tgz -C cinzel
tar xzf fontsource-cormorant-garamond-5.3.0.tgz -C cormorant
rm -f *.tgz
echo "fonts ready"
