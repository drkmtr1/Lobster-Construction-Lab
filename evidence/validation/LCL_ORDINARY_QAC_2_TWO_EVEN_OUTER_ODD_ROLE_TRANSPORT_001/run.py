"""Verify only the retained canonical sources and index-level D127 controls."""

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


def inverse_indices(indices):
    if len(indices) != 3 or any(type(i) is not int for i in indices) or set(indices) != {0, 1, 2}:
        return None
    inverse = [None]*3
    for j, physical in enumerate(indices):
        inverse[physical] = j
    return inverse


def canonical_supplier(q, a, c):
    assert all(type(value) is int for value in (q, a, c))
    assert q >= 6 and q % 2 == 0 and a >= 3 and a % 2 == 1 and c >= 2 and c % 2 == 0
    if a >= 5:
        return {"supplier": "D122", "branch": "II"}
    if c >= 6:
        return {"supplier": "D123" if q == c else "D124",
                "alternative": "D122.I" if c <= q-4 else None}
    if (q, a, c) == (6, 3, 4):
        return {"supplier": "D126"}
    assert a == 3 and c <= q-4
    return {"supplier": "D122", "branch": "I"}


def select_roles(quotas, *, canonical_comparison):
    if len(quotas) != 3 or any(type(value) is not int for value in quotas):
        raise ValueError("Require three exact integer quotas")
    odd = [j for j, value in enumerate(quotas) if value % 2]
    allowed = {1} if canonical_comparison else {0, 2}
    if len(odd) != 1 or odd[0] not in allowed or quotas[odd[0]] < 3:
        raise ValueError("Require the unique odd quota at a permitted index with quota at least three")
    i_a = odd[0]
    evens = [j for j in range(3) if j != i_a]
    qualifying = [j for j in evens if quotas[j] >= 6]
    if not qualifying or any(quotas[j] < 2 for j in evens):
        raise ValueError("Require both even quotas at least two and one at least six")
    i_q = min(qualifying)
    i_c = next(j for j in evens if j != i_q)
    indices = [i_q, i_a, i_c]
    canonical = [quotas[j] for j in indices]
    return {"indices": indices, "canonical_quotas": canonical,
            "dispatch": canonical_supplier(*canonical)}


def bind_roles(graph, requested_quotas, indices):
    inverse = inverse_indices(indices)
    if inverse is None:
        return {"status": "NONBIJECTIVE_ROLE_MAP", "valid": False, "indices": indices,
                "bijective": False, "quota_evaluated": False}
    assert len(requested_quotas) == 3 and all(type(q) is int and q >= 0 for q in requested_quotas)
    actual_quotas = graph["profile"][0]
    rows = []
    for role, physical in enumerate(indices):
        requested_quota = requested_quotas[role]
        center = f"b:0:{physical}"
        requested = [f"l:0:{physical}:{k}" for k in range(requested_quota)]
        actual_leaves = [w for v, w in graph["edges"] if v == center and graph["roles"][w]["kind"] == "leaf"]
        actual = sorted(actual_leaves, key=lambda leaf: graph["roles"][leaf]["leaf"])
        assert len(actual) == actual_quotas[physical]
        rows.append({"role": role, "physical_index": physical, "quota": requested_quota,
                     "actual_quota": actual_quotas[physical], "requested": requested, "actual": actual,
                     "absent": [leaf for leaf in requested if leaf not in actual],
                     "omitted": [leaf for leaf in actual if leaf not in requested]})
    quota_compatible = all(row["quota"] == row["actual_quota"] for row in rows)
    slots_exact = all(not row["absent"] and not row["omitted"] for row in rows)
    return {"valid": quota_compatible and slots_exact, "indices": indices, "inverse": inverse,
            "bijective": True, "quota_evaluated": True, "quota_compatible": quota_compatible,
            "slots_exact": slots_exact, "rows": rows}


def direction_gate(required, candidate):
    inverse = inverse_indices(candidate)
    assert inverse is not None and inverse_indices(required) is not None
    rows = []
    wrong_indices = []
    for j, forward_index in enumerate(candidate):
        if forward_index != required[j]:
            wrong_indices.append(j)
        source_terminal = (j, "k")
        mapped_terminal = (candidate[source_terminal[0]], source_terminal[1])
        returned_terminal = (inverse[mapped_terminal[0]], mapped_terminal[1])
        reverse_terminal = (inverse[source_terminal[0]], source_terminal[1])
        reverse_returned = (candidate[reverse_terminal[0]], reverse_terminal[1])
        rows.append({"source_center_index": j, "forward_center_index": forward_index,
                     "center_round_trip": inverse[forward_index], "reverse_center_round_trip": candidate[inverse[j]],
                     "source_terminal": list(source_terminal), "forward_terminal": list(mapped_terminal),
                     "terminal_round_trip": list(returned_terminal), "reverse_terminal_round_trip": list(reverse_returned)})
    round_trip = all(row["center_round_trip"] == row["reverse_center_round_trip"] == j
                     and row["terminal_round_trip"] == row["reverse_terminal_round_trip"] == [j, "k"]
                     for j, row in enumerate(rows))
    return {"valid": round_trip and not wrong_indices, "bijective": True, "candidate": candidate,
            "inverse": inverse, "round_trips": round_trip, "mismatched_canonical_indices": wrong_indices, "rows": rows}


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


def inspect_adverse(binding, archive, counts):
    folder, manifest, result = archive
    assert manifest["obstruction"] == result["obstruction"] == binding
    original_record = binding["original"]
    assert manifest["originals"]["adverse"] == original_record
    original_path, obstruction_path = folder / original_record["path"], folder / binding["path"]
    check_member(manifest, original_path, original_record["raw_sha256"])
    check_member(manifest, obstruction_path, binding["sha256"])
    original, record = read_json(original_path), read_json(obstruction_path)
    assert record["original"] == original_record and record["certificates"] == 0
    assert record["scope"] == "all_completions_of_the_specified_labeled_core"
    assert record["status"] == "FIXED_CORE_INFEASIBLE"
    assert record["graph_digest"] == original["graph_digest"] == original_record["graph_digest"]
    assert original["graph"]["profile"] == original_record["profile"] == [[6, 3, 4], [2]]
    core = record["core"]
    assert [core[f"b:0:{j}"] for j in range(3)] == [16, 2, 14]
    core_edges = [[u, v] for u, v in original["graph"]["edges"] if u in core and v in core]
    assert record["core_edges"] == core_edges
    assert record["core_differences"] == [abs(core[u]-core[v]) for u, v in core_edges]
    counts["retained_adverse_inspections"] += 1
    return original, original_path.relative_to(ROOT).as_posix(), {
        "status": record["status"], "scope": record["scope"], "binding": binding,
        "old_core": core, "historical_procedure_replayed": False}


def inspect_positive(name, binding, archive, adverse, counts):
    folder, manifest, result = archive
    variant = binding["variant"]
    if variant is None:
        source, original_record, ledger = result, manifest["original"], manifest["ledger_id"]
    else:
        source = result["positive"][variant]
        original_record, ledger = manifest["originals"][variant], manifest["positive_ledger_ids"][variant]
    assert original_record == source["original"] == binding["original_record"]
    if name == "D126":
        original, path, obstruction = adverse
        assert original_record == (obstruction["binding"]["original"] | {"path": path})
        assert source["prior_fixed_core_obstruction"]["sha256"] == obstruction["binding"]["sha256"]
        assert source["prior_fixed_core_obstruction"]["old_core"] == obstruction["old_core"]
        assert source["core"] != obstruction["old_core"]
    else:
        path = folder / original_record["path"]
        check_member(manifest, path, original_record["raw_sha256"])
        original = read_json(path)
    graph, cert = original["graph"], source["certificate"]
    structure = audit.inspect_original(original, binding["profile"])
    digest = structure["graph_digest"]
    assert original_record["graph_digest"] == digest == cert["graph_digest"]
    assert cert["kind"] == "ordinary_graceful" and cert["ledger_id"] == ledger == binding["ledger_id"]
    assert cert["physical_spine"] == graph["spine"]
    independent = audit.inspect_certificate(original, cert, structure)
    labels = cert["labels"]
    m = len(structure["edges"])
    growth = audit.check_growth_premises(graph, labels, m, structure)
    assert growth["valid"] and cert["physical_pins"]["actual"] == growth["pins"]
    assert [labels[f"l:1:0:{k}"] for k in range(2)] == [m-1, m-2]
    counts["retained_positive_rechecks"] += 1
    checker = verify_certificate(graph, labels, digest)
    assert checker["valid"] and checker == cert["checker"]
    assert checker["edge_differences"] == independent["edge_weights"]
    choice = select_roles(graph["profile"][0], canonical_comparison=True)
    binding_report = bind_roles(graph, choice["canonical_quotas"], choice["indices"])
    audit.check_canonical(graph, choice, binding_report, binding["expected_dispatch"])
    counts["canonical_comparisons"] += 1
    return original, cert, {"source": binding, "checker": checker, "selected": choice,
                            "identity_role_binding": binding_report, "D112_premises": growth,
                            "independent": independent, "original_manifest_binding_verified": True}


def run_controls(original, cert, counts):
    graph, digest = original["graph"], original["graph_digest"]
    wrong = "0"*64
    counts["declared_controls"] += 1
    rejected = verify_certificate(graph, cert["labels"], wrong)
    assert not rejected["valid"] and rejected["errors"] == ["original graph digest mismatch"]
    assert rejected["graph_digest"] == digest

    quotas = graph["profile"][0]
    assert quotas == [6, 3, 4]
    counts["declared_controls"] += 1
    duplicate = bind_roles(graph, quotas, [0, 0, 2])
    assert duplicate["status"] == "NONBIJECTIVE_ROLE_MAP" and not duplicate["quota_evaluated"]
    assert not duplicate["valid"]

    counts["declared_controls"] += 1
    wrong_slots = bind_roles(graph, quotas, [2, 1, 0])
    assert wrong_slots["bijective"] and wrong_slots["quota_evaluated"]
    assert not wrong_slots["quota_compatible"] and not wrong_slots["slots_exact"] and not wrong_slots["valid"]

    counts["declared_controls"] += 1
    forward = [1, 2, 0]
    valid = direction_gate(forward, forward)
    wrong_direction = direction_gate(forward, valid["inverse"])
    assert valid["valid"] and not wrong_direction["valid"] and wrong_direction["round_trips"]
    records = {"wrong_expected_digest": {"expected": wrong, "checker": rejected},
               "nonbijective_map": duplicate, "quota_incompatible_map": wrong_slots,
               "direction": {"forward_check": valid, "inverse_used_as_forward": wrong_direction,
                             "index_only": True}}
    return records, audit.check_controls(graph, cert, records)


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
    adverse = inspect_adverse(cfg["retained_adverse"], archives["D122"], counts)
    positives = {name: inspect_positive(name, binding, archives[binding["archive"]], adverse, counts)
                 for name, binding in cfg["retained_positives"].items()}
    assert set(positives) == {"D122_I", "D122_II", "D123", "D124", "D126"}
    assert len({original["graph_digest"] for original, _, _ in positives.values()}) == 5
    target, cert, _ = positives["D126"]
    assert target is adverse[0]
    controls, independent_controls = run_controls(target, cert, counts)
    counts["symbolic_theorems"] += 1
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "scope": cfg["scope"],
            "runtime": runtime, "canonical_comparisons": {name: report for name, (_, _, report) in positives.items()},
            "retained_D122_obstruction": adverse[2], "controls": controls, "independent_controls": independent_controls,
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
