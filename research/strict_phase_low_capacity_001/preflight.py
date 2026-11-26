"""Parse-only preparation verification. No task or graph-checker imports."""

import ast
from collections import Counter
import hashlib
from itertools import product
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
CODE = Path(__file__).resolve().parent
BUNDLE = ROOT / "evidence/validation/LCL_ORDINARY_SPINE_LOW_CAPACITY_STRICT_PHASE_MATCHED_001_PREP"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def identity(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def parsed(name):
    return json.loads(name.read_bytes())


def file_bytes(path, convention):
    raw = path.read_bytes()
    return raw if convention == "raw" else raw.replace(b"\r\n", b"\n")


def definitions(tree):
    """Reject repeated definitions in each lexical scope, even across branch suites."""
    names = []

    def scope(node, parent):
        declared = set()

        def visit(child):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                assert child.name not in declared, (parent, child.name)
                declared.add(child.name)
                qualified = parent + child.name
                names.append(qualified)
                scope(child, qualified + ".")
            else:
                for nested in ast.iter_child_nodes(child):
                    visit(nested)

        for child in ast.iter_child_nodes(node):
            visit(child)

    scope(tree, "")
    return names


def verify_bindings():
    bindings = parsed(BUNDLE / "SOURCE_BINDINGS.json")
    for rel, row in bindings.items():
        path = (ROOT / rel).resolve()
        assert path.is_relative_to(ROOT)
        assert identity(file_bytes(path, row["convention"])) == row["identity"], rel
    runtime = parsed(BUNDLE / "RUNTIME.json")
    assert runtime["version"] == sys.version
    assert runtime["implementation"] == sys.implementation.name
    assert runtime["launcher"] == identity(Path(sys.executable).read_bytes())
    assert runtime["base"] == identity(Path(sys._base_executable).read_bytes())
    assert runtime["interpreter_library"] == identity(
        Path(sys.base_prefix, f"python{sys.version_info.major}{sys.version_info.minor}.dll").read_bytes())
    assert sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode and not sys.flags.optimize
    assert not list(CODE.rglob("*.pyc")) and not list(CODE.rglob("__pycache__"))
    config = parsed(CODE / "config.json")
    assert config["execution_entry"] is None and config["execution_authorized"] is False
    for rel in config["required_vacant_paths"]:
        assert not (ROOT / rel).exists(), rel
    actual = {path.name: definitions(ast.parse(path.read_bytes(), filename=path.name))
              for path in sorted(CODE.glob("*.py"))}
    assert set(actual) == {"prepare_originals.py", "primary.py", "audit.py", "preflight.py"}
    return actual


def graph_identity(graph, profile):
    # Reconstruct a rooted parent for every fresh or old indexed role independently.
    spine = [f"s:{j}" for j in range(len(profile))]
    assert graph["spine"] == spine and graph["profile"] == profile and graph["schema_version"] == 1
    expected_edges = {frozenset(pair) for pair in zip(spine, spine[1:])}
    expected_roles = {name: {"section": i, "kind": "spine"} for i, name in enumerate(spine)}
    for i, (anchor, section) in enumerate(zip(spine, profile)):
        for j, quota in enumerate(section):
            host = f"b:{i}:{j}"
            expected_roles[host] = dict(section=i, kind="branch", branch=j)
            expected_edges.add(frozenset((anchor, host)))
            for k in range(quota):
                leaf = f"l:{i}:{j}:{k}"
                expected_roles[leaf] = dict(section=i, kind="leaf", branch=j, leaf=k)
                expected_edges.add(frozenset((host, leaf)))
    assert graph["roles"] == expected_roles
    assert len(graph["vertices"]) == len(expected_roles) and set(graph["vertices"]) == set(expected_roles)
    assert len(graph["edges"]) == len(expected_edges)
    assert {frozenset(edge) for edge in graph["edges"]} == expected_edges
    payload = {"vertices": sorted(expected_roles), "edges": sorted(sorted(edge) for edge in expected_edges),
               "profile": profile, "spine": spine, "roles": expected_roles}
    return identity(canonical(payload))["sha256"]


def prefix_spectrum(graph, labels, cut, edge_count, threshold, frontier):
    assert len(graph["edges"]) == edge_count and len(graph["vertices"]) == edge_count + 1
    assert set(labels) == set(graph["vertices"]) and labels[frontier] == edge_count
    assert all(type(x) is int for x in labels.values())
    assert sorted(labels.values()) == list(range(edge_count + 1))
    crossing, noncrossing = [], []
    for a, b in graph["edges"]:
        x, y = labels[a], labels[b]
        (crossing if (x < cut) != (y < cut) else noncrossing).append(abs(x - y))
    assert sorted(crossing) == list(range(threshold, edge_count + 1))
    assert sorted(noncrossing) == list(range(1, threshold))
    assert graph["spine"][-1] == frontier


def verify_inputs():
    old_path = ROOT / ("evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_MATCHED_001_PREP"
                       "/input/prefix.json")
    old = parsed(old_path)
    old_identity = graph_identity(old["graph"], old["graph"]["profile"])
    assert old_identity == old["digest"]
    prefix_spectrum(old["graph"], old["actual_labels"], 39, 74, 37, "s:27")
    new_orig = parsed(BUNDLE / "prefix94-original.json")
    new = parsed(BUNDLE / "prefix94.json")
    profile = old["graph"]["profile"] + [[5, 2], [2, 4, 0]]
    new_id = graph_identity(new_orig["graph"], profile)
    assert new_id == new_orig["digest"] == new["digest"]
    assert new["prefix74_identity"] == {"sha256": identity(old_path.read_bytes())["sha256"], "digest": old_identity}
    assert new["actual_cut"] == 49 and new["minimum_cut"] == 46 and new["edges"] == 94 and new["vertices"] == 95
    prefix_spectrum(new_orig["graph"], new["actual_labels"], 49, 94, 48, "s:29")
    for name, value in old["actual_labels"].items():
        assert new["actual_labels"][name] == value + (4 if value < 39 else 17)
    return {"S-1": (old["graph"]["profile"], old_identity, 74), "S0": (profile, new_id, 94)}


def verify_corpus(prefixes):
    matches = []
    pairs = sorted(((p, q) for p, q in product(range(2, 15), repeat=2)
                    if p + q in range(6, 17, 2)), key=lambda pair: (sum(pair), pair))
    assert len(pairs) == 48
    for stratum, low, companion, direct in (
            ("III", [3, 2, 1], [4, 1, 1], [0]),
            ("II", [3, 3, 0], [4, 2, 0], [0]),
            ("I", [3, 2, 0], [4, 1, 0], [])):
        for p, q in pairs:
            matches.append((f"{stratum}-{p:02}-{q:02}", stratum, low, companion, [p, q, *direct]))
    matches.extend((f"boundary-{p:02}-01", "boundary", [3, 2, 0], [4, 1, 0], [p, 1])
                   for p in (5, 7))
    expected = [(phase, key, stratum, arm, [first, second])
                for phase in ("S0", "S-1")
                for key, stratum, low, companion, second in matches
                for arm, first in (("low", low), ("companion", companion))]
    found = []
    seen = set()
    counts = Counter()
    bindings = {}
    with (BUNDLE / "originals.jsonl").open("rb") as stream:
        for raw in stream:
            row = json.loads(raw)
            record = row["record"]
            assert raw == canonical(row) + b"\n"
            assert identity(canonical(record))["sha256"] == row["record_sha256"]
            phase, key, stratum, arm, suffix = (record[k] for k in ("phase", "match", "stratum", "arm", "suffix"))
            found.append((phase, key, stratum, arm, suffix))
            prof, dig, old_size = prefixes[phase]
            assert dig == record["prefix_digest"]
            expected_digest = graph_identity(record["graph"], prof + suffix)
            assert record["digest"] == expected_digest and expected_digest not in seen
            seen.add(expected_digest)
            assert record["fresh_edges"] == 2 + sum(len(section) + sum(section) for section in suffix)
            assert record["fresh_edges"] % 2 == 0 and record["fresh_edges"] <= old_size
            assert len(record["graph"]["edges"]) == old_size + record["fresh_edges"]
            counts[phase + ":" + stratum] += 1
            if key in ("II-02-06", "boundary-05-01", "boundary-07-01"):
                bindings[f"{phase}:{key}:{arm}"] = {"record_sha256": row["record_sha256"],
                                                    "graph_digest": expected_digest}
    assert found == expected and len(found) == len(seen) == 584
    return {"records": len(found), "counts": counts, "named_control_bindings": bindings}


def main():
    cpu, wall = time.process_time(), time.perf_counter()
    names = verify_bindings()
    prefix_inputs = verify_inputs()
    corpus = verify_corpus(prefix_inputs)
    assert not any(name == "lcl" or name.startswith(("lcl.", "strict_phase_low_capacity_001"))
                   for name in sys.modules)
    print(json.dumps({"status": "PASS_PARSE_ONLY", "definitions": names,
                      "prefix_digests": {phase: spec[1] for phase, spec in prefix_inputs.items()},
                      "corpus": corpus, "cpu_seconds": time.process_time() - cpu,
                      "observed_process_wall_seconds": time.perf_counter() - wall,
                      "execution_entry": None, "official_outputs_vacant": True,
                      "task_modules_imported": 0, "numerical_evaluations": 0}))


if __name__ == "__main__":
    main()
