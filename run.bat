@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo [업무보고 md 생성기] 서버 기동 중...
start "" http://127.0.0.1:5000
python app.py
pause
