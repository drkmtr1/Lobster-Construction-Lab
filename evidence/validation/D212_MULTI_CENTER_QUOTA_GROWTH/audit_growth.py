"""Independent literal endpoint audit, reserved for future D212 admission."""


def audit_growth(original, candidate, expected_original_digest):
    """Recheck the frozen original and every claimed growth coefficient."""
    from lcl.verify import verify_certificate

    if not isinstance(candidate, dict) or set(candidate) != {"labels", "selected"}:
        return {"valid": False, "errors": ["Malformed candidate"]}
    if not isinstance(expected_original_digest, str) or not expected_original_digest:
        return {"valid": False, "errors": ["Original digest required"]}
    labels = candidate["labels"]
    selected = candidate["selected"]
    base = verify_certificate(original, labels, expected_original_digest)
    if not base["valid"]:
        return {"valid": False, "base": base, "errors": ["Base certificate failed"]}
    n = len(original["edges"])
    hosts = {v for v, role in original["roles"].items() if role["kind"] == "branch"}
    if not isinstance(selected, dict) or set(selected) != hosts:
        return {"valid": False, "base": base, "errors": ["Host coverage failed"]}
    for row in selected.values():
        if (not isinstance(row, dict) or set(row) != {"cut", "threshold"}
                or any(type(x) is not int or not 1 <= x <= n for x in row.values())):
            return {"valid": False, "base": base, "errors": ["Invalid cut coordinates"]}
    if (len({row["cut"] for row in selected.values()}) != len(hosts)
            or len({row["threshold"] for row in selected.values()}) != len(hosts)):
        return {"valid": False, "base": base, "errors": ["A cut or threshold was reused"]}

    errors = []
    named_rows = {}
    for host in sorted(hosts):
        cut = selected[host]["cut"]
        threshold = selected[host]["threshold"]
        a = labels[host]
        crossing = [
            [u, v, abs(labels[u] - labels[v])]
            for u, v in original["edges"]
            if (labels[u] < cut) != (labels[v] < cut)
        ]
        if sorted(row[2] for row in crossing) != list(range(threshold, n + 1)):
            errors.append(f"{host}: crossing spectrum differs from the claimed range")

        # Recompute the coefficients directly at the two gap boundary points.
        # Indicator of each other width in the closest leaf's difference:
        # lower host compares the left gap endpoint with the old host,
        # upper host compares the old host with the right gap endpoint.
        lower = a < cut
        boundary = cut if lower else cut - 1
        constant = abs(a - boundary)
        actual = []
        required = []
        for partner, other in selected.items():
            if partner == host:
                continue
            cut_other = other["cut"]
            coefficient = int(cut_other <= boundary) - int(cut_other <= a)
            if not lower:
                coefficient = -coefficient
            if coefficient == 1:
                actual.append(partner)
            if other["threshold"] < threshold:
                required.append(partner)
        if constant != threshold:
            errors.append(f"{host}: closest-gap difference constant is incorrect")
        if set(actual) != set(required):
            errors.append(f"{host}: joint coefficients do not match the threshold order")
        named_rows[host] = {
            "host_label": a, "cut": cut, "threshold": threshold,
            "orientation": "lower" if lower else "upper",
            "crossing_edges_and_weights": crossing,
            "start_constant": constant,
            "start_width_coefficients": sorted(actual),
            "required_width_coefficients": sorted(required),
        }
    return {"valid": not errors, "base": base, "errors": errors,
            "growth_rows": named_rows}
