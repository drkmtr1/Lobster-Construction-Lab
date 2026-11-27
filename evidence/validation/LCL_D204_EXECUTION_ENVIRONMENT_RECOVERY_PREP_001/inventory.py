import hashlib,json,os,platform,shutil,subprocess,sys,time
from pathlib import Path
start=time.monotonic();cpu=time.process_time()
wsldir=Path(os.environ['SystemRoot'])/'System32'
exe=wsldir/'wsl.exe'
inventory={
    'windows_build':list(sys.getwindowsversion()[:3]),
    'architecture':platform.machine(),
    'process_clock':time.get_clock_info('process_time').implementation,
    'win32_python_version':list(sys.version_info[:3]),
    'wsl_executable':dict(present=exe.is_file(),system_relative='System32/wsl.exe',
                           sha256=hashlib.sha256(exe.read_bytes()).hexdigest() if exe.is_file() else None),
    'native_discovery':{x:shutil.which(x) is not None for x in ('docker.exe','podman.exe','multipass.exe','bash.exe')},
    'wsl_queries':[], 'distro_started':False, 'synthetic_probes':0
}
def decode(raw):
    if raw.startswith((b'\xff\xfe',b'\xfe\xff')):
        return raw.decode('utf-16').replace('\r\n','\n').strip()
    if b'\x00' in raw:
        return raw.decode('utf-16-le',errors='replace').replace('\r\n','\n').strip()
    return raw.decode('utf-8',errors='replace').replace('\r\n','\n').strip()
if exe.is_file():
    for argv in (('--status',),('--version',),('--list','--verbose')):
        t=time.monotonic()
        try:
            q=subprocess.run([str(exe),*argv],stdin=subprocess.DEVNULL,capture_output=True,timeout=8,
                             creationflags=subprocess.CREATE_NO_WINDOW,check=False)
        except subprocess.TimeoutExpired:
            inventory['wsl_queries'].append({'args':argv, 'status':'TIMEOUT_AND_SUBPROCESS_CLEANUP'})
            break
        assert len(q.stdout)+len(q.stderr)<=16384
        inventory['wsl_queries'].append({'args':argv,'exit':q.returncode,'stdout':decode(q.stdout),
            'stderr':decode(q.stderr),'observed_elapsed_seconds':round(time.monotonic()-t,6)})
inventory['inventory_process_cpu_seconds']=round(time.process_time()-cpu,6)
inventory['inventory_elapsed_seconds']=round(time.monotonic()-start,6)
print(json.dumps(inventory))
