# D233 operational admission v1. This file defines functions only.
Set-StrictMode -Version Latest

function Read-D233Json([string]$Path) {
    Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json -AsHashtable -DateKind String
}
function Get-D233Hash([string]$Path) {
    (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Assert-D233($Condition, [string]$Message) {
    if (!$Condition) { throw $Message }
}
function Get-D233Ticks($Iso) {
    Assert-D233 ($Iso -is [string] -and $Iso -cmatch '^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{7}(Z|[+-]\d\d:\d\d)$') 'Expected strict timezone-aware ISO timestamp'
    if ($Iso.EndsWith('Z', [StringComparison]::Ordinal)) { $Iso = $Iso.Substring(0,$Iso.Length-1) + '+00:00' }
    [DateTimeOffset]::ParseExact($Iso,"yyyy-MM-dd'T'HH:mm:ss.fffffffzzz",
        [Globalization.CultureInfo]::InvariantCulture,[Globalization.DateTimeStyles]::None).UtcTicks
}
function Assert-D233PlainPath([string]$Path) {
    $item = Get-Item -LiteralPath $Path -Force -ErrorAction Stop
    while ($null -ne $item) {
        Assert-D233 (!($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) "Reparse ancestor: $($item.FullName)"
        $item = if ($item -is [IO.DirectoryInfo]) { $item.Parent } else { $item.Directory }
    }
}
function Assert-D233Vacant([string]$Path) {
    $full = [IO.Path]::GetFullPath($Path)
    $parent = [IO.Path]::GetDirectoryName($full)
    Assert-D233PlainPath $parent
    $entries = @([IO.Directory]::EnumerateFileSystemEntries($parent,[IO.Path]::GetFileName($full)))
    Assert-D233 ($entries.Count -eq 0) "Occupied destination: $Path"
}
function Assert-D233Cache([string]$Path,$Expected) {
    Assert-D233PlainPath $Path
    $item = Get-Item -LiteralPath $Path -Force -ErrorAction Stop
    Assert-D233 ($item -is [IO.FileInfo] -and $item.Length -eq $Expected.bytes) "Cache size or type: $Path"
    Assert-D233 ((Get-D233Hash $Path) -ceq $Expected.sha256) "Cache hash: $Path"
    Assert-D233 ($item.CreationTimeUtc.Ticks -eq (Get-D233Ticks $Expected.creation_utc)) "Cache creation time: $Path"
    Assert-D233 ($item.LastWriteTimeUtc.Ticks -eq (Get-D233Ticks $Expected.last_write_utc)) "Cache write time: $Path"
    Assert-D233 ($item.Attributes.ToString() -ceq $Expected.attributes) "Cache attributes: $Path"
}
function Invoke-D233Git([string[]]$ArgsForGit) {
    $result = & git @ArgsForGit
    if ($LASTEXITCODE -ne 0) { throw "Git exit $LASTEXITCODE for $($ArgsForGit -join ' ')" }
    $result
}
function Get-D233Ref([string]$Repo,[string]$Name) {
    $lines = @(Invoke-D233Git @('-C',$Repo,'ls-remote','origin',$Name))
    Assert-D233 ($lines.Count -eq 1 -and $lines[0] -cmatch '^([a-f0-9]{40})\s') "Exact remote ref required: $Repo $Name"
    ($lines[0] -split '\s+')[0]
}
function Assert-D233NoProcess {
    $hits = @(Get-CimInstance Win32_Process -Filter "Name='python.exe' OR Name='pythonw.exe' OR Name='python3.exe' OR Name='uv.exe' OR Name='py.exe'" |
        Where-Object {$_.CommandLine -and $_.CommandLine -match 'Lobster_Construction_Lab|d233[_-]unit[_-]partner|d231[_-]unequal[_-]pair|\b(lcl|research\.)'})
    Assert-D233 ($hits.Count -eq 0) 'Conflicting project process'
}
function Get-D233Targets($Config,[string]$Mode,[string]$TestRoot) {
    if ($Mode -eq 'Science') {
        $prefix = $Config.science.output
        $paths = @($Config.science.output,$Config.science.archive)
        $receipt = "$prefix-admission.json"
    } else {
        $prefix = Join-Path $TestRoot 'inert'
        $paths = @()
        $receipt = Join-Path $TestRoot 'admission.json'
    }
    $paths += $receipt
    $paths += @('stdout.txt','stderr.txt','suspended.json','released.json','worker.json','foreground.json','outer.json','outer-stdout.txt','outer-stderr.txt') |
        ForEach-Object {"$prefix-$_"}
    [ordered]@{prefix=$prefix;receipt=$receipt;paths=$paths}
}
function Assert-D233Authority($Config) {
    $science = $Config.science
    $head = Invoke-D233Git @('rev-parse','HEAD')
    $current = $head
    Assert-D233 ($head -cmatch '^[a-f0-9]{40}$') 'Wrong checkout identity'
    Assert-D233 ((Invoke-D233Git @('symbolic-ref','--short','HEAD')) -ceq 'main') 'Require branch main'
    Assert-D233 (@(Invoke-D233Git @('status','--porcelain')).Count -eq 0) 'Require clean worktree'
    Assert-D233 (@(Invoke-D233Git @('worktree','list','--porcelain') | Where-Object {$_ -match '^worktree '}).Count -eq 1 -and !(Test-Path -LiteralPath '.git/index.lock')) 'Require sole-writer checkout'
    foreach ($ancestor in $science.history) {
        $null = Invoke-D233Git @('merge-base','--is-ancestor',$ancestor,$current)
        $current = $ancestor
    }
    for ($i=1; $i -lt $science.history.Count; $i++) {
        Assert-D233 ((Invoke-D233Git @('rev-parse',($science.history[$i-1]+'^'))) -ceq $science.history[$i]) 'Historical direct ancestry'
    }
    $head
}
function Test-D233Admission($Config,$Targets) {
    $checks=[ordered]@{}
    $held=@{}
    function Check([string]$Name,[scriptblock]$Script) {
        try { $checks[$Name]=[ordered]@{passed=$true;value=(& $Script)} }
        catch { $checks[$Name]=[ordered]@{passed=$false;error=$_.Exception.Message} }
    }
    Check 'checkout' {$held.head=Assert-D233Authority $Config; $held.head}
    Check 'live_refs' {
        $tag=$Config.repos.baseline_tag
        $r=[ordered]@{head=(Get-D233Ref '.' 'refs/heads/main');tag=(Get-D233Ref '.' $tag);
            peel=(Get-D233Ref '.' "$tag^{}");mdl=(Get-D233Ref '../Math_Discovery_Lab' 'refs/heads/main');
            bounded=(Get-D233Ref '../MDL_Bounded_Search' 'refs/heads/main')}
        Assert-D233 ($r.head -ceq (Invoke-D233Git @('rev-parse','HEAD')) -and
            $r.tag -ceq $Config.repos.baseline_object -and $r.peel -ceq $Config.repos.baseline_peel -and
            $r.tag -ceq (Invoke-D233Git @('rev-parse',$tag)) -and $r.peel -ceq (Invoke-D233Git @('rev-parse',"$tag^{}")) -and
            $r.mdl -ceq $Config.repos.mdl -and $r.bounded -ceq $Config.repos.bounded) 'Protected refs or live main mismatch'
        $r
    }
    Check 'scientific_bytes_and_blobs' {
        $sc=$Config.science
        Assert-D233 ((Get-D233Hash $sc.manifest_path) -ceq $sc.manifest_sha256 -and (Get-D233Hash $sc.registration_path) -ceq $sc.registration_sha256) 'Frozen manifest or registration'
        $b=(Read-D233Json $sc.manifest_path).sha256
        Assert-D233 ($b.Count -eq $sc.binding_count) 'Manifest size'
        foreach ($path in $b.Keys) {
            Assert-D233PlainPath $path
            $binding=Invoke-D233Git @('rev-parse',($sc.preparation+':'+$path))
            $current=Invoke-D233Git @('rev-parse',('HEAD:'+$path))
            Assert-D233 ($binding -ceq $current -and (Get-D233Hash $path) -ceq $b[$path]) "Frozen source: $path"
        }
        $reg=Read-D233Json $sc.registration_path
        Assert-D233 ($reg.run_id -ceq $Config.run_id -and $reg.output -ceq $sc.output -and
            $reg.archive -ceq $sc.archive -and $reg.workers -eq 1 -and
            $reg.max_cpu_seconds -eq $sc.max_cpu_seconds -and $reg.max_wall_seconds -eq $sc.max_wall_seconds) 'Wrong scope'
        $b.Count
    }
    Check 'destinations' {
        foreach ($path in ($Targets.paths + (Get-D233Targets $Config 'Science' '').paths|Select-Object -Unique)) { Assert-D233Vacant $path }
        $Targets.paths
    }
    Check 'qualified_v3_custody' {
        Assert-D233 ((Get-D233Hash $Config.referents.v3_qualification) -ceq $Config.referents.v3_qualification_sha256) 'Historical V3 qualification identity'
        $v3=Read-D233Json $Config.referents.v3_qualification
        foreach ($relative in $v3.sha256.Keys) { Assert-D233 ((Get-D233Hash $relative) -ceq $v3.sha256[$relative]) "Historical V3 binding: $relative" }
        $v3.sha256.Count
    }
    Check 'quarantine' {
        $q=Read-D233Json $Config.referents.inventory
        Assert-D233 ((Get-D233Hash $Config.referents.inventory) -ceq $Config.referents.inventory_sha256 -and
            $q.files.Count -eq 7 -and $q.authorized_bytes -eq 68269 -and
            @(Get-ChildItem -LiteralPath $q.quarantine -Force).Count -eq 7) 'Quarantine inventory'
        foreach ($row in $q.files) {
            Assert-D233Vacant $row.original
            Assert-D233Cache $row.quarantined $row.before
        }
        foreach($p in $q.unrelated_cache_files_left_at_source){Assert-D233 (Test-Path -LiteralPath $p -PathType Leaf) "Missing unrelated cache $p"}
        & git check-ignore --quiet --no-index -- ($q.quarantine+'/')
        Assert-D233 ($LASTEXITCODE -eq 0 -and @(Invoke-D233Git @('ls-files','--',($q.quarantine+'/'))).Count -eq 0) 'Quarantine ignore custody'
        68269
    }
    Check 'processes' {Assert-D233NoProcess; 0}
    Check 'runtime_files' {
        $ref=$Config.referents
        Assert-D233 ((Get-D233Hash $ref.readiness) -ceq $ref.readiness_sha256) 'Runtime record custody'
        $ready=Read-D233Json $ref.readiness
        $ids=$ready.runtime
        Assert-D233 ($ids.launcher_sha256 -ceq (Read-D233Json $ref.legacy_receipt).launcher_sha256) 'Runtime launcher record conflict'
        foreach($pair in @(@('.venv/Scripts/python.exe',$ids.launcher_sha256),
                           @($ids.base_executable,$ids.base_sha256),
                           @((Join-Path (Split-Path -Parent $ids.base_executable) 'python313.dll'),$ids.dll_sha256),
                           @('.venv/pyvenv.cfg',$ids.venv_config_sha256),
                           @($ref.native,$ready.retained_native_sha256),@($ref.historical_wrapper,$ready.foreground_wrapper.sha256),
                           @($ref.outer_template,$ready.qualification_outer_template_sha256))){
            Assert-D233PlainPath $pair[0]
            Assert-D233 ((Get-D233Hash $pair[0]) -ceq $pair[1]) "Runtime or supervision bytes: $($pair[0])"
        }
        Assert-D233 (@(Get-ChildItem Env:PYTHON*).Count -eq 0 -and
            @(Get-ChildItem -LiteralPath '.venv/Lib/site-packages' -Filter '*.pth' -Force -File).Count -eq 0) 'Unexpected Python startup override'
        foreach($loc in @($ids.base_prefix,'.venv/Scripts','.venv/Lib/site-packages')){
            Assert-D233 (@(Get-ChildItem -LiteralPath $loc -Filter '*._pth' -Force -File).Count -eq 0) "Unexpected path override $loc"
            foreach ($name in @('sitecustomize','usercustomize')) {
                Assert-D233 (!(Test-Path -LiteralPath (Join-Path $loc ($name+'.py'))) -and
                    !(Test-Path -LiteralPath (Join-Path $loc $name))) "Unexpected site hook $loc/$name"
            }
        }
        foreach($loc in @('.','lcl','research','research/d231_unequal_pair_kernel','research/d233_unit_partner_kernel','research/d229_homogeneous_pair_kernel','research/d204_readiness_v9','research/d233_operations')){
            Assert-D233PlainPath $loc
        }
        foreach($loc in @('.',(Join-Path $ids.base_prefix 'Lib'))){
            foreach($name in @('sitecustomize','usercustomize')){
                Assert-D233 (!(Test-Path -LiteralPath (Join-Path $loc ($name+'.py'))) -and !(Test-Path -LiteralPath (Join-Path $loc $name))) "Unexpected site hook $loc/$name"
            }
        }
        $held.ready=$ready
        $ids
    }
    Check 'runtime_and_import_probe' {
        Assert-D233 ($checks.runtime_files.passed -and $checks.scientific_bytes_and_blobs.passed) 'Runtime prerequisites not met'
        $probe=Get-Content -LiteralPath 'research/d233_operations/probe.py' -Raw -Encoding UTF8
        $raw=$probe | & '.venv/Scripts/python.exe' -B -
        Assert-D233 ($LASTEXITCODE -eq 0) 'Benign PathFinder and runtime probe failed'
        $obs=$raw | ConvertFrom-Json -AsHashtable -DateKind String
        $ids=$held.ready.runtime
        foreach($field in @('implementation','version','machine','executable','base_executable','prefix','base_prefix')){
            Assert-D233 ($obs[$field] -ceq $ids[$field]) "Runtime $field"
        }
        $expected=@((Read-D233Json $Config.science.manifest_path).sha256.Keys | Where-Object { $_.EndsWith('.py') }) + @($Config.referents.native,$Config.referents.observer)
        Assert-D233 (!(Compare-Object $expected $obs.bound_source_paths -CaseSensitive) -and
                     ($obs.startup_paths -join '|') -ceq ($ids.startup_paths -join '|')) 'Runtime path or closure mismatch'
        $obs
    }
    [ordered]@{pass=@($checks.Values | Where-Object {!$_.passed}).Count -eq 0;checked_utc=[DateTimeOffset]::UtcNow.ToString('o');checks=$checks}
}

function Write-D233NewJson([string]$Path,$Value) {
    $data=[Text.UTF8Encoding]::new($false).GetBytes(($Value|ConvertTo-Json -Depth 24)+[char]10)
    Assert-D233 ($data.Length -le 65536) "Oversized operational record $Path"
    $file = [IO.File]::Open($Path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {$file.Write($data,0,$data.Length);$file.Flush($true)} finally {$file.Dispose()}
}
