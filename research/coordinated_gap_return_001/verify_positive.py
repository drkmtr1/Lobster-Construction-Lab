"""Exact independent witness and continuation receipts, inactive during preparation."""


def require(condition, description):
    if not condition:
        raise ValueError(description)


def edge_rows(graph, labels, cut):
    return [
        {"ends": [u, v], "labels": [labels[u], labels[v]],
         "weight": abs(labels[u] - labels[v]),
         "crosses": (labels[u] < cut) != (labels[v] < cut)}
        for u, v in graph["edges"]
    ]


def exact_state(graph, labels, cut, threshold):
    size = len(graph["edges"])
    require(set(labels) == set(graph["vertices"]), "original vertex coverage")
    require(all(type(x) is int for x in labels.values()), "exact integer labels")
    require(sorted(labels.values()) == list(range(size + 1)), "label alphabet")
    rows = edge_rows(graph, labels, cut)
    require(sorted(row["weight"] for row in rows) == list(range(1, size + 1)),
            "exact difference alphabet")
    require(all(row["crosses"] == (row["weight"] >= threshold) for row in rows),
            "exact crossing spectrum")
    mirrored = {v: size - x for v, x in labels.items()}
    mirror_cut = size + 1 - cut
    mirror = edge_rows(graph, mirrored, mirror_cut)
    require(all((x["weight"], x["crosses"]) == (y["weight"], y["crosses"])
                for x, y in zip(rows, mirror, strict=True)), "physical complement")
    return {
        "size": size, "threshold": threshold, "actual_labels": dict(labels),
        "actual_cut": cut, "actual_edges": rows,
        "complementary_labels": mirrored, "complementary_cut": mirror_cut,
        "complementary_edges": mirror,
    }


def inventory_partition(graph, state, old_names):
    old_names = frozenset(old_names)
    new_names = set(graph["vertices"]) - old_names
    record = {}
    for side in ("actual", "complementary"):
        labels = state[side + "_labels"]
        cut = state[side + "_cut"]
        rows = state[side + "_edges"]
        old_rows = [row for row in rows if set(row["ends"]) <= old_names]
        new_rows = [row for row in rows if not set(row["ends"]) <= old_names]
        connector, = [row for row in new_rows if old_names.intersection(row["ends"])]
        entry = {"cut": cut, "literal_connector": connector}
        for name, vertices, edges in (("old", old_names, old_rows), ("remaining", new_names, new_rows)):
            entry[name] = {
                "names": sorted(vertices), "lower_labels": sorted(labels[v] for v in vertices if labels[v] < cut),
                "upper_labels": sorted(labels[v] for v in vertices if labels[v] >= cut),
                "crossing_weights": sorted(row["weight"] for row in edges if row["crosses"]),
                "noncrossing_weights": sorted(row["weight"] for row in edges if not row["crosses"]),
            }
        record[side] = entry
    return record


def changed_resources(before_rows, after_rows, labels_before, c_before, labels_after, c_after):
    old_after = {tuple(row["ends"]): row for row in after_rows}
    return {
        "old_side_changes": sorted(v for v, x in labels_before.items()
                                   if (x < c_before) != (labels_after[v] < c_after)),
        "old_crossing_changes": [
            {"before": row, "after": old_after[tuple(row["ends"])]}
            for row in before_rows
            if row["crosses"] != old_after[tuple(row["ends"])]["crosses"]
        ],
    }


def transport_records(states, graphs, maps, installed):
    write_once = {}
    output = []
    for i, (state, graph, mapping) in enumerate(zip(states, graphs, maps, strict=True)):
        m = state["size"]
        names = set(graph["vertices"]) - (set(graphs[i - 1]["vertices"]) if i else set())
        local = state["actual_labels"]
        require(all(mapping(label) == installed[v] for v, label in local.items()), "pointwise transport")
        require(all(abs(mapping(local[v]) - mapping(local[u])) == abs(installed[v] - installed[u])
                    for u, v in graph["edges"]), "edge transport")
        actual_born = {v: mapping(local[v]) for v in sorted(names)}
        require(not set(write_once).intersection(actual_born), "write-once birth membership")
        write_once.update(actual_born)
        actual_map = [mapping(x) for x in range(m + 1)]
        output.append({"boundary_edges": m, "actual_pointwise_map": actual_map,
                       "complementary_pointwise_map": [48 - actual_map[m - x] for x in range(m + 1)],
                       "actual_born_labels": actual_born,
                       "complementary_born_labels": {v: 48 - x for v, x in actual_born.items()}})
    require(write_once == installed, "installed alphabet equals the disjoint union of births")
    return output


def verify_future_positive(candidate, original_records, prefix):
    """Only for an authorized run; independently check the actual 41/48 originals."""
    from lcl.verify import verify_certificate

    target = original_records["main_41"]["original"]
    suffix_target = original_records["main_48_if_admitted"]["original"]
    incoming = original_records["main_41"]["prefixes"][0]["graph"]
    graph = target["graph"]
    suffix = suffix_target["graph"]
    old = prefix["state"]["minimum_labels"]
    labels = dict(candidate["labels"])
    cut = candidate["cut"]
    require(cut in (18, 19) and labels["s:6"] == 0, "registered residual branch")
    ordered = sorted(old, key=old.__getitem__)
    embedding = [labels[v] for v in ordered]
    require(all(x < y for x, y in zip(embedding, embedding[1:])), "strictly increasing old labels")
    gaps = [y - x - 1 for x, y in zip(embedding, embedding[1:])]
    require(embedding[0] + sum(gaps) + (41 - embedding[-1]) == 9, "exact width inventory")
    require(sum(x < cut for x in embedding) == 14, "induced old bracket")
    threshold = cut + 2
    initial = exact_state(incoming, old, 20, 12)
    state = exact_state(graph, labels, cut, threshold)

    # D196 with actual minimum input, a=3,F=3,k=0, two opposite shifts and one identity.
    def lift(x):
        return 3 + x + 3 * (x >= cut)

    installed = {v: lift(x) for v, x in labels.items()}
    installed["s:7"] = 48
    for j, gap_position in enumerate((0, 2, 1)):
        installed[f"b:7:{j}"] = j
        installed[f"l:7:{j}:0"] = cut + 3 + gap_position
    suffix_state = exact_state(suffix, installed, cut + 3, threshold)
    require(installed["s:7"] == 48, "actual D196 frontier")
    checks = [verify_certificate(graph, labels, target["digest"]),
              verify_certificate(suffix, installed, suffix_target["digest"])]
    require(all(row["valid"] for row in checks), "protected original-target checker")

    named_ranks = sorted(initial["actual_edges"], key=lambda row: row["weight"])
    installed_old = {tuple(row["ends"]): row for row in state["actual_edges"]}
    old_rows = [{"rank": row["weight"], **installed_old[tuple(row["ends"])]} for row in named_ranks]
    inversions = [[r["rank"], s["rank"]] for i, r in enumerate(old_rows)
                  for s in old_rows[i + 1:] if r["weight"] > s["weight"]]
    rank_class = "rank_changing" if inversions else "rank_preserving"
    require(candidate["rank_class"] == rank_class, "actual edge rank classification")
    old_names = set(old)
    section_names = set(labels)
    return {
        "status": "INDEPENDENTLY_VERIFIED_POSITIVE", "rank_class": rank_class, "actual_old_edges": old_rows,
        "rank_inversions": inversions, "old_map": embedding, "gap_widths": gaps,
        "lower_exterior": embedding[0], "upper_exterior": 41 - embedding[-1],
        "states": [state, suffix_state], "normalized_suffix": [48, 46 - cut, threshold],
        "checker_results": checks,
        "local_inventories": [inventory_partition(graph, state, old_names),
                              inventory_partition(suffix, suffix_state, section_names)],
        "final_inventories": [inventory_partition(suffix, suffix_state, old_names),
                              inventory_partition(suffix, suffix_state, section_names)],
        "changed_resources": [
            changed_resources(initial["actual_edges"], state["actual_edges"], old, 20, labels, cut),
            changed_resources(state["actual_edges"], suffix_state["actual_edges"], labels, cut, installed, cut + 3),
        ],
        "transport": transport_records([initial, state, suffix_state], [incoming, graph, suffix],
                                       [lambda x: lift(embedding[x]), lift, lambda x: x], installed),
    }
