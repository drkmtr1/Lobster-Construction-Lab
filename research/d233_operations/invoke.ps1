param(
    [Parameter(Mandatory)][ValidateSet('Qualify','Science')][string]$Mode,
    [ValidatePattern('^pass-[1-5]$')][string]$Pass = 'pass-1'
)
$ErrorActionPreference='Stop'
$PSNativeCommandUseErrorActionPreference=$false
$ops='research/d233_operations'
. (Join-Path $PSScriptRoot 'admission.ps1')
Assert-D233 ((Get-Item -LiteralPath $ops).FullName -eq $PSScriptRoot) 'Run from LCL root'
$config=Read-D233Json "$ops/identities.json"

function Invoke-D233Watchdog($Data,$Target,[double]$StopSeconds,[double]$HardSeconds,[double]$CpuCeiling) {
    $receipt=$Target.receipt
    foreach ($p in $Target.paths) { Assert-D233Vacant $p }
    Assert-D233NoProcess
    Write-D233NewJson $receipt $Data
    $sha=Get-D233Hash $receipt
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
                        $row=Read-D233Json $record
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
    if (Test-Path -LiteralPath "$prefix-foreground.json") {$inner=Read-D233Json "$prefix-foreground.json"}
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
        inner_sha256=$(if($null -ne $inner){Get-D233Hash "$prefix-foreground.json"})}
    Write-D233NewJson "$prefix-outer.json" $record
    if($null -ne $process){$process.Dispose()}
    $outer.Dispose()
    $record
}

function Get-D233Approval($Admission,[string]$ModeLabel,[string]$Case,[string]$QualHash) {
    $scientific=$ModeLabel -eq 'Science'
    $sc=$config.science
    $ready=Read-D233Json $config.referents.readiness
    $inner=if($scientific){$sc.inner_wall_seconds}else{@{normal=6;inner=1.6;outer=10}[$Case]}
    [ordered]@{
        decision=$(if($scientific){$sc.decision}else{'D233_INERT_QUALIFICATION'})
        operational_version=$config.version
        run_id=$(if($scientific){$config.run_id}else{"$([IO.Path]::GetFileName($config.qualification_root))-$Pass-$Case"})
        test_case=$Case
        verified_checkpoint=$sc.preparation
        execution_checkout=$Admission.checks.checkout.value
        authority_checkpoint=$sc.authority_checkpoint
        source_manifest_sha256=$sc.manifest_sha256
        registration_sha256=$sc.registration_sha256
        qualification_manifest_sha256=$QualHash
        qualified_supervision=$QualHash
        director_review=$(if($scientific){"Director accepts exact D233 preparation $($sc.preparation) and its execution ceilings; recorded at $($sc.authority_checkpoint)."})
        owner_authorization=$(if($scientific){"Owner directive 'D233 — Director Acceptance, Integrated Operational Qualification and One-Shot Unit-Partner Kernel Execution', one release after qualified admission; recorded at $($sc.authority_checkpoint)."})
        verified_utc=$Admission.checked_utc
        runtime=$ready.runtime
        native_sha256=$ready.retained_native_sha256
        observer_sha256=(Get-D233Hash "$ops/observe_v1.py")
        outer_adapter_sha256=(Get-D233Hash "$ops/invoke.ps1")
        inner_wall_seconds=$inner
    }
}

if ($Mode -eq 'Science') {
    $qualified=$config.qualification_manifest
    $sc=$config.science
    $q=Read-D233Json $qualified
    Assert-D233 ($q.status -ceq 'QUALIFIED' -and $q.operational_version -ceq $config.version -and
        $q.scientific_manifest_sha256 -ceq $sc.manifest_sha256 -and
        $q.scientific_registration_sha256 -ceq $sc.registration_sha256 -and
        $q.authority_checkpoint -ceq $sc.authority_checkpoint) 'No matching independently reviewed operational qualification'
    $null=Invoke-D233Git @('merge-base','--is-ancestor',$q.reviewed_source_checkpoint,'HEAD')
    foreach($file in @('identities.json','probe.py','admission.ps1','invoke.ps1','observe_v1.py')) {
        $relative="$ops/$file"
        Assert-D233 ($q.sha256.Contains($relative) -and
            (Invoke-D233Git @('rev-parse',($q.reviewed_source_checkpoint+':'+$relative))) -ceq
            (Invoke-D233Git @('rev-parse',('HEAD:'+$relative)))) "Qualified source continuity: $relative"
    }
    foreach($path in $q.sha256.Keys) {
        Assert-D233PlainPath $path
        Assert-D233 ((Get-D233Hash $path) -ceq $q.sha256[$path]) "Qualification binding: $path"
    }
    $target=Get-D233Targets $config 'Science' ''
    $admission=Test-D233Admission $config $target
    $admission | ConvertTo-Json -Depth 16 -Compress
    $admissionRecord=Join-Path $config.qualification_root "live-admission-$Pass.json"
    Assert-D233Vacant $admissionRecord
    Write-D233NewJson $admissionRecord $admission
    Assert-D233 $admission.pass 'Fresh live admission failed'
    $receipt=Get-D233Approval $admission 'Science' '' (Get-D233Hash $qualified)
    $result=Invoke-D233Watchdog $receipt $target $sc.outer_stop_seconds $sc.max_wall_seconds $sc.max_cpu_seconds
    $result | ConvertTo-Json -Depth 12 -Compress
    exit $(if($result.observer_signaled -and $result.observer_exit -eq 0 -and
        $result.outer_status -eq 'NATURAL' -and $result.foreground_seconds -le $sc.max_wall_seconds -and
        $null -ne $result.combined_cpu_seconds -and $result.combined_cpu_seconds -lt $sc.max_cpu_seconds){0}else{1})
}

$parent=$config.qualification_root
if (!(Test-Path -LiteralPath $parent)) { $null=New-Item -ItemType Directory -Path $parent }
$folder=Join-Path $parent $Pass
Assert-D233Vacant $folder
$null=New-Item -ItemType Directory -Path $folder
$tests=@()
function Expect-Reject([string]$Name,[scriptblock]$Test,[string]$Pattern) {
    try { & $Test; throw "Unexpected success: $Name" }
    catch {
        if ($_.Exception.Message -notmatch $Pattern) { throw }
        $script:tests+=[ordered]@{id=$Name;rejected=$true;reason=$_.Exception.Message}
    }
}
$q=Read-D233Json $config.referents.inventory
foreach ($row in $q.files) { Assert-D233Cache $row.quarantined $row.before }
$row=$q.files[0]
$changed=@{}
foreach($key in $row.before.Keys){$changed[$key]=$row.before[$key]}
$changed.creation_utc='2026-11-21T06:25:49.9904097Z'
Expect-Reject 'one UTC tick changed' { Assert-D233Cache $row.quarantined $changed } '^Cache creation time:'
Expect-Reject 'missing timezone' { $null=Get-D233Ticks '2026-11-21T06:25:49.9904096' } '^Expected strict'
Expect-Reject 'malformed ISO calendar' { $null=Get-D233Ticks '2026-13-21T06:25:49.9904096Z' } 'valid DateTime|un-representable|DateTimeOffset|DateTime'
Assert-D233 ((Get-D233Ticks '2026-11-21T06:25:49.9904096Z') -eq (Get-D233Ticks '2026-11-20T20:25:49.9904096-10:00')) 'Offset equivalence'
$changed.creation_utc=$row.before.creation_utc
$changed.sha256='0'*64
Expect-Reject 'incorrect hash' { Assert-D233Cache $row.quarantined $changed } '^Cache hash:'
$changed.sha256=$row.before.sha256
$changed.bytes=$row.before.bytes+1
Expect-Reject 'incorrect size' { Assert-D233Cache $row.quarantined $changed } '^Cache size'
Expect-Reject 'missing file' { Assert-D233Cache (Join-Path $folder 'missing') $changed } 'Cannot find path'
$fixture=Join-Path $folder 'cache-guard-fixture.dat'
[IO.File]::WriteAllBytes($fixture,[byte[]](17,64))
$info=Get-Item -LiteralPath $fixture
$bytesExpected=@{bytes=$info.Length;sha256=(Get-D233Hash $fixture);creation_utc=$info.CreationTimeUtc.ToString('o');last_write_utc=$info.LastWriteTimeUtc.ToString('o');attributes=$info.Attributes.ToString()}
Assert-D233Cache $fixture $bytesExpected
[IO.File]::WriteAllBytes($fixture,[byte[]](17,65))
Expect-Reject 'genuinely changed fixture bytes' { Assert-D233Cache $fixture $bytesExpected } '^Cache hash:'
[IO.File]::WriteAllBytes($fixture,[byte[]](17))
Expect-Reject 'genuine fixture truncation' { Assert-D233Cache $fixture $bytesExpected } '^Cache size'
$collision=Join-Path $folder 'immutable.json'
Write-D233NewJson $collision @{payload='first'}
$held=Get-D233Hash $collision
Expect-Reject 'occupied destination' { Assert-D233Vacant $collision } '^Occupied destination:'
Expect-Reject 'immutable overwrite' { Write-D233NewJson $collision @{payload='changed'} } 'already exists'
Assert-D233 ((Get-D233Hash $collision) -ceq $held) 'Immutable bytes changed'
$bad=Join-Path $folder 'invalid-admission.json'
Write-D233NewJson $bad @{decision='BROKEN';operational_version=$config.version}
$base=(Read-D233Json $config.referents.readiness).runtime.base_executable
@'
import importlib.util
from pathlib import Path
import sys
path=Path("research/d233_operations/observe_v1.py")
spec=importlib.util.spec_from_file_location("d233_operational_receipt_test",path)
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
'@ | & $base -I -S -B - $bad (Get-D233Hash $bad)
Assert-D233 ($LASTEXITCODE -eq 0) 'Invalid receipt regression failed'
$tests+=@{id='invalid receipt hash and coherent invalid decision';rejected=$true}
$badBounds=Join-Path $folder 'invalid-inert-bounds'
$null=New-Item -ItemType Directory -Path $badBounds
$badBoundsReceipt=Join-Path $badBounds 'admission.json'
Write-D233NewJson $badBoundsReceipt @{decision='D233_INERT_QUALIFICATION';operational_version=$config.version;test_case='normal';inner_wall_seconds=60}
@'
import importlib.util
from pathlib import Path
import sys
spec=importlib.util.spec_from_file_location("d233_receipt_test", "research/d233_operations/observe_v1.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
try:
    module.validate_receipt(Path(sys.argv[1]).resolve(), sys.argv[2])
except ValueError as exc:
    assert str(exc) == "inert case bounds", exc
else:
    raise AssertionError("coherent incorrect receipt accepted")
'@ | & $base -I -S -B - $badBoundsReceipt (Get-D233Hash $badBoundsReceipt)
Assert-D233 ($LASTEXITCODE -eq 0) 'Coherent inert bounds regression failed'
$tests+=@{id='coherent inappropriate inert bounds';rejected=$true}
$tests+=@{id='all seven exact metadata and independent offset-equivalence controls';passed=$true}
Write-D233NewJson (Join-Path $folder 'regression.json') $tests

$first=Join-Path $folder 'normal'
$null=New-Item -ItemType Directory -Path $first
$admission=Test-D233Admission $config (Get-D233Targets $config 'Inert' $first)
Write-D233NewJson (Join-Path $folder 'complete-admission.json') $admission
$admission | ConvertTo-Json -Depth 16 -Compress
Assert-D233 $admission.pass 'Complete inert admission failed'
$outcomes=@()
foreach($case in @('normal','inner','outer')){
    $caseFolder=Join-Path $folder $case
    if ($case -ne 'normal') { $null=New-Item -ItemType Directory -Path $caseFolder }
    $target=Get-D233Targets $config 'Inert' $caseFolder
    $previousLaunches=@(Get-ChildItem -LiteralPath $parent -Recurse -File -Filter 'admission.json' | Where-Object { $_.Directory.Name -cin @('normal','inner','outer') }).Count
    Assert-D233 ($previousLaunches -lt 12) 'Benign launch ceiling'
    $receipt=Get-D233Approval $admission 'Inert' $case ''
    $stopAt=@{normal=8;inner=5;outer=2.5}[$case]
    $result=Invoke-D233Watchdog $receipt $target $stopAt ($stopAt+1) 6
    $outcomes+=$result
    $result | ConvertTo-Json -Depth 12 -Compress
    Assert-D233 ($result.released -and $result.observer_signaled -and
        $result.foreground_seconds -le $result.hard_seconds -and $null -ne $result.combined_cpu_seconds -and $result.combined_cpu_seconds -lt 6) "Inert terminal accounting $case"
    foreach ($stream in @('stdout','stderr')) {
        [string]$str=Get-Content -Raw -LiteralPath ($target.prefix+"-$stream.txt")
        Assert-D233 ($str.Trim() -ceq "D233 inert $stream") "Inert stream mismatch $case/$stream"
    }
    $s=Read-D233Json ($target.prefix+'-suspended.json')
    Assert-D233 ($s.in_job -and $s.job.lifetime -eq 1 -and $s.job.active -eq 1) 'Inert suspended case failed'
    if($case -eq 'outer'){
        Assert-D233 ($result.outer_status -ceq 'OUTER_WALL' -and $result.member_exit.Count -eq 2 -and
            $result.member_exit.suspended.signaled -and $result.member_exit.worker.signaled) 'Outer watchdog did not drain both members'
    } else {
        $obs=Read-D233Json ($target.prefix+'-foreground.json')
        Assert-D233 ($obs.job_limits.active_limit -eq 2 -and !$obs.job_limits.job_handle_inheritable -and
            $obs.job_final.active -eq 0 -and $obs.job_final.lifetime -eq 2 -and $obs.launcher_signaled -and
            $obs.worker_signaled -and $obs.resume_previous_count -eq 1) "Inert containment, release or drain mismatch $case"
        if ($case -eq 'normal'){
            Assert-D233 ($result.observer_exit -eq 0 -and $null -eq $obs.stop_reason -and $obs.launcher_exit_code -eq 0) 'Inert normal status'
        } else {
            Assert-D233 ($result.observer_exit -eq 1 -and $obs.stop_reason -ceq 'INNER_WALL' -and $obs.termination_errors.Count -eq 0) 'Inert inner stop status'
        }
    }
}
Write-D233NewJson (Join-Path $folder 'validation-summary.json') ([ordered]@{status='PASS';operational_version=$config.version;pass=$Pass;regressions=$tests.Count;benign_launches=$outcomes.Count;
    combined_cpu_seconds=($outcomes.combined_cpu_seconds | Measure-Object -Sum).Sum;
    foreground_seconds=($outcomes.foreground_seconds | Measure-Object -Sum).Sum})
