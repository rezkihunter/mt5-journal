@echo off
cd /d "%~dp0"
python fetch_closed.py >> run.log 2>&1
if %errorlevel% neq 0 exit /b %errorlevel%
python evaluate.py >> run.log 2>&1
