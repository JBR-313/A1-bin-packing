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


# ---------------------------------------------------------------- viewer
def test_viewer_writes_html(tmp_path):
    from packing.viz.view3d import write_comparison
    items = gen_3d(30, "mixed", 0)
    panels = [("Naive", items, BOX, naive.pack(items, BOX)), ("EP", items, BOX, ep.pack(items, BOX))]
    out = write_comparison(tmp_path / "v.html", panels, "test")
    text = out.read_text()
    assert "Mesh3d" in text or "mesh3d" in text
    assert text.count("scene") >= 2


# ---------------------------------------------------------------- box recommendation
from packing.generators import gen_order  # noqa: E402
from packing.threed import box_recommend as br  # noqa: E402

CATALOG = [(20, 15, 10), (30, 20, 15), (35, 25, 20), (40, 30, 25), (50, 40, 30), (60, 45, 40)]


def test_box_two_cubes_smallest_box():
    items = [(10, 10, 10, 1), (10, 10, 10, 1)]  # 20x10x10 fits in 20x15x10
    for f in (br.recommend, br.naive_box):
        r = f(items, CATALOG)
        validate_3d(items, CATALOG[0], r.placements)
        assert r.extra["box"] == 0 and r.extra["num_boxes"] == 1
        assert abs(r.extra["void_ratio"] - (1 - 2000 / 3000)) < 1e-9


def test_box_rotation_saves_a_size():
    items = [(15, 20, 10, 1)]  # needs a 90-degree turn to fit 20x15x10
    assert br.recommend(items, CATALOG).extra["box"] == 0
    assert br.naive_box(items, CATALOG).extra["box"] == 1


def test_box_split_when_too_big():
    items = [(25, 25, 25, 1)] * 12  # 187,500 > largest box 108,000
    r = br.recommend(items, CATALOG)
    assert r.extra["box"] == 5 and r.extra["num_boxes"] >= 2
    validate_3d(items, CATALOG[5], r.placements)


def test_box_random_orders_valid():
    for oid in range(40):
        items = gen_order(oid, 0)
        rec, nav = br.recommend(items, CATALOG), br.naive_box(items, CATALOG)
        validate_3d(items, CATALOG[rec.extra["box"]], rec.placements)
        validate_3d(items, CATALOG[nav.extra["box"]], nav.placements, allow_rotation=False)
        # Not a theorem (EP is a heuristic too), but holds on these 40 fixed orders;
        # if it ever fails, look at the order before trusting experiment C numbers.
        assert rec.extra["box_volume"] <= nav.extra["box_volume"]


def test_viewer_grid_layout_and_all_bins(tmp_path):
    from packing.viz.view3d import PER_ROW, bin_offset, world_boxes, write_comparison
    assert bin_offset(0, BOX) == (0, 0)
    assert bin_offset(PER_ROW, BOX)[0] == 0 and bin_offset(PER_ROW, BOX)[1] > BOX[1]
    items = gen_3d(120, "mixed", 0)
    r = naive.pack(items, BOX)
    assert r.num_bins > PER_ROW  # needs a second row
    assert len(world_boxes(items, BOX, r.placements, r.num_bins)) == len(items)
    write_comparison(tmp_path / "all.html", [("Naive", items, BOX, r)], "all bins")


# ---------------------------------------------------------------- heaviest-first sort
def test_weight_sort_order():
    items = [(10, 10, 10, 3), (20, 20, 20, 7), (5, 5, 5, 7), (30, 30, 30, 1)]
    # weight 7 first (bigger volume breaks the tie), then 3, then 1
    assert ep.sort_order(items, "weight") == [1, 2, 0, 3]
    assert "weight" not in ep.SORT_RULES  # box recommendation must stay unchanged


def test_weight_first_hand_example():
    # Light but bulky slab (10x10x4, weight 1) and heavy thin slab (10x10x2, weight 9).
    # Volume order: bulky light slab takes the floor; the heavy slab may not rest on a
    # lighter item -> 2 bins. Heaviest-first: heavy slab on the floor, light one on top
    # -> 1 bin. Both runs obey support and heavy-below.
    box = (10, 10, 10)
    items = [(10, 10, 4, 1), (10, 10, 2, 9)]
    kw = dict(allow_rotation=False, support_ratio=0.7, heavy_below=True)
    vol = ep.pack(items, box, sort="volume", **kw)
    wt = ep.pack(items, box, sort="weight", **kw)
    assert vol.num_bins == 2 and wt.num_bins == 1
    for r in (vol, wt):
        validate_3d(items, box, r.placements, allow_rotation=False)
        assert weight_violations(items, r.placements) == []


@pytest.mark.parametrize("dist", DISTS_3D)
def test_weight_first_valid_random(dist):
    for seed in range(3):
        items = gen_3d(150, dist, seed)
        r = ep.pack(items, BOX, sort="weight", support_ratio=0.7, heavy_below=True)
        validate_3d(items, BOX, r.placements)
        assert support_violations(r.placements, 0.7) == []
        assert weight_violations(items, r.placements) == []


# ---------------------------------------------------------------- animation
def _replay(fig, upto=None):
    """Apply frames in order like the browser does; return the trace data afterwards."""
    state = {i: tr for i, tr in enumerate(fig.data)}
    for fr in fig.frames[:upto]:
        for idx, tr in zip(fr.traces, fr.data):
            state[idx] = tr
    return state


def _boxes_from_mesh(mesh):
    xs, ys, zs = list(mesh.x), list(mesh.y), list(mesh.z)
    out = set()
    for b in range(0, len(xs), 8):  # 8 corners per box, corner 0 = min, corner 6 = max
        out.add((xs[b], ys[b], zs[b], xs[b + 6] - xs[b], ys[b + 6] - ys[b], zs[b + 6] - zs[b]))
    return out


def test_animation_last_frame_matches_packing(tmp_path):
    from packing.viz.animate3d import (TRACES_PER_PANEL, build_animation, frame_boxes,
                                       landing_boxes, write_animation)
    items = gen_3d(25, "mixed", 0)
    nv, e = naive.pack(items, BOX), ep.pack(items, BOX)
    panels = [("Naive", items, BOX, nv), ("EP", items, BOX, e)]
    fig = build_animation(panels, "t", drop_steps=3)
    assert len(fig.frames) == 3 * len(items)
    state = _replay(fig)
    for p, (_, _, _, res) in enumerate(panels):
        want = {b[:6] for b in landing_boxes(items, BOX, res)}
        placed = state[p * TRACES_PER_PANEL + 1]
        assert _boxes_from_mesh(placed) == want          # every item in its final spot
        assert len(state[p * TRACES_PER_PANEL + 3].x) == 0  # nothing still falling
        assert {b[:6] for b in frame_boxes(items, BOX, res)[-1]} == want
    out = write_animation(tmp_path / "a.html", panels, "t")
    assert out.stat().st_size < 10e6


def test_animation_slider_steps_are_complete_states():
    from packing.viz.animate3d import TRACES_PER_PANEL, build_animation
    items = gen_3d(10, "uniform", 1)
    fig = build_animation([("EP", items, BOX, ep.pack(items, BOX))], "t", drop_steps=3)
    steps = fig.layout.sliders[0].steps
    assert len(steps) == len(items)
    names = {f.name: f for f in fig.frames}
    for k, st in enumerate(steps):
        fr = names[st.args[0][0]]
        assert 1 in fr.traces  # landing frame carries the full placed set
        assert len(fr.data[list(fr.traces).index(1)].x) == 8 * (k + 1)
        assert TRACES_PER_PANEL == 4
