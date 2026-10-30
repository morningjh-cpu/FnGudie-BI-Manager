# 18. WiseReport B2B 대표상품 → B2C 독립 체계 (2026-10-30)

## 요청
- WiseReport가 B2B 대표상품에서 B2C 독립 체계로 바뀜
- 순서는 Retamin과 FnAPI 사이, 메인 컬러 #594FC8
- 서체 미리보기에도 색상 추가
- 홈 최근 업데이트에는 이 변경을 싣지 않음(사용자 요청)

## 결정
- 로고 글자는 지금처럼 전용서체(색만 #594FC8)
- 순서는 모든 곳에서 Retamin → WiseReport → FnAPI. 다운로드 표에서 FnAPI를 Retamin 앞으로 옮기던 예외 규칙은 지움

## 반영
- scripts/build_logotypes.py: WiseReport 를 b2c·#594FC8 로, 리타민을 B2C 맨 앞에 넣도록. B2C 색 이름 "리타민 · WiseReport · API". 다시 실행 → logos.js · logos/wisereport.svg (흰색 판은 같음)
- index.html
  - B2C_COLORS 에 wisereport #594FC8 (로고타입 소개 컬러 배경·디자인 아티클 오픈 그래프 바탕)
  - 홈 컬러 카드 B2C: 이름·칩·색 코드에 WiseReport
  - B2C 로고타입 소개: 컬러 줄·안내문
  - 사용 규칙 배경 조합: "B2C · WiseReport" 줄(흰 배경 대비 6.22, 계산값)
  - 서체 미리보기 색상칩: 지수 다음에 WiseReport #594FC8 추가, FnAPI 칩 이름은 "B2C 독립" → "API"
  - 다운로드 표 예외 규칙 삭제, logos.js 불러오기 ?v=1.31w
- 공유 문서 out/FnGuide-Logotype-share.md · .html: B2B 대표 목록에서 빼고 B2C 줄에 추가
- 헤드리스 크롬 화면으로 홈·서체 소개·B2C·사용 규칙·다운로드 확인

## 추가: WiseReport 심볼 (2026-10-30)
- 사용자가 디자인한 심볼 data/Symbol/wisereport/WR-White.svg (512, 바탕 #594FC8 + 흰 W·R + 보라 그림자 그러데이션 2개)
- scripts/build_symbols.py: 일러스트레이터 파일도 읽게 함(클래스 색 → fill, 한글 그러데이션 id → 영문. 사이트가 id 뒤에 크기를 붙일 때 영문만 알아봄). 설명 문구 "Wise·Report 이니셜 W·R"
- 디자인 아티클에서 WiseReport · 심볼 이 기본 선택. 아이콘·애플 터치 아이콘(네모 바탕이라 모서리 채우기 필요 없음) 화면 확인. symbols.js ?v=3
- 심볼 업데이트(2026-10-30 11:16): W 가운데가 갈라진 모양, 그림자는 검정 그러데이션 + 곱하기(multiply)·70% 투명. 도구가 fill 외 속성(opacity·mix-blend-mode·isolation)도 옮기게 고침. symbols.js ?v=4
