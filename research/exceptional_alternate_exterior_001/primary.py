
"""D172 primary role checks and finite folded-window allocation."""
from itertools import permutations, product


def in_menu(case, A, B, reduced):
    v, u, w, left, right, direct, parents, groups, _ = case
    if (A, B) != (6, 4) or direct in reduced:
        return False
    slot = {value: name for name, value in reduced.items()}
    return (tuple(slot.get(j) for j in (6, 7, 0)) == (v, u, w)
            and {slot.get(j) for j in (2, 3, 4, 5)} == set(left)
            and {slot.get(8), slot.get(10)} == set(right)
            and slot.get(9) in groups[slot[3]] and slot.get(1) in groups[slot[10]])


def menu(case, meter):
    v, u, w, left, right, _, _, groups, _ = case
    for b, a, c1, neutral in permutations(left):
        meter.tick("exterior_nodes")
        if len(groups[neutral]) != 4 or (len(groups[b])+len(groups[c1])) % 2 == 0:
            continue
        for q, p in permutations(right):
            meter.tick("exterior_nodes")
            if len(groups[q]) >= 2:
                yield 6, 4, {v: 6, u: 7, w: 0, b: 2, a: 3, c1: 4, neutral: 5,
                             q: 8, p: 10, groups[a][0]: 9, groups[p][0]: 1}


def folded_support(row, case, A, B, reduced, meter):
    _, _, w, left, right, _, parents, _, _ = case
    K = row["K"]
    s, k = 2*K-A-B, K-A
    hosts = (*left, *right, w)
    quotas = tuple(sum(parent == host and name not in reduced for name, parent in parents.items())
                   for host in hosts)
    upper = sorted(reduced[name]-A for name in right)
    beta, rho = upper[0], upper[1]-upper[0]
    J, ell, e = s+beta+1, beta+2, B-beta-1
    if beta != 2 or rho < 1 or sum(quotas) != s:
        raise ValueError("invalid folded host geometry")
    shifts = tuple(A-1-reduced[h] if reduced[h] < A else reduced[h]-A-beta for h in hosts)
    W = max(1, max(map(abs, shifts)))
    from_rows = ((0, k-1), (ell, k+A-e))
    to_rows = ((0, k+A-1), (ell, k-e))
    last = max(hi for _, hi in from_rows+to_rows)

    def contains(bounds, row_no, column):
        lo, hi = bounds[row_no]
        return lo <= column <= hi

    options = {}
    for j in range(last+1):
        cells = []
        for r in range(2):
            if not contains(from_rows, r, j):
                continue
            options_j = []
            for host_no, host in enumerate(hosts):
                meter.tick("transitions")
                is_upper = reduced[host] > A
                out_row = 1-r if is_upper else r
                out_j = j+shifts[host_no]*(1-2*r)*(-1 if is_upper else 1)
                if quotas[host_no] and contains(to_rows, out_row, out_j):
                    bit = 1 << (2*(out_j-j+W)+out_row)
                    numeric_source = j if r == 0 else J-j
                    numeric_image = out_j if out_row == 0 else J-out_j
                    options_j.append((host_no, bit, numeric_source, numeric_image))
            cells.append(tuple(options_j))
        options[j] = tuple(cells)

    retired = {j: sum(1 << r for r in range(2) if contains(to_rows, r, j-W))
               for j in range(last+W+1)}
    dead = set()
    stack = meter.frames

    def visit(j, mask, remaining):
        key = (j, mask, remaining)
        if key in dead:
            return None
        stack.append({"column": j, "image_mask": mask, "remaining": remaining, "choice": None})
        meter.memory(len(dead)+len(stack))
        meter.tick("transfer_states")
        if j > last+W:
            if mask or any(remaining):
                raise ValueError("folded terminal invariant")
            stack.pop()
            return ()
        for trial, moves in enumerate(product(*options.get(j, ()))):
            stack[-1]["choice"] = trial
            meter.tick("transitions")
            used = mask
            rest = list(remaining)
            for h, bit, _, _ in moves:
                if used & bit or not rest[h]:
                    break
                used |= bit
                rest[h] -= 1
            else:
                if used & 3 == retired[j]:
                    answer = visit(j+1, used >> 2, tuple(rest))
                    if answer is not None:
                        stack.pop()
                        return tuple((source, hosts[h], image) for h, _, source, image in moves)+answer
        # Replacing a live stack frame with this dead key consumes no new state.
        dead.add(key)
        stack.pop()
        return None

    answer = visit(0, 0, quotas)
    if answer is None:
        return None
    if [i for i, _, _ in sorted(answer)] != list(range(s)):
        raise ValueError("folded reconstruction source alphabet")
    return [[host, image] for _, host, image in sorted(answer)]


def solve(row, prefix, arm, meter, retained):
    case = retained.physical(row, prefix)
    counts = {"qualified_exteriors": 0, "qualified_strata": {}}
    if arm == "M":
        sequence = menu(case, meter)
    else:
        source_counts = {"entered_widths": 0, "rejected_widths": 0,
                         "qualified_exteriors": 0, "qualified_strata": {}}
        sequence = retained.candidates(row, prefix, "E+", meter, source_counts, case)
    meter.phase = "primary exterior"
    for A, B, reduced in sequence:
        if arm == "A" and in_menu(case, A, B, reduced):
            continue
        tally(counts, A, B, reduced, case)
        meter.candidate = {"A": A, "B": B, "reduced": reduced, "ordinal": counts["qualified_exteriors"]}
        meter.phase = "folded allocation"
        assignment = folded_support(row, case, A, B, reduced, meter)
        if assignment is not None:
            return {"claim": "YES", "counts": counts,
                    "solution": {"A": A, "B": B, "reduced": reduced, "assignment": assignment}}
        meter.phase = "primary exterior"
        meter.candidate = None
    return {"claim": "NO", "counts": counts}


def tally(counts, A, B, reduced, case):
    _, _, _, left, right, direct, _, groups, _ = case
    neutral = next(h for h in left if reduced[h] == A-1)
    pinned = next(h for h in right if reduced[h] == A+2)
    e1 = sum(name in reduced for host in left for name in groups[host])
    e2 = sum(name in reduced for host in right for name in groups[host])
    key = f"{A},{B},{e1},{e2},{int(direct in reduced)},{neutral},{pinned}"
    counts["qualified_exteriors"] += 1
    strata = counts["qualified_strata"]
    strata[key] = strata.get(key, 0)+1
