"""Prepare the two declared originals through the unchanged graph builder, without labels."""

from time import process_time

CPU_START = process_time()

from hashlib import sha256
import json
from pathlib import Path
import sys
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from lcl.model import build_graph, graph_digest


def write_json(name, data, limits):
    raw = (json.dumps(data, sort_keys=True, indent=2) + "\n").encode()
    total = sum(path.stat().st_size for path in HERE.iterdir() if path.is_file())
    if len(raw) > limits["bytes_per_record"] or total + len(raw) > limits["bytes_total"]:
        raise ValueError("Evidence size cap exceeded")
    with (HERE / name).open("xb") as output:
        output.write(raw)
    return sha256(raw).hexdigest()


def main():
    cfg_raw = (HERE / "config.json").read_bytes()
    cfg = json.loads(cfg_raw)
    receipt = {"status": "INCOMPLETE", "task": cfg["task"], "parent": cfg["parent"],
               "config_sha256": sha256(cfg_raw).hexdigest(), "argv": sys.orig_argv,
               "original_preparations": 0, "new_graph_identities": 0}
    try:
        assert __debug__ and sys.dont_write_bytecode
        assert all(not (HERE / name).exists() for name in ("original.json", "original_adverse.json", "__pycache__"))
        profiles = cfg["scope"]["boundary_profiles"]
        assert profiles == {"positive": [[2, 5, 6], [2]], "adverse": [[2, 5, 4], [2]]}
        originals = {}
        for key, filename, m in (("positive", "original.json", 20), ("adverse", "original_adverse.json", 18)):
            profile = profiles[key]
            receipt["original_preparations"] += 1
            graph = build_graph(profile)
            assert (len(graph["vertices"]), len(graph["edges"])) == (m + 1, m)
            digest = graph_digest(graph)
            raw_hash = write_json(filename, {"graph": graph, "graph_digest": digest}, cfg["limits"])
            originals[key] = {"path": filename, "profile": profile, "graph_digest": digest, "raw_sha256": raw_hash}
            receipt["new_graph_identities"] += 1
        assert originals["positive"]["graph_digest"] != originals["adverse"]["graph_digest"]
        receipt.update(status="PASS", originals=originals)
    except (Exception, KeyboardInterrupt):
        receipt["error"] = traceback.format_exc()
    receipt["process_cpu_seconds"] = process_time() - CPU_START
    write_json("preparation_receipt.json", receipt, cfg["limits"])
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
