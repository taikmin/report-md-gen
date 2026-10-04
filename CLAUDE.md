# CLAUDE.md

이 저장소에서 Claude Code가 작업할 때 참고할 지침.

## 프로젝트 개요
한국기계연구원 이차전지장비연구실 실장(이택민)이 매주/매달 작성하는 **주간업무보고 · 월간업무보고**를 통일된 양식으로 정리해 주는 로컬 웹앱.

사용자가 활동 메모를 자유형으로 입력하면, Claude가 `### 머리표 제목(책임자)` + `*` 불릿 구조로 다듬어 출력. 결과는 편집 가능, 복사 버튼 제공.

## 아키텍처
- **백엔드**: Flask (`app.py`) — 단일 파일. `GET /` → UI, `POST /api/generate` → Claude 호출.
- **LLM 호출**: Claude Code CLI를 `subprocess`로 호출 (API 키 **사용 안 함**, 사용자의 Claude 로그인 세션 이용).
  - 명령: `claude -p --append-system-prompt <SYS> --max-turns 1 <USER_TEXT>`
- **프롬프트**: `prompts.py`에 `WEEKLY_PROMPT`, `MONTHLY_PROMPT` 상수. few-shot 예시 포함.
- **프론트엔드**: 정적 HTML + Vanilla JS (`static/`). 입력창 2개(주간/월간) + 출력창 2개 + 생성/복사 버튼.

## 핵심 규칙 (프롬프트에 반영됨)
- 주간 머리표: 기본 `[이차]`, 국외출장은 `(국외출장)`.
- 월간 머리표: 활동 성격에 맞는 카테고리 — `(해외학회 참석)`, `(교육)`, `(초청강연)`, `(워크샵)`, `(기술료)`, `(창업 진행)`, `(과제신청)`, `(과제협약)`, `(이차)특허 출원` 등.
- 제목에는 "참석/진행/실시" 같은 군더더기 동사 금지.
- 주요내용 불릿은 제목과 중복 금지, 세부 내용만.
- 사용자가 적지 않은 수치/인명/기관명/날짜 지어내기 금지. 부족하면 해당 불릿 생략.
- 출력은 코드블록 없이 순수 텍스트.

## 양식 reference
`reference/` 폴더의 PDF 파일에 실제 사용된 주간/월간 보고서 예시가 있음. 프롬프트의 few-shot은 여기서 발췌.

## 실행
```powershell
pip install -r requirements.txt
python app.py
# http://127.0.0.1:5000
```
또는 `run.bat` 더블클릭.

## 작업 시 주의
- `prompts.py` 수정 시 양식 규칙과 few-shot 예시 모두 검토.
- Flask 서버 포트 변경 시 `app.py`와 안내 문구 함께 수정.
- 서버 재기동해야 프롬프트 변경이 반영됨.
- Windows에서 Claude CLI 경로 해석을 위해 `shutil.which`로 `claude`/`claude.cmd`/`claude.exe` 순서로 탐색 (`app.py:resolve_claude_cli`).
