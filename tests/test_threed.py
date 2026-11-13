import pytest

from packing.generators import DISTS_3D, gen_3d
from packing.threed import naive
from packing.threed.geometry import (lower_bound_3d, orientations, overlap_xy, overlaps,
                                     validate_3d)
from packing.types import Placement

BOX = (100, 100, 100)


def P(x, y, z, w, d, h, i=0, b=0):
    return Placement(i, b, x, y, z, w, d, h)


# ---------------------------------------------------------------- geometry
def test_touching_faces_do_not_overlap():
    assert not overlaps(P(0, 0, 0, 10, 10, 10), P(10, 0, 0, 10, 10, 10))
    assert not overlaps(P(0, 0, 0, 10, 10, 10), P(0, 0, 10, 10, 10, 10))
    assert overlaps(P(0, 0, 0, 10, 10, 10), P(9, 9, 9, 10, 10, 10))


def test_overlap_xy_area():
    assert overlap_xy(P(0, 0, 0, 10, 10, 1), P(5, 5, 7, 10, 10, 1)) == 25
    assert overlap_xy(P(0, 0, 0, 10, 10, 1), P(10, 0, 0, 10, 10, 1)) == 0


def test_orientations():
    assert orientations(1, 2, 3, False) == [(1, 2, 3)]
    assert len(orientations(1, 2, 3, True)) == 6
    assert len(orientations(2, 2, 3, True)) == 3
    assert orientations(5, 5, 5, True) == [(5, 5, 5)]


def test_lower_bound_3d():
    assert lower_bound_3d([(50, 50, 50, 1)] * 8, BOX) == 1
    assert lower_bound_3d([(50, 50, 50, 1)] * 9, BOX) == 2


def test_validate_catches_errors():
    items = [(10, 10, 10, 1), (10, 10, 10, 1)]
    with pytest.raises(AssertionError):  # overlap
        validate_3d(items, BOX, [P(0, 0, 0, 10, 10, 10, 0), P(5, 0, 0, 10, 10, 10, 1)])
    with pytest.raises(AssertionError):  # outside
        validate_3d(items, BOX, [P(0, 0, 0, 10, 10, 10, 0), P(95, 0, 0, 10, 10, 10, 1)])
    with pytest.raises(AssertionError):  # missing item
        validate_3d(items, BOX, [P(0, 0, 0, 10, 10, 10, 0)])
    validate_3d(items, BOX, [P(0, 0, 0, 10, 10, 10, 0), P(10, 0, 0, 10, 10, 10, 1)])


# ---------------------------------------------------------------- naive
def test_naive_hand_example():
    box = (10, 10, 10)
    # four 5x5x10 columns fill the box exactly; the fifth needs a new bin
    r = naive.pack([(5, 5, 10, 1)] * 5, box)
    validate_3d([(5, 5, 10, 1)] * 5, box, r.placements, allow_rotation=False)
    assert r.num_bins == 2
    assert [(p.x, p.y, p.z) for p in r.placements[:4]] == [(0, 0, 0), (5, 0, 0), (0, 5, 0), (5, 5, 0)]


def test_naive_layers():
    box = (10, 10, 10)
    items = [(10, 10, 3, 1), (10, 10, 3, 1), (10, 10, 4, 1), (10, 10, 1, 1)]
    r = naive.pack(items, box)
    assert r.num_bins == 2
    assert [p.z for p in r.placements] == [0, 3, 6, 0]


def test_naive_rejects_too_big():
    with pytest.raises(ValueError):
        naive.pack([(10, 20, 5, 1)], (20, 10, 5))


@pytest.mark.parametrize("dist", DISTS_3D)
def test_naive_valid_random(dist):
    for seed in range(3):
        items = gen_3d(80, dist, seed)
        r = naive.pack(items, BOX)
        validate_3d(items, BOX, r.placements, allow_rotation=False)
        assert r.num_bins >= lower_bound_3d(items, BOX)


# ---------------------------------------------------------------- extreme point
from packing.threed import extreme_point as ep  # noqa: E402
from packing.threed.constraints import support_violations, weight_violations  # noqa: E402


def test_ep_eight_cubes_fill_one_bin():
    box = (10, 10, 10)
    items = [(5, 5, 5, 1)] * 8
    r = ep.pack(items, box)
    validate_3d(items, box, r.placements)
    assert r.num_bins == 1
    assert ep.pack(items + [(5, 5, 5, 1)], box).num_bins == 2


def test_ep_lowest_point_first():
    box = (10, 10, 10)
    items = [(10, 5, 5, 1), (10, 5, 5, 1)]  # second goes next to the first, not on top
    r = ep.pack(items, box, allow_rotation=False)
    assert (r.placements[1].x, r.placements[1].y, r.placements[1].z) == (0, 5, 0)


def test_ep_rotation():
    box = (10, 5, 5)
    item = [(5, 10, 5, 1)]
    with pytest.raises(ValueError):
        ep.pack(item, box, allow_rotation=False)
    r = ep.pack(item, box, allow_rotation=True)
    validate_3d(item, box, r.placements)
    assert (r.placements[0].w, r.placements[0].d) == (10, 5)


def test_ep_beats_naive_where_naive_wastes_space():
    box = (10, 10, 10)
    items = [(6, 10, 5, 1), (6, 10, 5, 1), (4, 10, 5, 1), (4, 10, 5, 1)]
    # Naive (arrival order): 6 at z=0; next 6 does not fit beside it -> layer z=5;
    # 4 goes beside it at z=5; last 4 needs layer z=10 -> new bin. Total 2.
    # Exact fit exists: (6 + 4) side by side on each of two layers -> 1 bin.
    assert naive.pack(items, box).num_bins == 2
    r = ep.pack(items, box, allow_rotation=False)
    validate_3d(items, box, r.placements, allow_rotation=False)
    assert r.num_bins == 1


def test_ep_max_bins_infeasible():
    r = ep.pack([(10, 10, 10, 1)] * 2, (10, 10, 10), max_bins=1)
    assert r.status == "infeasible" and r.num_bins is None


@pytest.mark.parametrize("dist", DISTS_3D)
@pytest.mark.parametrize("rule", ep.SORT_RULES)
def test_ep_valid_random(dist, rule):
    for seed in range(2):
        items = gen_3d(80, dist, seed)
        for rot in (True, False):
            r = ep.pack(items, BOX, sort=rule, allow_rotation=rot)
            validate_3d(items, BOX, r.placements, allow_rotation=rot)
            assert r.num_bins >= lower_bound_3d(items, BOX)


# ---------------------------------------------------------------- loading constraints
def test_support_rejects_small_base():
    box = (10, 10, 10)
    items = [(2, 10, 6, 1), (10, 10, 2, 1)]  # flat slab can only go on top of the post
    free = ep.pack(items, box, sort="arrival", allow_rotation=False)
    assert free.num_bins == 1 and len(support_violations(free.placements)) == 1
    sup = ep.pack(items, box, sort="arrival", allow_rotation=False, support_ratio=0.7)
    assert sup.num_bins == 2 and support_violations(sup.placements) == []


def test_heavy_below():
    box = (10, 10, 10)
    items = [(10, 10, 2, 1), (2, 2, 2, 10)]  # heavy cube would sit on a light slab
    assert ep.pack(items, box, allow_rotation=False).num_bins == 1
    r = ep.pack(items, box, allow_rotation=False, support_ratio=0.7, heavy_below=True)
    assert r.num_bins == 2 and weight_violations(items, r.placements) == []


@pytest.mark.parametrize("dist", DISTS_3D)
def test_constraints_never_violated(dist):
    for seed in range(3):
        items = gen_3d(150, dist, seed)
        r = ep.pack(items, BOX, support_ratio=0.7)
        validate_3d(items, BOX, r.placements)
        assert support_violations(r.placements, 0.7) == []
        r = ep.pack(items, BOX, support_ratio=0.7, heavy_below=True)
        validate_3d(items, BOX, r.placements)
        assert support_violations(r.placements, 0.7) == []
        assert weight_violations(items, r.placements) == []
