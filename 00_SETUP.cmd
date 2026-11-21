@echo off
setlocal
cd /d "%~dp0"
py -3.13 -c "import sys" >nul 2>&1
if not errorlevel 1 (
  py -3.13 scripts\setup_env.py
  goto finish
)
py -3.12 -c "import sys" >nul 2>&1
if not errorlevel 1 (
  py -3.12 scripts\setup_env.py
  goto finish
)
python scripts\setup_env.py
:finish
set "LCL_EXIT=%errorlevel%"
if not "%LCL_EXIT%"=="0" echo Setup did not complete. See START_HERE.md.
pause
exit /b %LCL_EXIT%
