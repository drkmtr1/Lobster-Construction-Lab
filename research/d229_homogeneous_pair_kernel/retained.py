"""Hand-transcribed independent sources from D225, D228 and D229."""

from .model import CapKey, CoreKey

# D225 section 4. Prefix pairs are (high offset, input); upper low pairs
# are (low label, input decline from F-1).
UNIT_TABLE = {
    6: (
        ((1, 0), (3, 2), (4, 3)),
        ((1, 5), (2, 3), (5, 2), (8, 1)),
    ),
    7: (
        ((1, 0), (2, 2), (4, 3), (5, 4)),
        ((1, 4), (2, 6), (5, 1), (6, 3), (9, 2)),
    ),
    8: (
        ((1, 4), (2, 0), (3, 3), (5, 5), (6, 2)),
        ((1, 3), (2, 5), (5, 1), (6, 4), (7, 7), (10, 2)),
    ),
    9: (
        ((1, 4), (2, 0), (3, 5), (4, 2), (6, 3), (7, 6)),
        ((1, 3), (2, 5), (5, 1), (6, 4), (7, 8), (8, 6), (11, 2)),
    ),
}


def unit_rows(h, beta):
    size = 2 * h - 1
    if beta == 2:
        if h != 6:
            return None
        # D228 Control C, in independently supplied actual host order.
        rows = (
            ("L", 1, 5, 7), ("H", 1, 0, 9), ("L", 5, 8, 6),
            ("L", 2, 7, 8), ("L", 3, 10, 10), ("L", 4, 2, 1),
            ("L", 8, 9, 4), ("H", 4, 1, 5), ("H", 3, 4, 3),
            ("H", 2, 6, 2), ("L", 6, 3, 0),
        )
    else:
        high, low = UNIT_TABLE[h]
        rows = (
            ("L", 3, size - 1, size - 1), ("L", 4, 1, 0),
            ("L", h, h - 2, 1), ("H", h - 4, h, 2),
        )
        rows += tuple(("H", k, i, size - 1 - k - i) for k, i in high)
        rows += tuple(
            ("L", k, size - 1 - j, size - 1 - j + 3 - k) for k, j in low
        )
    return tuple(((kind, k), ("C", i), ("C", w)) for kind, k, i, w in rows)


def known_core(key):
    unit = unit_rows(key.h, key.beta)
    if unit is None:
        return None
    if key.triples == 0 and key.singles == (1, 1, 1):
        return unit
    if key.triples == key.h - 2 and key.singles == (3, 3, 3):
        size = 2 * key.h - 1
        return tuple(
            (host, ("C", i + b * size),
             ("C", w + (b if host[0] == "L" else 2 - b) * size))
            for host, (_, i), (_, w) in unit for b in range(3)
        )
    return None


# Each tokenized line is HOST, TAG, INPUT, WEIGHT, with upper offsets
# relative to F. These are the exact hand packets, before reinstating anchors.
PACKETS = {
    (1, 1): """
L1 UU 4 6
L2 UU 3 4
L7 UU 6 2
L8 UU 5 0
H1 LU 3 3
H2 LU 0 5
H3 LU 5 -1
H4 LU 2 1
""",
    (2, 1): """
L1 UU 3 5
L2 UU 5 6
L7 UU 6 2
L8 UU 4 -1
H1 LU 6 0
H2 LU 1 4
H3 LU 3 1
H4 LU 0 3
""",
    (1, 3): """
L1 LL 0 2
L2 LL 2 3
L3 LL 4 4
L4 LL 6 5
L1 UU 19 21
L1 UU 20 22
L2 UU 13 14
L2 UU 17 18
L3 UU 15 15
L4 UU 21 20
L7 UU 11 7
L8 UU 22 17
H1 LU 3 19
H1 LU 10 12
H2 LU 5 16
H2 LU 13 8
H3 LU 7 13
H3 LU 11 9
H4 LU 8 11
H4 LU 9 10
H1 UL 16 6
H2 UL 14 7
H3 UL 12 8
H4 UL 18 1
""",
    (2, 3): """
L1 LL 0 2
L2 LL 3 4
L3 LL 5 5
L4 LL 7 6
L1 UU 18 20
L1 UU 16 18
L2 UU 20 21
L2 UU 21 22
L3 UU 12 12
L4 UU 15 14
L7 UU 11 7
L8 UU 22 17
H1 LU 14 8
H1 LU 11 11
H2 LU 6 15
H2 LU 8 13
H3 LU 1 19
H3 LU 4 16
H4 LU 9 10
H4 LU 10 9
H1 UL 13 9
H2 UL 14 7
H3 UL 17 3
H4 UL 19 0
""",
}

X_PACKET = """
L1 LL 0 2
L1 UU 4 6
L1 UU 5 7
L2 UU 7 8
L7 UU 6 2
L8 UU 8 3
H1 LU 3 5
H2 LU 7 0
H3 LU 2 4
H4 LU 4 1
"""


def cap_rows(packet, beta_return, top):
    rows = []
    for line in packet.strip().splitlines():
        host, tags, i, w = line.split()
        rows.append(((host[0], int(host[1:])), (tags[0], int(i)), (tags[1], int(w))))
    rows.append((("L", 3), ("U", top), ("U", top)))
    rows.append((("L", 4), ("L", beta_return), ("L", beta_return - 1)))
    return tuple(rows)


def known_cap(key):
    q = key.left_flank
    if key.left_high == q and key.pairs == (q, q, q):
        return cap_rows(PACKETS[key.beta, q], key.beta, 8 * q - 1)
    if key == CapKey(3, 1, (1, 1, 1), 2):
        return cap_rows(X_PACKET, 1, 9)
    return None


def proved_cap_negative(key):
    return key == CapKey(3, 1, (1, 1, 1), 1)
