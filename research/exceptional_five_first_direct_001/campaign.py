
"""Future D174 official entry point. Preparation uses the separate parse-only script."""
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
    mod = types.ModuleType("d174_runtime")
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
                api.KIT/"runtime.py",api.EVIDENCE/"input/corpus_index.json",api.EVIDENCE/"PREFLIGHT.json",
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
    if (preflight["status"] != "PASS_PARSE_ONLY" or preflight["population"]!=config["domain"]["originals"]
            or preflight["numerical_work"] != 0 or preflight["task_module_imports"] != 0
            or measured["charged_cpu_seconds"] > config["preparation"]["cpu_seconds"]
            or measured["charged_wall_seconds"] > config["preparation"]["wall_seconds"]
            or measured["charged_cpu_seconds"] >= reserve["preparation_startup_cpu_seconds"]
            or measured["charged_wall_seconds"] >= reserve["preparation_startup_wall_seconds"]
            or execution["workers"] != 1
            or (measured["new_bundle_bytes"] > config["preparation"]["bytes"])):
        raise ValueError("preparation gate not satisfied")
    return manifest, config, api.repo_path(config["output"]), api.sha(approval_raw)



def original_rows(api, config, index):
    last_shard, shard = None, {}
    source = api.EVIDENCE/"input"
    entries = {e["id"]:e for e in index["targets"]}
    order = index["execution_order"]
    if len(order)!=config["domain"]["originals"] or len(order)!=len(set(order)) or set(order)!=entries.keys():
        raise ValueError("frozen named population or order")
    for name in order:
        entry=entries[name]
        if entry["shard"] != last_shard:
            last_shard = entry["shard"]
            if Path(last_shard).name != last_shard or not last_shard.startswith("targets-"):
                raise ValueError("invalid retained shard identity")
            shard = {item["id"]:item for item in api.read(source/last_shard)}
        row = shard[name]
        if (api.sha(api.encoded(row)) != entry["record_sha256"]
                or {k:v for k,v in row.items() if k!="graph"} != {k:v for k,v in entry.items() if k!="record_sha256"}):
            raise ValueError("original canonical record binding")
        yield row, entry


def disposition(row, entry, prefix, arm, meter, primary, audit, folded, independent_graph, checker):
    before = dict(meter.counts)
    meter.arm_start_counts = before
    meter.phase = f"{arm} admission"
    meter.tick("dispositions")
    meter.tick("numerical_dispositions")
    result = primary.solve(row,prefix,arm,meter,folded)
    if result["claim"] == "YES":
        proof = audit.positive(row,prefix,arm,result["solution"],meter,independent_graph,checker)
    else:
        proof = audit.negative(row,prefix,arm,meter,independent_graph)
        if any(result["counts"][k]!=proof["counts"][k] for k in ("qualified_exteriors","qualified_strata")):
            raise ValueError("primary and independent exterior accounting differ")
    meter.time_check()
    return {"id":row["id"],"digest":row["digest"],"record_sha256":entry["record_sha256"],
            "prefix_digest":prefix["digest"],"ordered_parameters":row["parameters"],"arm":arm,
            "raw_exterior":"SYMBOLIC_PRESENT","result":result,"audit":proof,
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
        folded = api.load_source("d174_bound_folded",api.repo_path(config["folded_source"]))
        primary = api.load_source("d174_primary",api.KIT/"primary.py")
        audit = api.load_source("d174_audit",api.KIT/"audit.py")
        graph = api.load_source("d174_original",api.repo_path(config["independent_graph"]))
        checker = api.load_source("d174_checker",api.ROOT/"lcl/verify.py").verify_certificate
        prefix = api.read(api.repo_path(config["prefix"]))
        if (prefix["n"],prefix["frontier"],prefix["actual_cut"],prefix["polarity"]) != (74,"s:27",39,"maximum"):
            raise ValueError("independent prefix identity")
        if prefix["digest"]!=config["prefix_digest"] or not checker(
                prefix["graph"],prefix["actual_labels"],expected_graph_digest=prefix["digest"])["valid"]:
            raise ValueError("independent prefix confirmation")

        index = api.read(api.EVIDENCE/"input/corpus_index.json")
        required = config["domain"]["originals"]
        if index["count"]!=required or index["all_even"]!=config["domain"]["all_even"]:
            raise ValueError("frozen census")
        for row, entry in original_rows(api,config,index):
            active, active_arm = row["id"], "H0"
            meter.phase = "target admission"
            meter.tick("targets")
            H0 = disposition(row,entry,prefix,"H0",meter,primary,audit,folded,graph,checker)
            meter.write(active+"-H0.json",H0)
            meter.candidate = None
            active_arm = "H1"
            if H0["result"]["claim"] == "YES":
                meter.phase = "H1 skipped after verified H0 YES"
                meter.arm_start_counts = dict(meter.counts)
                meter.tick("dispositions")
                H1 = {"id":active,"digest":row["digest"],"record_sha256":entry["record_sha256"],
                      "prefix_digest":prefix["digest"],"arm":"H1",
                      "result":{"claim":"NOT_REQUIRED_FOR_SEPARATOR","basis":"VERIFIED_H0_YES"}}
            else:
                H1 = disposition(row,entry,prefix,"H1",meter,primary,audit,folded,graph,checker)
            meter.write(active+"-H1.json",H1)
            claims = {r["arm"]:r["result"]["claim"] for r in (H0,H1)}
            separating = claims == {"H0":"NO","H1":"YES"}
            witness = None
            if separating:
                struct = H1["audit"]["exterior_structure"]
                witness = {"target":active,"original_digest":row["digest"],"prefix_digest":prefix["digest"],
                           "ordered_parameters":row["parameters"],"record_sha256":entry["record_sha256"],
                           "arm_files":[active+"-H0.json",active+"-H1.json"],
                           "arm_sha256":[api.sha(api.encoded(r)) for r in (H0,H1)],
                           "H0_negative":H0["result"],"H0_audit":H0["audit"],"H1_structure":struct,
                           "H1_reduced_roles":H1["audit"]["reduced"],"H1_gap_quotas":H1["audit"]["gap_quotas"],
                           "comparison":{"direct_leaf":struct["direct_leaf"],"H0_placement":"gap",
                                         "H0_direct_quota":1,"H1_placement":"exterior",
                                         "H1_direct_quota":0,
                                         "H1_direct_reduced":H1["audit"]["reduced"][struct["direct_leaf"]],
                                         "width_change_at_fixed_terminal_counts":"B increases by one; A stays fixed",
                                         "comparison_scope":"H0 has no completing exterior in its audited domain."},
                           "resources":H1["audit"]["resources"],"label_sides":H1["audit"]["label_side_partitions"],
                           "connector":H1["audit"]["connector"],"return_phase":H1["audit"]["return_phase"]}
            meter.write(active+"-PAIR.json",{"id":active,"digest":row["digest"],"prefix_digest":prefix["digest"],
                                            "claims":claims,"separating":separating,"separator":witness})
            completed += 1
            blocked += claims["H0"]=="YES"
            a_no += claims["H1"]=="NO"
            meter.time_check()
            if separating:
                separator = active
                break
            active, active_arm = None, None
        if separator is None and (completed,blocked+a_no)!=(required,required):
            raise ValueError("attempt to conclude from incomplete coverage")
    except (Exception, KeyboardInterrupt) as err:
        reason = f"{type(err).__name__}: {err}"[:512]
    if reason:
        status = "INCOMPLETE"
    else:
        status = "SEPARATOR_VERIFIED" if separator else "EXHAUSTED_NO_SEPARATOR"
    summary = {"status":status,"reason":reason,"separator":separator,"current_target":active,"current_arm":active_arm,
               "pairs_completed":completed,"disqualified_by_H0_positive":blocked,"disqualified_by_H1_negative":a_no,
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
