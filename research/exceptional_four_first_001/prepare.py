"""Freeze the 2,304 unlabeled D164 originals and exact reusable D161 prefix."""
from collections import Counter
from itertools import product
import os
from pathlib import Path
import time
import types


def bindings():
    path = Path(__file__).absolute().with_name("bindings.py")
    module = types.ModuleType("d164_prepare_bindings")
    module.__file__ = str(path)
    exec(compile(path.read_bytes(),str(path),"exec"),vars(module))
    return module


def audited_prefix(api,config,checker,retained):
    raw = api.ordinary(api.ROOT/config["retained_prefix"]).read_bytes()
    prefix = api.read(api.ROOT/config["retained_prefix"])
    parent = api.read(api.ROOT/config["retained_parent_prefix"])
    retained.verify_prefix(parent,checker.verify_certificate)
    graph,labels = prefix["graph"],prefix["actual_labels"]
    _,_,digest = retained.original(graph)
    n,c,d,cut = prefix["n"],prefix["c"],prefix["d"],prefix["actual_cut"]
    if ((n,c,d,cut,prefix["frontier"],prefix["polarity"])!=(74,36,38,39,"s:27","maximum")
            or graph["spine"][-1]!=prefix["frontier"] or labels["s:27"]!=74
            or prefix["digest"]!=digest or graph["profile"]!=parent["graph"]["profile"]+[[5,2],[2,4,0]]
            or prefix["supplier"]["id"]!="D157-outbound" or prefix["supplier"]["parameters"]!=[2,1,1]
            or prefix["supplier"]["parent"]!=parent["digest"] or prefix["supplier"]["s"]!=13
            or prefix["oriented_labels"]!={name:n-value for name,value in labels.items()}
            or not checker.verify_certificate(graph,labels,expected_graph_digest=digest)["valid"]):
        raise ValueError("frozen D161 prefix identity and certificate")
    cross,noncross = [],[]
    for x,y in graph["edges"]:
        (cross if (labels[x]<cut)!=(labels[y]<cut) else noncross).append(abs(labels[x]-labels[y]))
    if (sorted(cross)!=list(range(37,75)) or sorted(cross)!=prefix["crossing"]
            or sorted(noncross)!=list(range(1,37)) or sorted(noncross)!=prefix["noncrossing"]
            or any(labels[name]!=value+4+(13 if value>=parent["actual_cut"] else 0)
                   or (labels[name]<cut)!=(value<parent["actual_cut"])
                   for name,value in parent["actual_labels"].items())):
        raise ValueError("frozen D161 phase and actual D157 old shifts")
    return raw,prefix


def profiles():
    for first in product(range(1,5),repeat=4):
        T1 = sum(first)
        if T1%2:
            continue
        for second in product(range(1,7),repeat=2):
            T2 = sum(second)
            if T2%2:
                K = (T1+T2+9)//2
                yield first+second,[list(first),list(second)+[0]],T1,T2,K


def qualification(first,T2,K):
    reason = ("NO_NEUTRAL_QUOTA_FOUR" if 4 not in first else
              "T2_3_PHYSICAL_COUNT" if T2==3 else None)
    E_raw = K>=10
    return ({"T":"PRESENT","E+":"PRESENT" if E_raw else "ABSENT"},
            {"T":reason,"E+":"RAW_EPLUS_K_LT_10" if not E_raw else
             reason or ("T2_5_NO_EXTERIOR_TERMINALS" if T2==5 else None)})


def main():
    started = time.process_time()
    api = bindings()
    config = api.read(api.KIT/"config.json")
    api.exact_runtime(config,base_process=True)
    for path,digest in config["retained_sha256"].items():
        if api.sha(api.ordinary(api.ROOT/path).read_bytes())!=digest:
            raise ValueError("retained file identity: "+path)
    if any(os.path.lexists(api.ordinary(api.ROOT/config[key])) for key in ("output","approval")):
        raise ValueError("official paths must be vacant")
    out = api.ordinary(api.EVIDENCE/"input")
    out.mkdir()
    model = api.load_exact("d164_prep_model",api.ROOT/"lcl/model.py")
    checker = api.load_exact("d164_prep_checker",api.ROOT/"lcl/verify.py")
    retained = api.load_exact("d164_prep_original_audit",api.LEGACY/"audit.py")
    raw_prefix,prefix = audited_prefix(api,config,checker,retained)
    with (out/"prefix.json").open("xb") as stream:
        stream.write(raw_prefix)
    size = len(raw_prefix)
    index,shard,digests = [],[],set()
    firsts,seconds,strata = Counter(),Counter(),Counter()
    first_profiles,second_profiles = set(),set()
    domain = config["domain"]
    limit = config["limits"]["record_bytes"]
    for number,(parameters,suffix,T1,T2,K) in enumerate(profiles(),1):
        if (number>domain["targets"] or not domain["K_min"]<=K<=domain["K_max"]
                or 2*K>prefix["n"]):
            raise ValueError("corpus size or prefix admission")
        graph = model.build_graph(prefix["graph"]["profile"]+suffix)
        _,_,digest = retained.original(graph)
        certified = checker.verify_graph(graph)
        if (not certified["valid"] or certified["graph_digest"]!=digest or digest in digests
                or len(graph["edges"])!=prefix["n"]+2*K):
            raise ValueError("independent named original identity")
        digests.add(digest)
        first,second = parameters[:4],parameters[4:]
        if first not in first_profiles:
            first_profiles.add(first)
            firsts[first.count(4)] += 1
        if second not in second_profiles:
            second_profiles.add(second)
            seconds[T2] += 1
        raw_exterior,symbolic = qualification(first,T2,K)
        strata["both_excluded"] += symbolic["T"] is not None and symbolic["E+"] is not None
        strata["additional_Eplus_excluded"] += symbolic["T"] is None and symbolic["E+"] is not None
        strata["eligible_separation"] += all(value is None for value in symbolic.values())
        strata["remaining_T"] += symbolic["T"] is None
        strata["remaining_Eplus"] += symbolic["E+"] is None
        strata["symbolic_arm_dispositions"] += sum(value is not None for value in symbolic.values())
        strata["raw_Eplus_absent"] += raw_exterior["E+"]=="ABSENT"
        entry = {"id":f"target-{number:04d}","parameters":list(parameters),"suffix":suffix,"K":K,
                 "T1":T1,"T2":T2,"quota_four_count":first.count(4),"quota_parities":[q%2 for q in parameters],
                 "raw_exterior":raw_exterior,"symbolic_basis":symbolic,
                 "digest":digest,"shard":f"targets-{(number-1)//domain['shard_size']:03d}.json"}
        item = {**entry,"graph":graph}
        index.append({**entry,"record_sha256":api.sha(api.encoded(item))})
        shard.append(item)
        if len(shard)==domain["shard_size"]:
            size+=api.write_new(out/entry["shard"],shard,limit)
            shard=[]
        if size>config["preparation"]["evidence_bytes"]-2_000_000 or time.process_time()-started>1180:
            raise ValueError("preparation byte or CPU cap")
    expected = {"both_excluded":912,"additional_Eplus_excluded":348,"eligible_separation":1044,
                "remaining_T":1392,"remaining_Eplus":1044,"symbolic_arm_dispositions":2172,
                "raw_Eplus_absent":26}
    census_first = [firsts[i] for i in range(5)]
    census_second = [seconds[i] for i in (3,5,7,9,11)]
    if (len(index)!=2304 or shard or census_first!=[41,52,30,4,1]
            or census_second!=[2,4,6,4,2] or strata!=expected):
        raise ValueError("exact symbolic corpus census")
    # The compact full index is individually capped at the frozen record bound.
    size+=api.write_new(out/"corpus_index.json",{"targets":index,"count":2304,
                        "first_by_quota_four":census_first,"second_by_total":census_second,
                        "symbolic_strata":strata},limit)
    receipt = {"status":"FROZEN_UNLABELED_CORPUS_ONLY","originals":2304,"shards":72,
               "prefix_sha256":api.sha(raw_prefix),"prefix_digest":prefix["digest"],
               "prefix_certificate":"Exact retained bytes, independent graph/edge/cut checks and unchanged checker",
               "symbolic_strata":strata,"exterior_nodes":0,"allocation_evaluations":0,"transfer_states":0,
               "transitions":0,"target_labelings":0,"solver_calls":0,"official_fixtures":0,
               "official_invocations":0,"corpus_bytes_before_receipt":size,
               "cpu_seconds":time.process_time()-started}
    api.write_new(out/"corpus_receipt.json",receipt,limit)
    print(api.encoded(receipt).decode(),end="")


if __name__=="__main__":
    main()
