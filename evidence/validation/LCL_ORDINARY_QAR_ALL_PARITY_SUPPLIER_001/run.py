"""One D117 verification of the unified indexed formula on D111 and D114."""

from time import perf_counter, process_time

WALL_START = perf_counter()
CPU_START = process_time()

from collections import Counter
from datetime import datetime, timezone
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
    raw = (json.dumps(data, indent=2, sort_keys=True) + "\n").encode()
    total = sum(path.stat().st_size for path in HERE.iterdir() if path.is_file())
    if len(raw) > limits["bytes_per_record"] or total + len(raw) > limits["bytes_total"]:
        raise ValueError("Evidence byte cap exceeded")
    with (HERE / name).open("xb") as stream:
        stream.write(raw)
    return sha256(raw).hexdigest()


def indexed_formula(q, a, r):
    if type(q) is not int or type(a) is not int or type(r) is not int or q < 5 or a < 3 or r < 2:
        raise ValueError("Require exact integer q >= 5, a >= 3 and r >= 2")
    n = q + a + 6
    m = n + r - 2
    lower_index = 0 if q % 2 == 0 else 1
    higher_index = 1 - lower_index
    lower, higher = f"b:0:{lower_index}", f"b:0:{higher_index}"
    ell, h = (q, a)[lower_index], (q, a)[higher_index]
    j, epsilon = divmod(ell-2, 2)
    u, eta = (n-1)//2, int(n % 2 == 0)
    c = u-4
    assert 0 <= j <= c and 0 <= epsilon <= eta and 2*(c-j) == h-1-eta+epsilon
    core = {"s:0": 0, "s:1": n, lower: 2, higher: n-2, "b:1:0": 1,
            f"l:0:{lower_index}:0": 3, f"l:0:{lower_index}:{ell-1}": n-1,
            "l:1:0:0": n-4, "l:1:0:1": n-3}
    lower_palette = list(range(u-j+1, u+1))
    if epsilon:
        lower_palette.append(n//2)
    lower_palette.extend(range(n-u, n-u+j))
    allocated_lower = set(lower_palette)
    higher_palette = [x for x in range(4, n-4) if x not in allocated_lower]
    allocation = {lower: lower_palette, higher: higher_palette}
    assert len(lower_palette) == ell-2 and len(higher_palette) == h and 4 in higher_palette
    labels = core | {"s:1": m}
    labels.update({f"l:0:{lower_index}:{i}": x for i, x in enumerate(lower_palette, start=1)})
    labels.update({f"l:0:{higher_index}:{i}": x for i, x in enumerate(higher_palette)})
    labels.update({f"l:1:0:{k}": n+k-2 for k in range(2, r)})
    selection = {"n": n, "m": m, "lower": lower, "higher": higher, "ell": ell, "h": h,
                 "u": u, "j": j, "c": c, "eta": eta, "epsilon": epsilon}
    return core, allocation, labels, selection


def pins_gate(graph, labels, m):
    expected = {"s:0": 0, "s:1": m, "b:1:0": 1}
    assert graph["spine"] == ["s:0", "s:1"]
    actual_edges = {frozenset(edge) for edge in graph["edges"]}
    assert frozenset(graph["spine"]) in actual_edges
    assert frozenset(("s:1", "b:1:0")) in actual_edges
    actual = {v: labels[v] for v in expected}
    return {"actual": actual, "expected": expected,
            "valid": actual == expected and all(type(x) is int for x in actual.values())}


def allocation_gate(graph, core, allocation):
    hosts = ("b:0:0", "b:0:1")
    assert set(allocation) == set(hosts) and set(hosts) <= set(core)
    m = len(graph["edges"])
    occupied = [abs(core[u] - core[v]) for u, v in graph["edges"] if u in core and v in core]
    remaining_labels = set(range(m + 1)) - set(core.values())
    remaining_weights = set(range(1, m + 1)) - set(occupied)
    vacancies = [frozenset((u, v)) for u, v in graph["edges"] if u not in core or v not in core]
    assert all(len(edge.intersection(core)) == 1 and edge.intersection(core) <= set(hosts)
               for edge in vacancies)
    expected_quotas = {h: sum(h in edge for edge in vacancies) for h in hosts}
    actual_quotas = {h: len(allocation[h]) for h in hosts}
    labels = [x for h in hosts for x in allocation[h]]
    weights = [abs(core[h] - x) for h in hosts for x in allocation[h]]
    labels_exact = Counter(labels) == Counter(remaining_labels)
    weights_exact = Counter(weights) == Counter(remaining_weights)
    quotas_exact = actual_quotas == expected_quotas
    return {"residual_labels": sorted(remaining_labels), "residual_differences": sorted(remaining_weights),
            "allocated_labels": sorted(labels), "allocated_differences": sorted(weights),
            "expected_quotas": expected_quotas, "actual_quotas": actual_quotas,
            "labels_exact": labels_exact, "differences_exact": weights_exact,
            "quotas_exact": quotas_exact, "valid": labels_exact and weights_exact and quotas_exact}


def growth_gate(graph, labels, m):
    spine = graph["spine"]
    u, v, c = "s:0", "s:1", "b:1:0"
    neighbors = {x if y == v else y for x, y in graph["edges"] if v in (x, y)}
    tests = {"exit_and_predecessor": spine == [u, v],
             "host_off_spine": c in graph["vertices"] and c not in spine,
             "exact_exit_neighbors": neighbors == {u, c},
             "boundary_size": len(graph["edges"]) == m,
             "required_labels": (labels[u], labels[v], labels[c]) == (0, len(graph["edges"]), 1)}
    return {"tests": tests, "exit_neighbors": sorted(neighbors), "valid": all(tests.values())}


def retained_positive(binding, counts):
    path = ROOT / binding["original"]
    original = read_json(path)
    result = read_json(ROOT / binding["result"])
    cert, graph = result["certificate"], original["graph"]
    digest = binding["graph_digest"]
    assert digest_file(path) == binding["original_sha256"]
    assert result["status"] == "PASS"
    assert graph["profile"] == binding["profile"] and graph["spine"] == cert["physical_spine"]
    assert cert["graph_digest"] == original["graph_digest"] == digest and cert["ledger_id"] == binding["ledger_id"]
    assert cert["kind"] == "ordinary_graceful"
    counts["retained_positive_rechecks"] += 1
    checked = verify_certificate(graph, cert["labels"], digest)
    gate = pins_gate(graph, cert["labels"], len(graph["edges"]))
    assert checked["valid"] and checked == cert["checker"] and gate["valid"]
    return original, cert, {"original_path": binding["original"], "result_path": binding["result"],
                            "graph_digest": digest, "ledger_id": cert["ledger_id"], "checker": checked, "pins": gate}


def original_residual_allocation(graph, core, named_labels):
    hosts = ("b:0:0", "b:0:1")
    slots = {host: [] for host in hosts}
    for u, v in graph["edges"]:
        if (u in core) != (v in core):
            host, leaf = (u, v) if u in core else (v, u)
            slots[host].append(leaf)
    assert all(named_labels[v] == x for v, x in core.items())
    return {host: [named_labels[v] for v in sorted(slots[host])] for host in hosts}


def bound_formula(binding, parameters, counts):
    original, cert, retained = retained_positive(binding, counts)
    graph = original["graph"]
    q, a, r = parameters
    assert graph["profile"] == [[q, a], [r]] and r == 2
    counts["retained_boundary_evaluations"] += 1
    core, allocation, formula, selection = indexed_formula(q, a, r)
    assert formula == cert["labels"]
    gate = allocation_gate(graph, core, allocation)
    growth = growth_gate(graph, cert["labels"], len(graph["edges"]))
    assert gate["valid"] and growth["valid"]
    boundary = audit.boundary(original, cert, retained["checker"])
    assert core == boundary["core"]["labels"] and allocation == boundary["allocation"]
    assert selection == boundary["selection"] and gate["actual_quotas"] == boundary["actual_quotas"]
    answer = {"parameters": list(parameters), "retained": retained, "allocation_gate": gate,
              "pointwise_agreement": True, "growth_premises": growth, "independent": boundary}
    return original, cert, formula, core, answer


def run_controls(odd, even, counts):
    old, cert, formula, _, report = odd
    g, labels, digest = old["graph"], cert["labels"], old["graph_digest"]
    wrong = "0" * 64
    counts["declared_controls"] += 1
    wrong_report = verify_certificate(g, labels, wrong)
    assert not wrong_report["valid"] and wrong_report["errors"] == ["original graph digest mismatch"]

    counts["declared_controls"] += 1
    u, v = "l:0:0:0", "l:0:0:1"
    assert (labels[u], labels[v]) == (4, 5)
    within = labels | {u: labels[v], v: labels[u]}
    within_check = verify_certificate(g, within, digest)
    within_growth = growth_gate(g, within, len(g["edges"]))
    disagreements = sorted(x for x in formula if within[x] != formula[x])
    assert within_check["valid"] and within_growth["valid"] and disagreements == [u, v]
    assert within_growth == report["growth_premises"]

    original, cert, _, core, _ = even
    g, labels, digest = original["graph"], cert["labels"], original["graph_digest"]
    m = len(g["edges"])
    counts["declared_controls"] += 1
    u, v = "l:0:0:1", "l:0:1:1"
    assert (labels[u], labels[v]) == (6, 5)
    cross = labels | {u: labels[v], v: labels[u]}
    cross_check = verify_certificate(g, cross, digest)
    cross_pins = pins_gate(g, cross, m)
    cross_allocation = original_residual_allocation(g, core, cross)
    cross_quota = allocation_gate(g, core, cross_allocation)
    assert sorted(cross.values()) == sorted(labels.values()) and cross_pins["valid"]
    assert cross_quota["labels_exact"] and cross_quota["quotas_exact"] and not cross_quota["differences_exact"]
    assert not cross_check["valid"]
    assert cross_check["errors"] == ["edge differences repeat", "edge differences are not exactly 1..m"]

    counts["declared_controls"] += 1
    complement = {vertex: m-x for vertex, x in labels.items()}
    complement_check = verify_certificate(g, complement, digest)
    complement_pins = pins_gate(g, complement, m)
    complement_growth = growth_gate(g, complement, m)
    assert complement_check["valid"] and not complement_pins["valid"] and not complement_growth["valid"]
    assert {test for test, passed in complement_growth["tests"].items() if not passed} == {"required_labels"}
    return {"wrong_digest_D111": {"expected_digest": wrong, "checker": wrong_report},
            "within_D111": {"vertices": ["l:0:0:0", "l:0:0:1"], "checker": within_check,
                            "growth_premises": within_growth, "pointwise_agreement": False,
                            "disagreements": disagreements},
            "cross_D114": {"vertices": [u, v], "checker": cross_check, "pins": cross_pins,
                           "allocation_gate": cross_quota},
            "complement_D114": {"checker": complement_check, "pins": complement_pins,
                                 "growth_premises": complement_growth}}


def validate_inputs(cfg):
    receipt = read_json(HERE / "preflight_receipt.json")
    assert receipt["status"] == "PASS" and receipt["task"] == cfg["task"]
    assert receipt["parent"] == cfg["parent"] and receipt["preflight_invocations"] == 1
    assert receipt["input_hashes"] == {name: digest_file(HERE / name) for name in cfg["local_inputs"]}
    assert receipt["runtime"]["sha256"] == cfg["runtime_sha256"] == digest_file(Path(sys.executable))
    for path, expected in cfg["source_hashes"].items():
        assert digest_file(ROOT / path) == expected, path
    return receipt["runtime"]


def produce(cfg, counts):
    runtime = validate_inputs(cfg)
    scope = cfg["scope"]
    assert scope == {"symbolic_profile": [["q", "a"], ["r"]], "minimum_q": 5, "minimum_a": 3,
                     "minimum_r": 2, "boundaries": {"D111": [5, 3, 2], "D114": [6, 3, 2]}}
    assert set(cfg["retained"]) == {"D111", "D114"}
    history = {key: read_json(ROOT / path)["status"] for key, path in cfg["status_receipts"].items()}
    assert history == cfg["expected_statuses"]
    lineage = cfg["lineage"]
    archived = read_json(ROOT / lineage["result"])
    assert archived["status"] == "PASS" and digest_file(ROOT / lineage["result"]) == lineage["sha256"]
    assert archived["archived_transition"]["new_terminal"] == "l:1:0:2"
    odd = bound_formula(cfg["retained"]["D111"], scope["boundaries"]["D111"], counts)
    even = bound_formula(cfg["retained"]["D114"], scope["boundaries"]["D114"], counts)
    probes = run_controls(odd, even, counts)
    control_audit = audit.controls(odd[0], odd[1], even[0], even[1], even[4]["independent"], probes)
    counts["symbolic_theorems"] += 1
    return {"status": "PASS", "task": cfg["task"], "parent": cfg["parent"], "scope": scope,
            "runtime": runtime, "retained_boundaries": {"D111": odd[4], "D114": even[4]},
            "growth_lineage": lineage, "controls": probes, "control_audit": control_audit,
            "retained_execution_statuses": history}


def execute():
    cfg = read_json(HERE / "config.json")
    limits = cfg["limits"]
    counts = dict.fromkeys(cfg["count_keys"], 0)
    counts.update(workers=1, official_invocations=1, preflights=1)
    receipt = {"task": cfg["task"], "parent": cfg["parent"], "argv": sys.orig_argv,
               "started_utc": datetime.now(timezone.utc).isoformat(), "counts": counts, "limits": limits}
    try:
        if not __debug__ or not sys.dont_write_bytecode:
            raise RuntimeError("Require active assertions and -B")
        outputs = ("original.json", "result.json", "command_receipt.json", "supervisor_receipt.json", "__pycache__")
        assert all(not (HERE / name).exists() for name in outputs)
        receipt["input_hashes"] = {name: digest_file(HERE / name)
                                   for name in (*cfg["local_inputs"], "preflight_receipt.json")}
        result = produce(cfg, counts)
        assert all(value <= limits[key] for key, value in counts.items())
        assert (counts["retained_positive_rechecks"], counts["declared_controls"]) == (2, 4)
        assert counts["symbolic_theorems"] == 1 and counts["retained_boundary_evaluations"] == 2
        if process_time() - CPU_START >= limits["process_cpu_seconds"] or perf_counter() - WALL_START >= limits["wall_seconds"]:
            raise TimeoutError("Official time cap exceeded")
        receipt["result_sha256"] = write_record("result.json", result, limits)
        if process_time() - CPU_START >= limits["process_cpu_seconds"] or perf_counter() - WALL_START >= limits["wall_seconds"]:
            raise TimeoutError("Official time cap exceeded after writing the result")
        receipt.update(status="PASS", exit_code=0)
    except (Exception, KeyboardInterrupt):
        receipt.update(status="INCOMPLETE", exit_code=1, error=traceback.format_exc())
    receipt["process_cpu_seconds"] = process_time() - CPU_START
    receipt["wall_seconds"] = perf_counter() - WALL_START
    receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write_record("command_receipt.json", receipt, limits)
    return receipt["exit_code"]


if __name__ == "__main__":
    sys.exit(execute())
