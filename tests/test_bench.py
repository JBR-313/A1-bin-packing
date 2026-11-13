from packing.bench.timeout import _debug_sleep, run_with_timeout
from packing.oned import heuristics


def test_isolated_run_returns_result():
    res = run_with_timeout(heuristics.ffd, ([60, 50, 40], 100), timeout_s=10)
    assert res.status == "ok" and res.num_bins == 2
    assert 0 <= res.runtime_s < 1


def test_isolated_run_times_out():
    res = run_with_timeout(_debug_sleep, (30,), timeout_s=1)
    assert res.status == "timeout" and res.num_bins is None


def test_in_process_post_hoc_timeout():
    res = run_with_timeout(_debug_sleep, (0.3,), timeout_s=0.1, isolate=False)
    assert res.status == "timeout"
