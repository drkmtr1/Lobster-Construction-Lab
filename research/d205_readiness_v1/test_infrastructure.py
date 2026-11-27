"""Bounded infrastructure-only regressions. Imports no Win32 or scientific consumer."""
import io
import json
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
LIMIT = dict.fromkeys(p.COUNTERS, 10) | dict(cpu_seconds=10, wall_seconds=30, live_records=7,
                                            geometry_entries=sum(p.STREAM_COUNTS.values()))
CONTEXT = dict(pid=17, phase="primary", nonce="1"*32)


def inert_fixture(limits, phase, mode, context):
    return child.fixture(limits, phase, mode, context, p.STREAM_COUNTS)

class ProtocolTests(unittest.TestCase):
    def test_native_quota_exit_requires_job_corroboration(self):
        final = {"active": 0, "lifetime": 1, "terminated": 1, "user": 15156250}
        self.assertTrue(controller.native_user_limit_observed(
            0xC0000044, False, final, 5000000, [{"message": 1}]))
        self.assertTrue(controller.native_user_limit_observed(
            1816, True, final, 5000000, []))
        self.assertFalse(controller.native_user_limit_observed(
            0xC0000044, False, final, 5000000, []))
        self.assertFalse(controller.native_user_limit_observed(
            0xC0000044, True, final | {"terminated":0}, 5000000, []))
        self.assertFalse(controller.native_user_limit_observed(
            0xC0000044, True, final | {"user":10}, 5000000, []))

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
        r, _ = inert_fixture(LIMIT, "primary", "exhaust", CONTEXT)
        self.assertEqual(p.result_record(p.encode(r), "primary", LIMIT)["status"], "EXHAUSTED")
        r["counters"]["geometry_entries"] -= 1
        with self.assertRaisesRegex(p.Rejected, "STREAM_AGGREGATE"):
            p.result_record(p.encode(r), "primary", LIMIT)

    def test_counter_boolean_and_out_of_cap_rejected(self):
        r, _ = inert_fixture(LIMIT, "primary", "exhaust", CONTEXT)
        for bad in (True, 11, -1):
            r["counters"]["allocation_states"] = bad
            with self.subTest(bad=bad), self.assertRaisesRegex(p.Rejected, "COUNTER_LIMIT"):
                p.result_record(p.encode(r), "primary", LIMIT)

    def test_both_engines_use_same_candidate_cut_schema(self):
        r, _ = inert_fixture(LIMIT, "audit", "positive", CONTEXT)
        self.assertNotIn("admissible_old_cuts", r)
        for phase in ("audit", "primary"):
            self.assertEqual(p.result_record(p.encode(r), phase, LIMIT)["status"], "CANDIDATE")
        r["admissible_old_cuts"] = [18]
        with self.assertRaisesRegex(p.Rejected, "RESULT_SCHEMA"):
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
        result = dict(variant="B", induced_old_cut=14, rank_class="rank_preserving", rank_inversions=[],
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
        original = dict(variant="B", induced_old_cut=14, cut=18, labels=result["states"][0]["actual_labels"])
        lifted = {v: 3+x+3*(x >= 18) for v, x in original["labels"].items()}
        lifted["s:7"] = 48
        for j, slot in enumerate((0, 2, 1)):
            lifted[f"b:7:{j}"] = j
            lifted[f"l:7:{j}:0"] = 21+slot
        result["states"][1]["actual_labels"] = lifted
        wire = p.encode({"context": info, "candidate": pair, "result": result})
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

    def test_v3_extra_lifetime_is_always_nonqualifying(self):
        origin = {"user": 0, "kernel": 0}
        worker = {"user": 156250, "kernel": 468750}
        extra = {"active": 0, "lifetime": 2, "user": 156250, "kernel": 625000}
        self.assertFalse(controller.ordinary_job_reconciled(origin, origin, worker, extra))
        self.assertFalse(controller.ordinary_job_reconciled(origin, origin, worker, extra | worker))
        self.assertTrue(controller.ordinary_job_reconciled(
            origin, origin, worker, worker | {"active": 0, "lifetime": 1}))

    def test_terminal_increment_keeps_cleanup_roster_and_component_guards(self):
        origin = {"user": 0, "kernel": 0}
        process = {"user": 781250, "kernel": 156250}
        job = {"active": 0, "lifetime": 1, "user": 625000, "kernel": 156250}
        def read(source, finished, before=None, unexpected=()):
            observations = {"snapshots": [
                {"stage":"before-process-handle-close","accounting": before or source},
                {"stage":"after-job-active-zero","accounting":source,"pids":[]}],
                "observed_unexpected_identities":list(unexpected)}
            return controller.reconcile_terminal_cpu(origin, origin, finished, source, observations)
        value = read(job, process)
        self.assertEqual(value["mode"], "host-one-increment")
        self.assertEqual(value["guard_ticks"], 156250)
        self.assertEqual(read(job, {"user":781250, "kernel":0})["mode"], "unresolved")
        self.assertEqual(read(job, {"user":937500, "kernel":156250})["mode"], "unresolved")
        self.assertEqual(read(job | {"lifetime":2}, process)["mode"], "unresolved")
        self.assertEqual(read(job, process, job | {"user":0})["mode"], "unresolved")
        self.assertEqual(read(job, process, unexpected=(999,))["mode"], "unresolved")

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
                        "a"*32, "d205-readiness-v1", "primary", "0", "0"]
            with self.assertRaises(SystemExit) as error:
                child.main()
            self.assertEqual(error.exception.code, 65)
        finally:
            sys.argv = old

    def test_supplied_signaled_grant_cannot_launch_direct_science(self):
        args = [child.__file__, child.TASK, "0"*64, "official", "primary", "science",
                "a"*32, "d205-independent-path-order-menu-001", "primary", "17", "18"]
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
            result, _ = inert_fixture(LIMIT, "primary", "positive", CONTEXT)
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
            result, _ = inert_fixture(LIMIT, "primary", "positive", CONTEXT)
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
            candidate, _ = inert_fixture(LIMIT, "primary", "positive", CONTEXT)
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

class CrashEvidenceTests(unittest.TestCase):
    def setUp(self):
        native = patch.multiple(fake_native, create=True, FLAGS=8204,
                                WORKER_CREATION_FLAGS=0x0008040C,
                                TERMINATED_BY_SUPERVISOR=0xE2040001)
        native.start()
        self.addCleanup(native.stop)
        self.exe = Path("bound-python/python.exe")
        self.bundle = {"dependencies": {}}

    def evidence(self):
        exe, folder = str(self.exe), self.exe.parent
        common = dict(task=controller.TASK, phase="primary")
        own = dict(common, pid=110, nonce="1"*32)
        kid = dict(common, pid=120, nonce="2"*32)
        def runtime(context):
            return dict(context=context, executable=exe, dll=str(folder / "python313.dll"),
                        version=[3, 13, 17], isolated=True, no_site=True, no_bytecode=True,
                        console=dict(process_count=0, window=False), modules={},
                        search=[str(folder / path) for path in ("python313.zip", "DLLs", "Lib", "")])
        owner = dict(born=134415000000000001, user=0, kernel=0)
        worker = dict(born=134415000000155751, user=0, kernel=0)
        info = dict(context=own, process=owner, assigned=False, mode="crash-owner",
                    profile="synthetic", start_tick=1000, early_tick=10500, deadline_tick=31000,
                    run="inert", freeze="7"*64)
        limit = dict(native_user_ticks=60000000, flags=8204, active_limit=1, end_action=0,
                     job_handle_inheritable=False)
        room = dict(active=1, lifetime=1, user=0, kernel=0, terminated=0)
        pids = dict(pids=[120], reported_assigned=1)
        inner = dict(info, context=kid, process=worker, assigned=True, mode="crash-sleeper",
                     start_tick=1250, deadline_tick=19250, member=True,
                     effective=limit.copy(), job_empty=dict(room, active=0, lifetime=0),
                     job_suspended=room.copy(), job_pids=pids.copy(),
                     at_creation=dict(flags=0x0008040C, job_at_creation=True, job_handle=44,
                                      inherited=[48, 52, 56, 60]),
                     ownership=dict(unnamed_job=True, owner_retains_sole_job_handle=True),
                     controller=dict(pid=110, born=owner["born"]))
        ready = dict(worker_activation=kid.copy(), runtime=runtime(kid.copy()), resume_tick=1350,
                     ready_tick=1410, member=True, initial_suspend_count=1,
                     effective=limit.copy(), job_pids=pids.copy(), accounting=room.copy())
        request = dict(prior_samples=dict(owner=dict(owner, user=150), worker=dict(worker, user=62)),
                       checked_tick=1420, issued_tick=1421, returned_tick=1422,
                       owner_unsignaled=True, worker_unsignaled=True, target_pid=110,
                       target_born=owner["born"], intended_status=0xE2040001,
                       api_succeeded=True, winerror=None)
        raw = dict(inner=inner, ready=ready, ready_received_tick=1415, owner_runtime=runtime(own.copy()),
                   held=dict(owner=dict(pid=110, image=exe, times=owner.copy()),
                             worker=dict(pid=120, image=exe, times=worker.copy())),
                   request=request, errors=[], direct_worker_termination=False,
                   observer_job_handle=False, terminal_job_accounting=None,
                   cleanup_deadline_tick=5421, observations_complete_tick=1434,
                   exits=dict(owner=dict(signaled_tick=1433, code=0xE2040001,
                                         times=dict(owner, end=owner["born"]+3050011, user=170)),
                              worker=dict(signaled_tick=1434, code=0,
                                          times=dict(worker, end=owner["born"]+3060123, user=77))))
        return raw, info

    def classify(self, raw, info):
        return controller.classify_crash(raw, info, self.exe, self.bundle)

    def reject(self, raw, info, reason, cleanup=True):
        proof = self.classify(raw, info)
        self.assertFalse(proof["controlled_interruption"])
        self.assertEqual(proof["cleanup_verified"], cleanup, proof)
        self.assertEqual(proof["reason"], reason)

    def test_interruption_zero_with_observed_termination(self):
        raw, info = self.evidence()
        self.assertEqual(self.classify(raw, info), {
            "controlled_interruption": True, "cleanup_verified": True, "reason": None})
        # Process handles and terminal clocks may be observed in either order.
        raw["exits"]["worker"]["signaled_tick"] = 1430
        raw["exits"]["worker"]["times"]["end"] = raw["exits"]["owner"]["times"]["end"] - 150
        self.assertTrue(self.classify(raw, info)["controlled_interruption"])

    def test_zero_without_deliberate_interruption(self):
        raw, info = self.evidence()
        raw["request"] = None
        self.reject(raw, info, "CRASH_EVIDENCE_SCHEMA")

    def test_reject_process_already_signaled_before_request(self):
        for key in ("owner_unsignaled", "worker_unsignaled"):
            with self.subTest(process=key):
                raw, info = self.evidence()
                raw["request"][key] = False
                self.reject(raw, info, "CRASH_OWNER_TERMINATION_REQUEST")

    def test_reject_missing_or_wrong_activation_and_nonce(self):
        raw, info = self.evidence()
        raw["ready"]["worker_activation"] = None
        self.reject(raw, info, "CRASH_ACTIVATION")
        raw, info = self.evidence()
        raw["ready"]["runtime"]["context"]["nonce"] = "3"*32
        self.reject(raw, info, "WORKER_CONTEXT")

    def test_reject_stale_creation_identity(self):
        raw, info = self.evidence()
        raw["held"]["worker"]["times"]["born"] += 1
        self.reject(raw, info, "CRASH_RETAINED_IDENTITY", cleanup=False)

    def test_reject_failed_ambiguous_or_misdirected_request(self):
        for updates in ({"api_succeeded": False, "winerror": 5}, {"api_succeeded": None},
                        {"api_succeeded": True, "winerror": 5}, {"target_pid": 120}):
            with self.subTest(request=updates):
                raw, info = self.evidence()
                raw["request"].update(updates)
                self.reject(raw, info, "CRASH_OWNER_TERMINATION_REQUEST")

    def test_reject_natural_or_known_fixture_failure(self):
        for role, code in (("owner", 67), ("owner", 0), ("worker", 66),
                           ("worker", 1), ("worker", 64), ("worker", 0xC0000044)):
            with self.subTest(role=role, code=code):
                raw, info = self.evidence()
                raw["exits"][role]["code"] = code
                self.reject(raw, info, "CRASH_NATURAL_OR_FAILURE_EXIT")

    def test_reject_missing_retained_signaling(self):
        raw, info = self.evidence()
        raw["exits"]["worker"]["signaled_tick"] = None
        self.reject(raw, info, "CRASH_INDEPENDENT_SIGNAL_REQUIRED", cleanup=False)

    def test_reject_missing_regressing_or_float_terminal_measurements(self):
        for field, value in (("user", None), ("user", 9), ("end", 1.34415e17)):
            with self.subTest(field=field, value=value):
                raw, info = self.evidence()
                raw["exits"]["worker"]["times"][field] = value
                self.reject(raw, info, "CRASH_TERMINAL_ACCOUNTING")

    def test_reject_deadline_and_contradictory_chronology(self):
        for key, value in (("issued_tick", 19250), ("returned_tick", 1435)):
            with self.subTest(request=key):
                raw, info = self.evidence()
                raw["request"][key] = value
                self.reject(raw, info, "CRASH_CHRONOLOGY_OR_DEADLINE")
        raw, info = self.evidence()
        raw["observations_complete_tick"] = 5422
        self.reject(raw, info, "CRASH_CHRONOLOGY_OR_DEADLINE")
        raw, info = self.evidence()
        raw["exits"]["owner"]["times"]["end"] = raw["held"]["worker"]["times"]["born"] - 1
        self.reject(raw, info, "CRASH_FILETIME_CORROBORATION")

    def test_reject_direct_worker_termination(self):
        raw, info = self.evidence()
        raw["direct_worker_termination"] = True
        self.reject(raw, info, "CRASH_ALTERNATE_TERMINATION_OR_OBSERVATION_FAILURE")

    def test_reject_unverified_job_ownership_and_second_member(self):
        raw, info = self.evidence()
        raw["inner"]["ownership"]["owner_retains_sole_job_handle"] = False
        self.reject(raw, info, "CRASH_JOB_OWNERSHIP_OR_LIMITS")
        raw, info = self.evidence()
        raw["observer_job_handle"] = True
        self.reject(raw, info, "CRASH_OBSERVER_JOB_HANDLE")
        raw, info = self.evidence()
        raw["ready"]["accounting"]["lifetime"] = 2
        self.reject(raw, info, "CRASH_JOB_ACCOUNTING")
        raw, info = self.evidence()
        raw["inner"]["at_creation"]["inherited"][0] = 44
        self.reject(raw, info, "CRASH_ASSIGNMENT_OR_INHERITANCE")

    def test_phase_transport_retains_raw_when_classifier_rejects(self):
        raw, info = self.evidence()
        raw["request"]["api_succeeded"] = False
        with TemporaryDirectory() as tmp:
            ledger = p.Ledger(Path(tmp), 131072)
            wire = io.BytesIO(p.packet(b"H", p.encode(raw["owner_runtime"])) +
                              p.packet(b"J", p.encode(raw["inner"])))
            notices, records = queue.SimpleQueue(), {}
            def relay(inner, phase_info, save, read, queue_, app, exe, bundle, owner_runtime):
                self.assertEqual(inner, raw["inner"])
                controller.publish_crash(raw, app, save, phase_info, exe, bundle)
            controller.transport(wire, notices, records, threading.Event(), ledger, info,
                                 self.exe, self.bundle, "primary", "crash-owner", "crash-primary",
                                 False, None, relay, {})
            ledger.verify()
            preserved = Path(tmp, "crash-primary-crash-exit.json").read_bytes()
            self.assertEqual(p.decode(preserved), raw)
            self.assertEqual(records["crash_receipt"], raw)
            self.assertEqual(records["crash_raw_binding"], p.binding(preserved))
            self.assertEqual(records["crash_classification"]["reason"], "CRASH_OWNER_TERMINATION_REQUEST")
            self.assertTrue(records["crash_classification"]["cleanup_verified"])

    def test_failed_raw_sync_retains_observation_but_denies_classification(self):
        raw, info = self.evidence()
        records = {}
        def broken_save(name, payload):
            self.assertEqual(records["crash_receipt"], raw)
            self.assertNotIn("crash_classification", records)
            raise OSError("inert sync error")
        with self.assertRaisesRegex(OSError, "inert sync error"):
            controller.publish_crash(raw, records, broken_save, info, self.exe, self.bundle)
        self.assertTrue(records["crash_classification"]["cleanup_verified"])
        self.assertFalse(records["crash_classification"]["controlled_interruption"])
        self.assertNotIn("crash_raw_binding", records)

    def test_crash_evidence_does_not_admit_ordinary_scientific_phase(self):
        raw, info = self.evidence()
        self.reject(raw, dict(info, profile="official"), "CRASH_FIXTURE_BINDING")
        account = dict(active=0, lifetime=1, user=7, kernel=2)
        self.assertTrue(controller.ordinary_job_reconciled(account, account, account, account))
        self.assertFalse(controller.ordinary_job_reconciled(account, account, account, None))
        self.assertEqual(p.decide("primary", "CANDIDATE", None, False),
                         "STOP_RESOURCE_OR_CUSTODY_FAILURE")

    def test_artificial_marker_cannot_replace_sealed_actual_matrix(self):
        ready = dict(task=entry.TASK, freeze="a"*64, ready=True, all_required_checks_passed=True,
                     disposition="D205_EXECUTION_READY_AWAITING_OWNER_AUTHORIZATION")
        with self.assertRaisesRegex(RuntimeError, "QUALIFICATION_RECEIPT_BINDING"):
            entry.qualification_gate(p, ready, ready["freeze"], {}, b"{}", b"{}", b"{}", {})
        ready.update({kind:p.binding(b"{}") for kind in ("terminal", "seal", "outer")})
        with self.assertRaisesRegex(RuntimeError, "QUALIFICATION_NATIVE_TERMINAL"):
            entry.qualification_gate(p, ready, ready["freeze"], {}, b"{}", b"{}", b"{}", {})


class D205StreamAndAdapterTests(unittest.TestCase):
    def receipt(self, mode="exhaust"):
        return inert_fixture(LIMIT, "primary", mode, CONTEXT)[0]

    def validate(self, row, domain=None, limits=LIMIT):
        return p.result_record(p.encode(row), "primary", limits, domain)

    def test_exact_exhaustion_order_and_all_twelve_counts(self):
        row = self.validate(self.receipt())
        self.assertEqual(list(row["streams"]), list(p.STREAM_COUNTS))
        self.assertEqual(sum(r["geometry_entries"] for r in row["streams"].values()), 15067066)

    def test_missing_stream_with_correct_claimed_aggregate(self):
        row = self.receipt()
        row["streams"].pop("C:16:19")
        self.assertEqual(row["counters"]["geometry_entries"], 15067066)
        with self.assertRaisesRegex(p.Rejected, "STREAM_AGGREGATE"):
            self.validate(row)

    def test_wrong_stream_distribution_preserves_total_but_fails(self):
        row = self.receipt()
        row["streams"]["B:14:18"]["geometry_entries"] -= 1
        row["streams"]["B:14:19"]["geometry_entries"] += 1
        with self.assertRaisesRegex(p.Rejected, "INEXACT_COMPLETED_STREAM"):
            self.validate(row)

    def test_unknown_duplicate_and_out_of_order_streams(self):
        row = self.receipt()
        duplicate = p.encode(row).replace(b'"B:14:18":{', b'"B:14:18":{},"B:14:18":{', 1)
        self.assertNotEqual(duplicate, p.encode(row))
        with self.assertRaisesRegex(p.Rejected, "DUPLICATE_JSON_KEY"):
            p.result_record(duplicate, "primary", LIMIT)
        row["streams"] = dict(reversed(list(row["streams"].items())))
        with self.assertRaisesRegex(p.Rejected, "STREAM_ORDER_OR_IDENTITY"):
            p.result_record(json.dumps(row).encode(), "primary", LIMIT)
        row["streams"]["A:14:18"] = row["streams"].pop("B:14:18")
        with self.assertRaisesRegex(p.Rejected, "STREAM_ORDER_OR_IDENTITY"):
            self.validate(row)

    def test_partial_stream_prefix_may_end_at_zero_visited(self):
        row = self.receipt("incomplete")
        self.assertEqual(self.validate(row)["status"], "INCOMPLETE")
        first, second = list(p.STREAM_COUNTS)[:2]
        row["streams"][first]["geometry_entries"] = p.STREAM_COUNTS[first]
        row["streams"][second] = dict(geometry_entries=1, rank_preserving=1, rank_changing=0)
        row["counters"]["geometry_entries"] = p.STREAM_COUNTS[first]+1
        self.assertEqual(self.validate(row)["streams"][second]["geometry_entries"], 1)
        row["streams"][first]["geometry_entries"] -= 1
        row["counters"]["geometry_entries"] -= 1
        with self.assertRaisesRegex(p.Rejected, "INEXACT_COMPLETED_STREAM"):
            self.validate(row)

    def test_rank_types_range_and_joint_limit(self):
        for x, y in ((True, 0), (1.0, 0), (-1, 0), (1, 1)):
            row = self.receipt("positive")
            row["streams"]["B:14:18"].update(rank_preserving=x, rank_changing=y)
            with self.subTest(x=x, y=y), self.assertRaisesRegex(p.Rejected, "STREAM_RANK_COUNTERS"):
                self.validate(row)
        row = self.receipt("positive")
        row["streams"]["B:14:18"]["geometry_entries"] = 1.0
        with self.assertRaisesRegex(p.Rejected, "STREAM_GEOMETRY"):
            self.validate(row)

    def test_large_exact_caps_without_32_bit_truncation(self):
        cap = LIMIT | dict(placement_attempts=11769116626, allocation_states=7092178966,
                           pair_trials=28121614404)
        row = self.receipt()
        for key in ("placement_attempts", "allocation_states", "pair_trials"):
            row["counters"][key] = cap[key]
        result = self.validate(row, limits=cap)
        self.assertEqual(result["counters"]["pair_trials"], 28121614404)
        for bad in (28121614405, 28121614404.0, True):
            row["counters"]["pair_trials"] = bad
            with self.subTest(count=bad), self.assertRaisesRegex(p.Rejected, "COUNTER_LIMIT"):
                self.validate(row, limits=cap)

    def test_candidate_variant_rank_and_stream_position_are_bound(self):
        for update, reason in (({"variant": "A"}, "CANDIDATE_SCHEMA"),
                               ({"variant": "C"}, "CANDIDATE_STREAM_POSITION"),
                               ({"induced_old_cut": True}, "CANDIDATE_SCHEMA"),
                               ({"induced_old_cut": 15}, "CANDIDATE_STREAM_POSITION"),
                               ({"cut": 19}, "CANDIDATE_STREAM_POSITION"),
                               ({"rank_class": "rank_changing"}, "CANDIDATE_STREAM_POSITION")):
            row = self.receipt("positive")
            row.update(update)
            with self.subTest(fields=update), self.assertRaisesRegex(p.Rejected, reason):
                self.validate(row)

    def dummy_named_domain(self):
        # Synthetic names and no graph or edge weights.
        old = [f"inert-old-{i}" for i in range(33)]
        fresh = ["s:6", *(f"inert-fresh-{i}" for i in range(8))]
        names = old+fresh
        images = [*range(1, 15), *range(18, 37)]
        vacant = sorted(set(range(42))-set(images))
        domain = dict(vertices_41=sorted(names), old_order={"B":old, "C":old})
        return domain, dict(zip(names, (*images, *vacant), strict=True))

    def test_exact_named_alphabet_must_agree_with_actual_induced_cut(self):
        domain, labels = self.dummy_named_domain()
        row = self.receipt("positive")
        row["labels"] = labels
        self.assertEqual(self.validate(row, domain)["cut"], 18)
        # Claim third stream, including correct earlier totals, with an unchanged cut-14 map.
        visits = 0
        for i, (stream, ceiling) in enumerate(p.STREAM_COUNTS.items()):
            row["streams"][stream] = dict(geometry_entries=1 if i==2 else ceiling,
                                          rank_preserving=1 if i==2 else 0, rank_changing=0)
            visits += row["streams"][stream]["geometry_entries"]
            if i==2:
                break
        row["induced_old_cut"] = 15
        row["counters"]["geometry_entries"] = visits
        with self.assertRaisesRegex(p.Rejected, "CANDIDATE_OLD_EMBEDDING"):
            self.validate(row, domain)
        row = self.receipt("positive")
        row["labels"] = dict(labels, unexpected=42)
        with self.assertRaisesRegex(p.Rejected, "CANDIDATE_NAMED_ALPHABET"):
            self.validate(row, domain)

    def test_persisted_receipt_repeats_exact_menu_and_stream_fields(self):
        row = self.receipt("positive")
        raw = p.encode(row)
        with TemporaryDirectory() as tmp:
            ledger = p.Ledger(Path(tmp), 131072)
            p.persist_candidate(ledger, "fixture", raw, row, CONTEXT)
            stored = p.decode(Path(tmp, "fixture-candidate.json").read_bytes())
            self.assertEqual([stored[k] for k in ("variant", "induced_old_cut", "cut")], ["B", 14, 18])
            self.assertEqual(stored["stream"], "B:14:18")
            self.assertEqual(stored["stream_geometry_entries"], 1)
            self.assertEqual(Path(tmp, "fixture-candidate.bin").read_bytes(), raw)
            ledger.verify()

    def test_inert_verification_never_accepted_as_scientific(self):
        row, check = inert_fixture(LIMIT, "primary", "positive", CONTEXT)
        ident = p.binding(p.encode(row))
        raw = p.encode(dict(context=CONTEXT, candidate=ident, result=check(row)))
        self.assertTrue(p.verified_record(raw, CONTEXT, ident, False, []))
        with self.assertRaisesRegex(p.Rejected, "SYNTHETIC_VERIFICATION_FORBIDDEN"):
            p.verified_record(raw, CONTEXT, ident, True, [], row["rank_class"], row)

    def test_reject_verifier_variant_cut_and_suffix_substitutions(self):
        domain, labels = self.dummy_named_domain()
        row = self.receipt("positive")
        row["labels"] = labels
        self.validate(row, domain)
        ident = p.binding(p.encode(row))
        result = dict(status="INDEPENDENTLY_VERIFIED_POSITIVE", variant="C", induced_old_cut=14,
                      normalized_suffix=[48,28,20],
                      checker_results=[dict(valid=True, graph_digest=str(m), m=m, n=m+1, errors=[])
                                       for m in (41,48)],
                      states=[dict(actual_cut=18, actual_labels=labels), dict(actual_labels={})])
        def rejected(reason):
            with self.assertRaisesRegex(p.Rejected, reason):
                p.verified_record(p.encode(dict(context=CONTEXT, candidate=ident, result=result)),
                                  CONTEXT, ident, True, ["41","48"], row["rank_class"], row)
        rejected("VERIFIED_MENU_BINDING")
        result.update(variant="B", induced_old_cut=15)
        rejected("VERIFIED_MENU_BINDING")
        result["induced_old_cut"] = 14
        rejected("VERIFIED_SUFFIX_TRANSPORT")

    def test_separate_director_and_owner_receipts_are_required(self):
        with self.assertRaisesRegex(RuntimeError, "EXACT_DIRECTOR_QUALIFICATION_ACCEPTANCE_REQUIRED"):
            entry.director_gate(None, "f"*64, "q"*64)
        director = dict(task=entry.TASK, freeze="f"*64, qualification_sha256="8"*64,
                        disposition="ACCEPT_D205_EXECUTION_READINESS", director_decision="inert acceptance")
        with self.assertRaisesRegex(RuntimeError, "EXACT_DIRECTOR_QUALIFICATION_ACCEPTANCE_REQUIRED"):
            entry.director_gate(director, "f"*64, "9"*64)
        entry.director_gate(director, "f"*64, "8"*64)
        with patch.object(entry, "read_bound_doc", side_effect=FileNotFoundError("inert missing approval")), \
             patch.object(entry, "local_git") as git:
            with self.assertRaises(FileNotFoundError):
                entry.authorize(None, None, p, "official", "9"*64, "f"*64, {"limits": {}})
            git.assert_not_called()

    def test_d204_owner_intent_cannot_admit_d205(self):
        wrong = {"intent": "AUTHORIZE_ONE_D204_SCIENTIFIC_RUN"}
        with patch.object(entry, "read_bound_doc", return_value=(wrong, b"old")), \
             patch.object(entry, "verify_qualification") as qualifier:
            with self.assertRaisesRegex(RuntimeError, "EXACT_FRESH_OWNER_AUTHORIZATION_REQUIRED"):
                entry.authorize(None, None, p, "official", "a"*64, "b"*64, {"limits": {}})
            qualifier.assert_not_called()

    def adapter_inputs(self):
        domain, _ = self.dummy_named_domain()
        menu = {v: dict(prefix_digest=child.PREFIX_DIGEST, unique=v,
                       state={"minimum_labels": {name:i for i,name in enumerate(domain["old_order"][v])}})
                for v in ("B", "C")}
        records = {"main_41":{"original":{"digest":child.TARGETS[0],"graph":{"vertices":domain["vertices_41"]}},
                              "prefixes":[{"digest":child.PREFIX_DIGEST,"graph":{"dummy":"actual-old"}}]},
                   "main_48_if_admitted":{"original":{"digest":child.TARGETS[1]}}}
        limits = {"primary":LIMIT, "audit":LIMIT | {"pair_trials": 28121614404}}
        files = {
            child.PREP+"CONFIG.json": p.encode(dict(menu=["B","C"], prospective_limits=limits)),
            child.PREP+"PREFIXES.json": p.encode(dict(menu={"A":{"never":"dispatch"},**menu})),
            child.PREP+"ORIGINALS.json": p.encode(dict(records=records)),
        }
        return domain, menu, records, limits, files

    def test_actual_adapter_argument_bindings_with_inert_substitutes_only(self):
        domain, menu, records, limits, files = self.adapter_inputs()
        invocations = []
        marker = object()
        def substitute_capture(_bundle, name):
            return files[name] if name in files else b"inert substitute"
        def substitute_load(name, source, path, package=False):
            invocations.append(("load", name, source, path, package))
            def caller(*args):
                invocations.append(("call", name, args))
                return marker
            return SimpleNamespace(primary_search=caller, audit_search=caller, verify_future_positive=caller)
        with patch.object(child, "capture", side_effect=substitute_capture), \
             patch.object(child, "exact_load", side_effect=substitute_load):
            for phase in ("primary","audit"):
                invocations.clear()
                result, verify = child.scientific_adapter(dict(candidate_domain=domain, limits=limits), phase)
                self.assertIs(result, marker)
                before = [r for r in invocations if r[0]=="call"]
                args = (menu, limits[phase]) if phase=="primary" else (menu, {"dummy":"actual-old"}, limits[phase])
                self.assertEqual(before, [("call", child.PACKAGE+"."+phase, args)])
                self.assertEqual(list(before[0][2][0]), ["B","C"])
                self.assertIs(verify({"dummy":"candidate"}), marker)
                self.assertEqual(invocations[-1],
                                 ("call", child.PACKAGE+".verify_positive", ({"dummy":"candidate"}, records, menu)))
                self.assertFalse(any(r[0]=="load" and r[1]==child.PACKAGE+
                                    (".audit" if phase=="primary" else ".primary") for r in invocations))

    def test_adapter_wrong_limits_fails_before_any_load(self):
        domain, _, _, limits, files = self.adapter_inputs()
        drift = limits | {"primary":limits["primary"] | {"pair_trials":1}}
        with patch.object(child, "capture", side_effect=lambda _bundle,n: files[n]), \
             patch.object(child, "exact_load") as loader:
            with self.assertRaisesRegex(RuntimeError, "wrong scientific limits"):
                child.scientific_adapter(dict(candidate_domain=domain, limits=drift), "primary")
            loader.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
