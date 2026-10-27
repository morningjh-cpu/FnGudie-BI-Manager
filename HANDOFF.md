# HANDOFF — 이 파일은 clear 전에 항상 최신으로 덮어쓴다 (이 줄 포함)

## 현재 상태
- 주제: FnGuide Brand Identity Management(회사 CI/BI 자원 관리·공유 서비스) 웹페이지 디자인
- 요청·결정: plan/phase-1/01~03 (화면: 로고 목록/다운로드/사용 규칙, 전용서체 사용, 한글·본문 서체는 안 만듦, 심볼 디자인은 제외)
- 1차 시안 완성: out/brand-site/index.html (내 컴퓨터에서 여는 파일, 인터넷 공유 안 함 — 서체가 사내 전용)
  - 로고 19종: 전용서체로 새로 조판 → scripts/build_logotypes.py (다시 만들기: py scripts/build_logotypes.py, 필요: fonttools·uharfbuzz)
    - 회사 CI FnGuide만 공식 원본(data/FnGuide-Logotype-Font/source-svg/0_logo/FnGuide.svg) 사용 — 서체 문서 "로고를 서체로 대체하지 않음"
    - 피그마 로고(data/figma-logo-parts, scripts/build_logos.py)는 서체 제작 전 옛 로고라 쓰지 않음
    - 색: 서체 문서 그룹 컬러. 회사 CI = FnRed #B9023D (리뉴얼 후). FnWine #94243A 는 리뉴얼 이전 오리지널 CI 색 → 컬러 표 맨 아래 참고용
    - 리타민: B2C 독립 체계라 전용서체 안 씀 → 피그마 원래 로고 그대로 (data/figma-logo-parts/retamin.svg)
  - 서체: data/FnGuide-Logotype-Font/fonts → out/brand-site/fonts 로 복사
  - 문구·색상·규칙은 서체 문서(FnGuide-Logotype-v1.0 copy.md) 4~5장 내용만 사용
- 확인 필요(사용자에게 물어봄)
  - (해결됨) CI 색, 리타민 처리 — plan/phase-1/03 맨 아래
  - 로고 여백·최소 크기·금지 예시: 브랜드 매뉴얼 확정 전이라 "추가 예정" 칸만 둠

## 다음 할 일
- 사용자 검토 의견 반영
