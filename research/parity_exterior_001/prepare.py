"""Freeze unlabeled originals only. Does not load any search generator or allocator."""
from itertools import product
import os
from pathlib import Path
import time
import types


def bindings():
    path = Path(__file__).absolute().with_name("bindings.py")
    api = types.ModuleType("d154_bindings")
    api.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), "exec"), vars(api))
    return api


def main():
    started = time.process_time()
    api = bindings()
    config = api.read(api.KIT/"config.json")
    api.exact_runtime(config, base_process=True)
    for name, digest in config["retained_sha256"].items():
        if api.sha(api.ordinary(api.ROOT/name).read_bytes()) != digest:
            raise ValueError(f"retained original or source identity drift: {name}")
    for field in ("output", "approval"):
        if os.path.lexists(api.ordinary(api.ROOT/config[field])):
            raise ValueError("official paths must be vacant")
    out = api.ordinary(api.EVIDENCE/"input")
    if os.path.lexists(out):
        raise ValueError("corpus destination was already occupied")
    original_source = api.load_exact("d154_original_builder", api.ROOT/"lcl/model.py")
    checker = api.load_exact("d154_original_checker", api.ROOT/"lcl/verify.py")
    original_audit = api.load_exact("d154_retained_original_audit", api.LEGACY/"audit.py")
    prefix_bytes = (api.ROOT/config["retained_prefix"]).read_bytes()
    prefix = api.read(api.ROOT/config["retained_prefix"])
    original_audit.verify_prefix(prefix, checker.verify_certificate)
    if prefix["n"] != 54 or prefix["frontier"] != "s:25" or prefix["c"] != 26 or prefix["d"] != 28:
        raise ValueError("wrong retained prefix")
    out.mkdir()
    with (out/"prefix.json").open("xb") as stream:
        stream.write(prefix_bytes)
    size = len(prefix_bytes)
    items, index, digests = [], [], set()
    limit = config["limits"]["record_bytes"]
    for number, (r, t, p, q) in enumerate(product(range(1, 5), repeat=4), 1):
        fresh = 2*(r+t+p+q+4)
        suffix = [[2*r, 2*t], [2*p, 2*q+1, 0]]
        profile = prefix["graph"]["profile"] + suffix
        graph = original_source.build_graph(profile)
        _, _, digest = original_audit.original(graph)
        valid = checker.verify_graph(graph)
        if (not valid["valid"] or valid["graph_digest"] != digest or digest in digests
                or not 16 <= fresh <= 40 or len(graph["edges"]) != prefix["n"]+fresh):
            raise ValueError("independent original identity or extension range")
        digests.add(digest)
        entry = {"target_id": f"target-{number:04d}", "param": [r, t, p, q], "suffix": suffix,
                 "digest": digest, "fresh": fresh, "shard": f"targets-{(number-1)//16:02d}.json"}
        item = {**entry, "graph": graph}
        index.append({**entry, "record_sha256": api.sha(api.encoded(item))})
        items.append(item)
        if len(items) == 16:
            size += api.write_new(out/entry["shard"], items, limit)
            items = []
        if size > config["preparation"]["evidence_bytes"] or time.process_time()-started > 550:
            raise ValueError("preparation corpus cap")
    if items or len(index) != 256:
        raise ValueError("inexact corpus size")
    size += api.write_new(out/"corpus_index.json", {"targets": index, "count": 256}, limit)
    receipt = {"status": "FROZEN_UNLABELED_CORPUS_ONLY", "originals_checked": len(index),
               "prefix_reused_exact_bytes": True, "prefix_certificate_rechecked": True,
               "independent_reconstruction": "retained audit.original + unchanged verify_graph",
               "source_files_compiled_directly": True, "new_target_labelings": 0, "exterior_nodes": 0,
               "transfer_states": 0, "transitions": 0, "dispositions": 0, "solver_calls": 0,
               "corpus_bytes_before_receipt": size, "cpu_seconds": time.process_time()-started,
               "config_sha256": api.sha((api.KIT/"config.json").read_bytes())}
    api.write_new(out/"corpus_receipt.json", receipt, limit)
    print(api.encoded(receipt).decode(), end="")


if __name__ == "__main__":
    main()
