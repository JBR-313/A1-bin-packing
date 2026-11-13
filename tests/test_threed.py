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
