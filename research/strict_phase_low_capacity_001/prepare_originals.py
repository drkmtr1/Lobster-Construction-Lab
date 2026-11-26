"""Freeze D191 named topology and construct only the admitted D157 input prefix."""

from collections import Counter, deque
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "evidence/validation/LCL_ORDINARY_SPINE_LOW_CAPACITY_STRICT_PHASE_MATCHED_001_PREP"
PREFIX_74 = ROOT / (
    "evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_MATCHED_001_PREP"
    "/input/prefix.json"
)
PREFIX_74_SHA = "f48b56479dac85e1ddbbd36e5f6a6a3eaf94b9b32497e677fe5a96932abbac95"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def write_new(path, value):
    with path.open("xb") as stream:
        stream.write(canonical(value) + b"\n")


def independent_identity(graph, profile):
    # Recover parent links from physical section/branch/terminal indices.
    members = set()
    links = set()
    roles = {}
    for section, quotas in enumerate(profile):
        spine = f"s:{section}"
        members.add(spine)
        roles[spine] = {"section": section, "kind": "spine"}
        if section > 0:
            links.add(tuple(sorted((f"s:{section - 1}", spine))))
        for index, quota in enumerate(quotas):
            child = f"b:{section}:{index}"
            members.add(child)
            roles[child] = {"section": section, "kind": "branch", "branch": index}
            links.add(tuple(sorted((spine, child))))
            for terminal in range(quota):
                name = f"l:{section}:{index}:{terminal}"
                members.add(name)
                roles[name] = {"section": section, "kind": "leaf", "branch": index, "leaf": terminal}
                links.add(tuple(sorted((child, name))))
    spine = [f"s:{i}" for i in range(len(profile))]
    assert graph["schema_version"] == 1 and graph["profile"] == profile
    assert graph["spine"] == spine and graph["roles"] == roles
    assert len(graph["vertices"]) == len(members) and set(graph["vertices"]) == members
    assert len(graph["edges"]) == len(links) and {tuple(sorted(edge)) for edge in graph["edges"]} == links
    payload = {"vertices": sorted(members), "edges": sorted(links),
               "profile": profile, "spine": spine, "roles": roles}
    return hashlib.sha256(canonical(payload)).hexdigest()


def verify_prefix(graph, labels, cut, crossing, noncrossing, frontier):
    # Direct calculation only. No original-checker entry point is used.
    vertices = set(graph["vertices"])
    size = len(graph["edges"])
    assert len(vertices) == size + 1 and vertices == set(labels)
    assert all(type(value) is int for value in labels.values())
    assert sorted(labels.values()) == list(range(size + 1))
    spine = graph["spine"]
    assert len(set(spine)) == len(spine) and spine[-1] == frontier and labels[frontier] == size
    adjacency = {name: set() for name in vertices}
    cut_diffs, other_diffs = [], []
    for u, v in graph["edges"]:
        assert u != v and v not in adjacency[u]
        adjacency[u].add(v)
        adjacency[v].add(u)
        band = cut_diffs if (labels[u] < cut) != (labels[v] < cut) else other_diffs
        band.append(abs(labels[u] - labels[v]))
    assert sorted(cut_diffs) == list(range(*crossing))
    assert sorted(other_diffs) == list(range(*noncrossing))
    assert all(v in adjacency[u] for u, v in zip(spine, spine[1:]))
    distance = dict.fromkeys(spine, 0)
    pending = deque(spine)
    while pending:
        here = pending.popleft()
        for child in adjacency[here]:
            if child not in distance:
                distance[child] = 1 + distance[here]
                pending.append(child)
    assert distance.keys() == vertices and max(distance.values()) == 2


def matched_suffixes():
    strata = (
        ("III", [3, 2, 1], [4, 1, 1], [0]),
        ("II", [3, 3, 0], [4, 2, 0], [0]),
        ("I", [3, 2, 0], [4, 1, 0], []),
    )
    for stratum, low, companion, direct in strata:
        for total in range(6, 17, 2):
            for p in range(2, total - 1):
                q = total - p
                yield f"{stratum}-{p:02}-{q:02}", stratum, low, companion, [p, q, *direct]
    for p in (5, 7):
        yield f"boundary-{p:02}-01", "boundary", [3, 2, 0], [4, 1, 0], [p, 1]


def return_labels(prefix):
    # D157 return with (r,t,p)=(2,1,1), A=3, B=4, s=13, k=7, J=16.
    assert prefix["frontier"] == "s:27" and prefix["actual_cut"] == 39
    minimum = {name: 74 - value for name, value in prefix["actual_labels"].items()}
    label = {name: value + (3 if value < 36 else 16) for name, value in minimum.items()}
    label.update({"s:28": 91, "s:29": 0,
                  "b:28:0": 2, "b:28:1": 1, "b:29:0": 92, "b:29:1": 93, "b:29:2": 94})
    sources = {
        (28, 0): (0, 1, 2, 3, 6),
        (28, 1): (4, 11),
        (29, 0): (5, 12),
        (29, 1): (7, 8, 9, 10),
    }
    assert sorted(i for indices in sources.values() for i in indices) == list(range(13))
    for (section, branch), indices in sources.items():
        for terminal, source in enumerate(indices):
            label[f"l:{section}:{branch}:{terminal}"] = 39 + source
    return {name: 94 - value for name, value in label.items()}


def main():
    start_cpu, start_wall = time.process_time(), time.perf_counter()
    # The unchanged original builder is the sole project import.
    sys.path.insert(0, str(ROOT))
    from lcl.model import build_graph, graph_digest

    assert sys.flags.dont_write_bytecode
    raw = PREFIX_74.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PREFIX_74_SHA
    prefix74 = json.loads(raw)
    profile74 = prefix74["graph"]["profile"]
    digest74 = independent_identity(prefix74["graph"], profile74)
    assert graph_digest(build_graph(profile74)) == digest74 == prefix74["digest"]
    verify_prefix(prefix74["graph"], prefix74["actual_labels"], 39, (37, 75), (1, 37), "s:27")
    profile94 = [*profile74, [5, 2], [2, 4, 0]]
    graph94 = build_graph(profile94)
    digest94 = independent_identity(graph94, profile94)
    assert graph_digest(graph94) == digest94
    ARTIFACT.mkdir(parents=True, exist_ok=True)
    write_new(ARTIFACT / "prefix94-original.json", {"digest": digest94, "graph": graph94})
    matches = list(matched_suffixes())
    assert Counter(row[1] for row in matches) == {"I": 48, "II": 48, "III": 48, "boundary": 2}
    counts = Counter()
    all_digests = set()
    with (ARTIFACT / "originals.jsonl").open("xb") as stream:
        for phase, profile, digest in (("S0", profile94, digest94), ("S-1", profile74, digest74)):
            for key, stratum, low, companion, second in matches:
                for arm, first in (("low", low), ("companion", companion)):
                    suffix = [first, second]
                    full = [*profile, *suffix]
                    original = build_graph(full)
                    target_digest = independent_identity(original, full)
                    assert graph_digest(original) == target_digest and target_digest not in all_digests
                    all_digests.add(target_digest)
                    fresh = len(original["edges"]) - (94 if phase == "S0" else 74)
                    assert fresh == 2 + sum(len(row) + sum(row) for row in suffix)
                    assert fresh % 2 == 0 and fresh <= (94 if phase == "S0" else 74)
                    record = {"phase": phase, "match": key, "stratum": stratum, "arm": arm,
                              "suffix": suffix, "graph": original, "digest": target_digest,
                              "prefix_digest": digest, "fresh_edges": fresh}
                    stream.write(canonical({"record": record,
                                            "record_sha256": hashlib.sha256(canonical(record)).hexdigest()}) + b"\n")
                    counts[(phase, arm)] += 1
    assert set(counts.values()) == {146} and len(all_digests) == 584
    # Original graph and target records are frozen before any new label construction.
    labels = return_labels(prefix74)
    verify_prefix(graph94, labels, 49, (48, 95), (1, 48), "s:29")
    write_new(ARTIFACT / "prefix94.json", {"digest": digest94, "actual_labels": labels, "actual_cut": 49,
                "minimum_cut": 46, "edges": 94, "vertices": 95, "frontier": "s:29",
                "crossing": [48, 94], "noncrossing": [1, 47], "phase": "S0",
                "prefix74_identity": {"sha256": PREFIX_74_SHA, "digest": digest74}})
    print(json.dumps({"target_records": len(all_digests), "prefix74_digest": digest74,
                      "prefix94_digest": digest94, "cpu_seconds": time.process_time() - start_cpu,
                      "observed_process_wall_seconds": time.perf_counter() - start_wall}))


if __name__ == "__main__":
    main()
