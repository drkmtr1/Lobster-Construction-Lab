$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3.13 -c "import sys" 2>$null
    if ($LASTEXITCODE -eq 0) { & py -3.13 scripts/setup_env.py; exit $LASTEXITCODE }
    & py -3.12 -c "import sys" 2>$null
    if ($LASTEXITCODE -eq 0) { & py -3.12 scripts/setup_env.py; exit $LASTEXITCODE }
}
if (Get-Command python -ErrorAction SilentlyContinue) {
    & python scripts/setup_env.py
    exit $LASTEXITCODE
}
throw "Install or select 64-bit CPython 3.12/3.13, then rerun setup. See START_HERE.md."
