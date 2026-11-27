import ctypes,json,time
start=time.monotonic();cpu=time.process_time()
names=('CreateJobObjectW','SetInformationJobObject','QueryInformationJobObject',
       'CreateProcessW','AssignProcessToJobObject','IsProcessInJob','ResumeThread',
       'TerminateJobObject','TerminateProcess','WaitForSingleObject','GetProcessTimes',
       'GetTickCount64','QueryUnbiasedInterruptTimePrecise','InitializeProcThreadAttributeList',
       'UpdateProcThreadAttribute','DeleteProcThreadAttributeList','GetExitCodeProcess')
k=ctypes.WinDLL('kernel32.dll')
exports={name:hasattr(k,name) for name in names}
print(json.dumps({'found_exports':exports,'native_control_calls':0,'process_cpu_seconds':time.process_time()-cpu,
                  'elapsed_seconds':time.monotonic()-start}))
