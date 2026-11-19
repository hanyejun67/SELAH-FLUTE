# 무라마츠 14K+9K 판매 페이지 — 소스

배포 사이트: https://selah-muramatsu.vercel.app (Vercel 프로젝트 `selah-muramatsu`, `muramatsu` 브랜치 루트를 그대로 서빙)

이 브랜치(`muramatsu-src`)는 편집용 소스입니다. 배포 브랜치(`muramatsu`)에는 빌드 결과만 올립니다.

## 구조
- `src/page.html` — 페이지 원본 (HTML/CSS/JS 한 파일, 인트로 포함). `/*@FONTFACES@*/` 자리에 빌드 때 폰트가 들어갑니다.
- `src/img/` — 실물 사진(보정본), 케이스 일러스트, 가죽 질감. `.webp`는 같은 사진을 화면 크기별로 줄인 사본(srcset용). `src/og-real.jpg` — 공유 미리보기 이미지.
- `src/icons/` — 파비콘 PNG(32px), 홈 화면 아이콘(180px).
- `src/raw/` — 원본 실물 사진 5장 (보정 전).
- `src/tools/` — 사진 보정 스크립트 (수평·색·크롭만, 생성/합성 없음).
- `src/caser/` — 실버/올골드 케이스 비교 일러스트 렌더러 (Playwright).

## 빌드
```
./src/build.sh        # -> dist/  (index.html, og.jpg, img/)
```
폰트(Pretendard, MaruBuri, Cinzel, Cormorant Garamond)는 페이지에 실제로 쓰인 글자만 잘라 base64로 넣습니다. 외부 폰트 요청은 없습니다. 문구를 바꾸면 반드시 다시 빌드해야 새 글자가 들어갑니다.

## 배포
```
git worktree add ../deploy muramatsu
rm -rf ../deploy/img && cp -r dist/* ../deploy/
cd ../deploy && git add -A && git commit -m "..." && git push origin muramatsu
```
그다음 Vercel 대시보드에서 `selah-muramatsu` 프로젝트의 Production Redeploy (또는 `vercel --prod`).

## 사진 재처리 (필요할 때만)
```
cd src && mkdir -p real
python3 tools/rectify.py raw/1289e12a-image.jpg real/case-rect.jpg   # 케이스 전체 수평·원근 보정
python3 tools/real_assets.py img                                    # 케이스 반쪽, 클로즈업, 가죽 질감
python3 tools/wide_crops.py img                                     # 키/키컵/립플레이트 카드용 크롭
python3 tools/webp.py img                                           # 사진을 바꿨다면 WebP 사본도 다시 만든다
```
`real_assets.py`는 `opencv-python-headless`가 필요하고, 히어로용 2000px WebP(`case-lid-2000.webp`, `case-base-2000.webp`)도 함께 만듭니다.

## 디자인 값
색·간격·모서리·모션·금속 값은 `src/page.html` 맨 위 `:root`에 한 벌로 모여 있습니다. 새 값을 직접 쓰지 말고 이 변수를 쓰세요.
- 간격은 8pt 단위, 모서리는 사진 4px / 카드·버튼 8px.
- 모션은 커브 2개(`--ease-out`, `--ease-io`)와 시간 3단계(`--t1` 0.12s, `--t2` 0.32s, `--t3` 0.64s).
- 가운뎃점은 `<i class="sep"> · </i>`(구 사이), `<i class="mid">·</i>`(낱말 사이)로 감싸 간격을 맞춥니다.
