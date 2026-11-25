"""Freeze the D157-supplied prefix and only the unlabeled D161 corpus."""
from collections import Counter
from itertools import product
from pathlib import Path
import time
import types


def bindings():
    path = Path(__file__).absolute().with_name("bindings.py")
    module = types.ModuleType("d161_prepare_bindings")
    module.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), "exec"), vars(module))
    return module


def outgoing_prefix(old, model, check, retained):
    retained.verify_prefix(old, check.verify_certificate)
    if (old["n"], old["c"], old["d"], old["frontier"], old["actual_cut"]) != (54, 26, 28, "s:25", 29):
        raise ValueError("unexpected D134 initializer")
    if len(old["graph"]["profile"]) != 26:
        raise ValueError("initializer branch indices")
    profile = old["graph"]["profile"] + [[5, 2], [2, 4, 0]]
    graph = model.build_graph(profile)
    parents, _, digest = retained.original(graph)
    m, A, B, s, K = 74, 3, 4, 13, 10
    c, C, d = old["c"], 36, old["d"]
    k, J = K-A, s+2
    v, u, w = old["frontier"], "s:26", "s:27"
    a, b, P, Q = "b:26:0", "b:26:1", "b:27:0", "b:27:1"
    reduced = {v:3, u:4, w:0, a:1, b:2, P:5, Q:6, "b:27:2":7}
    if (m-old["n"] != 2*K or s+A+B != 2*K or old["n"] < 2*K or s < K-1
            or m != len(parents) or c+K != C or graph["spine"][-3:] != [v,u,w]):
        raise ValueError("D157 outbound size or physical connector")
    oriented = {name: value+A+(s if value >= c else 0) for name, value in old["oriented_labels"].items()}
    exterior = {name: value+(old["n"]+s if value > A else 0) for name,value in reduced.items()}
    if oriented[v] != exterior[v]:
        raise ValueError("D157 old/new frontier mismatch")
    oriented.update(exterior)
    owners = {i:a for i in range(3)}
    owners.update({J-k:P, J-k-1:P})
    left, h, word = 3, 3, (Q,b,Q)
    assignments = [(left,a), (J-left-h+1,Q), (J-left-h,a)]
    assignments += [(left+j, host) for j,host in enumerate(word,1)]
    assignments += [(J-left-j,word[j+1]) for j in range(h-1)]
    for source, host in assignments:
        if source in owners:
            raise ValueError("overlapping prescribed prefix cells")
        owners[source] = host
    if set(owners) != set(range(s)) or Counter(owners.values()) != {a:5,b:2,P:2,Q:4}:
        raise ValueError("D157 source and quota inventory")
    for host in (a,b,P,Q):
        terminals = sorted(name for name,parent in parents.items() if parent == host)
        sources = sorted(i for i,value in owners.items() if value == host)
        for name,i in zip(terminals,sources,strict=True):
            oriented[name] = A+c+i
    actual = {name:m-value for name,value in oriented.items()}
    # Independently check old names, old-side membership, actual edges and both spectra.
    opposite = 39
    crossing = sorted(abs(actual[x]-actual[y]) for x,y in graph["edges"]
                      if (actual[x]<opposite) != (actual[y]<opposite))
    noncrossing = sorted(abs(actual[x]-actual[y]) for x,y in graph["edges"]
                         if (actual[x]<opposite) == (actual[y]<opposite))
    if (crossing != list(range(37,75)) or noncrossing != list(range(1,37))
            or actual[w] != m or opposite != m+1-C
            or any(actual[name] != value+B+(s if value>=old["actual_cut"] else 0)
                   for name,value in old["actual_labels"].items())
            or not check.verify_certificate(graph,actual,expected_graph_digest=digest)["valid"]):
        raise ValueError("independent outbound certificate check failed")
    return {"n":m, "c":C, "d":C+2, "actual_cut":opposite, "polarity":"maximum", "frontier":w,
            "graph":graph, "digest":digest, "actual_labels":actual, "oriented_labels":oriented,
            "crossing":crossing,"noncrossing":noncrossing,
            "supplier":{"id":"D157-outbound","parameters":[2,1,1],"parent":old["digest"],
                        "A":A,"B":B,"s":s,"K":K,"reduced":reduced,"owners":owners}}


def profiles():
    for values in product(range(1,5), repeat=5):
        first, second = values[:3], values[3:]
        T1, T2 = sum(first), sum(second)
        K = (T1+T2+8)//2
        if first.count(4) == 1 and not (T1%2 or T2%2) and K >= 10:
            yield values, [list(first), list(second)+[0]], K


def main():
    started = time.process_time()
    api = bindings()
    config = api.read(api.KIT/"config.json")
    api.exact_runtime(config, base_process=True)
    for relative,digest in config["retained_sha256"].items():
        if api.sha(api.ordinary(api.ROOT/relative).read_bytes()) != digest:
            raise ValueError("source/retained prefix identity: "+relative)
    if any((api.ROOT/config[key]).exists() for key in ("output","approval")):
        raise ValueError("official paths must be vacant")
    out = api.ordinary(api.EVIDENCE/"input")
    out.mkdir()
    model = api.load_exact("d161_prep_model",api.ROOT/"lcl/model.py")
    check = api.load_exact("d161_prep_checker",api.ROOT/"lcl/verify.py")
    retained = api.load_exact("d161_prep_original_audit",api.LEGACY/"audit.py")
    prefix = outgoing_prefix(api.read(api.ROOT/config["retained_prefix"]),model,check,retained)
    record_max = config["limits"]["record_bytes"]
    size = api.write_new(out/"prefix.json",prefix,record_max)
    index, shard, digests, totals = [], [], set(), Counter()
    for number,(params,suffix,K) in enumerate(profiles(),1):
        if number>99 or K>13 or 2*K>prefix["n"]:
            raise ValueError("preparation corpus or size cap")
        graph = model.build_graph(prefix["graph"]["profile"]+suffix)
        _,_,digest = retained.original(graph)
        verified = check.verify_graph(graph)
        if (not verified["valid"] or verified["graph_digest"] != digest or digest in digests
                or len(graph["edges"]) != prefix["n"]+2*K):
            raise ValueError("independent original identity")
        digests.add(digest)
        T1,T2 = sum(suffix[0]),sum(suffix[1])
        totals[T1,T2] += 1
        entry = {"id":f"target-{number:03d}", "parameters":list(params), "suffix":suffix, "K":K,
                 "T1":T1,"T2":T2,"digest":digest,"shard":f"targets-{(number-1)//12:02d}.json"}
        item = {**entry,"graph":graph}
        index.append({**entry,"record_sha256":api.sha(api.encoded(item))})
        shard.append(item)
        if len(shard) == 12:
            size += api.write_new(out/entry["shard"],shard,record_max)
            shard = []
        if size>config["preparation"]["evidence_bytes"]-1_000_000 or time.process_time()-started>550:
            raise ValueError("preparation byte or CPU cap")
    if shard:
        size += api.write_new(out/index[-1]["shard"],shard,record_max)
    census = [[totals[T1,T2] for T2 in (2,4,6,8)] for T1 in (6,8,10)]
    if len(index) != 99 or census != [[0,0,9,3],[0,27,27,9],[3,9,9,3]]:
        raise ValueError("ordered census mismatch")
    size += api.write_new(out/"corpus_index.json",{"targets":index,"count":99,"census":census},record_max)
    receipt = {"status":"FROZEN_UNLABELED_CORPUS_ONLY","originals":99,"new_target_labelings":0,
               "prefix_digest":prefix["digest"],"prefix_sha256":api.sha((out/"prefix.json").read_bytes()),
               "prefix_certificate":"unchanged checker and independent named audit, spectra and old shifts",
               "exterior_nodes":0,"transfer_states":0,"transitions":0,"dispositions":0,"solver_calls":0,
               "official_fixtures":0,"official_invocations":0,"corpus_bytes_before_receipt":size,
               "cpu_seconds":time.process_time()-started}
    api.write_new(out/"corpus_receipt.json",receipt,record_max)
    print(api.encoded(receipt).decode(),end="")


if __name__ == "__main__":
    main()
