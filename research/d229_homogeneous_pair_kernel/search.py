"""Primary exact-cover search over the frozen row model."""

from .model import CoreKey, cap_problem, core_problem, placements


def solve_problem(problem, budget):
    """Return one complete row allocation, or None after exhaustive traversal."""
    hosts = tuple(problem.demands)
    index = {host: i for i, host in enumerate(hosts)}
    input_bit = {coord: 1 << i for i, coord in enumerate(problem.inputs)}
    weight_bit = {coord: 1 << i for i, coord in enumerate(problem.weights)}
    indexed = tuple(
        (index[host], input_bit[i], weight_bit[w], (host, i, w))
        for host, i, w in problem.rows
    )
    initial_input = (1 << len(input_bit)) - 1
    initial_weight = (1 << len(weight_bit)) - 1
    demand = [problem.demands[host] for host in hosts]
    selected = []

    def visit(inputs, weights):
        budget.charge()
        if inputs == 0:
            if weights == 0 and not any(demand):
                return problem.fixed + tuple(selected)
            return None

        by_input = {bit: [] for bit in input_bit.values() if inputs & bit}
        by_weight = {bit: [] for bit in weight_bit.values() if weights & bit}
        capacity = [0] * len(hosts)
        for host, ib, wb, row in indexed:
            budget.poll()
            if demand[host] and inputs & ib and weights & wb:
                choice = (host, ib, wb, row)
                by_input[ib].append(choice)
                by_weight[wb].append(choice)
                capacity[host] += 1
        if any(required > count for required, count in zip(demand, capacity, strict=True)):
            return None
        # Every solution covers each remaining input and each weight exactly once.
        column = min((*by_input.values(), *by_weight.values()), key=len)
        for host, ib, wb, row in column:
            demand[host] -= 1
            selected.append(row)
            found = visit(inputs ^ ib, weights ^ wb)
            if found is not None:
                return found
            selected.pop()
            demand[host] += 1
        return None

    return visit(initial_input, initial_weight)


def primary(key, budget):
    if isinstance(key, CoreKey):
        for placement in placements(key):
            budget.poll()
            problem = core_problem(key, placement, budget.poll)
            rows = solve_problem(problem, budget)
            if rows is not None:
                return rows
        return None
    return solve_problem(cap_problem(key, budget.poll), budget)
