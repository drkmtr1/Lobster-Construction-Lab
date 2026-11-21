"""Independent verification of the external B2 review pack and local run evidence.

Integration task: OC-20261121-b2-review-integration.
Classification: PROVISIONAL_INTEGRATION_PENDING_CODEX_REVIEW.

This script performs one read-only verification pass. It writes a single result
file next to itself (verification_result.json). It modifies no source, no
checker, no configuration, and no target graph. It runs no solver.

Checks (pass/fail recorded per item):
  A  Local-vs-pack byte identity: both historical record.json files, the four
     input JSONs (profile/pins/domains/limits), and the reviewer scratch script.
  B  Raw SHA-256 of both local records, both local configs, and the pack zip.
  C  Canonical record_sha256 recomputation: SHA-256 of canonical JSON of the
     record with the record_sha256 field omitted (scheme of lcl.records).
  D  config_sha256 recomputation from the local run config.json objects
     (canonical digest of the parsed object, not of the file bytes).
  E  Source inventory recomputation over the local 21 tracked source files,
     plus byte comparison of those files against the pack source_snapshot/.
  F  Every MANIFEST.json entry (byte count + SHA-256) verified against the
     pack bytes; manifest file set compared to the actual pack file set.
  G  Graph digest recomputed from build_graph([[1],[2],[]]); both records'
     embedded original_graph compared for equality with the fresh build.
  H  Own 144-assignment enumeration of the p=4 restricted negative:
     A-side vertices s:1, b:0:0, l:1:0:0, l:1:0:1 bijectively on {0,1,2,3};
     B-side s:0, b:1:0, l:0:0:0 bijectively on {5,6,7} with pin s:2 = 4;
     graceful iff the seven edge differences are exactly {1,...,7}.
     Independent of the DFS record, the oracle record, and the pack script.

Usage:
  python verify_b2_review_pack.py [pack_root]
The default pack root is the local download location on this machine; pass a
different pack root as the first argument to replay elsewhere.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
PROJECT_ROOT = HERE.parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

DEFAULT_PACK_ROOT = Path(
    r"C:\Users\Will\Downloads\LCL_B2_Independent_Review_2026-11-21"
    r"\LCL_B2_Independent_Review"
)
SCRATCH_LOCAL = Path(
    r"C:\Users\Will\AppData\Local\Temp\opencode\b2_review_scratch.py"
)
RESULT_PATH = HERE.parent / "verification_result.json"

# Expected identities (from the pack's own manifest/audit and prior verification).
EXPECTED = {
    "graph_digest": "9198e106ce33d9b83b8044e385b1599cfe26cd1fe471f4eec841a461868756b2",
    "source_inventory_sha256": "2dfe3231007a18f4a74e4c4b49fd4a112ebbb66ef439e711ff59ac11fde7bbfd",
    "dfs_record_raw": "1c84fcf14fe4f591455db0c0c4a0522ccc2f2c644791f1361c4fea03b88dbf44",
    "dfs_record_canonical": "f03d968e014e17d37382ef60a1836177497e388b86d779501fbe6b9dc0071f05",
    "oracle_record_raw": "0504e38a259a648e0f648b4ab1e5be4789d3b28de396b69710cfe394e2c88d11",
    "oracle_record_canonical": "d8c0359adc279d46e5aaffc6cd7affbf7aa70304f659dbc572f5f2eaf978a489",
    "pack_zip": "a2def9c494ff49d7dbe89ca10416b1da804e82052c9a79db773ae50c819e2b97",
    "input_seed": "486c501581240d0c6aabce3acdb31fa6d205d58d5881b4ac39b37c6648765db8",
    "input_pins": "a39bcce07fd8427ac3c11748836b0317cc609a4b45204a104f5bda36bfe31956",
    "input_domains": "0bd9694a536395db1532a68e02bbae51e501889280a99c9108564af8c72acfec",
    "input_limits": "64bb948a40862ce8238bab108fb00915d2ef48d31c8cfe50502cd0ca9cd0388a",
    "scratch": "1d3836ea74249ac49d3a4975d8c80eb18f2bb115b6c84b05bff275623c169408",
}

RUNS = {
    "dfs": "runs/dfs-20261121T081441Z-0a3c9a64",
    "oracle": "runs/oracle-20261121T081441Z-a5f3c783",
}
INPUTS = {
    "seed": ("examples/unequal_seed.json", "input_seed"),
    "pins": ("examples/unequal_seed_pins.json", "input_pins"),
    "domains": ("examples/unequal_seed_domains.json", "input_domains"),
    "limits": ("configs/unequal_seed_limits.json", "input_limits"),
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def main() -> int:
    pack_root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACK_ROOT
    if not pack_root.is_dir():
        print(f"FATAL: pack root not found: {pack_root}")
        return 2

    from lcl.model import build_graph, graph_digest  # noqa: E402
    from lcl.records import digest, source_inventory  # noqa: E402

    checks: list[dict] = []

    def record(cid: str, description: str, ok: bool, detail: dict | str = "") -> None:
        checks.append({"id": cid, "description": description,
                       "pass": bool(ok), "detail": detail})

    # ---- A. Local vs pack byte identity ---------------------------------
    byte_pairs = {
        "dfs record": (PROJECT_ROOT / RUNS["dfs"] / "record.json",
                       pack_root / "supplied" / RUNS["dfs"] / "record.json"),
        "oracle record": (PROJECT_ROOT / RUNS["oracle"] / "record.json",
                          pack_root / "supplied" / RUNS["oracle"] / "record.json"),
    }
    for i, (name, (local, packed)) in enumerate(
            list(byte_pairs.items()) + [
                (f"input {key}", (PROJECT_ROOT / rel, pack_root / "supplied" / rel))
                for key, (rel, _exp) in INPUTS.items()
            ] + [("reviewer scratch", (SCRATCH_LOCAL,
                                        pack_root / "supplied" / "b2_review_scratch.py"))],
            start=1):
        ok = local.is_file() and packed.is_file() and local.read_bytes() == packed.read_bytes()
        record(f"A{i}", f"byte-identical local vs pack: {name}", ok,
               {"local": str(local), "pack": str(packed),
                "local_bytes": local.stat().st_size if local.is_file() else None})

    # ---- B. Raw SHA-256 ---------------------------------------------------
    dfs_rec = PROJECT_ROOT / RUNS["dfs"] / "record.json"
    ora_rec = PROJECT_ROOT / RUNS["oracle"] / "record.json"
    dfs_cfg = PROJECT_ROOT / RUNS["dfs"] / "config.json"
    ora_cfg = PROJECT_ROOT / RUNS["oracle"] / "config.json"
    record("B1", "raw sha256 dfs record.json == expected",
           sha256_file(dfs_rec) == EXPECTED["dfs_record_raw"],
           sha256_file(dfs_rec))
    record("B2", "raw sha256 oracle record.json == expected",
           sha256_file(ora_rec) == EXPECTED["oracle_record_raw"],
           sha256_file(ora_rec))
    # Raw config file hashes have no independent expected value (the record
    # carries the canonical object digest, not the file hash); report only.
    record("B3", "raw sha256 dfs config.json (reported)", True, sha256_file(dfs_cfg))
    record("B4", "raw sha256 oracle config.json (reported)", True, sha256_file(ora_cfg))
    record("B5", "raw sha256 pack original_upload.zip == expected",
           sha256_file(pack_root / "original_upload.zip") == EXPECTED["pack_zip"],
           sha256_file(pack_root / "original_upload.zip"))
    for i, (key, (rel, exp_key)) in enumerate(INPUTS.items(), start=1):
        record(f"B{5 + i}", f"raw sha256 local {rel} == expected",
               sha256_file(PROJECT_ROOT / rel) == EXPECTED[exp_key],
               sha256_file(PROJECT_ROOT / rel))
    record("B10", "raw sha256 local reviewer scratch == expected",
           sha256_file(SCRATCH_LOCAL) == EXPECTED["scratch"],
           sha256_file(SCRATCH_LOCAL))

    # ---- C. Canonical record_sha256 --------------------------------------
    dfs_json = json.loads(dfs_rec.read_text(encoding="utf-8"))
    ora_json = json.loads(ora_rec.read_text(encoding="utf-8"))
    for cid, rec, exp_key in (("C1", dfs_json, "dfs_record_canonical"),
                              ("C2", ora_json, "oracle_record_canonical")):
        stored = rec.get("record_sha256")
        probe = {k: v for k, v in rec.items() if k != "record_sha256"}
        record(cid, "canonical record_sha256 recomputation (field omitted)",
               digest(probe) == stored == EXPECTED[exp_key],
               {"recomputed": digest(probe), "stored": stored,
                "expected": EXPECTED[exp_key]})

    # ---- D. config_sha256 -------------------------------------------------
    for cid, cfg_path, rec in (("D1", dfs_cfg, dfs_json), ("D2", ora_cfg, ora_json)):
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        record(cid, "config_sha256 recomputation from local config.json object",
               digest(cfg) == rec.get("config_sha256"),
               {"recomputed": digest(cfg), "stored": rec.get("config_sha256")})

    # ---- E. Source inventory ----------------------------------------------
    inventory = source_inventory(PROJECT_ROOT)
    record("E1", "source inventory sha256 == expected (21 files)",
           inventory["sha256"] == EXPECTED["source_inventory_sha256"]
           and len(inventory["files"]) == 21,
           {"sha256": inventory["sha256"], "file_count": len(inventory["files"])})
    mismatches = []
    for rel, expected_hash in sorted(inventory["files"].items()):
        local = PROJECT_ROOT / rel
        packed = pack_root / "source_snapshot" / rel
        if not packed.is_file() or local.read_bytes() != packed.read_bytes():
            mismatches.append(rel)
    record("E2", "21 local source files byte-identical to pack source_snapshot",
           not mismatches, {"mismatches": mismatches})
    per_file_bad = []
    for rec, tag in ((dfs_json, "dfs"), (ora_json, "oracle")):
        for rel, h in rec["source"]["files"].items():
            if sha256_file(PROJECT_ROOT / rel) != h:
                per_file_bad.append(f"{tag}:{rel}")
    record("E3", "record source.files per-file hashes match local files (both records)",
           not per_file_bad, {"mismatches": per_file_bad})

    # ---- F. Pack MANIFEST ---------------------------------------------------
    manifest = json.loads((pack_root / "MANIFEST.json").read_text(encoding="utf-8"))
    bad_entries = []
    for rel, meta in sorted(manifest["files"].items()):
        path = pack_root / rel
        data = path.read_bytes() if path.is_file() else None
        if data is None or len(data) != meta["bytes"] \
                or sha256_bytes(data) != meta["sha256"]:
            bad_entries.append(rel)
    record("F1", f"all {len(manifest['files'])} MANIFEST entries verified (bytes + sha256)",
           not bad_entries, {"bad": bad_entries})
    actual_pack = {p.relative_to(pack_root).as_posix()
                   for p in pack_root.rglob("*") if p.is_file()}
    listed = set(manifest["files"])
    record("F2", "MANIFEST file set == actual pack file set (MANIFEST.json excluded)",
           listed | {"MANIFEST.json"} == actual_pack,
           {"only_in_manifest": sorted(listed - actual_pack),
            "only_on_disk": sorted(actual_pack - listed - {"MANIFEST.json"})})

    # ---- G. Graph digest ----------------------------------------------------
    fresh = build_graph([[1], [2], []])
    gd = graph_digest(fresh)
    record("G1", "graph digest from build_graph([[1],[2],[]]) == expected",
           gd == EXPECTED["graph_digest"], gd)
    for cid, rec, tag in (("G2", dfs_json, "dfs"), ("G3", ora_json, "oracle")):
        record(cid, f"{tag} record embedded original_graph == fresh build_graph output",
               rec.get("original_graph") == fresh
               and rec.get("original_graph_digest") == gd,
               {"embedded_digest": rec.get("original_graph_digest")})

    # ---- H. Own 144-assignment enumeration ---------------------------------
    edges = [("s:0", "s:1"), ("s:0", "b:0:0"), ("b:0:0", "l:0:0:0"),
             ("s:1", "s:2"), ("s:1", "b:1:0"), ("b:1:0", "l:1:0:0"),
             ("b:1:0", "l:1:0:1")]
    a_side = ["s:1", "b:0:0", "l:1:0:0", "l:1:0:1"]
    b_side = ["s:0", "b:1:0", "l:0:0:0"]
    n_total = n_graceful = n_y3 = n_s28 = n_distinct7 = identity_mismatch = 0
    for pa in itertools.permutations((0, 1, 2, 3)):
        for pb in itertools.permutations((5, 6, 7)):
            lab = dict(zip(a_side, pa))
            lab.update(dict(zip(b_side, pb)))
            lab["s:2"] = 4
            n_total += 1
            diffs = [abs(lab[u] - lab[v]) for u, v in edges]
            if sorted(diffs) == list(range(1, 8)):
                n_graceful += 1
            if len(set(diffs)) == 7:
                n_distinct7 += 1
            s_total = sum(diffs)
            if s_total == 28:
                n_s28 += 1
            if lab["s:1"] == 3:
                n_y3 += 1
            # General sum identity (y unrestricted):
            # S = a + 2b - x - 2y + 16 with a=h(s:0), b=h(b:1:0),
            # x=h(b:0:0), y=h(s:1), using a+b+c=18 and x+u+v=3-y.
            rhs = (lab["s:0"] + 2 * lab["b:1:0"] - lab["b:0:0"]
                   - 2 * lab["s:1"] + 16)
            if s_total != rhs:
                identity_mismatch += 1
    record("H1", "enumeration covers exactly 144 domain-admissible assignments",
           n_total == 144, n_total)
    record("H2", "own enumeration: 0 graceful labelings (p=4 restricted negative)",
           n_graceful == 0, {"graceful": n_graceful,
                             "sum_28": n_s28, "distinct_seven": n_distinct7})
    record("H3", "own enumeration: 36 assignments have y = h(s:1) = 3",
           n_y3 == 36, n_y3)
    record("H4", "own enumeration: general sum identity S = a+2b-x-2y+16 holds for all 144",
           identity_mismatch == 0, {"mismatches": identity_mismatch})

    # ---- Summary -------------------------------------------------------------
    failed = [c for c in checks if not c["pass"]]
    result = {
        "task": "B2 review integration verification (OC-20261121-b2-review-integration)",
        "classification": "PROVISIONAL_INTEGRATION_PENDING_CODEX_REVIEW",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
        "pack_root": str(pack_root),
        "project_root": str(PROJECT_ROOT),
        "script_sha256": sha256_file(HERE),
        "checks": checks,
        "summary": {"total": len(checks), "passed": len(checks) - len(failed),
                    "failed": [c["id"] for c in failed]},
    }
    RESULT_PATH.write_text(
        json.dumps(result, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    for c in checks:
        mark = "PASS" if c["pass"] else "FAIL"
        print(f"{mark}  {c['id']:<4} {c['description']}")
    print(f"\n{len(checks) - len(failed)}/{len(checks)} passed; "
          f"result written to {RESULT_PATH}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
