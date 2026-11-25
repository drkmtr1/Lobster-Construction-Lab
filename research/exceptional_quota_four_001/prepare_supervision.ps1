# Preparation only. No official campaign script is loaded or invoked.
$ErrorActionPreference = 'Stop'
$kit = (Resolve-Path -LiteralPath $PSScriptRoot).ProviderPath
$repo = (Resolve-Path -LiteralPath (Join-Path $kit '..\..')).ProviderPath
$config = Get-Content -LiteralPath (Join-Path $kit 'config.json') -Raw | ConvertFrom-Json
$evidence = Join-Path $repo 'evidence\validation\LCL_ORDINARY_SPINE_EXCEPTIONAL_FIVE_HOST_QUOTA_FOUR_MATCHED_001_PREP'
$cfg = Join-Path $repo $config.runtime.cfg
$base = (((Get-Content -LiteralPath $cfg | Where-Object {$_ -match '^executable\s*='}) -split '=',2)[1]).Trim()
if ((Get-FileHash -LiteralPath $base -Algorithm SHA256).Hash.ToLowerInvariant() -cne $config.runtime.base_sha) {
    throw 'unexpected interpreter identity'
}
foreach ($path in @($evidence, (Join-Path $repo $config.output), (Join-Path $repo $config.approval))) {
    if (Test-Path -LiteralPath $path) { throw "preparation or official path already occupied: $path" }
    for ($dir = [IO.Path]::GetDirectoryName($path); $dir; $dir = [IO.Path]::GetDirectoryName($dir)) {
        if ((Get-Item -LiteralPath $dir -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {
            throw "unsafe ancestry: $dir"
        }
    }
}
$null = [IO.Directory]::CreateDirectory($evidence)
$clock = [Diagnostics.Stopwatch]::StartNew()
$self = [Diagnostics.Process]::GetCurrentProcess()
$cpuStart = $self.TotalProcessorTime.TotalSeconds
$cpuChildren = 0.0
$receipts = [Collections.Generic.List[object]]::new()
$state = 'INCOMPLETE'
$reason = $null
try {
    foreach ($phase in @(@('corpus','prepare.py','input\corpus_receipt.json'),@('preflight','preflight.py','PREFLIGHT.json'))) {
        $phaseClock = [Diagnostics.Stopwatch]::StartNew()
        $child = Start-Process -FilePath $base -ArgumentList @('-I','-S','-B',('"' + (Join-Path $kit $phase[1]) + '"')) `
            -WorkingDirectory $repo -WindowStyle Hidden -PassThru `
            -RedirectStandardOutput (Join-Path $evidence ($phase[0] + '-stdout.log')) `
            -RedirectStandardError (Join-Path $evidence ($phase[0] + '-stderr.log'))
        $timeout = $false
        $cap = $null
        try {
            $null = $child.Handle
            while (-not $child.WaitForExit(100)) {
                if ($clock.Elapsed.TotalSeconds -ge ($config.preparation.wall_seconds - 2)) {
                    $timeout = $true
                    $cap = 'observed preparation wall cap'
                } elseif (($cpuChildren + $child.TotalProcessorTime.TotalSeconds +
                          ($self.TotalProcessorTime.TotalSeconds - $cpuStart)) -ge ($config.preparation.cpu_seconds - 2)) {
                    $cap = 'preparation process CPU cap'
                }
                if ($cap) {
                    $child.Kill()
                    if (-not $child.WaitForExit(1500)) { throw 'preparation child exit unconfirmed' }
                    break
                }
            }
            $child.WaitForExit()
            $cputime = $child.TotalProcessorTime.TotalSeconds
            $cpuChildren += $cputime
            $receipt = [ordered]@{phase=$phase[0]; exit_code=$child.ExitCode; timeout=$timeout
                                   process_cpu_seconds=$cputime; wall_seconds=$phaseClock.Elapsed.TotalSeconds}
            $receipts.Add($receipt)
            if ($cap -or $child.ExitCode -ne 0 -or -not (Test-Path -LiteralPath (Join-Path $evidence $phase[2]))) {
                throw "unsuccessful preparation phase $($phase[0]): $cap exit $($child.ExitCode)"
            }
        } finally {
            try {
                if (-not $child.HasExited) {
                    $child.Kill()
                    if (-not $child.WaitForExit(1500)) { throw 'preparation child cleanup exit unconfirmed' }
                }
            } finally { $child.Dispose() }
        }
    }
    $files = @(Get-ChildItem -LiteralPath $evidence -Recurse -File)
    if (@($files | Where-Object Length -gt $config.limits.record_bytes).Count -or
        ($files | Measure-Object -Property Length -Sum).Sum + 4096 -gt $config.preparation.evidence_bytes -or
        $cpuChildren + ($self.TotalProcessorTime.TotalSeconds - $cpuStart) -gt $config.preparation.cpu_seconds -or
        $clock.Elapsed.TotalSeconds -gt $config.preparation.wall_seconds) { throw 'combined preparation cap' }
    $state = 'PASS'
} catch {
    $reason = $_.Exception.Message
} finally {
    $value = [ordered]@{status=$state; reason=$reason; phases=@($receipts.ToArray())
                       cpu_seconds=$cpuChildren+($self.TotalProcessorTime.TotalSeconds-$cpuStart)
                       wall_seconds=$clock.Elapsed.TotalSeconds
                       measurement='Single pinned base CPython child at a time. External handle wait and sampled process CPU, plus supervising shell CPU. No kernel CPU or memory containment.'}
    $record = (Join-Path $evidence 'PREPARATION_SUPERVISION.json')
    $stream = [IO.File]::Open($record,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {
        $utf8 = [Text.UTF8Encoding]::new($false)
        $payload = $utf8.GetBytes((($value | ConvertTo-Json -Depth 8) + "`n").Replace("`r`n","`n"))
        $stream.Write($payload, 0, $payload.Length)
    } finally { $stream.Dispose() }
    $self.Dispose()
}
$value | ConvertTo-Json -Compress -Depth 8
if ($state -cne 'PASS') { exit 1 }
