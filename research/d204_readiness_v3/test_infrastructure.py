"""Bounded infrastructure-only regressions. Imports no Win32 or scientific consumer."""
import io
import os
from pathlib import Path
import struct
import sys
import queue
import threading
from tempfile import TemporaryDirectory
from threading import Barrier, Thread
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

HERE = Path(__file__).parent
def load(name, file):
    value = ModuleType(name)
    value.__file__ = str(file)
    sys.modules[name] = value
    exec(compile(file.read_bytes(), str(file), "exec"), vars(value))
    return value

p = load("ready_protocol", HERE/"protocol.py")
child = load("ready_fixture_tests", HERE/"worker.py")
entry = load("ready_entry_tests", HERE/"entry.py")
fake_native = ModuleType("ready_native")
fake_native.thread_lease = object
fake_native.read = lambda pipe, size: pipe.read(size)
sys.modules["ready_native"] = fake_native
controller = load("ready_controller_tests", HERE/"controller.py")
LIMIT = dict.fromkeys(p.COUNTERS, 10) | dict(cpu_seconds=10, wall_seconds=30, live_records=7)
CONTEXT = dict(pid=17, phase="primary", nonce="1"*32)

class ProtocolTests(unittest.TestCase):
    def test_frame_boundary_and_empty_eof(self):
        stream = io.BytesIO(p.packet(b"R", b"result"))
        self.assertEqual(p.frame(stream.read), (b"R", b"result"))
        self.assertIsNone(p.frame(stream.read))

    def test_oversize_rejected_before_body_read(self):
        calls = []
        def read(size):
            calls.append(size)
            return struct.pack(">I", p.FRAME_MAX + 1)
        with self.assertRaisesRegex(p.Rejected, "IPC_FRAME_LIMIT"):
            p.frame(read)
        self.assertEqual(calls, [4])

    def test_partial_header_and_payload(self):
        for raw in (b"\x00", struct.pack(">I", 8)+b"Rshort"):
            with self.subTest(raw=raw), self.assertRaisesRegex(p.Rejected, "IPC_TRUNCATED"):
                p.frame(io.BytesIO(raw).read)

    def test_invalid_records(self):
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":"\xff"}'):
            with self.subTest(raw=raw), self.assertRaises(p.Rejected):
                p.decode(raw)

    def test_exhaustion_requires_exact_geometry(self):
        r, _ = child.fixture(LIMIT, "primary", "exhaust", CONTEXT)
        self.assertEqual(p.result_record(p.encode(r), "primary", LIMIT)["status"], "EXHAUSTED")
        r["counters"]["geometry_entries"] -= 1
        with self.assertRaisesRegex(p.Rejected, "PARTIAL_EXHAUSTION"):
            p.result_record(p.encode(r), "primary", LIMIT)

    def test_counter_boolean_and_out_of_cap_rejected(self):
        r, _ = child.fixture(LIMIT, "primary", "exhaust", CONTEXT)
        for bad in (True, 11, -1):
            r["counters"]["allocation_states"] = bad
            with self.subTest(bad=bad), self.assertRaisesRegex(p.Rejected, "COUNTER_LIMIT"):
                p.result_record(p.encode(r), "primary", LIMIT)

    def test_audit_candidate_does_not_require_primary_cuts(self):
        r, _ = child.fixture(LIMIT, "audit", "positive", CONTEXT)
        self.assertNotIn("admissible_old_cuts", r)
        self.assertEqual(p.result_record(p.encode(r), "audit", LIMIT)["status"], "CANDIDATE")
        with self.assertRaisesRegex(p.Rejected, "PRIMARY_CUT_SCHEMA"):
            p.result_record(p.encode(r), "primary", LIMIT)

    def test_ordered_fixture_dispositions(self):
        self.assertEqual(p.decide("primary", "CANDIDATE", True, True), "STOP_VERIFIED_POSITIVE")
        self.assertEqual(p.decide("primary", "CANDIDATE", False, True), "STOP_VERIFICATION_FAILURE")
        self.assertEqual(p.decide("primary", "EXHAUSTED", None, True), "ADMIT_AUDIT")
        self.assertEqual(p.decide("primary", "INCOMPLETE", None, True), "STOP_INCOMPLETE")
        self.assertEqual(p.decide("audit", "EXHAUSTED", None, True, "ADMIT_AUDIT"), "STOP_REGISTERED_NEGATIVE")
        self.assertEqual(p.decide("audit", "CANDIDATE", True, True, "ADMIT_AUDIT"), "STOP_ENGINE_DISCREPANCY")
        with self.assertRaisesRegex(p.Rejected, "AUDIT_WITHOUT"):
            p.decide("audit", "EXHAUSTED", None, True, "STOP_INCOMPLETE")

    def test_missing_or_breached_measurements_never_accept(self):
        for condition in (None, False, 1):
            with self.subTest(condition=condition):
                self.assertEqual(p.decide("primary", "EXHAUSTED", None, condition),
                                 "STOP_RESOURCE_OR_CUSTODY_FAILURE")

    def test_verification_cannot_replay_other_candidate_or_context(self):
        raw, info = b"candidate", CONTEXT
        pair = p.binding(raw)
        checks = [dict(valid=True, graph_digest=str(m), m=m, n=m+1, errors=[]) for m in (41,48)]
        result = dict(verified_fixture=True, rank_class="rank_preserving", rank_inversions=[],
                      normalized_suffix=[48,28,20], status="INDEPENDENTLY_VERIFIED_POSITIVE",
                      checker_results=checks)
        result["states"] = [
            dict(size=size, actual_cut=cut, complementary_cut=size+1-cut, threshold=20,
                 actual_labels={str(i): i for i in range(size+1)},
                 complementary_labels={str(i): size-i for i in range(size+1)},
                 actual_edges=[{}]*size, complementary_edges=[{}]*size)
            for size, cut in ((41,18),(48,21))]
        for key, length in (("actual_old_edges",32),("old_map",33),("gap_widths",32),
                            ("local_inventories",2),("final_inventories",2),
                            ("changed_resources",2),("transport",3)):
            result[key] = [{}]*length
        wire = p.encode({"context": info, "candidate": pair, "result": result})
        original = dict(cut=18, labels=result["states"][0]["actual_labels"])
        self.assertTrue(p.verified_record(wire, info, pair, True, ["41","48"], "rank_preserving", original))
        with self.assertRaisesRegex(p.Rejected, "REPORT_DIFFERS_FROM_DURABLE_CANDIDATE"):
            p.verified_record(wire, info, pair, True, ["41","48"], "rank_preserving",
                              {"cut": 19, "labels": original["labels"]})
        with self.assertRaisesRegex(p.Rejected, "VERIFICATION_BINDING"):
            p.verified_record(wire, info, p.binding(b"other"), True, ["41","48"])
        with self.assertRaisesRegex(p.Rejected, "CHECKER_ORIGINAL_BINDINGS"):
            p.verified_record(wire, info, pair, True, ["48","41"])
        result["transport"] = None
        incomplete = p.encode({"context": info, "candidate": pair, "result": result})
        with self.assertRaisesRegex(p.Rejected, "VERIFIED_ARTIFACTS"):
            p.verified_record(incomplete, info, pair, True, ["41","48"], "rank_preserving", original)

    def test_absolute_deadline_caps_every_wait(self):
        absolute = 30_000
        self.assertEqual(p.remaining(24_000, absolute, 5000), 5000)
        self.assertEqual(p.remaining(29_000, absolute, 4000), 1000)
        self.assertEqual(p.remaining(30_000, absolute, 1000), 0)
        self.assertEqual(p.remaining(31_000, absolute, 1000), 0)

    def test_no_public_helper_subcommand(self):
        old = sys.argv
        try:
            sys.argv = [entry.__file__, entry.TASK, "owner", "x"*64, "y"*64]
            with self.assertRaisesRegex(RuntimeError, "FIXED_TASK_AND_ENTRY_REQUIRED"):
                entry.main()
        finally:
            sys.argv = old

    def test_worker_rejects_unknown_non_scientific_mode(self):
        old = sys.argv
        try:
            sys.argv = [child.__file__, child.TASK, "0"*64, "synthetic", "primary", "science",
                        "a"*32, "d204-readiness-v3", "primary", "0", "0"]
            with self.assertRaises(SystemExit) as error:
                child.main()
            self.assertEqual(error.exception.code, 65)
        finally:
            sys.argv = old

    def test_supplied_signaled_grant_cannot_launch_direct_science(self):
        args = [child.__file__, child.TASK, "0"*64, "official", "primary", "science",
                "a"*32, "d204-science-v3", "primary", "17", "18"]
        with TemporaryDirectory() as tmp, patch.object(child, "ROOT", Path(tmp)), \
             patch.object(sys, "argv", args), patch.object(child, "hello", return_value={}), \
             patch.object(child, "ipc_frame"), patch.object(child, "wait_for_grant"), \
             patch.object(child, "freeze", return_value={}), \
             patch.object(child, "scientific_adapter") as future:
            with self.assertRaises(FileNotFoundError):
                child.main()
            future.assert_not_called()

    def test_shadow_relative_package_does_not_load(self):
        name = "_d204_inert_loader_test"
        path = HERE / "not-a-file.py"
        try:
            child.exact_load(name, b"", path, package=True)
            child.exact_load(name + ".budget", b"VALUE = 17\n", path)
            result = child.exact_load(name + ".primary", b"from .budget import VALUE\n", path)
            self.assertEqual(result.VALUE, 17)
            self.assertEqual(sys.modules[name].__path__, [])
        finally:
            for key in (name, name+".budget", name+".primary"):
                sys.modules.pop(key, None)

class EvidenceTests(unittest.TestCase):
    def test_reservation_is_atomic_and_repeat_denied(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp)/"run"
            barrier = Barrier(2)
            outcomes = []
            def attempt():
                barrier.wait(2)
                try:
                    p.reserve(path)
                except p.Rejected:
                    outcomes.append("denied")
                else:
                    outcomes.append("granted")
            pair = [Thread(target=attempt) for _ in range(2)]
            for thread in pair:
                thread.start()
            for thread in pair:
                thread.join(5)
            self.assertCountEqual(outcomes, ["denied", "granted"])
            with self.assertRaisesRegex(p.Rejected, "RUN_ALREADY_RESERVED"):
                p.reserve(path)

    def test_candidate_both_files_synced_before_ack(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp)
            calls = []
            def sync(fd):
                calls.append(fd)
                os.fsync(fd)
            ledger = p.Ledger(path, 80_000, sync=sync)
            result, _ = child.fixture(LIMIT, "primary", "positive", CONTEXT)
            raw = p.encode(result)
            ident = p.persist_candidate(ledger, "primary", raw, result, CONTEXT)
            self.assertEqual(len(calls), 2)
            self.assertEqual(ident, p.binding((path/"primary-candidate.bin").read_bytes()))
            self.assertEqual(p.decode((path/"primary-candidate.json").read_bytes())["candidate"], ident)
            ledger.verify()

    def test_receipt_sync_failure_denies_ack_and_no_retry(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp)
            calls = []
            def sync(fd):
                calls.append(fd)
                if len(calls) == 2:
                    raise OSError("synthetic receipt fsync failure")
                os.fsync(fd)
            ledger = p.Ledger(path, 80_000, sync=sync)
            result, _ = child.fixture(LIMIT, "primary", "positive", CONTEXT)
            with self.assertRaisesRegex(OSError, "fsync"):
                p.persist_candidate(ledger, "primary", p.encode(result), result, CONTEXT)
            self.assertIn("primary-candidate.bin", ledger.records)
            self.assertNotIn("primary-candidate.json", ledger.records)
            self.assertGreater(ledger.charged, (path/"primary-candidate.bin").stat().st_size)
            with self.assertRaises(p.Rejected):
                ledger.verify()

    def test_cap_enforced_before_first_file_and_reserves_terminal(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp)
            ledger = p.Ledger(path, 65536 + 16)
            with self.assertRaisesRegex(p.Rejected, "EVIDENCE_LIMIT"):
                ledger.save_all([("raw.bin", b"X"*16), ("receipt.json", b"{}")])
            self.assertEqual(list(path.iterdir()), [])
            ledger.save("raw.bin", b"X"*16)
            ledger.save("terminal.json", b"{}", terminal=True)
            ledger.verify()

    def test_foreign_directory_invalidates_publication(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp)
            ledger = p.Ledger(path, 100000)
            ledger.save("start.json", b"{}")
            (path/"foreign").mkdir()
            with self.assertRaisesRegex(p.Rejected, "EVIDENCE_FILE_SET"):
                ledger.verify()

    def test_real_transport_receipt_fault_does_not_emit_ack(self):
        with TemporaryDirectory() as tmp:
            sync_calls = []
            def sync(fd):
                sync_calls.append(fd)
                if len(sync_calls) == 4:
                    raise OSError("inert candidate receipt sync failure")
                os.fsync(fd)
            ledger = p.Ledger(Path(tmp), 131072, sync=sync)
            candidate, _ = child.fixture(LIMIT, "primary", "positive", CONTEXT)
            wire = io.BytesIO(p.packet(b"H", b"{}") + p.packet(b"C", p.encode(candidate)))
            events, retained = queue.SimpleQueue(), {}
            with patch.object(controller, "hello_check", return_value={}):
                controller.transport(wire, events, retained, threading.Event(), ledger,
                                     {"context": CONTEXT}, None, {"limits": {"primary": LIMIT}},
                                     "primary", "positive", "fixture-primary", False, None, None, {})
            self.assertEqual([events.get_nowait() for _ in range(3)], ["RESUME","GRANT","TRANSPORT_ERROR"])
            self.assertTrue(events.empty())
            self.assertIn("fixture-primary-candidate.bin", ledger.records)
            self.assertNotIn("fixture-primary-candidate.json", ledger.records)

    def test_real_transport_refuses_out_of_order_verification(self):
        with TemporaryDirectory() as tmp:
            ledger = p.Ledger(Path(tmp), 131072)
            wire = io.BytesIO(p.packet(b"H", b"{}") + p.packet(b"V", b"{}"))
            events, retained = queue.SimpleQueue(), {}
            with patch.object(controller, "hello_check", return_value={}):
                controller.transport(wire, events, retained, threading.Event(), ledger,
                                     {"context": CONTEXT}, None, {"limits": {"primary": LIMIT}},
                                     "primary", "positive", "fixture-primary", False, None, None, {})
            self.assertEqual(retained["transport_error"], "IPC_EXPECTED_RESULT")
            self.assertEqual([events.get_nowait() for _ in range(3)], ["RESUME","GRANT","TRANSPORT_ERROR"])

    def test_shared_sequence_denies_audit_on_missing_or_over_budget_meter(self):
        for worker_cpu in (None, 301):
            with TemporaryDirectory() as tmp, self.subTest(worker_cpu=worker_cpu):
                entered = []
                def simulate(*args, **kwargs):
                    entered.append(args[6])
                    return dict(app=dict(result=dict(status="EXHAUSTED")),
                                failure=None, measured=worker_cpu is not None, worker_cpu=worker_cpu,
                                start_tick=10, controller_start_cpu=7)
                c = SimpleNamespace(n=SimpleNamespace(Tick=lambda: 15, CurrentProcess=lambda: 1),
                    live_read=lambda _: {"user": 3, "kernel": 4},
                    run_phase=simulate, bounded_io=lambda fn, _: fn(),
                    ticks=lambda s: s["user"]+s["kernel"], observe_crash=None)
                root = Path(tmp)
                phases = entry.sequence(c, p, None, "0"*64, {}, p.Ledger(root, 131072),
                                        root, "case", (("primary","exhaust"),("audit","exhaust")),
                                        lambda _: dict(cpu_max=300, wall=30, early=20))
                self.assertEqual(entered, ["primary"])
                self.assertEqual(phases[-1]["disposition"], "STOP_RESOURCE_OR_CUSTODY_FAILURE")

if __name__ == "__main__":
    unittest.main(verbosity=2)
