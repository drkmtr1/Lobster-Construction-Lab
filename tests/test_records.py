"""Evidence binding, append-only attempts, bounded queues, and resume guards.

Storage tests use an isolated synthetic source project and a fixed environment
description, so concurrent development cannot turn a resume test into a source
change. Mathematical fixtures still run the actual local bounded DFS.
"""

import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from lcl.experiments import run_pilot, validate_config
from lcl.records import (atomic_json, checked_record, digest, read_json, run_lock,
                         save_single, save_source_snapshot, source_inventory)


def p4():
    return {"vertices": ["p0", "p1", "p2", "p3"],
            "edges": [["p0", "p1"], ["p1", "p2"], ["p2", "p3"]]}


def positive_result():
    return {"status": "SAT", "method": "test_fixture", "exhausted": False,
            "count": None, "count_lower_bound": 1,
            "witness": {"p0": 0, "p1": 3, "p2": 1, "p3": 2}}


def pilot_config(cases=2):
    return {"schema_version": 1, "objective": "B2-P1-interval-diagnostic",
            "engine": "dfs", "limits": {"max_nodes": 20000, "time_limit": 1.0,
                                            "max_vertices": 16, "max_states": 20000},
            "invocation": {"max_cases": 2, "wall_seconds": 4.0, "max_record_bytes": 2000000},
            "cases": [{"q": 1, "r": 1, "z0": 0, "z1": 0, "K": 1,
                       "interval_start": start, "side": "above"} for start in range(1, cases + 1)]}


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.project = self.root / "project"
        (self.project / "lcl").mkdir(parents=True)
        self.source_file = self.project / "lcl" / "fixture.py"
        self.source_file.write_text("# isolated source-snapshot fixture\n", encoding="utf-8")
        (self.project / "requirements-core.txt").write_text("# standard library\n", encoding="utf-8")
        self.fixed_environment = {"python": "test-runtime", "optional_dependencies": {"z3-solver": None}}
        for target in ("lcl.records.environment", "lcl.experiments.environment"):
            patcher = patch(target, return_value=self.fixed_environment)
            patcher.start()
            self.addCleanup(patcher.stop)

    def record(self, result, **kwargs):
        return checked_record(p4(), result, config={"fixture": True},
                              source=source_inventory(self.project), **kwargs)

    def test_original_target_witness_and_caller_restrictions_bound(self):
        result = positive_result()
        good = self.record(result, expected_pins={"p0": 0}, expected_domains={"p1": [3]})
        self.assertEqual(good["classification"], "SAT")
        self.assertTrue(good["certificate"]["valid"])
        self.assertFalse(good["universal_claim"])
        for kwargs in ({"expected_pins": {"p0": 3}}, {"expected_domains": {"p0": [1, 2]}}):
            # A valid unrestricted witness is insufficient for another declared scope.
            bad = self.record(result, **kwargs)
            self.assertEqual(bad["classification"], "QUARANTINED")
            self.assertTrue(bad["certificate"]["valid"])
            self.assertTrue(bad["consistency_errors"])
        substituted = positive_result()
        substituted["graph"] = {"vertices": p4()["vertices"],
                                 "edges": [["p0", "p1"], ["p0", "p2"], ["p0", "p3"]]}
        substituted["witness"] = {"p0": 0, "p1": 1, "p2": 2, "p3": 3}
        record = self.record(substituted)
        self.assertEqual(record["classification"], "QUARANTINED")
        self.assertFalse(record["certificate"]["valid"])
        self.assertEqual(record["original_graph"], p4())

    def test_inconsistent_counts_and_statuses_are_quarantined(self):
        cases = [dict(positive_result(), witness=None),
                 dict(positive_result(), status="EXHAUSTED_NO_SOLUTION", exhausted=True, count=0),
                 {"status": "EXHAUSTED_NO_SOLUTION", "exhausted": False, "count": 0, "witness": None},
                 {"status": "INCOMPLETE", "exhausted": False, "count": 0, "witness": None},
                 dict(positive_result(), exhausted=True, count=0),
                 dict(positive_result(), exhausted=True, count=True),
                 dict(positive_result(), exhausted=True, count=1, count_lower_bound=2)]
        for result in cases:
            self.assertEqual(self.record(result)["classification"], "QUARANTINED", result)
        incomplete = dict(positive_result(), status="INCOMPLETE")
        record = self.record(incomplete)
        self.assertEqual(record["classification"], "INCOMPLETE")
        self.assertTrue(record["certificate"]["valid"])

    def test_single_records_have_checksums_and_preserve_existing_directory(self):
        output = self.root / "single"
        record = save_single(self.project, output, p4(), positive_result(), {"example": 1})
        on_disk = read_json(output / "record.json")
        self.assertEqual(record, on_disk)
        payload = dict(on_disk)
        checksum = payload.pop("record_sha256")
        self.assertEqual(checksum, digest(payload))
        before = (output / "record.json").read_bytes()
        with self.assertRaises(FileExistsError):
            save_single(self.project, output, p4(), positive_result(), {"example": 2})
        self.assertEqual((output / "record.json").read_bytes(), before)
        self.assertEqual((output / "source" / "lcl" / "fixture.py").read_bytes(), self.source_file.read_bytes())

    def test_atomic_and_read_size_limits_preserve_old_evidence(self):
        target = self.root / "evidence.json"
        atomic_json(target, {"stable": 1})
        original = target.read_bytes()
        with self.assertRaises(FileExistsError):
            atomic_json(target, {"stable": 2})
        with self.assertRaises(ValueError):
            atomic_json(target, {"payload": "x" * 100}, replace=True, max_bytes=30)
        self.assertEqual(target.read_bytes(), original)
        self.assertFalse(list(self.root.glob("*.tmp")))
        with self.assertRaises(ValueError):
            read_json(target, max_bytes=1)

    def test_source_changed_during_snapshot_is_rejected(self):
        inventory = source_inventory(self.project)
        self.source_file.write_text("# changed after inventory\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            save_source_snapshot(self.project, self.root / "snapshot", inventory)

    def test_run_lock_is_exclusive_and_released_on_exception(self):
        directory = self.root / "locked"
        directory.mkdir()
        with self.assertRaisesRegex(RuntimeError, "simulated"):
            with run_lock(directory):
                lock = directory / "RUNNING.lock"
                original = lock.read_bytes()
                with self.assertRaises(FileExistsError):
                    with run_lock(directory):
                        self.fail("duplicate lock acquired")
                self.assertEqual(lock.read_bytes(), original)
                raise RuntimeError("simulated interruption")
        self.assertFalse((directory / "RUNNING.lock").exists())

    def test_case_cap_then_resume_preserves_attempts(self):
        config = pilot_config()
        config["invocation"]["max_cases"] = 1
        directory = self.root / "case-cap"
        first = run_pilot(self.project, config, output=directory)
        self.assertEqual(first["processed_this_invocation"], 1)
        self.assertEqual(first["unattempted_cases"], 1)
        self.assertEqual(first["stop_reason"], "invocation_max_cases")
        previous = next((directory / "cases").glob("*.json"))
        before = previous.read_bytes()
        second = run_pilot(self.project, config, resume=directory)
        self.assertEqual(second["recorded_cases"], 2)
        self.assertEqual(second["processed_this_invocation"], 1)
        self.assertEqual(second["counts"], {"EXHAUSTED_NO_SOLUTION": 1, "SAT": 1})
        self.assertEqual(previous.read_bytes(), before)
        self.assertEqual(len(list((directory / "cases").glob("*.json"))), 2)

    def test_retry_incomplete_appends_without_overwriting(self):
        config = pilot_config(cases=1)
        config["limits"]["max_nodes"] = 1
        directory = self.root / "retry"
        first = run_pilot(self.project, config, output=directory)
        self.assertEqual(first["counts"], {"INCOMPLETE": 1})
        previous = next((directory / "cases").glob("*.json"))
        before = previous.read_bytes()
        skipped = run_pilot(self.project, config, resume=directory)
        self.assertEqual(skipped["processed_this_invocation"], 0)
        retried = run_pilot(self.project, config, resume=directory, retry_incomplete=True)
        self.assertEqual(retried["processed_this_invocation"], 1)
        self.assertEqual(next(iter(retried["latest"].values()))["attempts"], 2)
        self.assertEqual(previous.read_bytes(), before)
        self.assertEqual(len(list((directory / "cases").glob("*.json"))), 2)

    def test_resume_rejects_config_source_and_environment_changes(self):
        config = pilot_config(cases=1)
        directory = self.root / "signature"
        run_pilot(self.project, config, output=directory)
        previous = next((directory / "cases").glob("*.json"))
        before = previous.read_bytes()
        changed = copy.deepcopy(config)
        changed["limits"]["max_nodes"] += 1
        with self.assertRaises(ValueError):
            run_pilot(self.project, changed, resume=directory)
        source_before = self.source_file.read_bytes()
        self.source_file.write_bytes(source_before + b"# edit\n")
        with self.assertRaises(ValueError):
            run_pilot(self.project, config, resume=directory)
        self.source_file.write_bytes(source_before)
        with patch("lcl.experiments.environment", return_value={"python": "changed-runtime"}):
            with self.assertRaises(ValueError):
                run_pilot(self.project, config, resume=directory)
        self.assertEqual(previous.read_bytes(), before)
        self.assertFalse((directory / "RUNNING.lock").exists())

    def test_quarantine_blocks_later_cases_and_resume(self):
        config = pilot_config()
        directory = self.root / "quarantined"
        # This is a genuine full graceful labeling, but it violates case 1's
        # caller-retained s:2=2 pin and suffix interval [1,1].
        labels = {"s:0": 1, "b:0:0": 4, "l:0:0:0": 6, "s:1": 7,
                  "b:1:0": 0, "l:1:0:0": 5, "s:2": 3, "s:3": 2}
        bad_engine = {"status": "SAT", "witness": labels, "count": None,
                      "count_lower_bound": 1, "exhausted": False, "method": "fault_injection"}
        with patch("lcl.experiments.solve", return_value=bad_engine) as engine:
            first = run_pilot(self.project, config, output=directory)
        self.assertEqual(engine.call_count, 1)
        self.assertEqual(first["counts"], {"QUARANTINED": 1})
        self.assertEqual(first["unattempted_cases"], 1)
        attempt = next((directory / "cases").glob("*.json"))
        before = attempt.read_bytes()
        self.assertNotIn("candidate", read_json(attempt)["extra"])
        with patch("lcl.experiments.solve", side_effect=AssertionError("continued after quarantine")):
            resumed = run_pilot(self.project, config, resume=directory)
        self.assertEqual(resumed["stop_reason"], "QUARANTINED_REVIEW_REQUIRED")
        self.assertEqual(resumed["processed_this_invocation"], 0)
        self.assertEqual(attempt.read_bytes(), before)

    def test_saved_attempt_integrity_and_positive_recheck(self):
        config = pilot_config(cases=1)
        config["cases"][0]["interval_start"] = 2
        directory = self.root / "integrity"
        run_pilot(self.project, config, output=directory)
        attempt = next((directory / "cases").glob("*.json"))
        original = read_json(attempt)
        self.assertEqual(original["classification"], "SAT")
        variants = []
        without_checksum = copy.deepcopy(original)
        without_checksum["result"]["witness"]["s:3"] = 99
        variants.append(without_checksum)
        recomputed = copy.deepcopy(without_checksum)
        recomputed.pop("record_sha256")
        recomputed["record_sha256"] = digest(recomputed)
        variants.append(recomputed)
        wrong_case = copy.deepcopy(original)
        wrong_case["extra"]["case_id"] = "0" * 64
        wrong_case.pop("record_sha256")
        wrong_case["record_sha256"] = digest(wrong_case)
        variants.append(wrong_case)
        for variant in variants:
            attempt.write_text(json.dumps(variant), encoding="utf-8")
            before = attempt.read_bytes()
            with patch("lcl.experiments.solve", side_effect=AssertionError("used corrupted evidence")):
                with self.assertRaises(ValueError):
                    run_pilot(self.project, config, resume=directory)
            self.assertEqual(attempt.read_bytes(), before)
            self.assertFalse((directory / "RUNNING.lock").exists())

    def test_manifest_and_source_snapshot_integrity_on_resume(self):
        config = pilot_config(cases=1)
        directory = self.root / "manifest"
        run_pilot(self.project, config, output=directory)
        manifest_path = directory / "manifest.json"
        original = manifest_path.read_bytes()
        manifest = read_json(manifest_path)
        manifest["config"]["limits"]["max_nodes"] += 1
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaises(ValueError):
            run_pilot(self.project, config, resume=directory)
        manifest_path.write_bytes(original)
        snapshot = directory / "source" / "lcl" / "fixture.py"
        snapshot.write_text("# altered retained source\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            run_pilot(self.project, config, resume=directory)

    def test_partial_limits_receive_defaults_before_case_execution(self):
        config = pilot_config(cases=1)
        config["limits"] = {}
        directory = self.root / "defaults"
        result = run_pilot(self.project, config, output=directory)
        self.assertEqual(result["recorded_cases"], 1)
        record = read_json(next((directory / "cases").glob("*.json")))
        self.assertEqual(set(record["config"]["effective_limits"]),
                         {"max_nodes", "time_limit", "max_vertices", "max_states"})

    def test_invocation_time_cap_stops_before_next_engine_call(self):
        config = pilot_config(cases=1)
        config["invocation"]["wall_seconds"] = 1
        with patch("lcl.experiments.monotonic", side_effect=[0.0, 2.0, 2.0]), \
             patch("lcl.experiments.solve", side_effect=AssertionError("started after invocation budget")):
            result = run_pilot(self.project, config, output=self.root / "wall-cap")
        self.assertEqual(result["processed_this_invocation"], 0)
        self.assertEqual(result["stop_reason"], "invocation_wall_seconds")
        self.assertEqual(result["unattempted_cases"], 1)

    def test_config_caps_and_strict_schema_before_profile_expansion(self):
        for version in (True, 1.0, 2):
            config = pilot_config(cases=1)
            config["schema_version"] = version
            with self.assertRaises(ValueError):
                validate_config(config)
        for key, value in (("max_cases", 101), ("max_cases", 0), ("wall_seconds", float("nan")),
                           ("max_record_bytes", 2000001)):
            config = pilot_config(cases=1)
            config["invocation"][key] = value
            with self.assertRaises(ValueError):
                validate_config(config)
        config = pilot_config(cases=1)
        config["cases"][0]["q"] = 10**12
        with patch("lcl.experiments.build_graph", side_effect=AssertionError("expanded unbounded profile")):
            with self.assertRaises(ValueError):
                validate_config(config)
        config = pilot_config(cases=1)
        config["cases"] *= 5001
        with self.assertRaises(ValueError):
            validate_config(config)


if __name__ == "__main__":
    unittest.main()
