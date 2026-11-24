"""Retained-only verification of the D125 dispatch and its r=2 identity."""

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


def dispatch(q, a, c, r):
    quotas = (q, a, c)
    if any(type(value) is not int for value in (*quotas, r)) or min(quotas) < 0 or r < 2:
        return {"status": "INVALID_INPUT"}
    even = [i for i, quota in enumerate(quotas) if quota % 2 == 0]
    if not even and q >= 5 and a >= 3 and c >= 3:
        return {"status": "COVERED", "sector": "I", "supplier": "D120"}
    if len(even) == 1 and quotas[even[0]] >= 2:
        odd = [i for i in range(3) if i != even[0]]
        qualifying = [i for i in odd if quotas[i] >= 5]
        if all(quotas[i] >= 3 for i in odd) and qualifying:
            high = min(qualifying)
            lower = next(i for i in odd if i != high)
            roles = [high, lower, even[0]]
            return {"status": "COVERED", "sector": "II", "role_indices_H_L_C": roles,
                    "supplier": "D119" if roles == [0, 1, 2] else "D121",
                    "D118_pointwise_specialization": roles == [0, 1, 2] and c == 2}
    if even == [0, 2] and q >= 6 and a >= 3 and c >= 2:
        if a == 3 and c >= 6:
            return {"status": "COVERED", "sector": "III", "supplier": "D123" if q == c else "D124",
                    "alternative": "D122" if c <= q-4 else None}
        if a >= 5 or c <= q-4:
            return {"status": "COVERED", "sector": "III", "supplier": "D122",
                    "branch": "II" if a >= 5 else "I"}
    if len(even) == 3:
        return {"status": "FIXED_INTERFACE_OBSTRUCTION", "basis": "all-even excess-degree parity"}
    return {"status": "OUTSIDE_ESTABLISHED_COVERAGE"}


def read_json(path):
    return json.loads(path.read_bytes())


def digest_file(path):
    return sha256(path.read_bytes()).hexdigest()


def write_record(name, payload, limits):
    raw = (json.dumps(payload, sort_keys=True, indent=2)+"\n").encode("utf-8")
    existing = sum(path.stat().st_size for path in HERE.iterdir() if path.is_file())
    if len(raw) > limits["bytes_per_record"] or existing+len(raw) > limits["bytes_total"]:
        raise ValueError("Evidence size cap exceeded")
    with (HERE / name).open("xb") as output:
        output.write(raw)
    return sha256(raw).hexdigest()


def check_member(manifest, path, pinned_hash):
    rows = [row for row in manifest["files"] if row["path"] == path.name]
    assert len(rows) == 1
    assert rows[0]["bytes"] == path.stat().st_size
    assert rows[0]["sha256"] == digest_file(path) == pinned_hash


def open_archive(binding):
    manifest_path = ROOT / binding["manifest"]
    result_path = manifest_path.with_name("result.json")
    assert digest_file(manifest_path) == binding["manifest_sha256"]
    manifest = read_json(manifest_path)
    assert manifest["task"] == binding["task"] and manifest["executable_status"] == "PASS"
    assert manifest[binding["disposition_field"]] == "ACCEPT"
    check_member(manifest, result_path, binding["result_sha256"])
    result = read_json(result_path)
    assert result["status"] == "PASS" and result["task"] == binding["task"]
    return manifest_path.parent, manifest, result


def identity_binding(actual_digest, certificate_metadata):
    claimed = certificate_metadata["graph_digest"]
    return {"valid": claimed == actual_digest, "actual_graph_digest": actual_digest,
            "certificate_graph_digest": claimed, "claimed_ledger_id": certificate_metadata["ledger_id"]}


def seed_size_admission(graph, labels, claimed_n):
    profile, actual_edges = graph["profile"], len(graph["edges"])
    profile_n = sum(profile[0])+7
    maximum = max(labels.values())
    tests = {"exact_integer": type(claimed_n) is int, "against_actual_edges": claimed_n == actual_edges,
             "against_profile": len(profile) == 2 and len(profile[0]) == 3 and profile[1] == [2]
             and claimed_n == profile_n,
             "against_maximum_label": claimed_n == maximum}
    return {"valid": all(tests.values()), "tests": tests, "claimed_n": claimed_n,
            "actual_edges": actual_edges, "profile_n": profile_n, "maximum_label": maximum}


def inspect_positive(binding, archive, counts):
    folder, manifest, result = archive
    variant = binding["variant"]
    if variant is None:
        source, original_record, ledger = result, manifest["original"], manifest["ledger_id"]
    else:
        source = result["positive"][variant]
        original_record, ledger = manifest["originals"][variant], manifest["positive_ledger_ids"][variant]
    assert original_record == source["original"] == binding["original_record"]
    original_path = folder / original_record["path"]
    check_member(manifest, original_path, original_record["raw_sha256"])
    original = read_json(original_path)
    graph, cert = original["graph"], source["certificate"]
    assert original["graph_digest"] == original_record["graph_digest"]
    structure = audit.inspect_original(original, binding["profile"])
    identity = identity_binding(structure["graph_digest"], cert)
    assert identity["valid"] and cert["ledger_id"] == ledger == binding["ledger_id"]
    assert cert["kind"] == "ordinary_graceful" and cert["physical_spine"] == graph["spine"]
    independent = audit.inspect_certificate(original, cert, structure)
    labels = cert["labels"]
    size = seed_size_admission(graph, labels, len(structure["edges"]))
    assert size["valid"]
    growth = audit.check_growth_premises(graph, labels, size["actual_edges"], structure)
    assert growth["valid"] and cert["physical_pins"]["actual"] == growth["pins"]
    counts["retained_positive_rechecks"] += 1
    checker = verify_certificate(graph, labels, structure["graph_digest"])
    assert checker["valid"] and checker == cert["checker"]
    assert checker["edge_differences"] == independent["edge_weights"]
    counts["retained_positive_dispatches"] += 1
    choice = dispatch(*graph["profile"][0], graph["profile"][1][0])
    assert choice == binding["expected_dispatch"]
    base = audit.check_base_specialization(graph, labels, size["actual_edges"], structure)
    report = {"source": binding, "manifest_verified": True, "identity": identity, "checker": checker,
              "seed_size": size, "D112_premises": growth, "independent": independent,
              "dispatch": choice, "r_equals_two": base}
    return original, cert, report


def inspect_D121(archive, d119_archive, d119, counts):
    _, manifest, result = archive
    _, _, d119_result = d119_archive
    original, cert, report = d119
    retained = result["retained_source"]
    assert retained == manifest["retained_certificates"]["D119"]
    original_record = report["source"]["original_record"]
    assert retained["graph_digest"] == original_record["graph_digest"]
    assert retained["original_sha256"] == original_record["raw_sha256"]
    assert retained["profile"] == original["graph"]["profile"]
    assert retained["ledger_id"] == cert["ledger_id"]
    assert retained["result_sha256"] == digest_file(d119_archive[0] / "result.json")
    assert ROOT / retained["original"] == d119_archive[0] / original_record["path"]
    assert ROOT / retained["result"] == d119_archive[0] / "result.json"
    binding, independent = result["binding"], result["independent"]
    assert binding["valid"] and binding["bijective"] and binding["quota_compatible"] and binding["slots_exact"]
    assert binding["indices"] == binding["inverse"] == independent["role_map"] == independent["inverse"] == [0, 1, 2]
    assert binding["actual_quotas"] == binding["requested_quotas"] == retained["profile"][0]
    for index, role in enumerate(("H", "L", "C")):
        row = binding["rows"][role]
        actual = [v for v, entry in original["graph"]["roles"].items()
                  if entry["kind"] == "leaf" and entry["section"] == 0 and entry["branch"] == index]
        assert row["center"] == f"b:0:{index}" and row["actual"] == row["requested"] == sorted(actual)
    assert result["pointwise_formula_agreement"] and result["checker"] == cert["checker"]
    assert result["core"] == d119_result["core"] and result["batches"] == d119_result["batches"]
    assert independent["scope"] == "identity_order_only"
    assert independent["graph_digest"] == retained["graph_digest"] and independent["ledger_id"] == retained["ledger_id"]
    assert independent["checked_original_edges"] == original["graph"]["edges"]
    assert set(independent["checked_names"]) == set(original["graph"]["vertices"])
    counts["retained_D121_inspections"] += 1
    return {"retained_source": retained, "identity_order": binding["indices"], "archived_agreement": True,
            "same_distinct_graph_as_D119": True, "extra_checker_recheck": False}


def inspect_D122_adverse(binding, archive, counts):
    folder, manifest, result = archive
    assert manifest["obstruction"] == result["obstruction"] == binding
    original_record = binding["original"]
    assert manifest["originals"]["adverse"] == original_record
    original_path = folder / original_record["path"]
    record_path = folder / binding["path"]
    check_member(manifest, original_path, original_record["raw_sha256"])
    check_member(manifest, record_path, binding["sha256"])
    original, record = read_json(original_path), read_json(record_path)
    assert record["original"] == original_record and record["certificates"] == 0
    assert record["status"] == "FIXED_CORE_INFEASIBLE" and record["scope"] == "all_completions_of_the_specified_labeled_core"
    structure = audit.inspect_original(original, original_record["profile"])
    assert record["graph_digest"] == structure["graph_digest"] == original_record["graph_digest"]
    core = record["core"]
    core_edges = [[v, w] for v, w in structure["edges"] if v in core and w in core]
    assert core_edges == record["core_edges"]
    assert [abs(core[v]-core[w]) for v, w in core_edges] == record["core_differences"]
    assert record["same_class_demand"] == 6 and record["available_parity_classes"] == {
        "even": [6, 8, 10, 12], "odd": [5, 7, 9, 11, 13]}
    counts["retained_adverse_inspections"] += 1
    return {"binding": binding, "status": record["status"], "scope": record["scope"],
            "certificates": record["certificates"], "archive_replayed": False}


def run_controls(positives, adverse, counts):
    original, cert, report = positives["D124"]
    graph, labels = original["graph"], cert["labels"]
    initial_identity = report["identity"]
    counts["declared_controls"] += 1
    wrong_digest = "0"*64
    rejected = verify_certificate(graph, labels, wrong_digest)
    assert not rejected["valid"] and rejected["errors"] == ["original graph digest mismatch"]
    assert rejected["graph_digest"] == initial_identity["actual_graph_digest"]
    assert rejected["edge_differences"] == report["independent"]["edge_weights"]

    counts["declared_controls"] += 1
    other_cert = positives["D123"][1]
    metadata = {key: other_cert[key] for key in ("graph_digest", "ledger_id")}
    wrong_binding = identity_binding(initial_identity["actual_graph_digest"], metadata)
    assert not wrong_binding["valid"]
    assert wrong_binding["certificate_graph_digest"] == positives["D123"][0]["graph_digest"]

    counts["declared_controls"] += 1
    profile = adverse["binding"]["original"]["profile"]
    assert profile == [[6, 3, 4], [2]]
    outside = dispatch(*profile[0], profile[1][0])
    assert outside == {"status": "OUTSIDE_ESTABLISHED_COVERAGE"}
    assert adverse["status"] == "FIXED_CORE_INFEASIBLE"

    counts["declared_controls"] += 1
    wrong_n = seed_size_admission(graph, labels, report["seed_size"]["actual_edges"]+1)
    assert not wrong_n["valid"] and wrong_n["claimed_n"] == 25
    assert wrong_n["actual_edges"] == wrong_n["profile_n"] == wrong_n["maximum_label"] == 24
    assert wrong_n["tests"] == {"exact_integer": True, "against_actual_edges": False,
                                "against_profile": False, "against_maximum_label": False}
    return {"wrong_expected_digest": {"expected": wrong_digest, "checker": rejected},
            "cross_bind_D123_to_D124": wrong_binding,
            "adverse_dispatch": {"profile": profile, "dispatch": outside, "retained_obstruction": adverse},
            "wrong_seed_size": wrong_n}


def validate_inputs(cfg):
    receipt_path = HERE / "preflight_receipt.json"
    receipt = read_json(receipt_path)
    supervised = read_json(HERE / "preflight_supervision.json")
    assert receipt["status"] == supervised["status"] == "PASS"
    assert receipt["task"] == supervised["task"] == cfg["task"] and receipt["parent"] == cfg["parent"]
    assert receipt["preflights"] == 1 and receipt["task_module_imports"] == 0
    assert supervised["receipt_sha256"] == digest_file(receipt_path)
    assert supervised["config_sha256"] == digest_file(HERE / "config.json")
    assert receipt["input_hashes"] == {name: digest_file(HERE / name) for name in cfg["preflight_inputs"]}
    assert receipt["retained_inputs"] == cfg["retained_inputs"]
    assert receipt["runtime"]["sha256"] == cfg["runtime_sha256"] == digest_file(Path(sys.executable))
    for path, expected in cfg["source_hashes"].items():
        assert digest_file(ROOT / path) == expected, path
    return receipt["runtime"]


def produce(cfg, counts):
    runtime = validate_inputs(cfg)
    history = {name: read_json(ROOT / path)["status"] for name, path in cfg["status_receipts"].items()}
    assert history == cfg["expected_statuses"]
    archives = {name: open_archive(binding) for name, binding in cfg["archives"].items()}
    positives = {}
    for name, binding in cfg["retained_positives"].items():
        positives[name] = inspect_positive(binding, archives[binding["archive"]], counts)
    assert set(positives) == {"D118", "D119", "D120", "D122_I", "D122_II", "D123", "D124"}
    assert len({original["graph_digest"] for original, _, _ in positives.values()}) == 7
    transport = inspect_D121(archives["D121"], archives["D119"], positives["D119"], counts)
    adverse = inspect_D122_adverse(cfg["retained_adverse"], archives["D122"], counts)
    controls = run_controls(positives, adverse, counts)
    counts["symbolic_theorems"] += 1
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "scope": cfg["scope"],
            "runtime": runtime, "positives": {name: report for name, (_, _, report) in positives.items()},
            "D121_identity_inspection": transport, "controls": controls,
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
        if prior_cpu+process_time()-CPU_START >= limits["process_cpu_seconds"]:
            raise TimeoutError("Combined process CPU limit reached")
        receipt["status"] = "PASS"
    except (Exception, KeyboardInterrupt):
        receipt["error"] = traceback.format_exc()
    receipt["process_cpu_seconds"] = process_time()-CPU_START
    write_record("command_receipt.json", receipt, limits)
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(execute())
