"""Prepare the single original input independently of all labeling code."""

from time import perf_counter, process_time

WALL_START = perf_counter()
CPU_START = process_time()

from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))

from lcl.model import build_graph, graph_digest


def main():
    if not __debug__ or not sys.dont_write_bytecode or sys.version_info[:2] not in {(3, 12), (3, 13)}:
        raise RuntimeError("Require project-local Python 3.12/3.13, active assertions and -B")
    original_path, receipt_path = HERE / "original.json", HERE / "original_freeze_receipt.json"
    if original_path.exists() or receipt_path.exists():
        raise RuntimeError("The boundary must be frozen only once")
    graph = build_graph([[6, 3], [2]])
    assert len(graph["vertices"]) == 16 and len(graph["edges"]) == 15
    digest = graph_digest(graph)
    raw = (json.dumps({"graph": graph, "graph_digest": digest}, indent=2, sort_keys=True) + "\n").encode()
    with original_path.open("xb") as stream:
        stream.write(raw)
    receipt = {"status": "PASS", "stage": "independent original preparation", "q": 6,
               "argv": sys.orig_argv, "new_graph_identities": 1, "certificates": 0,
               "graph_digest": digest, "original_sha256": sha256(raw).hexdigest(),
               "generator_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
               "builder_sha256": sha256((ROOT / "lcl/model.py").read_bytes()).hexdigest(),
               "runtime_sha256": sha256(Path(sys.executable).read_bytes()).hexdigest(),
               "process_cpu_seconds": process_time()-CPU_START, "wall_seconds": perf_counter()-WALL_START}
    with receipt_path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(receipt, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(digest, receipt["original_sha256"])


if __name__ == "__main__":
    main()
