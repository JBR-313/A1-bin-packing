"""3D geometry helpers: orientations, overlap tests, lower bound, validation.

Boxes are axis-aligned with integer coordinates. A box occupies the half-open region
[x, x+w) × [y, y+d) × [z, z+h), so two boxes that only touch faces do NOT overlap.
"""
from __future__ import annotations

from itertools import permutations

from packing.types import Box, Item3D, Placement


def volume(dims) -> int:
    return dims[0] * dims[1] * dims[2]


def orientations(w: int, d: int, h: int, allow_rotation: bool) -> list[tuple[int, int, int]]:
    """Distinct (w, d, h) orientations. Without rotation only the given one.
    With rotation: up to 6, ordered lowest height first (flat placements first)."""
    if not allow_rotation:
        return [(w, d, h)]
    return sorted(set(permutations((w, d, h))), key=lambda o: (o[2], o[1], o[0]))


def fits_empty(item: Item3D, box: Box, allow_rotation: bool) -> bool:
    """Can the item fit into an empty container in some allowed orientation?"""
    return any(w <= box[0] and d <= box[1] and h <= box[2]
               for w, d, h in orientations(*item[:3], allow_rotation))


def overlaps(a: Placement, b: Placement) -> bool:
    return (a.x < b.x + b.w and b.x < a.x + a.w and
            a.y < b.y + b.d and b.y < a.y + a.d and
            a.z < b.z + b.h and b.z < a.z + a.h)


def overlap_xy(a: Placement, b: Placement) -> int:
    """Area of the overlap of the two footprints (x-y rectangles)."""
    dx = min(a.x + a.w, b.x + b.w) - max(a.x, b.x)
    dy = min(a.y + a.d, b.y + b.d) - max(a.y, b.y)
    return dx * dy if dx > 0 and dy > 0 else 0


def lower_bound_3d(items: list[Item3D], box: Box) -> int:
    """L = ceil(sum of item volumes / container volume)."""
    return -(-sum(volume(it) for it in items) // volume(box))


def validate_3d(items: list[Item3D], box: Box, placements: list[Placement],
                allow_rotation: bool = True) -> None:
    """Raise AssertionError unless: every item placed exactly once, in an allowed
    orientation, inside the container, with no two items overlapping in a bin."""
    ids = sorted(p.item_id for p in placements)
    assert ids == list(range(len(items))), "each item must be placed exactly once"
    by_bin: dict[int, list[Placement]] = {}
    W, D, H = box
    for p in placements:
        w, d, h = items[p.item_id][:3]
        if allow_rotation:
            assert sorted((p.w, p.d, p.h)) == sorted((w, d, h)), f"wrong size: {p}"
        else:
            assert (p.w, p.d, p.h) == (w, d, h), f"rotated without permission: {p}"
        assert 0 <= p.x and p.x + p.w <= W, f"outside container (x): {p}"
        assert 0 <= p.y and p.y + p.d <= D, f"outside container (y): {p}"
        assert 0 <= p.z and p.z + p.h <= H, f"outside container (z): {p}"
        by_bin.setdefault(p.bin_id, []).append(p)
    for ps in by_bin.values():
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                assert not overlaps(ps[i], ps[j]), f"overlap: {ps[i]} {ps[j]}"
