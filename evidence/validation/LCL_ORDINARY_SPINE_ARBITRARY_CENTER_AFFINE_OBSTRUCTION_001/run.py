"""Verify the two archived D133 seeds and four declared controls only."""

from time import process_time

CPU_START = process_time()

from hashlib import sha256
import json
from pathlib import Path
import sys
import traceback

import audit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from lcl.verify import verify_certificate


def read_json(path):
    return json.loads(path.read_bytes())


def digest_file(path):
    return sha256(path.read_bytes()).hexdigest()


def write_record(name, data, limits):
    raw = (json.dumps(data, sort_keys=True, indent=2) + "\n").encode()
    total = sum(path.stat().st_size for path in HERE.iterdir() if path.is_file())
    if len(raw) > limits["bytes_per_record"] or total + len(raw) > limits["bytes_total"]:
        raise ValueError("Evidence size cap exceeded")
    with (HERE / name).open("xb") as output:
        output.write(raw)
    return sha256(raw).hexdigest()


def check_member(manifest, path, pinned_hash):
    matches = [member for member in manifest["files"] if member["path"] == path.name]
    assert len(matches) == 1 and matches[0]["bytes"] == path.stat().st_size
    assert digest_file(path) == matches[0]["sha256"] == pinned_hash


def open_archive(binding):
    path = ROOT / binding["manifest"]
    assert digest_file(path) == binding["manifest_sha256"]
    manifest = read_json(path)
    result_path = path.with_name("result.json")
    check_member(manifest, result_path, binding["result_sha256"])
    result = read_json(result_path)
    assert manifest["task"] == result["task"] == binding["task"] and result["status"] == "PASS"
    return path.parent, manifest, result


def check_nonalpha(archive, binding):
    _, manifest, result = open_archive(archive)
    assert manifest["executable_status"] == "PASS" and manifest["proof_disposition"] == "ACCEPT"
    assert manifest["state_disposition"] == result["state_disposition"] == "REJECT"
    scope = manifest["alpha_scope"]
    assert scope == result["alpha_scope"]
    assert scope["alpha_labeling"] == scope["cut_9"] == "EXCLUDED"
    assert scope["cut_5"] == "EXCLUDED_BY_COMPLEMENT"
    assert scope["graph_digest"] == manifest["target_graph_digest"] == binding["graph_digest"]
    assert scope["original_sha256"] == result["target_original_sha256"] == binding["raw_sha256"]
    assert result["target_original"] == binding["original_path"]
    proof = archive["proof"]
    assert manifest["repository_input_hashes"][proof["path"]] == proof["sha256"]
    assert digest_file(ROOT / proof["path"]) == proof["sha256"]
    return {"binding": archive, "disposition_scope": scope, "historical_alpha_procedure_replayed": False}


def retained_seed(name, binding, archives, counts):
    folder, manifest, result = open_archive(binding)
    assert manifest["executable_status"] == "PASS"
    proof = binding["proof"]
    assert digest_file(ROOT / proof["path"]) == proof["sha256"]
    original_path = ROOT / binding["original_path"]
    if name == "D105":
        owner, original_manifest, owner_result = open_archive(archives["D099"])
        assert original_path == owner / "original.json"
        check_member(original_manifest, original_path, binding["raw_sha256"])
        assert manifest["proof_disposition"] == manifest["state_disposition"] == "ACCEPT"
        assert manifest["repository_input_hashes"][proof["path"]] == proof["sha256"]
        assert manifest["repository_input_hashes"][binding["original_path"]] == binding["raw_sha256"]
        assert manifest["repository_input_hashes"][archives["D099"]["manifest"]] == archives["D099"]["manifest_sha256"]
        assert owner_result["target_original_sha256"] == result["target_original_sha256"] == binding["raw_sha256"]
        assert result["target_original"] == binding["original_path"]
        assert result["target_graph_digest"] == manifest["target_graph_digest"] == binding["graph_digest"]
        assert manifest["certificate_ledger_id"] == binding["ledger_id"]
    else:
        assert name == "D130" and original_path == folder / "original.json"
        assert manifest["scientific_disposition"] == "ACCEPT" and manifest["proof"] == proof
        check_member(manifest, original_path, binding["raw_sha256"])
        expected = {"path": original_path.name, "raw_sha256": binding["raw_sha256"],
                    "graph_digest": binding["graph_digest"], "profile": binding["profile"]}
        assert manifest["originals"]["positive"] == result["originals"]["positive"] == expected
        assert manifest["ledger_id"] == binding["ledger_id"]
    original = read_json(original_path)
    graph, digest = original["graph"], original["graph_digest"]
    cert = result["certificate"]
    assert graph["profile"] == binding["profile"]
    assert cert["kind"] == "ordinary_graceful" and cert["graph_digest"] == digest == binding["graph_digest"]
    assert cert["ledger_id"] == binding["ledger_id"]
    counts["retained_positive_rechecks"] += 1
    checker = verify_certificate(graph, cert["labels"], digest)
    assert checker["valid"] and checker == cert["checker"]
    independent = audit.inspect_seed(original, binding, cert, checker)
    report = {"binding": binding, "checker": checker, "independent": independent}
    return graph, cert, report


def inspect_D131(binding, cfg, counts):
    _, manifest, result = open_archive(binding)
    counts["D131_binding_inspections"] += 1
    proof = binding["proof"]
    assert manifest["scientific_disposition"] == "ACCEPT" and manifest["executable_status"] == "PASS"
    assert manifest["proof"] == proof and digest_file(ROOT / proof["path"]) == proof["sha256"]
    assert manifest["retained_seeds"] == cfg["retained_seeds"]
    assert manifest["retained_archives"] == cfg["archives"]
    assert manifest["result_sha256"] == binding["result_sha256"]
    assert set(result["retained_seeds"]) == {"D105", "D130"}
    for name, prior in result["retained_seeds"].items():
        assert prior["binding"] == cfg["retained_seeds"][name]
        assert prior["independent"]["deficit_state"]["claimed_deficit"] == 0
        assert prior["checker"]["valid"]
    return result


def inspect_D132(binding, cfg, counts):
    _, manifest, result = open_archive(binding)
    counts["D132_binding_inspections"] += 1
    proof = binding["proof"]
    assert manifest["scientific_disposition"] == "ACCEPT" and manifest["executable_status"] == "PASS"
    assert manifest["proof"] == proof and digest_file(ROOT / proof["path"]) == proof["sha256"]
    assert manifest["result_sha256"] == binding["result_sha256"]
    assert manifest["retained_seeds"] == cfg["retained_seeds"]
    assert manifest["retained_archives"] == cfg["archives"]
    assert manifest["retained_D131"] == result["D131_binding"] == cfg["retained_D131"]
    assert set(result["retained_seeds"]) == {"D105", "D130"}
    for name, prior in result["retained_seeds"].items():
        assert prior["binding"] == cfg["retained_seeds"][name]
        assert prior["independent"]["deficit_state"]["claimed_deficit"] == 0
        assert prior["checker"]["valid"]
    return result


def run_controls(seed_data, counts):
    graph, certificate, _ = seed_data["D105"]
    counts["declared_controls"] += 1
    wrong = "0" * 64
    identity = verify_certificate(graph, certificate["labels"], wrong)
    assert wrong != certificate["graph_digest"]
    assert not identity["valid"] and identity["errors"] == ["original graph digest mismatch"]
    assert identity["edge_differences"] == certificate["checker"]["edge_differences"]

    symbolic = audit.symbolic_checks()
    structural = ("equality_boundary", "intermediate_host", "two_center_specialization")
    controls = {name: symbolic[name] for name in structural}
    counts["declared_controls"] += len(controls)
    controls["wrong_digest"] = {"expected_digest": wrong, "checker": identity}
    return controls, symbolic


def validate_inputs(cfg):
    pre = read_json(HERE / "preflight_receipt.json")
    supervisor = read_json(HERE / "preflight_supervision.json")
    assert pre["status"] == supervisor["status"] == "PASS"
    assert pre["task"] == supervisor["task"] == cfg["task"] and pre["parent"] == cfg["parent"]
    assert supervisor["receipt_sha256"] == digest_file(HERE / "preflight_receipt.json")
    assert supervisor["config_sha256"] == digest_file(HERE / "config.json")
    assert pre["preflights"] == 1 and pre["task_module_imports"] == 0
    assert pre["input_hashes"] == {name: digest_file(HERE / name) for name in cfg["preflight_inputs"]}
    assert pre["retained_inputs"] == cfg["retained_inputs"]
    assert pre["runtime"]["sha256"] == cfg["runtime_sha256"] == digest_file(Path(sys.executable))
    for path, expected in cfg["source_hashes"].items():
        assert digest_file(ROOT / path) == expected, path
    return pre


def produce(cfg, counts):
    pre = validate_inputs(cfg)
    history = {key: read_json(ROOT / path)["status"] for key, path in cfg["status_receipts"].items()}
    assert history == cfg["expected_statuses"]
    prior_d131 = inspect_D131(cfg["retained_D131"], cfg, counts)
    prior_d132 = inspect_D132(cfg["retained_D132"], cfg, counts)
    seeds = {name: retained_seed(name, cfg["retained_seeds"][name], cfg["archives"], counts)
             for name in ("D105", "D130")}
    for name, data in seeds.items():
        assert data[2] == prior_d131["retained_seeds"][name] == prior_d132["retained_seeds"][name]
    alpha = check_nonalpha(cfg["archives"]["D104"], cfg["retained_seeds"]["D105"])
    counts["D104_binding_inspections"] += 1
    assert alpha == prior_d131["D104_alpha_disposition"] == prior_d132["D104_alpha_disposition"]
    assert not seeds["D105"][2]["independent"]["certificate_has_alpha_separation"]
    controls, symbolic = run_controls(seeds, counts)
    counts["symbolic_theorems"] += 1
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "scope": cfg["scope"],
            "runtime": pre["runtime"], "retained_seeds": {name: data[2] for name, data in seeds.items()},
            "D131_binding": cfg["retained_D131"], "D132_binding": cfg["retained_D132"],
            "D104_alpha_disposition": alpha, "controls": controls, "formal_arithmetic": symbolic,
            "retained_execution_statuses": history}


def execute():
    cfg = read_json(HERE / "config.json")
    limits = cfg["limits"]
    counts = dict.fromkeys(cfg["count_keys"], 0)
    counts.update(workers=1, official_invocations=1, preflights=1)
    receipt = {"status": "INCOMPLETE", "task": cfg["task"], "parent": cfg["parent"], "argv": sys.orig_argv,
               "counts": counts, "limits": limits}
    try:
        assert __debug__ and sys.dont_write_bytecode
        assert all(not (HERE / name).exists() for name in ("result.json", "command_receipt.json", "__pycache__"))
        bound_names = (*cfg["preflight_inputs"], "preflight_receipt.json", "preflight_supervision.json")
        receipt["input_hashes"] = {name: digest_file(HERE / name) for name in bound_names}
        result = produce(cfg, counts)
        assert all(value == limits[key] for key, value in counts.items())
        receipt["result_sha256"] = write_record("result.json", result, limits)
        prior_cpu = read_json(HERE / "preflight_receipt.json")["process_cpu_seconds"]
        if prior_cpu + process_time() - CPU_START >= limits["process_cpu_seconds"]:
            raise TimeoutError("Combined process CPU limit reached")
        receipt["status"] = "PASS"
    except (Exception, KeyboardInterrupt):
        receipt["error"] = traceback.format_exc()
    receipt["process_cpu_seconds"] = process_time() - CPU_START
    write_record("command_receipt.json", receipt, limits)
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(execute())
