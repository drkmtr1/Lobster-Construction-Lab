# B4-UNPADDED-3111-001

For every integer K>=1, excluding booleans, the exact ordered
unpadded `[[3],[1],[1],[1]]+[[]]*(K+1)` profile is alpha graceful.
This is the q=3 case of the [symbolic zero-port family corollary](ALPHA_ZERO_PORT_LEAF_EXTENSION.md#immediate-symbolic-q111-corollary).
The public `four_section_3111(K)` constructor and executable
validation cover this exact profile.

## Original graph and direct prefix

There are K+5 consecutive spine vertices, four centers and six
terminal leaves. Each center b:i:0 attaches to s:i. All three
named leaves l:0:0:0, l:0:0:1 and l:0:0:2 attach to b:0:0.
Each other center has its original single terminal. The vertex
count is K+15 and the K+4 spine edges, four attachments and six
terminal edges give m=K+14. Take the five spine vertices through
s:4 and all original branches, a 15-vertex, 14-edge prefix.
Only s:5,...,s:(K+4) remain. Their incident edges are exactly
the consecutive original spine edges starting at s:4, and the
sole crossing edge is s:4--s:5.

| Named vertices, in order | Supplied labels, in order |
|---|---|
| s:0,s:1,s:2,s:3,s:4 | K+12,2,K+9,5,K+6 |
| b:0:0,l:0:0:0,l:0:0:1,l:0:0:2 | 0,K+11,K+13,K+14 |
| b:1:0,l:1:0:0 | K+10,1 |
| b:2:0,l:2:0:0 | 3,K+8 |
| b:3:0,l:3:0:0 | K+7,4 |

The low vertices in label order are b:0:0, l:1:0:0, s:1, b:2:0,
l:3:0:0, s:3. They use 0..5. In label order the high vertices
are s:4, b:3:0, l:2:0:0, s:2, b:1:0, l:0:0:0, s:0, l:0:0:1,
l:0:0:2. They use K+6..K+14. The original root is m-2 and
the two added leaves receive m-1 and m. Each prefix edge crosses
the two blocks. Direct subtraction gives every original prefix
difference exactly once.

| Edge | Difference |
|---|---:|
| s:3--s:4 | K+1 |
| s:3--b:3:0 | K+2 |
| b:3:0--l:3:0:0 | K+3 |
| s:2--s:3 | K+4 |
| b:2:0--l:2:0:0 | K+5 |
| s:2--b:2:0 | K+6 |
| s:1--s:2 | K+7 |
| s:1--b:1:0 | K+8 |
| b:1:0--l:1:0:0 | K+9 |
| s:0--s:1 | K+10 |
| b:0:0--l:0:0:0 | K+11 |
| s:0--b:0:0 | K+12 |
| b:0:0--l:0:0:1 | K+13 |
| b:0:0--l:0:0:2 | K+14 |

The table uses all four prefix spine edges, four attachments and
six terminal edges. Taking complements in 0..m and 1..m gives
R=[6,K+5] and D=[1,K]. The actual port is s:4=K+6, immediately
above R.

## Seed and completion

The [zero-port extension](ALPHA_ZERO_PORT_LEAF_EXTENSION.md#supplied-state-and-finite-closure)
adds the two named leaves to the existing label-zero b:0:0 of
the retained 13-vertex R241/L008 unit seed. Their labels 13 and
14 give the new differences 13 and 14. The enlarged arithmetic
seed on `[[3],[1],[1],[1],[]]` uses labels 0..14, differences
1..14 and low-class size 6. Its actual ports b:0:0=0 and s:4=6
stay fixed. The path b:0:0--s:0--s:1--s:2--s:3--s:4 still
witnesses it, since the two new leaves are one edge away.
The seed is separately certified. The direct formula raises
each of its nine high labels by K. The public constructor
admits K>=1.

On the actual path from s:4 the unchanged adjacent consumer
starts at index 4. It takes alternating unused low and high
endpoints. For path position j=2i+1 it uses 6+i. For positive
even j=2i it uses K+6-i. The odd positions fill
[6,5+ceil(K/2)] and the even positions fill [6+ceil(K/2),K+5],
with the even set empty at K=1. This partitions R. The odd
step follows label K+6-i, including the original port at
i=0, so the difference is K-2i. The even step follows 6+i-1
and gives K-2i+1. Both equal K-j+1, exhausting D once. The
consumer writes exactly the K suffix labels and retains all
prefix labels.

The prefix lows and odd suffix positions give 0..p-1, where
p=6+ceil(K/2). Prefix highs and even suffix positions give
p..K+14. The prefix crosses the cut and the suffix alternates
across it from high s:4. This proves alpha gracefulness with
cutoff p-1. At K=1, R={6}, D={1}, s:4=7, s:5=6 and p=7.
The mathematical theorem covers all K>=1. CLI graph preflight
limits K to 9985 under the 10,000-vertex ceiling and retains
the separate record byte cap.
