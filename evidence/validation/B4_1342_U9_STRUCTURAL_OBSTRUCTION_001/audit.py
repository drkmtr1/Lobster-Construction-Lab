"""Independently reconstruct the original graphs and audit saved arithmetic."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "validation"
PARENT = "3ac2ccc91d28063e89ebd21bf3ec5bf525f72992"
PROOF = "research/B4_1342_U9_STRUCTURAL_OBSTRUCTION.md"
EXPECTED_INPUTS = [
  "evidence/validation/B4_1342_UPPER_BLOCK_OBSTRUCTION_001/validation/originals/1342.json",
  "evidence/validation/B4_1RT2_TWO_HOST_COMPATIBILITY_001/validation/originals/normalized-r3-t4.json",
  "evidence/validation/B4_1RT2_TWO_HOST_COMPATIBILITY_001/validation/normalized-r3-t4.json",
  "evidence/validation/B4_THIRD_ZERO_HOST_NONADJACENT_001/original_graph.json",
  "evidence/validation/B4_THIRD_ZERO_HOST_NONADJACENT_001/query_record.json",
  "evidence/validation/B4_UNPADDED_Q1T2_001/validation/retained_seed.json"
]
H, Z, U = "b:0:0", "b:2:0", "s:4"
F, B, T = "b:3:0", "b:1:0", "l:0:0:0"


def check(condition, context):
    if not condition:
        raise ValueError(context)


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob(path):
    return subprocess.check_output(["git", "show", f"{PARENT}:{path}"], cwd=ROOT)


def rebuild(counts):
    """Use explicit spine/center name roles and attach leaves to their sections."""
    edges = [(f"s:{i}", f"s:{i+1}") for i in range(4)]
    roles = {f"s:{i}": {"kind": "spine", "section": i} for i in range(5)}
    for section, n in enumerate(counts):
        center = f"b:{section}:0"
        roles[center] = {"kind": "branch", "section": section, "branch": 0}
        edges.append((f"s:{section}", center))
        for index in range(n):
            leaf = f"l:{section}:0:{index}"
            roles[leaf] = {"kind": "leaf", "section": section, "branch": 0, "leaf": index}
            edges.append((center, leaf))
    return roles, edges


def edge_id(pair):
    return tuple(sorted(pair))


def audit_graph(counts, original, cert, record, cutoff, pins):
    roles, edges = rebuild(counts)
    check(Counter(original["vertices"]) == Counter(roles.keys()), "named vertex multiplicities")
    check(Counter(map(edge_id, original["edges"])) == Counter(map(edge_id, edges)), "named edge multiplicities")
    check(original["roles"] == roles and original["profile"] == [[x] for x in counts] + [[]]
          and original["spine"] == [f"s:{i}" for i in range(5)] and original["schema_version"] == 1,
          "original structural metadata")
    payload = {"profile": original["profile"], "spine": original["spine"], "roles": roles,
               "vertices": sorted(roles), "edges": sorted(map(edge_id, edges))}
    identity = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    check(identity == cert["graph_digest"] == record["graph_digest"], "canonical digest")
    m = len(edges)
    g = record["labels"]
    check(set(g) == set(roles) and all(type(label) is int for label in g.values())
          and sorted(g.values()) == list(range(m + 1)), "label bijection")
    check(record["pins"] == pins == {v: g[v] for v in pins}, "retained control pins")
    adj = {v: [] for v in roles}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    high = sorted(v for v, r in roles.items() if (r["section"] + (r["kind"] == "branch")) % 2 == 0)
    low = sorted(roles.keys() - set(high))
    check(all((u in high) != (v in high) for u, v in edges)
          and sorted(g[v] for v in high) == list(range(cutoff, m + 1))
          and sorted(g[v] for v in low) == list(range(cutoff)), "physical alpha orientation")
    witness = [H, *original["spine"]]
    check(all(v in adj[u] for u, v in zip(witness, witness[1:])), "named witness")
    distance = {v: 0 if v in witness else
                1 if roles[v]["kind"] == "branch" or roles[v]["section"] == 0 else 2 for v in roles}
    check(all(d == 0 or any(distance[u] == d - 1 for u in adj[v]) for v, d in distance.items())
          and all(abs(distance[u] - distance[v]) <= 1 for u, v in edges), "exact witness distances")
    expected_facts = {"high": high, "low": low, "neighbors": {v: sorted(adj[v]) for v in adj},
                      "witness": witness, "witness_distances": distance}
    check(record["facts"] == expected_facts and distance[Z] == 1, "saved physical data")
    weights = [abs(g[u] - g[v]) for u, v in original["edges"]]
    check(sorted(weights) == list(range(1, m + 1)), "original graceful spectrum")
    check(cert == record["checker"] and cert["valid"] is True and not cert["errors"]
          and cert["n"] == m + 1 and cert["m"] == m and cert["edge_differences"] == weights, "checker receipt")
    ledger = [{"edge": pair, "difference": weight} for pair, weight in zip(original["edges"], weights)]
    check(record["edge_ledger"] == ledger, "edge ledger")
    return high, adj


def audit_reduction(datum, high, adj):
    census = {v: len(adj[v]) for v in high}
    eligible = sorted(set(high) - {U})
    check(census == datum["subset_table"]["degree"] and eligible == datum["subset_table"]["eligible"]
          and len(eligible) == 9 and sum(census.values()) == 18, "high census")
    forced = datum["forcing"]
    pairs = {str(d): [[v-d, v] for v in range(9, 19) if 0 <= v-d <= 8] for d in (1, 2, 18)}
    check(forced["alpha_pairs"] == pairs == {"1": [[8, 9]], "2": [[7, 9], [8, 10]], "18": [[0, 18]]}
          and adj[U] == [forced["exit_neighbor"]] == ["s:3"]
          and set(adj["s:3"]) == set(forced["s3_neighbors"]) == {U, "s:2", F}
          and forced["forced"] == {"s:3": 8, F: 10} and forced["force_fourth_center_from_c"] == 11,
          "forced labels one and two")
    mandatory = set(adj[Z])
    terminal = mandatory - {"s:2"}
    check(mandatory == set(forced["zero_neighbors"]) == {"s:2", *[f"l:2:0:{i}" for i in range(4)]}
          and sorted(terminal) == forced["zero_terminals"] and all(adj[v] == [Z] for v in terminal)
          and forced["descend"] == {"start": 18, "stop": "c", "other_zero_neighbor": "s:2",
                                    "degree_excess_if_s2_unselected": 0}
          and forced["selected_s2_s3_max_difference"] == 18 - 8 == 10, "zero forcing and selected edge bound")
    optional = set(eligible) - mandatory - {F}
    check(optional == {"s:0", B, T}, "exact remaining choices after the pins")
    # The selected edge bound d0<=10 excludes all unselected zero-neighbor slots.
    # Expand the optional choices by size, without revisiting the 9-vertex masks.
    named_choices = [optional, optional - {"s:0"}, optional - {B}, optional - {T},
                     {"s:0"}, {B}, {T}, set()]
    survivors = {}
    for extra in named_choices:
        named = mandatory | extra
        c = 19 - len(named)
        a = sum(census[v] for v in named) - len(named)
        if c-a <= 10 and 2 <= a <= 7:
            check((c, a) not in survivors, "uniqueness of the physical selection")
            survivors[c, a] = named
    check(sorted(survivors) == [(11, 6), (12, 3), (12, 5), (12, 6), (13, 3), (13, 5)], "six-case list")
    expected_rows = [{"a": a, "c": c, "k": 19-c, "d0": c-a,
                      "surviving_sets": [sorted(survivors[c, a])] if (c, a) in survivors else []}
                     for c in range(10, 19) for a in range(2, 9)]
    table = datum["subset_table"]
    check(table["pairs"] == expected_rows and table["subsets_visited"] == 2**len(eligible)
          and table["c10_selected_degree_sum"] == sum(census[v] for v in eligible) == 17
          and table["c10_required_a"] == 17 - 9 == 8, "63 pairs and c=10 elimination")
    return survivors


def audit_cases(receipts, high, adj, survivors):
    check(set(receipts) == {f"{c},{a}" for c, a in survivors}, "exact residual receipt keys")
    check(adj[U] == ["s:3"] and set(adj[F]) == {"s:3", "l:3:0:0", "l:3:0:1"}
          and set(adj["s:0"]) == {"s:1", H} and set(adj["s:2"]) == {Z, "s:1", "s:3"}
          and set(adj[B]) == {"s:1", "l:1:0:0", "l:1:0:1", "l:1:0:2"}
          and adj[T] == [H], "residual incidences")
    for (c, a), selected in survivors.items():
        unselected = set(high) - selected
        record = receipts[f"{c},{a}"]
        check(record["unselected_highs"] == sorted(unselected) and record["band"] == [1, c-a-1]
              and sum(len(adj[v]) for v in unselected) == c-a-1, "complete unselected band")

    fourth_lows = [7, 6]
    for key in ("11,6", "12,5", "12,6", "13,5"):
        check(receipts[key]["fourth_terminal_labels"] == fourth_lows
              and receipts[key]["fourth_terminal_weights"] == [10-low for low in fourth_lows],
              "fourth-terminal arithmetic")
    r = receipts["11,6"]
    check(r["unselected_highs"] == sorted([U, F]) and r["band"] == [1, 4]
          and r["repeated_label"] == 6 in fourth_lows, "11,6 terminal conflict")

    r = receipts["12,3"]
    blocked = [d for d in range(1, 9) if 11-d in (3, 8)]
    check(H not in adj[B] and "s:3" not in adj[B] and r["second_center_forbidden_weights"] == blocked == [3, 8]
          and r["fourth_terminal_labels"] == [10-d for d in blocked]
          and r["repeated_label"] == 7
          and (11-r["repeated_label"]) in (set(range(1, 9)) - {1, 2, *blocked}), "12,3 forced overlap")

    r = receipts["12,5"]
    check(r["first_attachment_weight"] == 11-5 == 6 and 10-5 == 5
          and r["forced_s1"] == 11-5 == r["repeated_label"] in fourth_lows, "12,5 blocked weight and overlap")
    r = receipts["12,6"]
    check(r["first_terminal_weight"] == 11-6 == 5 and r["repeated_label"] == 6 in fourth_lows,
          "12,6 single-terminal accounting")

    r = receipts["13,3"]
    get_gap = lambda values: max(values) - min(values)
    check(r["forced_s2"] == 18 and "s:1" in set(adj["s:2"]) & set(adj["s:0"])
          and r["gaps"] == [{"s0": v, "remaining_weights": w,
                            "required_gap": get_gap(w), "physical_gap": get_gap([v, 18])}
                           for v, w in [(14, [12, 14]), (15, [11, 15])]]
          and all(v-3 not in {11, 12, v} for v in (13, 16, 17))
          and all(x["required_gap"] != x["physical_gap"] for x in r["gaps"]), "13,3 selected-edge gap")

    r = receipts["13,5"]
    check(r["orderings"] == [{"s0": v, "first_terminal": w, "forced_s1": v-5, "repeated_label": v-5}
                             for v, w in ((11, 12), (12, 11))]
          and all({x["s0"]-5, x["first_terminal"]-5} == {6, 7}
                  and x["forced_s1"] in fourth_lows for x in r["orderings"]), "13,5 both orderings")


def audit_batch(datum):
    check(datum == {"m": 18, "d0": "c-a", "h_min": 1, "fixed_below_d0": [1, "d0-1"],
                    "forced_by_new": ["d0", "min(m,d0+h-1)"],
                    "forced_by_shift": ["d0+h", "m"], "predecessor": "w-h",
                    "necessary_spectrum": ["d0", "m"]}, "positive batch argument binding")
    # For each old cutoff w, let C(w) count selected old weights <= w.
    # The new prefix count equals w-C(w)+C(w-h)+clamp(w-d0+1,0,h).
    # Thus gracefulness forces C(w)=C(w-h)+clamp(...). By induction from
    # C(w)=0 at w<=0, the right side equals max(0,w-d0+1) for every h>=1,
    # using max(0,x-h)+min(h,max(0,x))=max(0,x).
    # These arithmetic probes exercise all d0 values with the smallest and
    # endpoint-spanning batches. They generate neither graphs nor labelings.
    checks = 0
    for d0 in sorted({c-a for c in range(10, 19) for a in range(2, 9)}):
        for h in sorted({1, 18-d0+1, 18-d0+2}):
            cut_counts = {w: 0 for w in range(1-h, 1)}
            for w in range(1, 19):
                cut_counts[w] = cut_counts[w-h] + min(h, max(0, w-d0+1))
            selected = [w for w in range(1, 19) if cut_counts[w] - cut_counts[w-1] == 1]
            check(selected == list(range(d0, 19)), "positive batch prefix identity")
            checks += 1
    return checks


def main():
    config = read(HERE / "config.json")
    ident = read(DATA / "identity.json")
    check(config["parent"] == ident["parent"] == PARENT and config["id"] == ident["id"]
          and config["domain"] == {"a": [2, 8], "c": [10, 18], "h_min": 1} and
          config["limits"] == {"workers": 1, "max_order": 19, "max_bytes": 2_000_000,
                               "max_named_subsets": 512, "solver_queries": 0, "graceful_labeling_enumeration": 0,
                               "historical_search_replay": 0, "new_graphs": 0, "new_enlarged_attempts": 0}, "frozen scope")
    check(config["retained"] == EXPECTED_INPUTS and ident["retained_sha256"] ==
          {p: sha(ROOT / p) for p in EXPECTED_INPUTS}, "retained source identities")
    for path in EXPECTED_INPUTS:
        check((ROOT / path).read_bytes() == blob(path), path)
    expected_sources = {"lcl/__init__.py", "lcl/verify.py", "pyproject.toml", "requirements.txt"}
    check(set(config["sources"]) == set(ident["sources_sha256"]) == expected_sources, "source inventory")
    for path, expected in ident["sources_sha256"].items():
        snapshot = DATA / "source" / path
        check(sha(snapshot) == sha(ROOT / path) == expected
              and snapshot.read_bytes().replace(b"\r\n", b"\n") == blob(path).replace(b"\r\n", b"\n"), path)
    expected_files = {PROOF, *[(HERE / name).relative_to(ROOT).as_posix() for name in
                       ("config.json", "commands.json", "validate.py", "audit.py")]}
    check(ident["inputs_sha256"] == {path: sha(ROOT / path) for path in expected_files}, "task input identities")
    check(ident["runtime"] == {"version": sys.version, "platform": platform.platform(),
                               "implementation": sys.implementation.name, "utf8_mode": 1,
                               "python": ".venv/Scripts/python.exe", "optional_dependencies": []}
          and sys.flags.utf8_mode == 1 and sys.version_info[:2] in ((3, 12), (3, 13)), "runtime identity")

    original, same, previous, pos_graph, query, seed = [read(ROOT / p) for p in EXPECTED_INPUTS]
    records = read(DATA / "controls.json")
    check(set(records) == {"1342_previous_u10", "1122_positive"}, "retained controls only")
    neg, pos = records["1342_previous_u10"], records["1122_positive"]
    check(original == same and previous["original"]["graph_digest"] == original["graph_digest"] == neg["graph_digest"]
          and previous["original"]["sha256_raw"] == sha(ROOT / EXPECTED_INPUTS[1])
          and previous["labels"] == neg["labels"] and previous["edge_ledger"] == neg["edge_ledger"]
          and previous["witness"] == neg["facts"]["witness"]
          and previous["witness_distances"] == neg["facts"]["witness_distances"], "1342 original/certificate binding")
    high, adj = audit_graph([1,3,4,2], original["graph"], previous["verification"], neg, 9, {U: 10, H: 1, Z: 0})
    check(query["original_graph"] == pos_graph and query["classification"] == "SAT"
          and query["original_graph_digest"] == pos["graph_digest"]
          and query["certificate"] == seed["certificate"]
          and pos["labels"] == query["result"]["witness"] == seed["normalized"]["labels"]
          and seed["source"] == {"path": EXPECTED_INPUTS[4], "sha256_raw": sha(ROOT / EXPECTED_INPUTS[4]),
                                 "graph_digest": pos["graph_digest"]}, "1122 original/certificate binding")
    audit_graph([1,1,2,2], pos_graph, seed["certificate"], pos, 7, {U: 8, H: 4, Z: 0})
    selected = sorted(v for v, g in pos["labels"].items() if g > 8)
    ledger = [item for item in pos["edge_ledger"] if set(item["edge"]).intersection(selected)]
    weights = sorted(row["difference"] for row in ledger)
    check(pos["predicate"] == {"c": 9, "selected": selected, "ledger": ledger, "spectrum": weights}
          and ledger == seed["normalized"]["selected_incident_edges"]
          and weights == list(range(5,15)), "1122 complete positive premise")

    datum = read(DATA / "structural.json")
    survivors = audit_reduction(datum, high, adj)
    audit_cases(datum["contradictions"], high, adj, survivors)
    batches = audit_batch(datum["batch_necessity"])
    guards = read(DATA / "invalid_inputs.json")
    expect = [("a", [True,1,9,2.0,"2"]), ("c", [True,9,19,10.0,"10"]), ("h",[True,0,-1,1.0,"1"])]
    expected_probes = []
    for i, (name, values) in enumerate(expect):
        for value in values:
            trial = [2, 10, 1]
            trial[i] = value
            expected_probes.append({"input": trial, "parameter": name, "type": type(value).__name__, "evaluation_calls": 0})
    check(json.dumps(guards, sort_keys=True) == json.dumps(expected_probes, sort_keys=True), "typed and range guard receipts")
    summary = read(DATA / "summary.json")
    check(summary == {"status": "PASS", "id": config["id"], "limits": config["limits"], "retained_graph_records": 2,
                      "pairs": 63, "pairs_excluded_by_reduction": 57, "residual_cases": 6,
                      "subsets_visited": 512, "input_rejections": 15}, "exact totals")
    expected_outputs = {"identity.json", "controls.json", "structural.json", "invalid_inputs.json", "summary.json",
                        *["source/" + p for p in expected_sources]}
    check({f.relative_to(DATA).as_posix() for f in DATA.rglob("*") if f.is_file()} == expected_outputs
          and all((DATA / f).stat().st_size <= config["limits"]["max_bytes"] for f in expected_outputs), "output inventory and byte cap")
    result = {"status": "PASS", "id": config["id"], "retained_graph_records": 2, "pairs": 63,
              "residual_cases": 6, "batch_arithmetic_probes": batches, "rechecked_guards": 15,
              "audited_sha256": {f: sha(DATA / f) for f in sorted(expected_outputs)},
              "new_graph_records": 0, "solver_queries": 0, "labeling_enumeration": 0, "historical_search_replay": 0}
    raw = (json.dumps(result, sort_keys=True, indent=2) + "\n").encode()
    check(len(raw) <= config["limits"]["max_bytes"], "audit result byte cap")
    with (HERE / "audit_result.json").open("xb") as handle:
        handle.write(raw)
    print(json.dumps({k: v for k, v in result.items() if k != "audited_sha256"}, sort_keys=True))


if __name__ == "__main__":
    main()
