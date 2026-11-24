$ErrorActionPreference = 'Stop'
$folder = $PSScriptRoot
$root = (Get-Item -LiteralPath $folder).Parent.Parent.Parent.FullName
$configPath = Join-Path $folder 'config.json'
$cfg = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
$preflight = Get-Content -LiteralPath (Join-Path $folder 'preflight_receipt.json') -Raw | ConvertFrom-Json
if ($preflight.status -ne 'PASS' -or $preflight.task -ne $cfg.task -or $preflight.parent -ne $cfg.parent) {
    throw 'Missing matching passing preflight'
}
$configHash = (Get-FileHash -LiteralPath $configPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($preflight.input_hashes.'config.json' -ne $configHash) { throw 'Configuration changed after preflight' }
foreach ($entry in $cfg.task_source_hashes.PSObject.Properties) {
    $source = Join-Path $folder $entry.Name
    if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.Value) {
        throw "Task source changed after preflight: $($entry.Name)"
    }
}
foreach ($name in @('result.json', 'command_receipt.json', 'supervisor_receipt.json', 'official_stderr.txt')) {
    if (Test-Path -LiteralPath (Join-Path $folder $name)) { throw "Output already exists: $name" }
}
$runtime = Join-Path $root '.venv/Scripts/python.exe'
if ((Get-FileHash -LiteralPath $runtime -Algorithm SHA256).Hash.ToLowerInvariant() -ne $cfg.runtime_sha256) {
    throw 'Runtime changed after preflight'
}
$scriptPath = Join-Path $folder 'run.py'
$stderr = Join-Path $folder 'official_stderr.txt'
$started = [DateTimeOffset]::UtcNow.ToString('o')
$timer = [Diagnostics.Stopwatch]::StartNew()
$child = $null
$status = 'INCOMPLETE'
$failure = $null
$exitCode = $null
try {
    $child = Start-Process -FilePath $runtime -ArgumentList @('-B', '-E', '-X', 'utf8', ('"' + $scriptPath + '"')) -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardError $stderr -PassThru
    while ($true) {
        $remainingMs = [int][Math]::Floor(($cfg.limits.wall_seconds - $timer.Elapsed.TotalSeconds) * 1000)
        if ($remainingMs -le 0) { throw 'Official process reached the externally supervised wall limit' }
        if ($child.WaitForExit([Math]::Min($remainingMs, 100))) { break }
        if ($child.TotalProcessorTime.TotalSeconds -ge $cfg.limits.process_cpu_seconds) {
            throw 'Official process reached the CPU limit'
        }
    }
    $exitCode = $child.ExitCode
    if ($exitCode -ne 0) { throw "Official process failed with exit code $exitCode" }
    if ($timer.Elapsed.TotalSeconds -ge $cfg.limits.wall_seconds) { throw 'Externally supervised wall limit exceeded' }
    $official = Get-Content -LiteralPath (Join-Path $folder 'command_receipt.json') -Raw | ConvertFrom-Json
    if ($official.status -ne 'PASS' -or $official.task -ne $cfg.task -or $official.parent -ne $cfg.parent -or
        $null -eq $official.process_cpu_seconds -or $official.process_cpu_seconds -ge $cfg.limits.process_cpu_seconds) {
        throw 'Official receipt failed or exceeded the CPU cap'
    }
    $status = 'PASS'
} catch {
    $failure = $_.ToString()
    if ($null -ne $child -and -not $child.HasExited) {
        $child.Kill($true)
        $null = $child.WaitForExit(1000)
    }
}
$timer.Stop()
$receipt = [ordered]@{
    status = $status
    task = $cfg.task
    started_utc = $started
    config_sha256 = $configHash
    wall_seconds = $timer.Elapsed.TotalSeconds
    child_exit_code = $exitCode
    error = $failure
}
$raw = ($receipt | ConvertTo-Json) + "`n"
$path = Join-Path $folder 'supervisor_receipt.json'
$stream = [System.IO.File]::Open($path, [System.IO.FileMode]::CreateNew)
$bytes = [System.Text.Encoding]::UTF8.GetBytes($raw)
try { $stream.Write($bytes, 0, $bytes.Length) } finally { $stream.Dispose() }
Write-Output $raw
if ($status -ne 'PASS') { exit 1 }
