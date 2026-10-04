# PROGRESS

## 2026-10-04 — 초기 구현
- 요구사항 수집
  - 사용자: 한국기계연구원 이차전지장비연구실 실장
  - 목적: 주간/월간 업무보고 양식 통일
  - UI: 입력창 2개 + 출력창 2개 + 생성/복사 버튼
  - 백엔드: Python Flask
  - LLM: Claude (초기엔 API 키 → 이후 Claude CLI로 전환)
- Reference PDF 분석 → 양식 규칙 도출
  - 주간: `### [이차] 제목(책임자)` + `* 일시 및 장소`, `* 주요내용`
  - 월간: `### (카테고리) 제목 (책임자)` + 유사 불릿
- 플랜 승인 후 구현
  - `app.py`, `prompts.py`, `static/{index.html,style.css,app.js}`
  - 초기엔 Anthropic SDK + `.env`의 API 키 사용
- CLI 모드로 전환
  - 사용자 요청으로 Anthropic SDK 제거, `claude -p` subprocess 호출로 변경
  - API 키 불필요, 사용자의 Claude 로그인 세션 재사용
- 프롬프트 보강
  - 제목에 "참석/진행" 군더더기 동사 금지
  - 주요내용과 제목 중복 금지
  - 메모 부족 시 억지로 지어내지 말고 불릿 생략
- 다중 항목 입력 테스트
  - 한 입력에 활동 3개 → 3개 블록으로 정상 분리 변환 확인
- 배포 편의 추가
  - `run.bat` (더블클릭 실행용)
  - 문서화: `CLAUDE.md`, `PROGRESS.md`, `LESSONS.md`, `README.md`

## 2026-10-04 — 후속 작업
- exe 패키징 시도 (PyInstaller) → **중단**
  - `--onefile`, `--onedir` 모두 "Failed to extract app: failed to open archive file!" 발생
  - 원인 추정: Python 3.14 + PyInstaller 6.22 호환성 문제 (한글 경로는 ASCII 경로로 복사해도 재현)
  - `app.py`의 PyInstaller 관련 수정은 원복, 빌드 산출물(`build/`, `dist/`, `*.spec`) 삭제
- 실행 파일 리네임
  - `run.bat` → `업무보고md 생성기.bat` (사용자가 직접 변경)
- 작업 표시줄 고정
  - `.bat`는 작업 표시줄에 직접 고정 불가 → `cmd.exe /c "<bat>"`을 Target으로 하는 `.lnk` 바로가기를 PowerShell로 생성하는 방법 사용
  - 바로가기 파일은 PC마다 경로가 달라 `.gitignore`로 제외
- `.gitignore` 보강: `build/`, `dist/`, `*.spec`, `.cursor/`, `.mcp.json`, `*.lnk`

## 다음 할 일 (후보)
- 결과 하단에 "다시 생성" 버튼 (프롬프트 미세조정 반영)
- 자주 쓰는 카테고리 템플릿 버튼 (예: `(해외학회 참석)` 삽입)
- 저장 이력 로컬 보존 (localStorage) — 실수로 창 닫아도 복구
- 월말/주말 자동 알림 (스케줄러) — 선택사항
