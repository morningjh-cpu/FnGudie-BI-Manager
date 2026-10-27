# HANDOFF — 이 파일은 clear 전에 항상 최신으로 덮어쓴다 (이 줄 포함)

## 현재 상태
- 주제: FnGuide Brand Identity Management(회사 CI/BI 자원 관리·공유 서비스) 웹페이지 디자인
- 요청·결정 기록: plan/phase-1/01~06 (06에 최종 콘텐츠 결정)
- 2차 시안 완성: out/brand-site/index.html — 왼쪽 메뉴 구조
  - 0 홈(소개·브랜드 방향·사업별 컬러 체계·B2B/B2C·기대 효과·최근 업데이트)
  - 1 전용서체 소개(왜·업데이트 현황·사양·품질 기준·미리보기·사용 방법·파일 받기)
  - 2 로고타입 소개(하위: B2B 대표/지수/펀드/B2B 계약/B2C/회사 CI — 흰 배경+컬러 배경 흰색 판, 서비스 이력 메모, CI 화면에 로고타입 개선·이전 CI 2종 전시용)
  - 3 다운로드(로고 컬러·흰색 SVG/PNG, 서체 파일), 4 사용 규칙(원칙·배경 조합·협력사·매뉴얼 빈칸)
- 로고 만들기: py scripts/build_logotypes.py (fonttools·uharfbuzz 필요)
  - 서비스 17종 전용서체 조판 / 회사 CI 공식 원본 / 리타민 피그마 원래 로고 / 흰색 판 logos/white / 이전 CI는 data/figma-logo-parts 조각으로 합침
  - scripts/build_logos.py 는 옛 피그마 로고용, 더 이상 안 씀
- 회사 CI(공식) = 홈페이지 CIP 파일(data/corp-cip), 색 Fn Wine #94243A(홈페이지 표기 Fn Red, 홈페이지 HEX #962E45는 오류)·Fn Dark Gray #778288(홈페이지 표 #6B7B84 대신). 개선된 브랜드 로고 = FnRed 2025 #B9023D(B2B와 같은 색)
- 리타민 주 #1C1C3A · 보조 #26C0D2
- 로고 표시 크기: 다운로드 표·로고타입 카드 모두 같은 배율(DL_SCALE·STAGE_SCALE)로 글자 크기 통일
- 사이트는 내 컴퓨터용 파일. 서체가 사내 전용이라 인터넷 공유 안 함
- 확인 안 된 것: 다운로드 단추 실제 동작(브라우저에서 눌러 보기)
- 대기: FnAPI 로고를 전용서체로 둘지 (사용자가 대기 요청)
- 회사 CI 전용색상 표의 Pantone·CMYK 값은 홈페이지 값 그대로(검증 안 됨)

## 다음 할 일
- 사용자가 전용서체(폰트) 디자인을 업데이트할 예정 → 새 서체 파일을 받으면 data/ 에 넣고 py scripts/build_logotypes.py 로 로고타입 다시 만들기, 서체 화면의 버전·업데이트 현황 갱신
