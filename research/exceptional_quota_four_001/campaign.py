"""Future D161 authorization gate and supervised matched execution. Preparation must not run it."""
import argparse
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import time
import types


def bindings():
    path = Path(__file__).absolute().with_name("bindings.py")
    api = types.ModuleType("d161_campaign_bindings")
    api.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), "exec"), vars(api))
    return api


def relative(name):
    path = PurePosixPath(name)
    if (path.is_absolute() or name != path.as_posix() or "\\" in name or ":" in name
            or not path.parts or ".." in path.parts):
        raise ValueError("unsafe manifest path")
    return path


def gate(api,args):
    manifest_path = api.ordinary(api.EVIDENCE/"MANIFEST.json")
    raw_manifest = manifest_path.read_bytes()
    if api.sha(raw_manifest)!=args.manifest_sha:
        raise ValueError("approved manifest SHA mismatch")
    manifest = api.read(manifest_path)
    if (manifest["task"]!=api.TASK or manifest["status"]!="FROZEN_PREPARATION_ONLY"
            or manifest["parent"]!=api.read(api.KIT/"config.json")["base"]):
        raise ValueError("wrong task or preparation freeze")
    members = {}
    for item in manifest["files"]:
        name = item["path"]
        path = api.ordinary(api.ROOT/relative(name))
        if (name.casefold() in members or path.stat().st_size!=item["bytes"]
                or api.sha(path.read_bytes())!=item["sha256"]):
            raise ValueError("frozen member identity: "+name)
        members[name.casefold()] = item
    state = api.ordinary(api.ROOT/"STATE.md").read_bytes().replace(b"\r\n",b"\n")
    if api.sha(state)!=manifest["canonical_state_sha256"]:
        raise ValueError("prepared STATE identity")
    config = api.read(api.KIT/"config.json")
    runtime = api.exact_runtime(config,base_process=args.worker)
    preflight = api.read(api.EVIDENCE/"PREFLIGHT.json")
    preparation = api.read(api.EVIDENCE/"PREPARATION_SUPERVISION.json")
    paths = {p.relative_to(api.ROOT).as_posix() for p in
             (*api.KIT.iterdir(),*(api.EVIDENCE/"input").iterdir())}|set(config["retained_sha256"])
    required = paths|{(api.EVIDENCE/name).relative_to(api.ROOT).as_posix() for name in
                      ("PREFLIGHT.json","PREPARATION_SUPERVISION.json","REVIEWS.md")}
    if not {name.casefold() for name in required}<=members.keys():
        raise ValueError("missing reviewed freeze member")
    if (preflight["status"]!="PASS_PARSE_ONLY" or preflight["count"]!=99
            or preflight["runtime"]!=runtime or preflight["python_version"]!=config["python_version"]
            or any(not preflight[k] for k in ("no_task_imports","no_task_bytecode","isolated","no_site",
                                              "approval_vacant","official_outputs_vacant"))
            or len(preflight["files"])!=len(paths) or {r["path"] for r in preflight["files"]}!=paths
            or any(members.get(r["path"].casefold())!=r for r in preflight["files"])
            or set(preflight["definitions"])!={p.name for p in api.KIT.glob("*.py")}
            or any(len(names)!=len(set(names)) for names in preflight["definitions"].values())):
        raise ValueError("parse-only receipt binding")
    for name,digest in config["retained_sha256"].items():
        if members[name.casefold()]["sha256"]!=digest:
            raise ValueError("retained source binding")
    if (preparation["status"]!="PASS" or [r["phase"] for r in preparation["phases"]]!=["corpus","preflight"]
            or any(r["exit_code"]!=0 or r["timeout"] for r in preparation["phases"])
            or not 0<=preparation["cpu_seconds"]<=config["preparation"]["cpu_seconds"]
            or not 0<=preparation["wall_seconds"]<=config["preparation"]["wall_seconds"]
            or config["task"]!=api.TASK or config["limits"]["workers"]!=1):
        raise ValueError("measured preparation or task binding")
    approval = api.ordinary(Path(args.approval).absolute())
    if approval!=api.ordinary(api.ROOT/config["approval"]) or approval.stat().st_size>4096:
        raise ValueError("unapproved authority path")
    raw_approval = approval.read_bytes()
    if api.read(approval)!={"task":api.TASK,"manifest_sha256":args.manifest_sha,
                           "status":"AUTHORIZED_FOR_OFFICIAL_RUN"}:
        raise ValueError("later Owner approval record required")
    frozen = len(raw_manifest)+len(raw_approval)+sum(item["bytes"] for item in members.values())
    if frozen+config["reserve"]["final_records_bytes"]+4096>config["limits"]["evidence_bytes"]:
        raise ValueError("initial evidence reservation")
    return config,api.ordinary(api.ROOT/config["output"]),frozen,preparation,api.sha(raw_approval)


def corpus(api):
    root = api.EVIDENCE/"input"
    index = api.read(root/"corpus_index.json")["targets"]
    if len(index)!=99:
        raise ValueError("frozen corpus count")
    for start in range(0,99,12):
        entries = index[start:start+12]
        shard = api.read(root/entries[0]["shard"])
        for row,entry in zip(shard,entries,strict=True):
            if (api.sha(api.encoded(row))!=entry["record_sha256"]
                    or {k:v for k,v in row.items() if k!="graph"}!=
                       {k:v for k,v in entry.items() if k!="record_sha256"}):
                raise ValueError("frozen original binding")
            yield row


def disposition(row,prefix,arm,meter,primary,audit,retained,check):
    meter.tick("dispositions")
    start = dict(meter.counts)
    symbol = ("T2_2_PHYSICAL_COUNT" if row["T2"]==2 else
              "T2_4_NO_EXTERIOR_TERMINALS" if arm=="E+" and row["T2"]==4 else None)
    if symbol:
        result = {"claim":"NO","basis":symbol}
        audited = {"status":"SYMBOLIC_QUALIFICATION","original":audit.original_context(row,prefix,retained)[0]}
    else:
        result = primary.search(row,prefix,arm,meter)
        if result["claim"]=="YES":
            audited = audit.positive(row,prefix,arm,result["solution"],meter,retained,check)
        else:
            audited = audit.negative(row,prefix,arm,meter,retained)
            if result["basis"]!=audited["basis"]:
                raise ValueError("audit disagrees on candidate-existence category")
    meter.time_check()
    return {"target":row["id"],"digest":row["digest"],"arm":arm,"K":row["K"],
            "parameters":row["parameters"],"raw_exterior":"PRESENT_SYMBOLIC_D160",
            "result":result,"audit":audited,
            "meter_delta":{key:val-start[key] for key,val in meter.counts.items()}}


def worker(api,args,config,output,frozen,approval_hash):
    if ({p.name for p in output.iterdir()}!={"CLAIM.json"} or
            api.read(output/"CLAIM.json")!={"manifest_sha256":args.manifest_sha,
                                             "approval_sha256":approval_hash,"status":"CLAIMED_ONCE"}):
        raise ValueError("worker exclusive claim")
    with (output/"WORKER").open("xb") as stream:
        stream.write(b"D161 one worker\n")
    retained_campaign = api.load_exact("d161_retained_meter",api.LEGACY/"campaign.py")
    meter = retained_campaign.Meter(config,output,frozen+sum(p.stat().st_size for p in output.iterdir()))
    active,arm,reason = None,None,None
    paired,separating,completed = 0,0,0
    try:
        primary = api.load_exact("d161_primary",api.KIT/"primary.py")
        audit = api.load_exact("d161_audit",api.KIT/"audit.py")
        retained = api.load_exact("d161_retained_original",api.LEGACY/"audit.py")
        check = api.load_exact("d161_original_checker",api.ROOT/"lcl/verify.py").verify_certificate
        prefix = api.read(api.EVIDENCE/"input/prefix.json")
        _,_,prefix_digest = retained.original(prefix["graph"])
        if (prefix_digest!=prefix["digest"] or prefix["n"]!=74 or prefix["actual_cut"]!=39
                or prefix["polarity"]!="maximum" or prefix["actual_labels"][prefix["frontier"]]!=74
                or not check(prefix["graph"],prefix["actual_labels"],expected_graph_digest=prefix_digest)["valid"]):
            raise ValueError("official prefix binding")
        for row in corpus(api):
            active = row["id"]
            meter.tick("targets")
            arms = {}
            for arm in ("T","E+"):
                record = disposition(row,prefix,arm,meter,primary,audit,retained,check)
                meter.write(active+"-"+arm.replace("+","plus")+".json",record)
                completed += 1
                arms[arm] = record["result"]["claim"]
            derived_E = "YES" if "YES" in arms.values() else "NO"
            separated = arms=={"T":"NO","E+":"YES"}
            meter.write(active+"-PAIR.json",{"target":active,"graph_digest":row["digest"],"arms":arms,
                                              "E":derived_E,"separating":separated})
            paired += 1
            separating += int(separated)
            active,arm = None,None
        if (paired,completed)!=(99,198):
            raise ValueError("incomplete official coverage")
        meter.time_check()
    except retained_campaign.Limit as error:
        reason = f"LIMIT: {error}"[:300]
    except Exception as error:
        reason = f"{type(error).__name__}: {error}"[:300]
    scientific = "SUPPORTED" if separating else "FALSIFIED_FINITE" if reason is None else "UNDECIDED"
    summary = {"status":"COMPLETE" if reason is None else "INCOMPLETE","reason":reason,
               "active_target":active,"active_arm":arm,"entered":meter.counts,"completed_arms":completed,
               "paired_audits":paired,"separating":separating,"finite_hypothesis":scientific,
               "cpu_seconds":time.process_time(),"bytes_before_summary":meter.bytes}
    meter.write("SUMMARY.json",summary,emergency=True)
    return int(reason is not None)


def supervise(api, args, config, output, preparation, approval_hash, started):
    if os.path.lexists(output):
        raise ValueError("official output must be vacant")
    output.mkdir()
    api.write_new(output/"CLAIM.json", {"manifest_sha256":args.manifest_sha, "approval_sha256":approval_hash,
                                        "status":"CLAIMED_ONCE"}, 4096)
    command = [sys._base_executable, "-I", "-S", "-B", str(Path(__file__).absolute()),
               "--manifest-sha", args.manifest_sha, "--approval", str(Path(args.approval).absolute()), "--worker"]
    wall_limit = config["limits"]["wall_seconds"]-config["reserve"]["preparation_and_startup_wall_seconds"]
    process, reason = None, None
    try:
        process = subprocess.Popen(command, cwd=api.ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        process.wait(timeout=max(0, wall_limit-(time.monotonic()-started)))
    except (subprocess.TimeoutExpired, KeyboardInterrupt, OSError) as error:
        reason = type(error).__name__
    if reason and process is not None and process.poll() is None:
        try:
            process.kill()
            process.wait(timeout=5)
        except (subprocess.TimeoutExpired, OSError):
            reason += ": worker exit unconfirmed"
    try:
        summary = api.read(output/"SUMMARY.json")
    except (OSError, ValueError):
        summary = {}
        reason = reason or "worker summary unavailable"
    worker_cpu = summary.get("cpu_seconds")
    supervisor_cpu = time.process_time()
    wall = time.monotonic()-started
    cpu = (preparation["cpu_seconds"]+supervisor_cpu+worker_cpu
           if type(worker_cpu) in (int, float) and worker_cpu >= 0 else None)
    combined_wall = preparation["wall_seconds"]+wall
    status = ("COMPLETE" if reason is None and process is not None and process.returncode == 0
              and summary.get("status") == "COMPLETE" and cpu is not None and cpu+1 <= config["limits"]["cpu_seconds"]
              and combined_wall+1 <= config["limits"]["wall_seconds"] and wall <= wall_limit else "INCOMPLETE")
    api.write_new(output/"SUPERVISION.json",
                  {"status":status, "reason":reason or (None if status == "COMPLETE" else "worker or combined cap"),
                   "worker_pid":process.pid if process is not None else None,
                   "worker_exit":process.returncode if process is not None else None, "worker_cpu":worker_cpu,
                   "supervisor_cpu":supervisor_cpu, "combined_cpu":cpu, "combined_observed_wall":combined_wall}, 8192)
    return int(status != "COMPLETE")


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-sha", required=True)
    parser.add_argument("--approval", required=True)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    api = bindings()
    config, output, frozen, preparation, approval_hash = gate(api, args)
    if args.worker:
        code = worker(api, args, config, output, frozen, approval_hash)
    else:
        code = supervise(api, args, config, output, preparation, approval_hash, started)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
