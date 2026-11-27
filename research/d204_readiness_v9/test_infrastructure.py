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
                        "a"*32, "d204-readiness-v9", "primary", "0", "0"]
            with self.assertRaises(SystemExit) as error:
                child.main()
            self.assertEqual(error.exception.code, 65)
        finally:
            sys.argv = old

    def test_supplied_signaled_grant_cannot_launch_direct_science(self):
        args = [child.__file__, child.TASK, "0"*64, "official", "primary", "science",
                "a"*32, "d204-science-v9", "primary", "17", "18"]
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
                     disposition="D204_EXECUTION_READY_AWAITING_OWNER_AUTHORIZATION")
        with self.assertRaisesRegex(RuntimeError, "QUALIFICATION_RECEIPT_BINDING"):
            entry.qualification_gate(p, ready, ready["freeze"], {}, b"{}", b"{}", b"{}", {})
        ready.update({kind:p.binding(b"{}") for kind in ("terminal", "seal", "outer")})
        with self.assertRaisesRegex(RuntimeError, "QUALIFICATION_NATIVE_TERMINAL"):
            entry.qualification_gate(p, ready, ready["freeze"], {}, b"{}", b"{}", b"{}", {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
