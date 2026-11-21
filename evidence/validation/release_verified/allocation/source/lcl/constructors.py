"""Direct retained constructions: no successful full labeling is an input.

These routines implement restricted theorems; a failed domain check says
nothing about ordinary gracefulness of the requested graph.
"""

from __future__ import annotations

from .model import (_integer, branched_prefix_profile, build_graph, graph_digest,
                    normalize_profile)


BOUNDED_COMMIT = "e48b94eec4091b4fe189e325cab2eda464409943"
SOURCE_BASE = f"https://github.com/drkmtr1/MDL_Bounded_Search/blob/{BOUNDED_COMMIT}/"


def _result(graph: dict, labels: dict[str, int], method: str, scope: dict, trace: list) -> dict:
    # A local development assertion is not the independent certificate checker.
    m = len(graph["edges"])
    if set(labels) != set(graph["vertices"]) or sorted(labels.values()) != list(range(m + 1)):
        raise ArithmeticError(f"{method}: constructed vertex inventory is inconsistent")
    differences = [abs(labels[u] - labels[v]) for u, v in graph["edges"]]
    if sorted(differences) != list(range(1, m + 1)):
        raise ArithmeticError(f"{method}: constructed difference inventory is inconsistent")
    return {"status": "CONSTRUCTED", "graph": graph, "graph_digest": graph_digest(graph),
            "labels": labels, "method": method, "claim_scope": scope, "trace": trace,
            "evidence_level": "retained_construction_implementation; independent checking required"}


def _consume_suffix(graph: dict, start: int, labels: dict[str, int], low: int, high: int,
                    trace: list) -> None:
    """Apply the proved endpoint interval invariant to an all-q=0 suffix."""
    profile = graph["profile"]
    for i in range(start, len(profile)):
        parent = f"s:{i}"
        a = labels[parent]
        for j, q in enumerate(profile[i]):
            if q != 0:
                raise ValueError("caterpillar suffix must have only q=0 branches in this representation")
            if low > high or a not in (low - 1, high + 1):
                raise ArithmeticError("caterpillar interval invariant was not supplied")
            x = high if a == low - 1 else low
            leaf = f"b:{i}:{j}"
            labels[leaf] = x
            trace.append({"operation": "direct_leaf", "parent": parent, "vertex": leaf,
                          "label": x, "difference": abs(a - x)})
            if x == high:
                high -= 1
            else:
                low += 1
        if i + 1 < len(profile):
            if low > high or a not in (low - 1, high + 1):
                raise ArithmeticError("next-spine interval invariant was not supplied")
            x = high if a == low - 1 else low
            following = f"s:{i + 1}"
            labels[following] = x
            trace.append({"operation": "next_spine", "parent": parent, "vertex": following,
                          "label": x, "difference": abs(a - x)})
            if x == high:
                high -= 1
            else:
                low += 1
    if low <= high:
        raise ArithmeticError("caterpillar suffix did not exhaust the declared resources")


def caterpillar(profile: list[list[int]]) -> dict:
    """Construct an all-direct-leaf profile, including the zero-edge singleton."""
    profile = normalize_profile(profile)
    if any(q != 0 for section in profile for q in section):
        raise ValueError("outside caterpillar constructor domain: every supplied q must be zero")
    graph = build_graph(profile)
    m = len(graph["edges"])
    labels = {"s:0": 0}
    trace: list = []
    _consume_suffix(graph, 0, labels, 1, m, trace)
    return _result(graph, labels, "caterpillar", {
        "family": "profiles with only direct leaves on the supplied spine",
        "independent_input_supply": True, "universal_lobster_claim": False,
        "source": SOURCE_BASE + "MATHEMATICS.md#6-caterpillar-interval-baseline"}, trace)


def l007(q: int, r: int, z: int = 0) -> dict:
    """L007: r equal q-leaf branches, z direct leaves, one terminal spine edge."""
    _integer(q, "q", 1)
    _integer(r, "r", 1)
    _integer(z, "z")
    s = q + 1
    graph = build_graph([[q] * r + [0] * z, []])
    labels = {"s:0": 0, "s:1": s * r + 1}
    for i in range(1, r + 1):
        labels[f"b:0:{i - 1}"] = s * i
        for j in range(1, q + 1):
            labels[f"l:0:{i - 1}:{j - 1}"] = s * (r - i) + j
    for j in range(z):
        labels[f"b:0:{r + j}"] = s * r + 2 + j
    return _result(graph, labels, "l007", {
        "parameters": {"q": q, "r": r, "z": z},
        "family": "equal positive branch sizes; isolated cluster plus terminal next edge",
        "independent_input_supply": True, "later_suffix_supplied": False,
        "universal_lobster_claim": False, "source": SOURCE_BASE + "research/LEMMAS.md"},
        [{"operation": "formula", "center": "(q+1)*i", "leaf": "(q+1)*(r-i)+j"}])


def _suffix_input(qs: list[int], z: int, suffix_profile: list[list[int]]) -> tuple[list[int], list[list[int]], int]:
    if not isinstance(qs, list) or not qs:
        raise ValueError("qs must be a nonempty list of positive branch sizes")
    qs = [_integer(q, f"qs[{i}]", 1) for i, q in enumerate(qs)]
    _integer(z, "z")
    suffix = normalize_profile(suffix_profile)
    if any(q != 0 for section in suffix for q in section):
        raise ValueError("suffix must have only direct leaves (q=0) on its supplied spine")
    K = len(suffix) - 1 + sum(len(section) for section in suffix)
    if K < 1:
        raise ValueError("outside suffix construction domain: suffix must have K>=1 internal edges")
    return qs, suffix, K


def _branched_section(qs: list[int], z: int, suffix: list[list[int]], K: int,
                      starts: list[int], centers: list[int], method: str, conditions: dict) -> dict:
    graph = build_graph([qs + [0] * z] + suffix)
    m = len(graph["edges"])
    labels = {"s:0": 0, "s:1": K + 1}
    for i, (q, t, b) in enumerate(zip(qs, starts, centers)):
        labels[f"b:0:{i}"] = b
        for j in range(q):
            labels[f"l:0:{i}:{j}"] = t + j
    high_unused = sorted(set(range(K + 2, m + 1)) - set(labels.values()))
    if len(high_unused) != z:
        raise ArithmeticError("branch formula failed its distinct high-label inventory")
    for j, label in enumerate(high_unused):
        labels[f"b:0:{len(qs) + j}"] = label
    prefix = dict(labels)
    trace = [{"operation": "supplied_suffix_interface", "active_vertex": "s:1",
              "active_label": K + 1, "unused_labels": list(range(1, K + 1)),
              "unused_differences": list(range(1, K + 1)), "prefix_labels": prefix}]
    _consume_suffix(graph, 1, labels, 1, K, trace)
    source = ("research/verification/pilot_inputs/H010-proof.txt" if method == "h010"
              else "research/LEMMAS.md")
    return _result(graph, labels, method, {
        "parameters": {"qs": qs, "z": z, "suffix_profile": suffix, "K": K},
        "conditions": conditions, "independent_input_supply": True,
        "suffix_interface": {"unused_labels": [1, K], "unused_differences": [1, K],
                             "active_label": K + 1, "notation": "inclusive intervals"},
        "family": "one branched section followed by a supplied all-q=0 caterpillar suffix",
        "arbitrary_branched_suffix": False, "universal_lobster_claim": False,
        "source": SOURCE_BASE + source}, trace)


def h010(qs: list[int], z: int, suffix_profile: list[list[int]]) -> dict:
    """H010's packed leaf intervals; preserves the original supplied topology."""
    qs, suffix, K = _suffix_input(qs, z, suffix_profile)
    Q, r = sum(qs), len(qs)
    required_z = max(0, K + 2 + Q - qs[-1] - r)
    if Q > K + 2:
        raise ValueError(f"outside H010 domain: sum(qs)={Q} exceeds K+2={K + 2}")
    if z < required_z:
        raise ValueError(f"outside H010 domain: z={z}; this recipe requires z>={required_z}")
    starts = []
    cursor = K + 2
    for q in qs:
        starts.append(cursor)
        cursor += q
    centers = [2 * t + q - 1 for t, q in zip(starts, qs)]
    return _branched_section(qs, z, suffix, K, starts, centers, "h010",
                             {"sum_qs_at_most_K_plus_2": True, "required_z": required_z,
                              "bound_is_necessary_for_all_labelings": False})


def l010(qs: list[int], z: int, suffix_profile: list[list[int]]) -> dict:
    """L010's separated blocks, with its explicit sufficient budget test."""
    qs, suffix, K = _suffix_input(qs, z, suffix_profile)
    m = K + 1 + sum(q + 1 for q in qs) + z
    starts, centers = [], []
    t = K + 2
    for q in qs:
        b = 2 * t + q - 1
        starts.append(t)
        centers.append(b)
        t = b + 1
    required_z = max(0, centers[-1] - (K + 1 + sum(q + 1 for q in qs)))
    if m < centers[-1]:
        raise ValueError(f"outside L010 domain: final alphabet m={m} < last center={centers[-1]}; z>={required_z} required")
    return _branched_section(qs, z, suffix, K, starts, centers, "l010",
                             {"last_center": centers[-1], "final_m": m, "required_z": required_z,
                              "bound_is_necessary_for_all_labelings": False})


def _one_branch_prefix_labels(q: int, z: int, K: int, section: int) -> dict[str, int]:
    """L010's one-branch PREFIX, leaving labels/differences 1..K untouched.

    This helper asserts no topology for that pending suffix.  The caller must
    supply a valid consumer; in particular it does not call the full l010()
    constructor with an out-of-domain branched suffix.
    """
    if z < K + 1:
        raise ValueError("one-branch L010 prefix requires z>=K+1")
    m, t, center = K + q + z + 2, K + 2, 2 * K + q + 3
    labels = {f"s:{section}": 0, f"s:{section + 1}": K + 1,
              f"b:{section}:0": center}
    for j in range(q):
        labels[f"l:{section}:0:{j}"] = t + j
    direct = sorted(set(range(K + 2, m + 1)) - set(labels.values()))
    if len(direct) != z:
        raise ArithmeticError("one-branch prefix high-label inventory failed")
    for j, x in enumerate(direct, start=1):
        labels[f"b:{section}:{j}"] = x
    return labels


def two_section_padded(q: int, r: int, z0: int, z1: int, K: int) -> dict:
    """Compose retained L010 prefixes on two exact padded branched sections.

    Requires q,r,K>=1, z1>=K+1, z0>=r+z1+K+3.  These are sufficient
    budgets for this composition, not necessary conditions for gracefulness.
    This is a new implementation of a retained-formula corollary, with no
    mathematical novelty or arbitrary-lobster claim.
    """
    _integer(q, "q", 1)
    _integer(r, "r", 1)
    _integer(K, "K", 1)
    _integer(z0, "z0")
    _integer(z1, "z1")
    K1 = r + z1 + K + 2
    if z1 < K + 1:
        raise ValueError(f"outside composed L010 domain: z1={z1}; z1>={K + 1} required")
    if z0 < K1 + 1:
        raise ValueError(f"outside composed L010 domain: z0={z0}; z0>={K1 + 1} required")
    graph = build_graph(branched_prefix_profile(q, r, z0, z1, K))
    labels = _one_branch_prefix_labels(q, z0, K1, 0)
    trace = [{"operation": "supplied_interval_interface", "stage": 1,
              "active_vertex": "s:1", "active_label": K1 + 1,
              "unused_labels": list(range(1, K1 + 1)),
              "unused_differences": list(range(1, K1 + 1)),
              "prefix_labels": dict(labels)}]
    local_second = _one_branch_prefix_labels(r, z1, K, 1)
    second = {vertex: K1 + 1 - value for vertex, value in local_second.items()}
    if labels["s:1"] != second["s:1"]:
        raise ArithmeticError("composed prefixes disagree at the shared physical spine vertex")
    labels.update(second)
    low, high = K1 - K + 1, K1
    trace.append({"operation": "supplied_interval_interface", "stage": 2,
                  "map": "global_label = K1 + 1 - local_label", "K1": K1,
                  "active_vertex": "s:2", "active_label": K1 - K,
                  "unused_labels": list(range(low, high + 1)),
                  "unused_differences": list(range(1, K + 1)),
                  "prefix_labels": dict(labels)})
    _consume_suffix(graph, 2, labels, low, high, trace)
    result = _result(graph, labels, "two_section_padded", {
        "parameters": {"q": q, "r": r, "z0": z0, "z1": z1, "K": K, "K1": K1},
        "family": "two one-positive-branch sections with supplied direct leaves and a K-edge path suffix",
        "conditions": {"required_z1": K + 1, "required_z0": K1 + 1,
                       "bound_is_necessary_for_all_labelings": False},
        "independent_input_supply": True, "universal_lobster_claim": False,
        "arbitrary_branched_suffix": False,
        "suffix_interface": {"unused_labels": [low, high], "unused_differences": [1, K],
                             "active_label": low - 1, "notation": "inclusive intervals"},
        "derivation_status": "composition corollary of retained L010 prefixes and the caterpillar invariant",
        "mathematical_novelty_claim": False,
        "source": SOURCE_BASE + "research/LEMMAS.md",
        "interval_source": SOURCE_BASE + "MATHEMATICS.md#6-caterpillar-interval-baseline"}, trace)
    result["evidence_level"] = "retained_formula_composition_corollary; independent checking required"
    return result
