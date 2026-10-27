# HANDOFF — 이 파일은 clear 전에 항상 최신으로 덮어쓴다 (이 줄 포함)

## 현재 상태
- 주제: FnGuide Brand Identity Management(회사 CI/BI 자원 관리·공유 서비스) 웹페이지 디자인
- 요청·결정 기록: plan/phase-1/01~06 (06에 최종 콘텐츠 결정)
- 2차 시안 완성: index.html(폴더 맨 위로 옮김, 그림·서체·logos.js 등은 out/brand-site/ 그대로) — 위쪽 메뉴(왼쪽 FnGuide Brand Identity, 오른쪽 회사소개·그룹웨어·FnGuide.com 새 창) + 왼쪽 메뉴 구조
  - BI 디자인 운영(홈: 소개·브랜드 방향·사업별 컬러 체계·B2B/B2C·기대 효과·최근 업데이트) — 메뉴 숫자는 없앰
  - 브랜드 전용서체 소개(왜·업데이트 현황·사양·품질 기준·미리보기·사용 방법·파일 받기). 미리보기 문구를 SVG·PNG로 받기 가능(font-data.js 의 글자 윤곽·간격으로 그림, 하르프버즈 조판과 5천여 문구 일치 확인)
  - 브랜드 로고타입 소개(하위: B2B 대표/지수/펀드/B2B 계약/B2C/회사 CI — 흰 배경+컬러 배경 흰색 판, 웹사이트 링크(서비스 이력 메모는 삭제), CI 화면에 로고타입 개선·이전 CI 2종 전시용)
  - 로고타입 다운로드(로고 컬러·흰색 SVG/PNG. 서체 파일은 전용서체 소개에만), 사용 규칙(원칙·배경 조합·협력사·매뉴얼 빈칸)
- 사이트는 전용서체 v1.200 반영 완료(서체 파일·로고타입 13종·업데이트 글). 기록: plan/phase-1/09. 옛 v1.100 서체·로고는 _trash/
- 로고 만들기: py scripts/build_logotypes.py (fonttools·uharfbuzz 설치됨). 서체는 기둥 조정본 out/font-update/v1.200/fonts 를 씀(조정 전 서체는 out/font-update/logo-font). 로고는 조정본으로 다시 만든 상태(?v=1.200z)
  - 펀드에 FnSpectrum·FnARES 추가(2026-10-27). 서비스 웹사이트 링크는 스크립트의 SERVICE_URL(서비스 18종 입력됨. FnARES 는 개발 서버(devares) 주소. 없는 것: MarketMonitor·FnAPI·회사 CI)
  - 서비스 17종 전용서체 조판 / 회사 CI 공식 원본 / 리타민 피그마 원래 로고 / 흰색 판 logos/white / 이전 CI는 data/figma-logo-parts 조각으로 합침
  - 미리보기용 글자 정보만 다시 만들 땐 py scripts/build_logotypes.py --font-data (사이트 fonts/ 의 OTF 를 읽음)
  - scripts/build_logos.py 는 옛 피그마 로고용, 더 이상 안 씀
- 회사 CI(공식) = 홈페이지 CIP 파일(data/corp-cip), 색 FnWine #94243A(홈페이지 표기 Fn Red, 홈페이지 HEX #962E45는 오류)·FnDarkGray #778288(홈페이지 표 #6B7B84 대신). 개선된 브랜드 로고 = FnRed 2025 #B9023D(B2B와 같은 색)
- 리타민 주 #1C1C3A · 보조 #26C0D2
- 로고 표시 크기: 다운로드 표·로고타입 카드 모두 같은 배율(DL_SCALE·STAGE_SCALE)로 글자 크기 통일
- 사이트는 내 컴퓨터용 파일. 서체가 사내 전용이라 인터넷 공유 안 함
- 받는 SVG·PNG는 그림 둘레에 여백을 넣음(2026-10-27 요청): SVG 10px, PNG는 파일 안에서 16px(4배 크기 기준). index.html 의 PAD_SVG·PAD_PNG. 회사 CI 원본 압축(AI·PNG)은 원본 그대로라 해당 없음
- 확인 완료(2026-10-27, Edge 자동 조작): 로고 SVG·PNG 단추 90종, 서체 3종, 회사 CI 압축 2종, 서체 미리보기 SVG·PNG 받기 모두 정상
- FnAPI 로고는 이미 전용서체로 만든 것(별도 작업 없음)
- 회사 CI 전용색상 표의 Pantone·CMYK 값은 홈페이지 값 그대로(검증 안 됨)

## 다음 할 일
- 전용서체 v1.200 완성(새 글자 f m M s S y r 반영 + I 기둥 -4% 시안 A 반영 + f 이어 쓰기 8종 다시 만듦): out/font-update/v1.200/ (fonts, preview, 만든 과정). 기록: plan/phase-1/07
- r 까지 사이트 반영 완료(plan/phase-1/09 추가분). 불러오기 주소 ?v=1.200r
- f·m·r 기둥 0.15(≈4%) 가늘게 조정 완료(plan/phase-1/08 추가분). 사이트 다운로드 파일·업데이트 글·규칙 수(1,203)·로고타입 모두 반영(plan/phase-1/09·10)
- 공유 문서(전용서체 결과 공유) = out/FnGuide-Logotype-share.md (v1.200). 서체·사이트가 바뀌면 이 문서도 함께 갱신(사용자 요청). data/ 의 v1.0 copy.md 는 받은 원본 그대로
- 결정 대기 4건 정리 완료(plan/phase-1/10): 로고타입 조정본으로 다시 만듦, data/FnGuide-Logotype-Font 의 fonts·spacing 을 v1.200 으로 교체(source-svg 는 8_v1.200/ 추가; README·proof·preview·build 는 아직 v1.100 기준으로 섞여 있음; 옛 파일 _trash/data-font-v1.100/)
- 남은 것: f 이어 쓰기 8종 디자이너 확인(사람이 할 일, 보낼 글 out/font-update/f-이어쓰기-디자이너확인요청.md, 회신 대기)
- 서체를 또 고치면: work 에서 다시 만들기 → v1.200 폴더 갱신 → out/brand-site/fonts 복사 → py scripts/build_logotypes.py(또는 --font-data) → index.html 의 ?v= 숫자 올리기(서체·logos.js·font-data.js)
- 서체 다시 만드는 법: out/font-update/work 에서 sh run_all.sh (numpy·matplotlib·scipy·scikit-image 설치 필요). 새 글자 SVG 는 py scripts/font_prepare_update.py 로 정리해 all/ 에 넣음
