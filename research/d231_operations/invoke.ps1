param(
    [Parameter(Mandatory)][ValidateSet('Qualify','Science')][string]$Mode,
    [ValidatePattern('^pass-[1-5]$')][string]$Pass = 'pass-1'
)
$ErrorActionPreference='Stop'
$PSNativeCommandUseErrorActionPreference=$false
$ops='research/d231_operations'
. (Join-Path $PSScriptRoot 'admission.ps1')
Assert-D231 ((Get-Item -LiteralPath $ops).FullName -eq $PSScriptRoot) 'Run from LCL root'
$config=Read-D231Json "$ops/identities.json"

function Invoke-D231Watchdog($Data,$Target,[double]$StopSeconds,[double]$HardSeconds,[double]$CpuCeiling) {
    $receipt=$Target.receipt
    foreach ($p in $Target.paths) { Assert-D231Vacant $p }
    Assert-D231NoProcess
    Write-D231NewJson $receipt $Data
    $sha=Get-D231Hash $receipt
    $prefix=$Target.prefix
    $process=$null
    $members=@{}
    $status='NATURAL'
    $errorText=$null
    $outer=Get-Process -Id $PID
    $outer.Refresh()
    $cpu0=$outer.TotalProcessorTime.TotalSeconds
    $argsForObserver=@('-I','-S','-B',('"' + (Resolve-Path -LiteralPath "$ops/observe_v1.py").Path + '"'),
        ('"' + (Resolve-Path -LiteralPath $receipt).Path + '"'),$sha)
    $wall0=[DateTimeOffset]::UtcNow.ToString('o')
    $watch=[Diagnostics.Stopwatch]::StartNew()
    try {
        $process=Start-Process -FilePath $Data.runtime.base_executable -ArgumentList $argsForObserver -WorkingDirectory (Get-Location).Path -WindowStyle Hidden -PassThru -RedirectStandardOutput "$prefix-outer-stdout.txt" -RedirectStandardError "$prefix-outer-stderr.txt"
        $retained=$process.Handle
        while (!$process.HasExited) {
            foreach ($kind in @('suspended','worker')) {
                $record="$prefix-$kind.json"
                if (!$members.ContainsKey($kind) -and (Test-Path -LiteralPath $record -PathType Leaf)) {
                    try {
                        $row=Read-D231Json $record
                        $candidate=Get-Process -Id $row.pid -ErrorAction Stop
                        $null=$candidate.Handle
                        if ($candidate.StartTime.ToFileTimeUtc() -eq [long]$row.times.born) {
                            $members[$kind]=$candidate
                        } else { $candidate.Dispose() }
                    } catch {
                        # A record can be mid-write, or a fast member already signaled.
                        # The observer's retained handles and terminal Job record remain authoritative.
                    }
                }
            }
            $outer.Refresh()
            $process.Refresh()
            $sample=$process.TotalProcessorTime.TotalSeconds+$outer.TotalProcessorTime.TotalSeconds-$cpu0
            foreach ($p in $members.Values) {$p.Refresh();$sample+=$p.TotalProcessorTime.TotalSeconds}
            $remaining=[int][Math]::Max(0,[Math]::Floor(1000*($StopSeconds-$watch.Elapsed.TotalSeconds)))
            if (!$remaining -or $sample -ge ($CpuCeiling-1)) {
                $status=if (!$remaining) {'OUTER_WALL'} else {'OUTER_SAMPLED_CPU'}
                if (!$process.HasExited) {$process.Kill()}
                break
            }
            $null=$process.WaitForExit([Math]::Min(35,$remaining))
        }
    } catch {
        $status='OUTER_ERROR'
        $errorText=$_.Exception.Message
        if ($null -ne $process -and !$process.HasExited) {
            try { $process.Kill() } catch { $errorText += ' | kill: '+$_.Exception.Message }
        }
    }
    $signaled=$null -ne $process -and $process.WaitForExit([int][Math]::Max(0,[Math]::Floor(1000*($HardSeconds-$watch.Elapsed.TotalSeconds))))
    $memberExit=[ordered]@{}
    foreach ($kind in @('suspended','worker')) {
        if ($members.ContainsKey($kind)) {
            $p=$members[$kind]
            $s=$p.WaitForExit([int][Math]::Max(0,[Math]::Floor(1000*($HardSeconds-$watch.Elapsed.TotalSeconds))))
            $memberExit[$kind]=[ordered]@{pid=$p.Id;signaled=$s;cpu_seconds=$(if($s){$p.TotalProcessorTime.TotalSeconds})}
            $p.Dispose()
        }
    }
    $inner=$null
    if (Test-Path -LiteralPath "$prefix-foreground.json") {$inner=Read-D231Json "$prefix-foreground.json"}
    $observerCpu=if($signaled){$process.TotalProcessorTime.TotalSeconds}else{$null}
    $outer.Refresh()
    $shellCpu=$outer.TotalProcessorTime.TotalSeconds-$cpu0
    $combined=$null
    if ($null -ne $inner -and $null -ne $observerCpu) {
        $combined=($inner.job_final.user+$inner.job_final.kernel)/10000000 + $observerCpu + $shellCpu
    } elseif ($signaled -and $memberExit.Count -eq 2 -and $memberExit.suspended.signaled -and $memberExit.worker.signaled) {
        $combined=$observerCpu+$shellCpu+$memberExit.suspended.cpu_seconds+$memberExit.worker.cpu_seconds
    }
    $record=[ordered]@{run_id=$Data.run_id;receipt=$receipt;receipt_sha256=$sha;
        start_utc=$wall0;end_utc=[DateTimeOffset]::UtcNow.ToString('o');observer_argv=$argsForObserver;
        observer_pid=$(if($null -ne $process){$process.Id});observer_signaled=$signaled;
        observer_exit=$(if($signaled){$process.ExitCode});outer_status=$status;error=$errorText;
        outer_stop_seconds=$StopSeconds;hard_seconds=$HardSeconds;
        foreground_seconds=$watch.Elapsed.TotalSeconds;observer_cpu_seconds=$observerCpu;
        outer_monitor_cpu_seconds=$shellCpu;combined_cpu_seconds=$combined;cpu_ceiling_seconds=$CpuCeiling;
        member_exit=$memberExit;
        released=(Test-Path -LiteralPath "$prefix-released.json");
        inner_sha256=$(if($null -ne $inner){Get-D231Hash "$prefix-foreground.json"})}
    Write-D231NewJson "$prefix-outer.json" $record
    if($null -ne $process){$process.Dispose()}
    $outer.Dispose()
    $record
}

function Get-D231Approval($Admission,[string]$ModeLabel,[string]$Case,[string]$QualHash) {
    $scientific=$ModeLabel -eq 'Science'
    $sc=$config.science
    $ready=Read-D231Json $config.referents.readiness
    $inner=if($scientific){1198}else{@{normal=6;inner=1.6;outer=10}[$Case]}
    [ordered]@{
        decision=$(if($scientific){'AUTHORIZE_D231_EXECUTION'}else{'D231_INERT_QUALIFICATION'})
        operational_version=$config.version
        run_id=$(if($scientific){$config.run_id}else{"D231_OPERATIONAL_QUALIFICATION_001-$Pass-$Case"})
        test_case=$Case
        verified_checkpoint=$sc.preparation
        execution_checkout=$Admission.checks.checkout.value
        authority_checkpoint=$sc.authority_checkpoint
        accepted_operator_stop=$sc.accepted_operator_stop
        accepted_recovery=$sc.accepted_recovery
        source_manifest_sha256=$sc.manifest_sha256
        registration_sha256=$sc.registration_sha256
        qualification_manifest_sha256=$QualHash
        director_review=$(if($scientific){"Director accepts the recovered scientific path and prior timestamp stop, recorded at $($sc.authority_checkpoint); qualification is independently reviewed under integrated authority."})
        owner_authorization=$(if($scientific){"Owner directive 'D231 — Autonomous Bug Sweep, Repair, Qualification and Scientific Execution', one release after qualified admission; recorded at $($sc.authority_checkpoint)."})
        verified_utc=$Admission.checked_utc
        runtime=$ready.runtime
        native_sha256=$ready.retained_native_sha256
        observer_sha256=(Get-D231Hash "$ops/observe_v1.py")
        outer_adapter_sha256=(Get-D231Hash "$ops/invoke.ps1")
        inner_wall_seconds=$inner
    }
}

if ($Mode -eq 'Science') {
    $qualified='evidence/validation/D231_OPERATIONAL_QUALIFICATION_001/QUALIFIED.json'
    $q=Read-D231Json $qualified
    Assert-D231 ($q.status -ceq 'QUALIFIED' -and $q.operational_version -ceq $config.version -and
        $q.scientific_manifest_sha256 -ceq $config.science.manifest_sha256) 'No matching independently reviewed operational qualification'
    foreach($path in $q.sha256.Keys) {
        Assert-D231 ((Get-D231Hash $path) -ceq $q.sha256[$path]) "Qualification binding: $path"
    }
    $target=Get-D231Targets $config 'Science' ''
    $admission=Test-D231Admission $config $target
    $admission | ConvertTo-Json -Depth 16 -Compress
    Assert-D231 $admission.pass 'Fresh live admission failed'
    $receipt=Get-D231Approval $admission 'Science' '' (Get-D231Hash $qualified)
    $result=Invoke-D231Watchdog $receipt $target 1199 1200 900
    $result | ConvertTo-Json -Depth 12 -Compress
    exit $(if($result.observer_signaled -and $result.observer_exit -eq 0 -and
        $result.outer_status -eq 'NATURAL' -and $result.foreground_seconds -le 1200 -and
        $null -ne $result.combined_cpu_seconds -and $result.combined_cpu_seconds -lt 900){0}else{1})
}

$parent='runs/D231_OPERATIONAL_QUALIFICATION_001'
if (!(Test-Path -LiteralPath $parent)) { $null=New-Item -ItemType Directory -Path $parent }
$folder=Join-Path $parent $Pass
Assert-D231Vacant $folder
$null=New-Item -ItemType Directory -Path $folder
$tests=@()
function Expect-Reject([string]$Name,[scriptblock]$Test,[string]$Pattern) {
    try { & $Test; throw "Unexpected success: $Name" }
    catch {
        if ($_.Exception.Message -notmatch $Pattern) { throw }
        $script:tests+=[ordered]@{id=$Name;rejected=$true;reason=$_.Exception.Message}
    }
}
$q=Read-D231Json $config.referents.inventory
foreach ($row in $q.files) { Assert-D231Cache $row.quarantined $row.before }
$row=$q.files[0]
$changed=@{}
foreach($key in $row.before.Keys){$changed[$key]=$row.before[$key]}
$changed.creation_utc='2026-11-21T06:25:49.9904097Z'
Expect-Reject 'one UTC tick changed' { Assert-D231Cache $row.quarantined $changed } '^Cache creation time:'
Expect-Reject 'missing timezone' { $null=Get-D231Ticks '2026-11-21T06:25:49.9904096' } '^Expected strict'
Expect-Reject 'malformed ISO calendar' { $null=Get-D231Ticks '2026-13-21T06:25:49.9904096Z' } 'valid DateTime|un-representable|DateTimeOffset|DateTime'
Assert-D231 ((Get-D231Ticks '2026-11-21T06:25:49.9904096Z') -eq (Get-D231Ticks '2026-11-20T20:25:49.9904096-10:00')) 'Offset equivalence'
$changed.creation_utc=$row.before.creation_utc
$changed.sha256='0'*64
Expect-Reject 'incorrect hash' { Assert-D231Cache $row.quarantined $changed } '^Cache hash:'
$changed.sha256=$row.before.sha256
$changed.bytes=$row.before.bytes+1
Expect-Reject 'incorrect size' { Assert-D231Cache $row.quarantined $changed } '^Cache size'
Expect-Reject 'missing file' { Assert-D231Cache (Join-Path $folder 'missing') $changed } 'Cannot find path'
$collision=Join-Path $folder 'immutable.json'
Write-D231NewJson $collision @{payload='first'}
$held=Get-D231Hash $collision
Expect-Reject 'occupied destination' { Assert-D231Vacant $collision } '^Occupied destination:'
Expect-Reject 'immutable overwrite' { Write-D231NewJson $collision @{payload='changed'} } 'already exists'
Assert-D231 ((Get-D231Hash $collision) -ceq $held) 'Immutable bytes changed'
$bad=Join-Path $folder 'invalid-admission.json'
Write-D231NewJson $bad @{decision='BROKEN';operational_version=$config.version}
$base=(Read-D231Json $config.referents.readiness).runtime.base_executable
@'
import importlib.util
from pathlib import Path
import sys
path=Path("research/d231_operations/observe_v1.py")
spec=importlib.util.spec_from_file_location("d231_operational_receipt_test",path)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
for digest, expected in (("0"*64,"receipt bytes or digest"), (sys.argv[2],"receipt decision")):
    try:
        module.validate_receipt(Path(sys.argv[1]).resolve(),digest)
    except ValueError as exc:
        assert str(exc)==expected, exc
    else:
        raise AssertionError("invalid receipt accepted")
assert not any(name.split(".")[0] in ("lcl","research") for name in sys.modules)
print("invalid byte hash and invalid coherent receipt rejected")
'@ | & $base -I -S -B - $bad (Get-D231Hash $bad)
Assert-D231 ($LASTEXITCODE -eq 0) 'Invalid receipt regression failed'
$tests+=@{id='invalid receipt hash and coherent invalid decision';rejected=$true}
$tests+=@{id='all seven exact metadata and independent offset-equivalence controls';passed=$true}
Write-D231NewJson (Join-Path $folder 'regression.json') $tests

$first=Join-Path $folder 'normal'
$null=New-Item -ItemType Directory -Path $first
$admission=Test-D231Admission $config (Get-D231Targets $config 'Inert' $first)
Write-D231NewJson (Join-Path $folder 'complete-admission.json') $admission
$admission | ConvertTo-Json -Depth 16 -Compress
Assert-D231 $admission.pass 'Complete inert admission failed'
$outcomes=@()
foreach($case in @('normal','inner','outer')){
    $caseFolder=Join-Path $folder $case
    if ($case -ne 'normal') { $null=New-Item -ItemType Directory -Path $caseFolder }
    $target=Get-D231Targets $config 'Inert' $caseFolder
    $previousLaunches=@(Get-ChildItem -LiteralPath $parent -Recurse -File -Filter 'admission.json').Count
    Assert-D231 ($previousLaunches -lt 12) 'Benign launch ceiling'
    $receipt=Get-D231Approval $admission 'Inert' $case ''
    $stopAt=@{normal=8;inner=5;outer=2.5}[$case]
    $result=Invoke-D231Watchdog $receipt $target $stopAt ($stopAt+1) 6
    $outcomes+=$result
    $result | ConvertTo-Json -Depth 12 -Compress
    Assert-D231 ($result.released -and $result.observer_signaled -and
        $result.foreground_seconds -le $result.hard_seconds -and $null -ne $result.combined_cpu_seconds -and $result.combined_cpu_seconds -lt 6) "Inert terminal accounting $case"
    foreach ($stream in @('stdout','stderr')) {
        $str=Get-Content -Raw -LiteralPath ($target.prefix+"-$stream.txt")
        Assert-D231 ($str.Trim() -ceq "D231 inert $stream") "Inert stream mismatch $case/$stream"
    }
    $s=Read-D231Json ($target.prefix+'-suspended.json')
    Assert-D231 ($s.in_job -and $s.job.lifetime -eq 1 -and $s.job.active -eq 1) 'Inert suspended case failed'
    if($case -eq 'outer'){
        Assert-D231 ($result.outer_status -ceq 'OUTER_WALL' -and $result.member_exit.Count -eq 2 -and
            $result.member_exit.suspended.signaled -and $result.member_exit.worker.signaled) 'Outer watchdog did not drain both members'
    } else {
        $obs=Read-D231Json ($target.prefix+'-foreground.json')
        Assert-D231 ($obs.job_limits.active_limit -eq 2 -and !$obs.job_limits.job_handle_inheritable -and
            $obs.job_final.active -eq 0 -and $obs.job_final.lifetime -eq 2 -and $obs.launcher_signaled -and
            $obs.worker_signaled -and $obs.resume_previous_count -eq 1) "Inert containment, release or drain mismatch $case"
        if ($case -eq 'normal'){
            Assert-D231 ($result.observer_exit -eq 0 -and $null -eq $obs.stop_reason -and $obs.launcher_exit_code -eq 0) 'Inert normal status'
        } else {
            Assert-D231 ($result.observer_exit -eq 1 -and $obs.stop_reason -ceq 'INNER_WALL' -and $obs.termination_errors.Count -eq 0) 'Inert inner stop status'
        }
    }
}
Write-D231NewJson (Join-Path $folder 'validation-summary.json') ([ordered]@{status='PASS';operational_version=$config.version;pass=$Pass;regressions=$tests.Count;benign_launches=$outcomes.Count;
    combined_cpu_seconds=($outcomes.combined_cpu_seconds | Measure-Object -Sum).Sum;
    foreground_seconds=($outcomes.foreground_seconds | Measure-Object -Sum).Sum})
