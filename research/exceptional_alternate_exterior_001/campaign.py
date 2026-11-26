
"""Future D172 official entry point. Preparation uses the separate parse-only script."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import tracemalloc
import types


def runtime():
    path = Path(__file__).absolute().with_name("runtime.py")
    mod = types.ModuleType("d172_runtime")
    mod.__file__ = str(path)
    exec(compile(path.read_bytes(),str(path),"exec"),mod.__dict__)
    return mod


def gate(api, args):
    manifest_path = api.EVIDENCE/"MANIFEST.json"
    config_path = api.KIT/"config.json"
    config = api.read(config_path)
    manifest_raw = api.ordinary(manifest_path).read_bytes()
    if api.sha(manifest_raw) != args.manifest_sha:
        raise ValueError("reviewed manifest hash mismatch")
    manifest = json.loads(manifest_raw)
    approval = api.repo_path(config["approval"])
    if Path(args.approval).absolute() != approval or not approval.is_file():
        raise ValueError("exact separate Owner authorization required")
    approval_raw = api.ordinary(approval).read_bytes()
    if (json.loads(approval_raw) != {"task":config["task"], "manifest_sha256":args.manifest_sha,
                                     "status":"AUTHORIZED_FOR_OFFICIAL_RUN"}
            or manifest["status"] != "PREPARED_PENDING_DIRECTOR_REVIEW"
            or manifest["task"] != config["task"]):
        raise ValueError("unapproved manifest or execution disposition")
    frozen = manifest["files"]
    required = [config_path,Path(__file__).absolute(),api.KIT/"primary.py",api.KIT/"audit.py",
                api.KIT/"runtime.py",api.EVIDENCE/"POPULATION.json",api.EVIDENCE/"PREFLIGHT.json",
                api.EVIDENCE/"CONTROLS.json",api.KIT/"CONTRACT.md"]
    keys = {p.relative_to(api.ROOT).as_posix() for p in required}
    if not keys <= frozen.keys():
        raise ValueError("missing preparation binding")
    for name, binding in (frozen | manifest["retained_inputs"]).items():
        if api.file_binding(api.repo_path(name)) != binding:
            raise ValueError(f"frozen binding mismatch: {name}")
    if api.file_binding(api.ROOT/"STATE.md") != manifest["prepared_state"]:
        raise ValueError("canonical prepared STATE differs")
    api.check_runtime(config,base_process=args.worker)
    preflight = api.read(api.EVIDENCE/"PREFLIGHT.json")
    measured = manifest["preparation_accounting"]
    execution = config["limits"]
    reserve = config["reserve"]
    if (preflight["status"] != "PASS_PARSE_ONLY" or preflight["population"]!=396
            or preflight["numerical_work"] != 0 or preflight["task_module_imports"] != 0
            or measured["charged_cpu_seconds"] > config["preparation"]["cpu_seconds"]
            or measured["charged_wall_seconds"] > config["preparation"]["wall_seconds"]
            or measured["charged_cpu_seconds"] >= reserve["preparation_startup_cpu_seconds"]
            or measured["charged_wall_seconds"] >= reserve["preparation_startup_wall_seconds"]
            or execution["workers"] != 1
            or (measured["new_bundle_bytes"] > config["preparation"]["bytes"])):
        raise ValueError("preparation gate not satisfied")
    return manifest, config, api.repo_path(config["output"]), api.sha(approval_raw)


def original_rows(api, config, population):
    last_shard, shard = None, {}
    source = api.repo_path(config["D164_input"])
    for entry in population:
        if entry["shard"] != last_shard:
            last_shard = entry["shard"]
            if Path(last_shard).name != last_shard or not last_shard.startswith("targets-"):
                raise ValueError("invalid retained shard identity")
            shard = {item["id"]:item for item in api.read(source/last_shard)}
        row = shard[entry["id"]]
        if (api.sha(api.encoded(row)) != entry["record_sha256"] or row["digest"]!=entry["digest"]
                or row["parameters"]!=entry["parameters"] or row["K"]!=entry["K"]):
            raise ValueError("original canonical record binding")
        yield row, entry


def disposition(row, entry, prefix, arm, meter, primary, audit, dependencies):
    old_primary, old_audit, independent_graph, checker = dependencies
    before = dict(meter.counts)
    meter.arm_start_counts = before
    meter.phase = f"{arm} admission"
    meter.tick("dispositions")
    if arm == "M" and all(q%2==0 for q in row["suffix"][0]):
        if entry["M_symbolic"] != "EVEN_FIRST_MENU_TRANSLATION_PARITY":
            raise ValueError("frozen symbolic basis")
        meter.phase = "symbolic menu check"
        old_audit.original_context(row,prefix,independent_graph)
        result = {"claim":"NO", "basis":entry["M_symbolic"]}
        proof = {"status":"SYMBOLIC", "reference":"CONTRACT.md#3-menu-moment"}
    else:
        if arm=="M" and entry["M_symbolic"] is not None:
            raise ValueError("unexpected menu symbolic basis")
        meter.tick("numerical_dispositions")
        result = primary.solve(row,prefix,arm,meter,old_primary)
        if result["claim"] == "YES":
            proof = audit.positive(row,prefix,arm,result["solution"],meter,old_audit,independent_graph,checker)
        else:
            proof = audit.negative(row,prefix,arm,meter,old_audit,independent_graph)
            if result["counts"] != proof["counts"]:
                raise ValueError("primary and independent exterior accounting differ")
    meter.time_check()
    return {"id":row["id"],"digest":row["digest"],"record_sha256":entry["record_sha256"],
            "prefix_digest":prefix["digest"],
            "ordered_parameters":row["parameters"],"arm":arm,"result":result,"audit":proof,
            "work":{key:after-before[key] for key,after in meter.counts.items()}}


def worker(api, manifest, config, output, approval_sha, args):
    claim = api.read(output/"CLAIM.json")
    if (claim["manifest_sha256"] != args.manifest_sha or claim["approval_sha256"] != approval_sha
            or claim["status"]!="CLAIMED_ONCE" or claim["supervisor_pid"] != os.getppid()
            or set(p.name for p in output.iterdir()) != {"CLAIM.json"}):
        raise ValueError("missing exclusive supervisor claim")
    tracemalloc.start(1)
    charged = manifest["preparation_accounting"]["new_bundle_bytes"] + (output/"CLAIM.json").stat().st_size
    charged += api.write_new(output/"WORKER.json", {"pid":os.getpid(),"status":"STARTED_ONCE"},4096)
    meter = api.Meter(config,output,charged,claim["worker_deadline"])
    active, active_arm, separator, reason = None, None, None, None
    completed, blocked, a_no = 0, 0, 0
    try:
        old = api.repo_path(config["D164_code"])
        old_primary = api.load_source("d172_bound_primary",old/"primary.py")
        old_audit = api.load_source("d172_bound_audit",old/"audit.py")
        primary = api.load_source("d172_primary",api.KIT/"primary.py")
        audit = api.load_source("d172_audit",api.KIT/"audit.py")
        graph = api.load_source("d172_original",api.repo_path(config["independent_graph"]))
        checker = api.load_source("d172_checker",api.ROOT/"lcl/verify.py").verify_certificate
        prefix = api.read(api.repo_path(config["D164_input"])/"prefix.json")
        if (prefix["n"],prefix["frontier"],prefix["actual_cut"],prefix["polarity"]) != (74,"s:27",39,"maximum"):
            raise ValueError("independent prefix identity")
        if not checker(prefix["graph"],prefix["actual_labels"],expected_graph_digest=prefix["digest"])["valid"]:
            raise ValueError("independent prefix confirmation")
        population = api.read(api.EVIDENCE/"POPULATION.json")["execution_order"]
        if len(population)!=396:
            raise ValueError("frozen population count")
        for row, entry in original_rows(api,config,population):
            active, active_arm = row["id"], "M"
            meter.phase = "target admission"
            meter.tick("targets")
            M = disposition(row,entry,prefix,"M",meter,primary,audit,(old_primary,old_audit,graph,checker))
            meter.write(active+"-M.json",M)
            meter.candidate = None
            active_arm = "A"
            if M["result"]["claim"] == "YES":
                meter.phase = "A skipped after verified M YES"
                meter.arm_start_counts = dict(meter.counts)
                meter.tick("dispositions")
                A = {"id":active,"digest":row["digest"],"record_sha256":entry["record_sha256"],
                     "prefix_digest":prefix["digest"],
                     "arm":"A","result":{"claim":"NOT_REQUIRED_FOR_SEPARATOR","basis":"VERIFIED_M_YES"}}
            else:
                A = disposition(row,entry,prefix,"A",meter,primary,audit,(old_primary,old_audit,graph,checker))
            meter.write(active+"-A.json",A)
            claims = {r["arm"]:r["result"]["claim"] for r in (M,A)}
            separating = claims == {"M":"NO","A":"YES"}
            if separating:
                struct = A["audit"]["exterior_structure"]
                witness = {"target":active,"original_digest":row["digest"],"ordered_parameters":row["parameters"],
                           "record_sha256":entry["record_sha256"],"arm_files":[active+"-M.json",active+"-A.json"],
                           "arm_sha256":[api.sha(api.encoded(r)) for r in (M,A)],
                           "menu_negative":M["result"],"menu_audit":M["audit"],"alternate_structure":struct,
                           "resources":A["audit"]["resources"],"connector":A["audit"]["connector"]}
            else:
                witness = None
            meter.write(active+"-PAIR.json",{"id":active,"digest":row["digest"],"prefix_digest":prefix["digest"],"claims":claims,
                                            "separating":separating,"separator":witness})
            completed += 1
            blocked += claims["M"]=="YES"
            a_no += claims["A"]=="NO"
            meter.time_check()
            if separating:
                separator = active
                break
            active, active_arm = None, None
        if separator is None and (completed,blocked+a_no)!=(396,396):
            raise ValueError("attempt to conclude from incomplete coverage")
    except (Exception, KeyboardInterrupt) as err:
        reason = f"{type(err).__name__}: {err}"[:512]
    if reason:
        status = "INCOMPLETE"
    else:
        status = "SEPARATOR_VERIFIED" if separator else "EXHAUSTED_NO_SEPARATOR"
    summary = {"status":status,"reason":reason,"separator":separator,"current_target":active,"current_arm":active_arm,
               "pairs_completed":completed,"disqualified_by_M_positive":blocked,"disqualified_by_A_negative":a_no,
               "pending_checkpoint":meter.interruption() if reason else None,
               "counts":meter.counts,"counts_by_phase":meter.by_phase,"bytes_before_summary":meter.bytes,
               "traced_peak_bytes":tracemalloc.get_traced_memory()[1],
               "peak_candidate_states":meter.peak_candidate_states,"worker_cpu_seconds":time.process_time()}
    api.write_new(output/"SUMMARY.json",summary,config["reserve"]["worker_summary_bytes"])
    return int(reason is not None)


def supervise(api, manifest, config, output, approval_sha, args, began_wall):
    reserve, limit = config["reserve"], config["limits"]
    combined_allowance = limit["wall_seconds"]-reserve["preparation_startup_wall_seconds"]
    absolute_deadline = began_wall+combined_allowance
    if time.monotonic() >= absolute_deadline-reserve["controlled_stop_seconds"]:
        raise ValueError("supervisor startup exhausted available wall")
    api.ordinary(output.parent)
    if os.path.lexists(output):
        raise ValueError("official output must be vacant")
    output.mkdir(exist_ok=False)
    api.write_new(output/"CLAIM.json",{"manifest_sha256":args.manifest_sha,"approval_sha256":approval_sha,
                  "status":"CLAIMED_ONCE","supervisor_pid":os.getpid(),
                  "worker_deadline":absolute_deadline-reserve["controlled_stop_seconds"]},4096)
    command = [sys._base_executable,"-I","-S","-B",str(Path(__file__).absolute()),"--manifest-sha",args.manifest_sha,
               "--approval",str(Path(args.approval).absolute()),"--worker"]
    child, reason = None, None
    try:
        child = subprocess.Popen(command,cwd=api.ROOT,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
        child.wait(timeout=max(0,absolute_deadline-time.monotonic()))
    except (subprocess.TimeoutExpired, KeyboardInterrupt, OSError) as err:
        reason = type(err).__name__
        if child is not None and child.poll() is None:
            try:
                child.kill()
                child.wait(timeout=5)
            except (subprocess.TimeoutExpired,OSError):
                reason += ": worker exit unconfirmed"
    try:
        summary = api.read(output/"SUMMARY.json")
    except (OSError, ValueError):
        summary = {}
    counted = manifest["preparation_accounting"]
    worker_cpu = summary.get("worker_cpu_seconds")
    supervisor_cpu = time.process_time()
    wall = time.monotonic()-began_wall
    cpu = counted["charged_cpu_seconds"]+supervisor_cpu+worker_cpu if type(worker_cpu) in (int,float) else None
    bytes_used = counted["new_bundle_bytes"]+sum(p.stat().st_size for p in output.iterdir())
    success = (reason is None and child is not None and child.returncode == 0
               and summary.get("status") in ("SEPARATOR_VERIFIED","EXHAUSTED_NO_SEPARATOR")
               and cpu is not None and cpu+2<=limit["cpu_seconds"]
               and counted["charged_cpu_seconds"]+supervisor_cpu+2<=reserve["preparation_startup_cpu_seconds"]
               and counted["charged_wall_seconds"]+wall+2<=limit["wall_seconds"]
               and summary["traced_peak_bytes"]<=limit["traced_worker_bytes"]
               and summary["peak_candidate_states"]<=limit["live_candidate_states"]
               and all(summary["counts"][name]<=limit[name] for name in summary["counts"])
               and bytes_used+reserve["supervision_record_bytes"]<=limit["evidence_bytes"])
    receipt = {"status":summary["status"] if success else "INCOMPLETE",
               "reason":None if success else reason or summary.get("reason") or "missing or out-of-envelope worker receipt",
               "worker_rc":child.returncode if child is not None else None,"worker_summary":bool(summary),
               "worker_cpu_seconds":worker_cpu,"supervisor_cpu_seconds":supervisor_cpu,
               "preparation_cpu_charged":counted["charged_cpu_seconds"],
               "preparation_wall_charged":counted["charged_wall_seconds"],
               "combined_cpu_seconds":cpu,"combined_wall_before_receipt":counted["charged_wall_seconds"]+wall,
               "worker_and_supervisor_wall":wall,"bytes_before_receipt":bytes_used}
    api.write_new(output/"SUPERVISION.json",receipt,reserve["supervision_record_bytes"])
    return int(not success)


def main():
    began_wall = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-sha",required=True)
    parser.add_argument("--approval",required=True)
    parser.add_argument("--worker",action="store_true",help=argparse.SUPPRESS)
    args = parser.parse_args()
    api = runtime()
    manifest, config, output, approval_sha = gate(api,args)
    if args.worker:
        return worker(api,manifest,config,output,approval_sha,args)
    return supervise(api,manifest,config,output,approval_sha,args,began_wall)


if __name__ == "__main__":
    raise SystemExit(main())
