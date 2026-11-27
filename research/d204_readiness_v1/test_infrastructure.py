"""Bounded infrastructure-only regressions. Imports no Win32 or scientific consumer."""
import io
import os
from pathlib import Path
import struct
import sys
from tempfile import TemporaryDirectory
from threading import Barrier, Thread
from types import ModuleType
import unittest

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
        checks = [dict(valid=True, graph_digest=str(m), m=m) for m in (41,48)]
        result = dict.fromkeys(("states", "rank_class", "rank_inversions", "gap_widths",
                                "local_inventories", "final_inventories", "transport"))
        result.update(status="INDEPENDENTLY_VERIFIED_POSITIVE", checker_results=checks)
        wire = p.encode({"context": info, "candidate": pair, "result": result})
        self.assertTrue(p.verified_record(wire, info, pair, True, ["41","48"]))
        with self.assertRaisesRegex(p.Rejected, "VERIFICATION_BINDING"):
            p.verified_record(wire, info, p.binding(b"other"), True, ["41","48"])
        with self.assertRaisesRegex(p.Rejected, "CHECKER_ORIGINAL_BINDINGS"):
            p.verified_record(wire, info, pair, True, ["48","41"])

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
                        "a"*32, "d204-readiness-v1", "0", "0"]
            with self.assertRaises(SystemExit) as error:
                child.main()
            self.assertEqual(error.exception.code, 65)
        finally:
            sys.argv = old

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

if __name__ == "__main__":
    unittest.main(verbosity=2)
