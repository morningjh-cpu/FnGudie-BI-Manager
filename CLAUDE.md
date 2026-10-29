이 폴더는 FnGuide Brand Identity Management(회사 CI/BI 자원 관리·공유 서비스) 웹페이지 디자인 프로젝트다.
처음 시작할 때는 내 말을 plan/phase-1/01-상황.md 에 받아쓰고 위 첫 줄의 (주제)를 채운 뒤, 이 폴더에서 git init 하고 "시작"으로 첫 커밋한다.
폴더 역할 — plan/: 계획·결정, phase 별로 나누고 파일은 01-부터 번호. data/: 받은 파일, 고치지 않는다. out/: 만든 결과물. scripts/: 네가 짠 도구.
흐름이 크게 바뀌면 plan/phase-2/ 를 새로 만든다. 새 일은 번호를 늘려 새 파일, 옛 파일은 지우지 않는다.
다른 폴더가 필요하면 영문 이름으로 만들고 이 파일에 역할을 한 줄 적는다.
.vscode/: VS Code 설정. 마크다운 미리보기를 밝은 화면으로(markdown-light.css).
out/font-backup/: 옛 버전 폰트 압축 파일 보관.
data/Symbol/: 서비스 심볼 원본(피그마 내보내기 포함). 사이트용은 py scripts/build_symbols.py 로 out/brand-site/symbols.js 에 만든다.
index.html(맨 위): 브랜드 사이트 페이지. out/ 규칙의 예외로 맨 위에 둔다. 서체·logos.js·font-data.js·다운로드 파일은 out/brand-site/ 에 그대로 두고 페이지가 그 위치를 불러온다.
폰트가 업데이트되면 — ① 폰트 안의 버전을 확인하고 ② otf·ttf·woff 3개만 out/FnGuideLogotype-v(버전).zip 으로 묶는다(압축 안 폴더·파일 이름에도 버전 표시). ③ out/ 에 있던 옛 버전 zip은 out/font-backup/ 으로 옮긴다. out/ 에는 최신 zip 하나만 둔다.
HANDOFF.md 에 현재 상태와 다음 할 일을 적어 두고, clear 하기 전에 항상 최신으로 덮어쓴다.
내 수준에 맞춰 전문용어 없이 말해라. 애매하면 먼저 물어라.
