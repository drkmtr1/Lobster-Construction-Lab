"""Primary exterior slot traversal for the two-first-center stratum."""
from itertools import permutations


def exterior_candidates(case, arm, meter, prunes):
    if arm not in ("T", "E"):
        raise ValueError("unknown arm")
    roles = case.graph["roles"]
    profile = case.graph["profile"]
    first, second = profile[-2:]
    if (len(first) != 2 or any(q < 2 or q % 2 for q in first)
            or len(second) != 3 or second[0] < 2 or second[0] % 2
            or second[1] < 3 or not second[1] % 2 or second[2] != 0):
        raise ValueError("outside frozen two-first-center domain")
    centers = tuple(
        tuple(sorted((name for name in case.compulsory if case.parents[name] == spine
                      and roles[name]["kind"] == "branch"), key=lambda name: roles[name]["branch"]))
        for spine in (case.u, case.w)
    )
    if tuple(map(len, centers)) != (2, 2):
        raise ValueError("wrong physical centers")
    direct, = (name for name in case.optional if name not in case.terminals)
    if case.parents[direct] != case.w:
        raise ValueError("wrong physical direct-leaf parent")
    leaves = {host: tuple(sorted((name for name in case.terminals if case.parents[name] == host),
                                 key=lambda name: roles[name]["leaf"]))
              for group in centers for host in group}
    if tuple(len(leaves[host]) for group in centers for host in group) != tuple(first + second[:2]):
        raise ValueError("centers and named quotas disagree")

    def reject(reason):
        prunes[reason] = prunes.get(reason, 0) + 1

    max_A = 1 + (second[0] + second[1] + 1)//2
    max_B = 2 + sum(first)//2
    for e in (0, 1):
        a_values = (3,) if arm == "T" else range(3, max_A+1)
        b_values = (3 + e,) if arm == "T" else range(3 + e, max_B+1)
        for A in a_values:
            for B in b_values:
                meter.tick("exterior_nodes")
                if A+B > case.k_total:
                    reject("combined-width")
                    continue
                # The range endpoints are exactly the D153 widths.
                high_roles = centers[1] + ((direct,) if e else ())
                high_slots = tuple(range(A+2, A+B+1))
                for first_labels in permutations(range(1, A), 2):
                    meter.tick("exterior_nodes")
                    if A-1 not in first_labels:
                        reject("forced-weight-two")
                        continue
                    for upper_labels in permutations(high_slots, len(high_roles)):
                        meter.tick("exterior_nodes")
                        if A+B not in upper_labels:
                            reject("maximum-physical-neighbor")
                            continue
                        if arm == "T" and upper_labels[1] != A+3:
                            reject("terminal-free-odd-center-index")
                            continue
                        fixed = {case.v: A, case.u: A+1, case.w: 0}
                        fixed.update(zip(centers[0], first_labels))
                        fixed.update(zip(high_roles, upper_labels))
                        weights = {abs(value - fixed[case.parents[name]])
                                   for name, value in fixed.items() if name != case.v}
                        if len(weights) != len(fixed)-1:
                            reject("repeated-fixed-weight")
                            continue
                        slots = tuple((j, centers[1]) for j in range(1, A) if j not in first_labels)
                        slots += tuple((j, centers[0]) for j in high_slots if j not in upper_labels)

                        def assign_slots(index):
                            if index == len(slots):
                                yield A, B, dict(fixed)
                                return
                            label, hosts = slots[index]
                            for host in hosts:
                                meter.tick("exterior_nodes")
                                next_index = counts[host]
                                if next_index >= len(leaves[host]):
                                    reject("actual-parent-quota")
                                    continue
                                weight = abs(label - fixed[host])
                                if weight in weights:
                                    reject("repeated-terminal-weight")
                                    continue
                                name = leaves[host][next_index]
                                fixed[name] = label
                                counts[host] += 1
                                weights.add(weight)
                                yield from assign_slots(index+1)
                                weights.remove(weight)
                                counts[host] -= 1
                                del fixed[name]

                        counts = dict.fromkeys(leaves, 0)
                        yield from assign_slots(0)


def search(row, prefix, arm, meter, retained):
    case = retained.case_data(row, prefix)
    prunes = {}
    count = 0
    for A, B, reduced in exterior_candidates(case, arm, meter, prunes):
        count += 1
        witness = retained.assignment(case, prefix, A, B, reduced, meter)
        if witness is not None:
            return {"claim": "YES", "prunes": prunes, "representative_exteriors": count, "witness": witness}
    return {"claim": "NO", "prunes": prunes, "representative_exteriors": count}
