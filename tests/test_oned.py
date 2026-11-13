import pytest

from packing.bounds import lower_bound_1d, validate_1d
from packing.generators import DISTS_1D, gen_1d
from packing.oned import dp, exhaustive, heuristics, mip

C = 100
HEURISTICS = {
    "next_fit": heuristics.next_fit,
    "first_fit": heuristics.first_fit,
    "best_fit": heuristics.best_fit,
    "ffd": heuristics.ffd,
}
EXACT = {"exhaustive": exhaustive.solve, "dp": dp.solve, "mip": mip.solve}


def first_fit_simple(sizes, C):
    """Textbook O(n*k) First Fit, to check the segment-tree version."""
    loads, bins = [], []
    for i, s in enumerate(sizes):
        for b, l in enumerate(loads):
            if l + s <= C:
                loads[b] += s
                bins[b].append(i)
                break
        else:
            loads.append(s)
            bins.append([i])
    return bins


def best_fit_simple(sizes, C):
    loads, bins = [], []
    for i, s in enumerate(sizes):
        cands = [(C - l - s, b) for b, l in enumerate(loads) if l + s <= C]
        if cands:
            _, b = min(cands)
            loads[b] += s
            bins[b].append(i)
        else:
            loads.append(s)
            bins.append([i])
    return bins


def test_hand_example():
    sizes = [60, 50, 40]  # lower bound ceil(150/100) = 2, and 60+40 | 50 achieves it
    for name, f in {**HEURISTICS, **EXACT}.items():
        res = f(sizes, C)
        validate_1d(sizes, C, res.bins)
        assert res.num_bins == 2, name


def test_next_fit_bad_case():
    sizes = [60, 50, 40, 50]  # NF: 60 | 50,40 | 50 = 3 ; OPT: 60+40 | 50+50 = 2
    assert heuristics.next_fit(sizes, C).num_bins == 3
    assert dp.solve(sizes, C).num_bins == 2


def test_empty_input():
    for f in {**HEURISTICS, **EXACT}.values():
        assert f([], C).num_bins == 0


@pytest.mark.parametrize("dist", DISTS_1D)
@pytest.mark.parametrize("n", [1, 50, 500])
def test_heuristics_valid_and_above_lower_bound(dist, n):
    for seed in range(3):
        sizes = gen_1d(n, C, dist, seed)
        lb = lower_bound_1d(sizes, C)
        for name, f in HEURISTICS.items():
            res = f(sizes, C)
            validate_1d(sizes, C, res.bins)
            assert res.num_bins >= lb, name


@pytest.mark.parametrize("dist", DISTS_1D)
def test_fast_ff_bf_match_textbook(dist):
    for seed in range(5):
        sizes = gen_1d(300, C, dist, seed)
        assert heuristics.first_fit(sizes, C).bins == first_fit_simple(sizes, C)
        assert heuristics.best_fit(sizes, C).bins == best_fit_simple(sizes, C)


@pytest.mark.parametrize("dist", DISTS_1D)
def test_exact_methods_agree(dist):
    """Exhaustive = DP = MIP for n <= 8. A mismatch means a bug."""
    for n in range(1, 9):
        for seed in range(2):
            sizes = gen_1d(n, C, dist, seed)
            counts = {}
            for name, f in EXACT.items():
                res = f(sizes, C)
                validate_1d(sizes, C, res.bins)
                assert res.status == "ok", name
                counts[name] = res.num_bins
            assert len(set(counts.values())) == 1, (sizes, counts)
            opt = counts["dp"]
            assert opt >= lower_bound_1d(sizes, C)
            # worst-case guarantees
            assert heuristics.ffd(sizes, C).num_bins <= 11 / 9 * opt + 6 / 9
            assert heuristics.next_fit(sizes, C).num_bins <= 2 * opt
            for name in ("first_fit", "best_fit"):
                assert HEURISTICS[name](sizes, C).num_bins <= 1.7 * opt + 1e-9


@pytest.mark.parametrize("dist", DISTS_1D)
def test_dp_matches_mip_medium(dist):
    for seed in range(2):
        sizes = gen_1d(14, C, dist, seed)
        d = dp.solve(sizes, C)
        validate_1d(sizes, C, d.bins)
        m = mip.solve(sizes, C, time_limit_s=30)
        assert m.status == "ok"
        assert d.num_bins == m.num_bins


def test_mip_skips_huge():
    res = mip.solve([1] * 5, C, max_n=4)
    assert res.status == "skipped" and res.num_bins is None
