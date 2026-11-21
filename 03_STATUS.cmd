@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Run 00_SETUP.cmd first.
  pause
  exit /b 2
)
".venv\Scripts\python.exe" -m lcl status
set "LCL_EXIT=%errorlevel%"
pause
exit /b %LCL_EXIT%
