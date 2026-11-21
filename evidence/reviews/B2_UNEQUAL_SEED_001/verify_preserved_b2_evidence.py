"""Verify the tracked B2 evidence directly, without research enumeration.

Python 3.12/3.13, standard library only. No Downloads or Temp dependency.
Inputs are read only. A required NEW output file is created exclusively;
historical verification_result.json is never overwritten.

Example from the project root, after installing this file beside the manifest:
  python evidence/reviews/B2_UNEQUAL_SEED_001/verify_preserved_b2_evidence.py \
      --out evidence/reviews/B2_UNEQUAL_SEED_001/custody_check_NEW.json
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import platform


EXPECTED_SOURCE = "2dfe3231007a18f4a74e4c4b49fd4a112ebbb66ef439e711ff59ac11fde7bbfd"
EXPECTED_GRAPH = "9198e106ce33d9b83b8044e385b1599cfe26cd1fe471f4eec841a461868756b2"
EXPECTED_RECORDS = {
    "dfs-20261121T081441Z-0a3c9a64": "f03d968e014e17d37382ef60a1836177497e388b86d779501fbe6b9dc0071f05",
    "oracle-20261121T081441Z-a5f3c783": "d8c0359adc279d46e5aaffc6cd7affbf7aa70304f659dbc572f5f2eaf978a489",
}
EXPECTED_EDGES = {
    tuple(sorted(e)) for e in (
        ("s:0", "s:1"), ("s:0", "b:0:0"), ("b:0:0", "l:0:0:0"),
        ("s:1", "b:1:0"), ("b:1:0", "l:1:0:0"),
        ("b:1:0", "l:1:0:1"), ("s:1", "s:2"),
    )
}


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_object(value: object) -> str:
    return digest_bytes(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                  ensure_ascii=False).encode("utf-8"))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def member(root: Path, name: str) -> Path:
    pure = PurePosixPath(name)
    if pure.is_absolute() or ".." in pure.parts or ":" in name or "\\" in name:
        raise ValueError(f"Unsafe or noncanonical relative path: {name}")
    target = root.joinpath(*pure.parts).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes evidence root: {name}")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--project-root", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    evidence = args.evidence_root.resolve()
    project = args.project_root.resolve() if args.project_root else evidence.parents[2]
    output = args.out.resolve()
    if output.exists():
        parser.error("Output already exists. Choose a new filename; historical outputs are immutable.")
    if any(output.is_relative_to(evidence / folder) for folder in ("raw", "pack")):
        parser.error("Output must be outside the preserved raw/ and pack/ payload directories.")

    checks: list[dict] = []

    def check(name: str, ok: bool, detail: object = None) -> None:
        checks.append({"id": name, "pass": bool(ok), "detail": detail})

    manifest = read_json(evidence / "RAW_FILE_MANIFEST.json")
    entries = manifest["preserved_files"]
    check("manifest_entry_count", len(entries) == 21, len(entries))
    for name, expected in sorted(entries.items()):
        path = member(evidence, name)
        data = path.read_bytes() if path.is_file() else None
        observed = None if data is None else {"bytes": len(data), "raw_file_sha256": digest_bytes(data)}
        check("preserved:" + name, observed == expected,
              {"expected": expected, "observed": observed})
    actual = {
        p.relative_to(evidence).as_posix()
        for folder in ("raw", "pack")
        for p in (evidence / folder).rglob("*") if p.is_file()
    }
    check("manifest_covers_exact_preserved_set", set(entries) == actual,
          {"missing": sorted(set(entries) - actual), "unlisted": sorted(actual - set(entries))})

    original_manifest = read_json(evidence / "pack/MANIFEST.json")
    copied_pack_payloads = sorted(name[5:] for name in actual
                                  if name.startswith("pack/") and name != "pack/MANIFEST.json")
    for name in copied_pack_payloads:
        data = member(evidence / "pack", name).read_bytes()
        expected = original_manifest["files"].get(name)
        check("original_pack_member:" + name,
              expected == {"bytes": len(data), "sha256": digest_bytes(data)})

    records = []
    for run, expected_hash in EXPECTED_RECORDS.items():
        relative = f"raw/runs/{run}/record.json"
        record = read_json(member(evidence, relative))
        config = read_json(member(evidence, f"raw/runs/{run}/config.json"))
        canonical = digest_object({k: v for k, v in record.items() if k != "record_sha256"})
        check("canonical_record:" + run, canonical == record["record_sha256"] == expected_hash)
        check("canonical_config:" + run, config == record["config"]
              and digest_object(config) == record["config_sha256"])
        declared = manifest["canonical_record_fields"].get(relative)
        check("manifest_record_reference:" + run,
              declared == {"record_sha256": record["record_sha256"],
                           "config_sha256": record["config_sha256"]})
        graph = record["original_graph"]
        check("original_target:" + run,
              graph["profile"] == [[1], [2], []]
              and len(graph["vertices"]) == 8
              and len(set(graph["vertices"])) == 8
              and len(graph["edges"]) == 7
              and {tuple(sorted(e)) for e in graph["edges"]} == EXPECTED_EDGES
              and record["original_graph_digest"] == EXPECTED_GRAPH)
        check("saved_negative_status:" + run,
              record["result"]["status"] == "EXHAUSTED_NO_SOLUTION"
              and record["result"]["exhausted"] is True
              and record["result"]["count"] == 0
              and record["consistency_errors"] == [])
        records.append(record)

    source = records[0]["source"]
    check("identical_source_inventories", source == records[1]["source"])
    check("source_inventory_identity", len(source["files"]) == 21
          and digest_object(source["files"]) == source["sha256"] == EXPECTED_SOURCE)
    for name, expected_hash in sorted(source["files"].items()):
        path = member(project, name)
        observed = digest_bytes(path.read_bytes()) if path.is_file() else None
        check("source:" + name, observed == expected_hash,
              {"expected": expected_hash, "observed": observed})

    historical = read_json(evidence / "verification_result.json")
    check("historical_script_identity", digest_bytes((evidence / "verify_b2_review_pack.py").read_bytes())
          == historical["script_sha256"])
    seed_result = read_json(evidence / "pack/independent_seed_check.json")
    check("saved_independent_script_identity",
          digest_bytes((evidence / "pack/independent_seed_check.py").read_bytes())
          == seed_result["script_sha256"])
    check("saved_independent_result_scope", seed_result["exhausted"] is True
          and seed_result["attempted_named_assignments"] == 144
          and seed_result["count"] == 0
          and len(seed_result["all_named_assignments"]) == 144)
    attrs_path = evidence / ".gitattributes"
    attrs = set(attrs_path.read_text().splitlines()) if attrs_path.is_file() else set()
    check("scoped_eol_rules_declared", {"raw/** -text", "pack/** -text"} <= attrs)

    failures = [c["id"] for c in checks if not c["pass"]]
    result = {
        "task": "B2 preserved-evidence custody check",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "evidence_root": str(evidence), "project_root": str(project),
        "script_sha256": digest_bytes(Path(__file__).read_bytes()),
        "scope": "Hash, metadata and saved-record verification only; no new labeling enumeration or proof acceptance.",
        "historical_output_not_overwritten": True,
        "checks": checks,
        "summary": {"total": len(checks), "passed": len(checks) - len(failures), "failed": failures},
    }
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    if len(encoded) > 2_000_000:
        raise RuntimeError("Result exceeds the 2 MB output cap")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as handle:
        handle.write(encoded)
    print(json.dumps(result["summary"], indent=2))
    print(f"New output: {output}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
