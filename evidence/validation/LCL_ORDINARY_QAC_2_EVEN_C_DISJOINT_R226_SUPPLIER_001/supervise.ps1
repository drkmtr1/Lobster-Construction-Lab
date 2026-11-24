param(
    [Parameter(Mandatory)][ValidateSet('prepare', 'preflight', 'verify')][string]$Phase,
    [Parameter(Mandatory)][ValidatePattern('^[0-9a-f]{64}$')][string]$FrozenConfig
)

$ErrorActionPreference = 'Stop'
$folder = $PSScriptRoot
$root = (Get-Item -LiteralPath $folder).Parent.Parent.Parent.FullName
$prefix = @{prepare = 'preparation'; preflight = 'preflight'; verify = 'verification'}[$Phase]
$scriptName = @{prepare = 'prepare.py'; preflight = 'preflight.py'; verify = 'run.py'}[$Phase]
$receiptName = @{prepare = 'preparation_receipt.json'; preflight = 'preflight_receipt.json'; verify = 'command_receipt.json'}[$Phase]
$priorNames = @{prepare = @(); preflight = @('preparation'); verify = @('preparation', 'preflight')}[$Phase]
$outputName = Join-Path $folder "${prefix}_supervision.json"
$stderr = Join-Path $folder "${prefix}_stderr.txt"
foreach ($path in @($outputName, $stderr, (Join-Path $folder $receiptName))) {
    if (Test-Path -LiteralPath $path) { throw "Existing output: $path" }
}

$timer = [Diagnostics.Stopwatch]::StartNew()
$status = 'INCOMPLETE'
$failure = $null
$exitCode = $null
$child = $null
$cpu = $null
$cpuBefore = 0.0
$wallBefore = 0.0
$task = $null
$receiptHash = $null
$started = [DateTimeOffset]::UtcNow.ToString('o')
try {
    $configPath = Join-Path $folder 'config.json'
    if ((Get-FileHash -LiteralPath $configPath).Hash.ToLowerInvariant() -ne $FrozenConfig) {
        throw 'Frozen config hash mismatch'
    }
    $cfg = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
    $task = $cfg.task
    foreach ($entry in $cfg.task_source_hashes.PSObject.Properties) {
        if ((Get-FileHash -LiteralPath (Join-Path $folder $entry.Name)).Hash.ToLowerInvariant() -ne $entry.Value) {
            throw "Frozen source hash mismatch: $($entry.Name)"
        }
    }
    $runtime = Join-Path $root '.venv/Scripts/python.exe'
    if ((Get-FileHash -LiteralPath $runtime).Hash.ToLowerInvariant() -ne $cfg.runtime_sha256) {
        throw 'Runtime hash mismatch'
    }
    if ($Phase -eq 'prepare') {
        foreach ($name in @('lcl/model.py', 'lcl/__init__.py')) {
            if ((Get-FileHash -LiteralPath (Join-Path $root $name)).Hash.ToLowerInvariant() -ne $cfg.source_hashes.$name) {
                throw "Unchanged builder input hash mismatch: $name"
            }
        }
    }
    foreach ($priorName in $priorNames) {
        $prior = Get-Content -LiteralPath (Join-Path $folder "${priorName}_supervision.json") -Raw | ConvertFrom-Json
        if ($prior.status -ne 'PASS' -or $prior.task -ne $task -or $prior.config_sha256 -ne $FrozenConfig) {
            throw "Prior stage did not pass: $priorName"
        }
        $priorPath = Join-Path $folder "${priorName}_receipt.json"
        if ((Get-FileHash -LiteralPath $priorPath).Hash.ToLowerInvariant() -ne $prior.receipt_sha256) {
            throw "Prior stage receipt changed: $priorName"
        }
        $cpuBefore += $prior.process_cpu_seconds
        $wallBefore += $prior.supervised_wall_seconds
    }
    $scriptPath = Join-Path $folder $scriptName
    $arguments = @('-B', '-E', '-X', 'utf8', ('"' + $scriptPath + '"'))
    if ($Phase -eq 'preflight') {
        $originalHash = (Get-FileHash -LiteralPath (Join-Path $folder 'original.json')).Hash.ToLowerInvariant()
        $arguments += @($FrozenConfig, $originalHash)
    }
    if ($cpuBefore -ge $cfg.limits.process_cpu_seconds -or
        $wallBefore + $timer.Elapsed.TotalSeconds -ge $cfg.limits.wall_seconds) {
        throw 'Combined limits exhausted before launch'
    }
    $child = Start-Process -FilePath $runtime -ArgumentList $arguments -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardError $stderr -PassThru
    while ($true) {
        $remainingMs = [int][Math]::Floor(($cfg.limits.wall_seconds - $wallBefore - $timer.Elapsed.TotalSeconds) * 1000)
        if ($remainingMs -le 0) { throw 'Combined externally supervised wall limit reached' }
        if ($child.WaitForExit([Math]::Min(100, $remainingMs))) { break }
        if ($cpuBefore + $child.TotalProcessorTime.TotalSeconds -ge $cfg.limits.process_cpu_seconds) {
            throw 'Combined CPU limit reached'
        }
    }
    $exitCode = $child.ExitCode
    $receiptPath = Join-Path $folder $receiptName
    $receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
    $receiptHash = (Get-FileHash -LiteralPath $receiptPath).Hash.ToLowerInvariant()
    $cpu = $receipt.process_cpu_seconds
    if ($exitCode -ne 0 -or $receipt.status -ne 'PASS' -or $receipt.task -ne $task -or $receipt.parent -ne $cfg.parent) {
        throw "Unsuccessful $Phase child or receipt (exit $exitCode)"
    }
    if ($null -eq $cpu -or $cpu -lt 0 -or $cpuBefore + $cpu -ge $cfg.limits.process_cpu_seconds -or
        $wallBefore + $timer.Elapsed.TotalSeconds -ge $cfg.limits.wall_seconds) { throw 'Combined limit reached or CPU unmeasured' }
    $status = 'PASS'
} catch {
    $failure = $_.ToString()
    if ($null -ne $child -and -not $child.HasExited) {
        $child.Kill($true)
        $null = $child.WaitForExit(1000)
    }
}
$timer.Stop()
$wall = $timer.Elapsed.TotalSeconds
$receipt = [ordered]@{
    status = $status
    task = $task
    phase = $Phase
    config_sha256 = $FrozenConfig
    receipt_sha256 = $receiptHash
    started_utc = $started
    launched = $null -ne $child
    child_exit_code = $exitCode
    process_cpu_seconds = $cpu
    supervised_wall_seconds = $wall
    combined_process_cpu_seconds = $(if ($null -ne $cpu) { $cpuBefore + $cpu })
    combined_supervised_wall_seconds = $wallBefore + $wall
    error = $failure
}
$bytes = [System.Text.Encoding]::UTF8.GetBytes(($receipt | ConvertTo-Json) + "`n")
$stream = [System.IO.File]::Open($outputName, [System.IO.FileMode]::CreateNew)
try { $stream.Write($bytes, 0, $bytes.Length) } finally { $stream.Dispose() }
$receipt | ConvertTo-Json
if ($status -ne 'PASS') { exit 1 }
