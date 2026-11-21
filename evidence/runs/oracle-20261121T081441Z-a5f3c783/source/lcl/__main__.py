"""Bounded command-line entry points: python -m lcl --help."""
import argparse
import json
from pathlib import Path
import platform
import sys

from . import __version__
from .allocation import complete_two_host
from .budget import Limits
from .dp import count_labelings
from .engines import dependency_versions, networkx_diagnostics, symbolic_h010_check, z3_solve
from .experiments import run_pilot
from .ingest import graph_input, construction_input, allocation_input
from .oracle import permutation_oracle
from .records import read_json, save_single, unique_output
from .search import solve
from .verify import verify_certificate

PROJECT = Path(__file__).resolve().parent.parent


def emit(value):
    print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False))


def construct_declared(spec):
    return construction_input(spec)


def record_summary(directory, record):
    result = record["result"]
    return {"record": str(Path(directory).resolve() / "record.json"),
            "status": record["classification"], "method": result.get("method"),
            "original_graph_digest": record["original_graph_digest"],
            "vertices": len(record["original_graph"]["vertices"]),
            "edges": len(record["original_graph"]["edges"]),
            "independently_verified": bool(record["certificate"] and record["certificate"]["valid"]),
            "count": result.get("count"), "count_lower_bound": result.get("count_lower_bound"),
            "reason": result.get("reason"),
            "next_action": "Read STATE.md; inspect this certificate before using the result as evidence"}


def parser():
    p = argparse.ArgumentParser(description="Lobster Construction Lab: exact mathematics with bounded experiments")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="Show environment and optional dependency availability")
    d = sub.add_parser("demo", help="Load H010 example, construct, independently check and save evidence")
    d.add_argument("--out")
    c = sub.add_parser("construct", help="Apply an implemented formula to a declared original profile")
    c.add_argument("input"); c.add_argument("--out")
    s = sub.add_parser("solve", help="Run one bounded exact engine")
    s.add_argument("input"); s.add_argument("--engine", choices=("dfs", "dp", "z3", "oracle"), default="dfs")
    s.add_argument("--count", action="store_true", help="Request full enumeration (DFS); DP/oracle always count")
    s.add_argument("--limits", default=str(PROJECT / "configs" / "reference.json"))
    s.add_argument("--pins"); s.add_argument("--domains"); s.add_argument("--out")
    v = sub.add_parser("verify", help="Recheck labels against a separately supplied original graph/profile")
    v.add_argument("original"); v.add_argument("certificate")
    a = sub.add_parser("allocate", help="Apply R226 to a declared original graph and fixed core")
    a.add_argument("input"); a.add_argument("--out")
    e = sub.add_parser("pilot", help="Run or resume the finite declared B2 diagnostic queue")
    e.add_argument("config", nargs="?", default=str(PROJECT / "configs" / "b2_pilot.json"))
    e.add_argument("--resume"); e.add_argument("--retry-incomplete", action="store_true"); e.add_argument("--out")
    t = sub.add_parser("status", help="Read durable project state, optionally a pilot checkpoint")
    t.add_argument("--run")
    h = sub.add_parser("context", help="Print a compact handoff assembled from authoritative state")
    h.add_argument("--out")
    sub.add_parser("diagnostics", help="Run optional NetworkX/SymPy checks on a declared example")
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "doctor":
            emit({"project": str(PROJECT), "version": __version__, "python": sys.version,
                  "platform": platform.platform(), "executable": sys.executable,
                  "supported_python": "CPython 3.12 or 3.13, 64-bit recommended",
                  "optional_dependencies": dependency_versions(), "core_requires_external_packages": False})
            return 0
        if args.command in ("demo", "construct"):
            path = PROJECT / "examples" / "h010.json" if args.command == "demo" else Path(args.input)
            spec = read_json(path)
            original, result = construct_declared(spec)
            directory = args.out or unique_output(PROJECT, args.command)
            record = save_single(PROJECT, directory, original, result, spec)
            emit(record_summary(directory, record))
            return 0 if record["classification"] != "QUARANTINED" else 2
        if args.command == "solve":
            original = graph_input(args.input, max_vertices=100)
            limits = Limits.from_mapping(read_json(args.limits))
            pins = read_json(args.pins) if args.pins else None
            domains = read_json(args.domains) if args.domains else None
            if args.engine == "dfs":
                result = solve(original, pins=pins, domains=domains, limits=limits, count=args.count)
            elif args.engine == "dp":
                result = count_labelings(original, limits=limits, pins=pins, domains=domains)
            elif args.engine == "z3":
                if args.count:
                    raise ValueError("Z3 adapter provides one witness/existence status, not full counts")
                result = z3_solve(original, pins=pins, domains=domains, limits=limits)
            else:
                result = permutation_oracle(original, pins=pins, domains=domains,
                                            max_vertices=min(limits.max_vertices, 8),
                                            max_permutations=limits.max_nodes, time_limit=limits.time_limit)
            directory = args.out or unique_output(PROJECT, args.engine)
            config = {"engine": args.engine, "limits": limits.to_dict(), "pins": pins,
                      "domains": domains, "count_requested": args.count}
            record = save_single(PROJECT, directory, original, result, config,
                                 expected_pins=pins, expected_domains=domains)
            emit(record_summary(directory, record))
            return 2 if record["classification"] in ("QUARANTINED", "INVALID_INPUT", "UNAVAILABLE") else 0
        if args.command == "verify":
            original = graph_input(args.original)
            supplied = read_json(args.certificate)
            if not isinstance(supplied, dict):
                raise ValueError("Certificate must be a JSON object")
            expected = supplied.get("original_graph_digest")
            payload = supplied.get("result", supplied)
            if not isinstance(payload, dict):
                raise ValueError("Certificate result must be an object")
            labels = payload.get("witness", payload.get("labels", payload))
            checked = verify_certificate(original, labels, expected_graph_digest=expected)
            emit(checked)
            return 0 if checked["valid"] else 2
        if args.command == "allocate":
            spec = read_json(args.input)
            original = allocation_input(spec)
            result = complete_two_host(original, spec["core_labels"], tuple(spec["hosts"]))
            directory = args.out or unique_output(PROJECT, "r226")
            record = save_single(PROJECT, directory, original, result, spec,
                                 expected_pins=spec["core_labels"])
            emit(record_summary(directory, record))
            return 2 if record["classification"] in ("QUARANTINED", "INVALID_INPUT") else 0
        if args.command == "pilot":
            checkpoint = run_pilot(PROJECT, read_json(args.config), resume=args.resume,
                                   retry_incomplete=args.retry_incomplete, output=args.out)
            emit(checkpoint)
            return 2 if checkpoint["stop_reason"] in ("QUARANTINED", "QUARANTINED_REVIEW_REQUIRED", "INVALID_INPUT", "UNAVAILABLE") else 0
        if args.command == "status":
            print((PROJECT / "STATE.md").read_text(encoding="utf-8"))
            if args.run:
                emit(read_json(Path(args.run) / "checkpoint.json"))
            return 0
        if args.command == "context":
            context = "# Current handoff\n\n" + (PROJECT / "STATE.md").read_text(encoding="utf-8")
            context += "\n\n## Open obligations\n\n" + (PROJECT / "research" / "PROOF_OBLIGATIONS.md").read_text(encoding="utf-8")
            context += "\n\nRead AGENTS.md and the source-linked FINDINGS.md before changes. Include exact run IDs when reporting evidence.\n"
            if args.out:
                with Path(args.out).open("x", encoding="utf-8") as stream:
                    stream.write(context)
            else:
                print(context)
            return 0
        if args.command == "diagnostics":
            emit({"graph": networkx_diagnostics(graph_input(PROJECT / "examples" / "p4.json")),
                  "symbolic": symbolic_h010_check()})
            return 0
    except (ValueError, TypeError, KeyError, OSError) as exc:
        emit({"status": "ERROR", "error": str(exc), "next_action": "Correct the declared input or consult docs/OPERATIONS.md"})
        return 2
    except KeyboardInterrupt:
        emit({"status": "INCOMPLETE", "reason": "interrupted_outside_engine",
              "next_action": "Inspect saved case attempts; resume only a matching manifest"})
        return 130
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
