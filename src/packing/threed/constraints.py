"""Loading constraints (optional, switchable).

support (ratio, default 0.7):
    An item not on the floor must have at least `ratio` of its bottom area resting on
    top faces of other items at exactly the same height z. The 70% value is OUR
    assumption (no single standard); experiment C should be read with that in mind.

heavy-below:
    An item may only rest directly on items whose weight is >= its own weight.
    Only direct contact is checked (items whose top face is at the item's z and whose
    footprint overlaps it), not everything further below.
"""
from __future__ import annotations

from packing.threed.geometry import overlap_xy
from packing.types import Item3D, Placement


def contacts_below(cand: Placement, placed: list[Placement]) -> list[tuple[Placement, int]]:
    """Items whose top face touches cand's bottom face, with the shared area."""
    out = []
    for q in placed:
        if q.z + q.h == cand.z:
            a = overlap_xy(cand, q)
            if a > 0:
                out.append((q, a))
    return out


def contacts_above(cand: Placement, placed: list[Placement]) -> list[tuple[Placement, int]]:
    """Items resting on cand's top face. Needed because an item can be slid UNDER an
    overhanging item that was placed earlier (support only needs 70%)."""
    out = []
    for q in placed:
        if q.z == cand.z + cand.h:
            a = overlap_xy(cand, q)
            if a > 0:
                out.append((q, a))
    return out


def support_ok(cand: Placement, contacts: list[tuple[Placement, int]], ratio: float) -> bool:
    if cand.z == 0:
        return True
    return sum(a for _, a in contacts) >= ratio * cand.w * cand.d


def weight_ok(weight: int, contacts: list[tuple[Placement, int]], weights) -> bool:
    """Every item below must be at least as heavy as `weight`."""
    return all(weights[q.item_id] >= weight for q, _ in contacts)


def weight_ok_above(weight: int, above: list[tuple[Placement, int]], weights) -> bool:
    """Every item resting on top must be at most as heavy as `weight`."""
    return all(weights[q.item_id] <= weight for q, _ in above)


def support_violations(placements: list[Placement], ratio: float = 0.7) -> list[Placement]:
    by_bin = _by_bin(placements)
    return [p for p in placements
            if not support_ok(p, contacts_below(p, by_bin[p.bin_id]), ratio)]


def weight_violations(items: list[Item3D], placements: list[Placement]) -> list[Placement]:
    by_bin = _by_bin(placements)
    weights = [it[3] for it in items]
    return [p for p in placements
            if not weight_ok(weights[p.item_id], contacts_below(p, by_bin[p.bin_id]), weights)]


def _by_bin(placements):
    out: dict[int, list[Placement]] = {}
    for p in placements:
        out.setdefault(p.bin_id, []).append(p)
    return out
