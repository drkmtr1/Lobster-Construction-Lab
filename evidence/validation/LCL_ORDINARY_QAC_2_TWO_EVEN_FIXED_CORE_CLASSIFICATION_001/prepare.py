"""Prepare the three declared originals through the unchanged builder, without labels."""

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
        assert not (HERE / "__pycache__").exists()
        profiles = cfg["scope"]["boundaries"]
        assert profiles == {"I": [[6, 3, 2], [2]], "adverse": [[6, 3, 4], [2]], "II": [[6, 5, 6], [2]]}
        assert all(not (HERE / f"original_{key}.json").exists() for key in profiles)
        receipt["originals"] = {}
        for key, profile in profiles.items():
            receipt["original_preparations"] += 1
            graph = build_graph(profile)
            m = sum(profile[0])+7
            assert (len(graph["vertices"]), len(graph["edges"])) == (m+1, m)
            digest = graph_digest(graph)
            name = f"original_{key}.json"
            raw_sha = write_json(name, {"graph": graph, "graph_digest": digest}, cfg["limits"])
            receipt["originals"][key] = {"path": name, "raw_sha256": raw_sha, "graph_digest": digest,
                                         "profile": profile}
            receipt["new_graph_identities"] += 1
        assert len({record["graph_digest"] for record in receipt["originals"].values()}) == 3
        receipt["status"] = "PASS"
    except (Exception, KeyboardInterrupt):
        receipt["error"] = traceback.format_exc()
    receipt["process_cpu_seconds"] = process_time() - CPU_START
    write_json("preparation_receipt.json", receipt, cfg["limits"])
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
