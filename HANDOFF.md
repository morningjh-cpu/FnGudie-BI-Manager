# HANDOFF — 이 파일은 clear 전에 항상 최신으로 덮어쓴다 (이 줄 포함)

## 현재 상태
- 주제: FnGuide Brand Identity Management(회사 CI/BI 자원 관리·공유 서비스) 웹페이지 디자인
- 요청·결정 기록: plan/phase-1/01~06 (06에 최종 콘텐츠 결정)
- 왼쪽 메뉴: 마우스를 올리면 글자색 #B9023D(위쪽 메뉴 회사소개와 같은 색), 선택된 1단계 메뉴는 배경 없이 글자색 #B9023D + 굵게 + 밑줄(글자와 1px 띄움, offset 2px), 선택된 하위 메뉴는 옅은 배경 + 글자색 #B9023D + 굵게
- 로고타입 다운로드 맨 아래 "전체 로고타입 받기 (ZIP)" 버튼(2026-10-29): 표의 로고 23종 × 컬러·흰색 × SVG·PNG(4배) = 90개 파일을 브라우저에서 바로 묶음(외부 라이브러리 없음, 개별 받기와 같은 여백·크기). 크롬에서 눌러 ZIP 정상 확인
- 담당 부서 표기: "웹&모바일팀 디자인 파트"(사이트·공유 문서 모두, 2026-10-29)
- 홈 바로가기 카드: 링크 문구는 카드 맨 아래 고정, 마우스를 올리면 움직이지 않고 약한 그림자. 본문 글자 링크는 마우스를 올리면 #B9023D
- 2차 시안 완성: index.html(폴더 맨 위로 옮김, 그림·서체·logos.js 등은 out/brand-site/ 그대로) — 위쪽 메뉴(왼쪽 FnGuide Brand Identity, 오른쪽 회사소개·그룹웨어·FnGuide.com 새 창) + 왼쪽 메뉴 구조
  - BI 디자인 운영(홈: 소개·브랜드 방향·사업별 컬러 체계·B2B/B2C·기대 효과·최근 업데이트) — 메뉴 숫자는 없앰
  - 브랜드 전용서체 소개 — 하위 메뉴 3개(이 순서): 서체 소개(#font) · 폰트 업데이트(#font/update, 제목 Font Update, 2026-10-29 추가. 버전별 수정 전/후 + 버전 이력 표. 새 버전은 page-update 맨 위에 단락 추가 + 버전 이력 맨 위에 한 줄) · 디자인 크리틱(#font/critique, 제목 Design Critic, 2026-10-29 추가. 크리틱 이력 표 + 회차별 결과. 그림은 out/font-critique/img 를 불러옴. 새 회차는 index.html 의 page-critique 이력 표에 줄 추가 + 회차 단락 추가)
  - 서체 소개(왜·현재 버전 한 줄 링크·사양·품질 기준·미리보기·사용 방법·파일 받기). 미리보기 문구를 SVG·PNG로 받기 가능(font-data.js 의 글자 윤곽·간격으로 그림, 하르프버즈 조판과 5천여 문구 일치 확인)
  - 브랜드 로고타입 소개(하위: B2B 대표/지수/펀드/B2B 계약/B2C/회사 CI — 흰 배경+컬러 배경 흰색 판, 웹사이트 링크(서비스 이력 메모는 삭제), CI 화면에 로고타입 개선·이전 CI 2종 전시용)
  - 로고타입 다운로드(로고 컬러·흰색 SVG/PNG. 서체 파일은 전용서체 소개에만), 사용 규칙(원칙·배경 조합·협력사·매뉴얼 빈칸)
- **사이트 콘텐츠 크리틱 완료(2026-10-29)**: 브랜드 전략가·카피라이터·UX 콘텐츠 3인, 수정 필요 6·개선 권장 18·유지 6, 문장 수정안(지금→수정안). 보고서 out/content-critique/brand-site-content-critique.html, 기록 plan/phase-1/15. 결정 필요 없는 수정안 45곳 반영 완료(plan/phase-1/15 반영 단락). 품질 수치 v1.3 으로 다시 잼(1,268 규칙·9,793쌍 충돌 0), 그 과정에서 CV·CW·CY 닿음 발견 → 서체 커닝 고침(plan/phase-1/14). 폰트 업데이트 화면은 ₩ 숨김·받기 항목 삭제. 결정 완료(2026-10-29): 헤더 안내문 유지(이후 사용자 요청으로 삭제), 연락처 넣지 않음, 한글 지정 서체 없음(규칙 04 문장 삭제), 메뉴 이름·기대 효과는 제외(현행 유지), 사양의 ₩ 유지
- **전용서체 v1.3 완성·사이트 반영(2026-10-29)**: 크리틱 수정 필요 5건 + ⑥ 1 받침·l 꼬리 + ⑨ 금융 기호 5개·고정폭 숫자(tnum). 서체 out/font-update/v1.3/fonts, 압축 out/FnGuideLogotype-v1.3.zip(옛 v1.200 zip 은 out/font-backup/), 만드는 도구 py scripts/build_v13.py(v1.200 서체 + 개선안 윤곽, --control 로 v1.200 그대로 다시 만들어 비교 가능). 로고타입 17종도 v1.3 으로 다시 만듦(사용자 결정). 기록 plan/phase-1/14. 디자이너 확인은 아직
- (이전) 사이트 v1.200 반영 기록: plan/phase-1/09. 옛 v1.100 서체·로고는 _trash/
- 로고 만들기: py scripts/build_logotypes.py (fonttools·uharfbuzz 설치됨). 서체는 최신 out/font-update/v1.3/fonts 를 씀(v1.200·조정 전 서체는 out/font-update/v1.200, logo-font). 불러오기 번호 ?v=1.3
  - 펀드에 FnSpectrum·FnARES 추가(2026-10-27). 서비스 웹사이트 링크는 스크립트의 SERVICE_URL(서비스 18종 입력됨. FnARES 는 개발 서버(devares) 주소. 없는 것: MarketMonitor·FnAPI·회사 CI)
  - 서비스 17종 전용서체 조판 / 회사 CI 공식 원본 / 리타민 피그마 원래 로고 / 흰색 판 logos/white / 이전 CI는 data/figma-logo-parts 조각으로 합침
  - 미리보기용 글자 정보만 다시 만들 땐 py scripts/build_logotypes.py --font-data (사이트 fonts/ 의 OTF 를 읽음)
  - scripts/build_logos.py 는 옛 피그마 로고용, 더 이상 안 씀
- 회사 CI(공식) = 홈페이지 CIP 파일(data/corp-cip), 색 FnWine #94243A(홈페이지 표기 Fn Red, 홈페이지 HEX #962E45는 오류)·FnDarkGray #778288(홈페이지 표 #6B7B84 대신). 개선된 브랜드 로고 = FnRed 2025 #B9023D(B2B와 같은 색)
- 리타민 주 #1C1C3A · 보조 #26C0D2
- 로고 표시 크기: 다운로드 표·로고타입 카드 모두 같은 배율(DL_SCALE·STAGE_SCALE)로 글자 크기 통일
- 사이트는 내 컴퓨터용 파일. 서체가 사내 전용이라 인터넷 공유 안 함
- 받는 SVG·PNG는 그림 둘레에 여백을 넣음(2026-10-27 요청): SVG 10px, PNG는 파일 안에서 16px(4배 크기 기준). index.html 의 PAD_SVG·PAD_PNG. 회사 CI 원본 압축(AI·PNG)은 원본 그대로라 해당 없음
- 서체 미리보기(2026-10-27): 입력한 문구는 색을 바꿔도 유지, 색상칩 B2B 대표·B2B 계약·펀드·지수·B2C 독립·흰색·사용자(웹 컬러 코드 입력) 순·같은 간격·이름 표기, 기본색 FnRed, 크기 32~150px 게이지+숫자 칸, 미리보기 칸 높이 고정(한 줄, 긴 문구는 옆으로 넘김), 게이지 막대 연회색·손잡이 고른 색, 알파벳 세트 36px·자간 6px
- 그룹 순서: 홈 컬러 카드·다운로드 표 = 회사 CI→B2B 대표→B2B 계약→펀드→지수→B2C, 로고타입 소개 하위 메뉴 = B2B 대표→B2B 계약→펀드→지수→B2C→회사 CI
- 확인 완료(2026-10-27, Edge 자동 조작): 로고 SVG·PNG 단추 90종, 서체 3종, 회사 CI 압축 2종, 서체 미리보기 SVG·PNG 받기 모두 정상
- FnAPI 로고는 이미 전용서체로 만든 것(별도 작업 없음)
- 회사 CI 전용색상 표의 Pantone·CMYK 값은 홈페이지 값 그대로(검증 안 됨)

## 다음 할 일
- 크리틱 개선 권장 ⑥(1·I·l 구분)·⑨(고정폭 숫자·금융 기호) 개선안 각 2개 제안(2026-10-29): plan/phase-1/12, 보고서 out/font-critique/FnGuide-Logotype-v1.200-proposal.html, 그림 out/font-critique/img/20~25, 도구 scripts/font_critique/drafts.py. ⑥ 은 안 A 결정 — 받침을 F 왼쪽 위 세리프를 뒤집어 좌우 대칭으로 붙인 형태로 수정, 받침 너비는 해외 서체 비율로 420(그림 28). 안 B(l 꼬리)도 시안 진행 — t 꼬리를 가져와 끝이 얇게(그림 31·32, tail_l.py), 1 과 l 모두 마지막 수정본으로 반영 결정(로고 CompanyGlobal·ETF Global 2종도 바뀜). 금융 기호: − 는 + 너비 기준 0.98, × 는 492 네모·획 94, ₩ 가로획 65(그림 26·27, one_base.py). ⑨ 은 안 B 결정 — 비례 숫자 유지 + 고정폭 선택 기능, 새 1 반영, 금융 기호 1순위(₩ 한 줄형 − ± × ·)만(그림 29·30, symbols.py). 시안 그림만, 서체 파일은 그대로
- 개선안 보고서를 수정 전/후 형식으로 다시 씀(2026-10-29): 수정 필요 ①~⑤ + ⑥ 1 받침·l 꼬리 + ⑨ 안 B·금융 기호 5개만 실음. 그림 33~39, 도구 scripts/font_critique/after.py, 기록 plan/phase-1/13. 이전판은 _trash/. 서체 파일은 그대로 — 다음: 디자이너 확인, v1.300 제작 여부 결정
- 전용서체 v1.200 디자인 크리틱 완료(2026-10-27): 기록 plan/phase-1/11, 보고서 out/font-critique/FnGuide-Logotype-v1.200-critique.html(그림 img/, 수치 metrics.json), 도구 scripts/font_critique/. 사용자 결정 대기: 수정 필요 5건(C·G 높이, v·w·x·y 높이, o·c·e 위 넘침, ft·fj 이어 쓰기, 파일 높이 값·Regular 표시)을 v1.300으로 반영할지 / 서체 사용 범위(로고·제목 전용 또는 본문·표까지) / 사용 규칙에 최소 크기·한글 짝 서체 넣을지
- 전용서체 v1.200 완성(새 글자 f m M s S y r 반영 + I 기둥 -4% 시안 A 반영 + f 이어 쓰기 8종 다시 만듦): out/font-update/v1.200/ (fonts, preview, 만든 과정). 기록: plan/phase-1/07
- r 까지 사이트 반영 완료(plan/phase-1/09 추가분). 불러오기 주소 ?v=1.200r
- f·m·r 기둥 0.15(≈4%) 가늘게 조정 완료(plan/phase-1/08 추가분). 사이트 다운로드 파일·업데이트 글·규칙 수(1,203)·로고타입 모두 반영(plan/phase-1/09·10)
- 공유 문서(전용서체 결과 공유) = out/FnGuide-Logotype-share.md · .html (v1.3). 서체·사이트가 바뀌면 이 문서도 함께 갱신(사용자 요청). data/ 의 v1.0 copy.md 는 받은 원본 그대로
- 결정 대기 4건 정리 완료(plan/phase-1/10): 로고타입 조정본으로 다시 만듦, data/FnGuide-Logotype-Font 의 fonts·spacing 을 v1.200 으로 교체(source-svg 는 8_v1.200/ 추가; README·proof·preview·build 는 아직 v1.100 기준으로 섞여 있음; 옛 파일 _trash/data-font-v1.100/)
- 남은 것: f 이어 쓰기 8종 확인 — 사용자가 2026-10-28 회사에서 직접 확인·정리 예정(보낼 글 out/font-update/f-이어쓰기-디자이너확인요청.md, 그림·파일 링크 포함)
- 서체를 또 고치면(v1.3 부터): scripts/build_v13.py 처럼 앞 버전 서체를 읽어 바꿀 글자만 바꿔 새 버전 폴더에 만들기 → zip·옛 zip 은 font-backup → out/brand-site/fonts 복사 → py scripts/build_logotypes.py(또는 --font-data) → index.html 의 ?v= 숫자 올리기(서체·logos.js·font-data.js)
- 서체 다시 만드는 법: out/font-update/work 에서 sh run_all.sh (numpy·matplotlib·scipy·scikit-image 설치 필요). 새 글자 SVG 는 py scripts/font_prepare_update.py 로 정리해 all/ 에 넣음
