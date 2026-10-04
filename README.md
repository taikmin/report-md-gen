# 업무보고 md 생성기

한국기계연구원 이차전지장비연구실용 **주간/월간 업무보고 양식 자동 정리기**.

활동 메모를 자유형으로 입력 → Claude가 통일된 `### 머리표 제목(책임자)` + `*` 불릿 양식으로 변환 → 편집·복사하여 보고서에 붙여넣기.

## 설치 (최초 1회)
사전 조건:
- Python 3.10+
- [Claude Code](https://docs.claude.com/claude-code) 설치 및 로그인 완료 (`claude` 명령이 PATH에 있어야 함)

```powershell
pip install -r requirements.txt
```

## 실행
방법 1 — 더블클릭:
- `업무보고md 생성기.bat` 더블클릭 → 서버 기동 + 브라우저 자동 열림

방법 2 — 수동:
```powershell
python app.py
```
→ 브라우저에서 http://127.0.0.1:5000

## 작업 표시줄에 고정하기 (Windows)
`.bat` 파일은 Windows 작업 표시줄에 바로 고정이 안 됩니다. 바로가기를 하나 만들어서 고정하세요.

PowerShell에서 (경로는 본인 환경에 맞게):
```powershell
$dir = "경로\업무보고용 md 내용 생성기"
$bat = Join-Path $dir "업무보고md 생성기.bat"
$lnkPath = Join-Path $dir "업무보고 생성기.lnk"
$WshShell = New-Object -ComObject WScript.Shell
$lnk = $WshShell.CreateShortcut($lnkPath)
$lnk.TargetPath = "$env:SystemRoot\System32\cmd.exe"
$lnk.Arguments  = "/c `"`"$bat`"`""
$lnk.WorkingDirectory = $dir
$lnk.IconLocation = "$env:SystemRoot\System32\shell32.dll,13"
$lnk.Save()
```
생성된 `.lnk` **우클릭 → "작업 표시줄에 고정"** (안 보이면 Shift+우클릭 또는 "자세한 옵션 표시"). 이제 작업 표시줄 아이콘 클릭이면 바로 실행됩니다.

## 사용
1. 왼쪽(주간) 또는 오른쪽(월간) 입력창에 활동 메모 자유형으로 입력
   - 여러 항목은 줄바꿈이나 번호(1), 2), ...)로 구분
2. **생성** 버튼 클릭
3. 아래 출력창에 양식에 맞춰 정리된 결과 표시 (편집 가능)
4. **복사** 버튼으로 클립보드 복사 후 보고서 문서에 붙여넣기

## 다른 컴퓨터로 옮기기
1. 이 저장소 clone
2. 해당 PC에 Python과 Claude Code 설치, `claude` 로그인
3. `pip install -r requirements.txt`
4. `run.bat` 실행

## 양식 reference
`reference/` 폴더의 PDF가 실제 보고서 예시. 프롬프트가 이 양식을 학습 참고로 사용.
