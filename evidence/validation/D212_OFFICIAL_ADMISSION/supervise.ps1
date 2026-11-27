param(
    [Parameter(Mandatory)][ValidateSet('preflight','official')][string]$Phase,
    [ValidatePattern('^[a-f0-9]{64}$')][string]$AdmissionHash
)

$ErrorActionPreference = 'Stop'
$root = (Get-Item -LiteralPath $PSScriptRoot).Parent.Parent.Parent.FullName
$run = 'd212-multi-center-quota-growth-001'
$prep = Join-Path $root "runs/$run-intake"
$output = Join-Path $root "evidence/runs/$run"
$timer = [Diagnostics.Stopwatch]::StartNew()
$controller = [Diagnostics.Process]::GetCurrentProcess()
$cpuStart = $controller.TotalProcessorTime.Ticks
$receiptName = 'PREFLIGHT_OBSERVER.json'
$destination = $prep
if ($Phase -eq 'official') {
    $receiptName = 'OFFICIAL_OBSERVER.json'
}
$charge = @(0L, 0L)
$cpuMax = 4000000000L
$wallMax = 10000000000L
$margin = 250000000L
if ($Phase -eq 'official') {
    $cpuMax = 450000000000L
    $wallMax = 660000000000L
    $margin = 1000000000L
}

function Sha256([string]$Path) {
    (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function ControllerCpu {
    $controller.Refresh()
    100L * ($controller.TotalProcessorTime.Ticks - $cpuStart)
}

function WallNs {
    100L * $timer.Elapsed.Ticks
}

function WriteReceipt($Record, [string]$Directory) {
    $path = Join-Path $Directory $receiptName
    $bytes = [Text.UTF8Encoding]::new($false).GetBytes(($Record | ConvertTo-Json -Depth 8) + [Environment]::NewLine)
    $files = @(Get-ChildItem -LiteralPath $prep -File)
    if ($Phase -eq 'official' -and (Test-Path -LiteralPath $output)) {
        $files += @(Get-ChildItem -LiteralPath $output -File)
    }
    $files = @($files | Where-Object Name -notin @('RUNNING.lock','INVOCATION.lock','PYTHON_ENTRY.lock'))
    $used = ($files | Measure-Object -Property Length -Sum).Sum
    $byteCap = if ($Phase -eq 'preflight') { 131072 } else { 2000000 }
    if ($bytes.Length -gt 65536 -or $files.Count + 1 -gt 16 -or
        $used + $bytes.Length + 512 -gt $byteCap) { throw 'Observer evidence limit' }
    $stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write)
    try {
        $stream.Write($bytes, 0, $bytes.Length)
        $stream.Flush($true)
    } finally {
        $stream.Dispose()
    }
}

if (Test-Path -LiteralPath $output) { throw 'Official output is occupied; no second start' }
if ($Phase -eq 'preflight') {
    if (Test-Path -LiteralPath $prep) { throw 'Preflight output is occupied' }
    New-Item -ItemType Directory -Path $prep | Out-Null
} else {
    if (!$AdmissionHash) { throw 'Admission hash required' }
    $admissionPath = Join-Path $prep 'ADMISSION.json'
    if ((Sha256 $admissionPath) -ne $AdmissionHash) { throw 'Admission hash mismatch' }
    $admission = Get-Content -LiteralPath $admissionPath -Raw | ConvertFrom-Json
    $charge = @($admission.intake_charge_ns)
    if ($charge.Count -ne 2 -or
        !($charge[0] -is [long] -or $charge[0] -is [int]) -or
        !($charge[1] -is [long] -or $charge[1] -is [int]) -or
        $charge[0] -lt 0 -or $charge[1] -lt 0) { throw 'Missing intake measurements' }
    $age = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds() - [long]$admission.checked_unix
    if ($age -lt 0 -or $age -gt 900) { throw 'Admission remote observations are stale' }
    $localHead = git -C $root rev-parse HEAD
    if ($LASTEXITCODE -ne 0 -or $localHead -ne $admission.repository_head -or
        $localHead -ne $admission.live_refs.lcl_main) { throw 'Admission HEAD mismatch' }
    $dirty = @(git -C $root status --porcelain)
    if ($LASTEXITCODE -ne 0 -or $dirty.Count) { throw 'Repository is not clean at invocation' }
    $lockPath = Join-Path $prep 'INVOCATION.lock'
    $lock = [IO.File]::Open($lockPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write)
    $lock.Dispose()
}

$child = $null
$failure = $null
$exitCode = $null
$childCpu = $null
$verifiedExit = $false
$terminalHash = $null
$launchedPid = $null
$exe = $null
$arguments = @()
try {
    $tokens = $null
    $parseErrors = $null
    $syntax = [Management.Automation.Language.Parser]::ParseFile(
        $PSCommandPath, [ref]$tokens, [ref]$parseErrors)
    $definitions = @($syntax.FindAll({
        param($node)
        $node -is [Management.Automation.Language.FunctionDefinitionAst]
    }, $true))
    if ($parseErrors.Count -or ($definitions.Name | Sort-Object -Unique).Count -ne $definitions.Count) {
        throw 'Supervisor parse-only definition gate failed'
    }
    $cfg = Get-Content -LiteralPath (Join-Path $root '.venv/pyvenv.cfg')
    $exeLine = @($cfg | Where-Object { $_ -match '^executable = ' })
    if ($exeLine.Count -ne 1) { throw 'Project-local interpreter identity is ambiguous' }
    $exe = $exeLine[0].Substring('executable = '.Length).Trim()
    if ($Phase -eq 'official') {
        $intake = Get-Content -LiteralPath (Join-Path $prep 'PREFLIGHT.json') -Raw | ConvertFrom-Json
        $prior = Get-Content -LiteralPath (Join-Path $prep 'PREFLIGHT_OBSERVER.json') -Raw | ConvertFrom-Json
        if ($prior.status -ne 'PASS' -or $intake.status -ne 'PASS' -or
            (Sha256 (Join-Path $prep 'PREFLIGHT_OBSERVER.json')) -ne $admission.preflight_observer_sha256 -or
            (Sha256 (Join-Path $prep 'PREFLIGHT.json')) -ne $admission.preflight_sha256 -or
            $exe -ne $intake.runtime.executable -or (Sha256 $exe) -ne $intake.runtime.sha256 -or
            (Sha256 $intake.runtime.dll) -ne $intake.runtime.dll_sha256) { throw 'Preflight or runtime changed' }
        foreach ($binding in $intake.source_sha256.PSObject.Properties) {
            if ((Sha256 (Join-Path $root $binding.Name)) -ne $binding.Value) {
                throw "Source binding changed: $($binding.Name)"
            }
        }
    }
    $info = [Diagnostics.ProcessStartInfo]::new()
    $info.FileName = $exe
    $info.WorkingDirectory = $root
    $info.UseShellExecute = $false
    $info.CreateNoWindow = $true
    $cache = Join-Path $prep 'bytecode-vacant'
    if (Test-Path -LiteralPath $cache) { throw 'Bytecode prefix is occupied' }
    $arguments = @('-I','-S','-B','-X',"pycache_prefix=$cache",(Join-Path $PSScriptRoot 'runner.py'),$Phase)
    if ($Phase -eq 'official') { $arguments += $AdmissionHash }
    foreach ($argument in $arguments) {
        $info.ArgumentList.Add($argument)
    }
    if (($charge[0] + (ControllerCpu)) -ge ($cpuMax - $margin) -or
        ($charge[1] + (WallNs)) -ge ($wallMax - $margin)) { throw 'Insufficient launch headroom' }

    $child = [Diagnostics.Process]::Start($info)
    $null = $child.Handle
    $launchedPid = $child.Id
    do {
        $exited = $child.WaitForExit(100)
        $childCpu = 100L * $child.TotalProcessorTime.Ticks
        if ($charge[0] + $childCpu + (ControllerCpu) -ge ($cpuMax - $margin) -or
            $charge[1] + (WallNs) -ge ($wallMax - $margin)) { throw 'Observed shared resource stop' }
    } until ($exited)
    $verifiedExit = $true
    $exitCode = $child.ExitCode
    if ($Phase -eq 'official') {
        if (!(Test-Path -LiteralPath (Join-Path $output 'TERMINAL.json'))) {
            throw 'Missing official terminal evidence'
        }
        $destination = $output
        $terminal = Join-Path $output 'TERMINAL.json'
    } else {
        $terminal = Join-Path $prep 'PREFLIGHT.json'
    }
    $terminalHash = Sha256 $terminal
    if ($exitCode -ne 0) { throw "Child exit $exitCode" }
} catch {
    $failure = $_.ToString()
} finally {
    if ($null -ne $child) {
        try {
            if (!$child.HasExited) {
                $child.Kill()
                $remaining = [int][Math]::Clamp(
                    [Math]::Floor(($wallMax - $charge[1] - (WallNs)) / 1000000), 0, 1000)
                $null = $child.WaitForExit($remaining)
            }
            $verifiedExit = $child.HasExited
            if ($verifiedExit) {
                $childCpu = 100L * $child.TotalProcessorTime.Ticks
                $exitCode = $child.ExitCode
            }
        } catch {
            $failure = "$failure; cleanup/measurement: $_"
        } finally {
            $child.Dispose()
        }
    }
}

$controllerCpu = ControllerCpu
$wall = WallNs
$totalCpu = if ($null -ne $childCpu) { $charge[0] + $controllerCpu + $childCpu }
$totalWall = $charge[1] + $wall
if ($null -eq $totalCpu -or $totalCpu -ge ($cpuMax - $margin) -or
    $totalWall -ge ($wallMax - $margin) -or !$verifiedExit) {
    $failure = "$failure; resource reconciliation failed"
}
if ($Phase -eq 'official' -and (Test-Path -LiteralPath $output)) { $destination = $output }
$record = [ordered]@{
    status = $(if ($failure) { 'STOPPED' } else { 'PASS' })
    run = $run
    phase = $Phase
    admission_sha256 = $AdmissionHash
    child_launched = $null -ne $child
    child_pid = $launchedPid
    executable = $exe
    arguments = $arguments
    verified_exit = $verifiedExit
    exit_code = $exitCode
    terminal_sha256 = $terminalHash
    child_cpu_ns = $childCpu
    controller_cpu_ns_before_observer_write = $controllerCpu
    observed_wall_ns_before_observer_write = $wall
    aggregate_cpu_ns_before_observer_write = $totalCpu
    aggregate_wall_ns_before_observer_write = $totalWall
    caps_ns = @($cpuMax, $wallMax)
    observer_write_reserve_ns = $margin
    error = $failure
}
WriteReceipt $record $destination
if ($null -ne $childCpu) {
    $afterCpu = $charge[0] + $childCpu + (ControllerCpu)
    $afterWall = $charge[1] + (WallNs)
    Write-Output "D212 observer closed: cpu_ns=$afterCpu wall_ns=$afterWall"
    if ($afterCpu -ge $cpuMax -or $afterWall -ge $wallMax) { exit 1 }
}
if ($failure) { exit 1 }
