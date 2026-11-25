"""Read-only custody check of the saved corpus through uncached original sources."""

import hashlib
import json
import os
from pathlib import Path
import sys


KIT = Path(__file__).absolute().parent
ROOT = KIT.parents[1]
EVIDENCE = ROOT / "evidence/validation/LCL_ORDINARY_SPINE_MATCHED_EXTERIOR_TWO_CENTER_001"


def main():
    cache = EVIDENCE / ".source-only-cache-unused"
    if os.path.lexists(cache) or not sys.dont_write_bytecode:
        raise ValueError("source-only check requires a vacant cache root and -B")
    if any(item.is_dir() or item.is_symlink() for item in KIT.iterdir()):
        raise ValueError("kit package shadows are forbidden")
    for name in ("model", "verify"):
        if os.path.lexists(ROOT/"lcl"/name):
            raise ValueError("unexpected original-source package shadow")
    sys.pycache_prefix = str(cache)
    sys.path[:0] = [str(KIT),str(ROOT)]
    import audit
    import lcl
    from lcl import model, verify
    expected = {
        "__init__.py":"134055506d3e9cd4fa538177844d28a44d5ab567ec220cf54048e63d1a8a7374",
        "model.py":"7cfe57895aaf6ec977f3ce6ff948ecdc6ed9d9629c4b28c603d57200db4849a6",
        "verify.py":"230b852035a49eb2973a42730f31a5b94c733a92886dcc9158b50c3e94649909",
    }
    hashes = {}
    for module in (lcl,model,verify):
        file = Path(module.__file__).absolute()
        if file.parent != ROOT/"lcl" or not Path(module.__cached__).is_relative_to(cache):
            raise ValueError("loaded-source custody")
        hashes[file.name] = hashlib.sha256(file.read_bytes()).hexdigest()
    if hashes != expected:
        raise ValueError("original-source byte identity")
    frozen = EVIDENCE/"input"
    prefix = json.loads((frozen/"prefix.json").read_bytes())
    audit.verify_prefix(prefix,verify.verify_certificate)
    seed_config = json.loads((KIT/"config.json").read_bytes())["seed"]
    seed = json.loads((ROOT/seed_config["original"]).read_bytes())["graph"]
    retained = json.loads((ROOT/seed_config["result"]).read_bytes())["certificate"]
    if not verify.verify_certificate(seed,retained["labels"],seed_config["digest"])["valid"]:
        raise ValueError("D105 raw checker custody")
    count = 0
    for path in sorted(frozen.glob("targets-*.json")):
        for row in json.loads(path.read_bytes()):
            _, _, independent = audit.original(row["graph"])
            built = model.build_graph(row["graph"]["profile"])
            result = verify.verify_graph(row["graph"])
            if (not result["valid"] or result["graph_digest"] != row["digest"] or
                independent != row["digest"] or built != row["graph"]):
                raise ValueError("raw original reconstruction mismatch")
            count += 1
    if os.path.lexists(cache) or count != 320:
        raise ValueError("unexpected source-cache output or corpus coverage")
    result = {"status":"PASS_SOURCE_ONLY_ORIGINALS","originals_checked":count,
              "source_sha256":hashes,"initialized_prefix_checked":True,"retained_D105_checked":True,
              "preexisting_lcl_caches_bypassed":True,"bytecode_written":False,
              "exterior_nodes":0,"transfer_states":0,"official_target_labelings":0}
    with (EVIDENCE/"RAW_ORIGINAL_CHECK.json").open("x",encoding="utf-8",newline="\n") as stream:
        stream.write(json.dumps(result,sort_keys=True,separators=(",",":"))+"\n")
    print(json.dumps(result,sort_keys=True))


if __name__ == "__main__":
    main()
