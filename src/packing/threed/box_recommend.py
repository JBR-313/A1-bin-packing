"""Practical 3D: pick the smallest shipping box from a catalog for one order.

Inspired by the idea behind CJ Logistics' LoIS O'Pack (choose the box per order
automatically). This is our own simplified version, NOT a re-implementation of
their system, and the numbers are not directly comparable.

recommend():   boxes from smallest to largest volume; skip a box if the items' total
               volume exceeds it or an item cannot fit in any orientation; otherwise
               run Extreme Point once per sort rule (multi-start, rotation allowed)
               and return the first box where ALL items fit. If no single box works,
               split the order over several copies of the largest box.
naive_box():   baseline — smallest box whose volume >= total item volume, packed with
               3D Naive (arrival order, no rotation); if it needs more than one box,
               try the next box. Same fallback to the largest box.

Metric: void ratio = 1 - (item volume / total volume of the boxes used).
extra["tries"] counts packing attempts (= the multi-start cost).
"""
from __future__ import annotations

from packing.threed import extreme_point as ep
from packing.threed import naive
from packing.threed.geometry import fits_empty, volume
from packing.types import OK, Box, Item3D, Result


def _finish(items, catalog, res: Result, box_idx: int, tries: int, method: str) -> Result:
    item_vol = sum(volume(it) for it in items)
    used = res.num_bins * volume(catalog[box_idx])
    res.extra = {"method": method, "box": box_idx, "num_boxes": res.num_bins,
                 "box_dims": list(catalog[box_idx]), "tries": tries,
                 "item_volume": item_vol, "box_volume": used,
                 "void_ratio": 1 - item_vol / used}
    return res


def _by_volume(catalog: list[Box]) -> list[int]:
    return sorted(range(len(catalog)), key=lambda b: volume(catalog[b]))


def recommend(items: list[Item3D], catalog: list[Box],
              rules: tuple[str, ...] = ep.SORT_RULES) -> Result:
    total = sum(volume(it) for it in items)
    tries = 0
    order = _by_volume(catalog)
    for b in order:
        box = catalog[b]
        if total > volume(box) or not all(fits_empty(it, box, True) for it in items):
            continue
        for rule in rules:
            tries += 1
            r = ep.pack(items, box, sort=rule, allow_rotation=True, max_bins=1)
            if r.status == OK:
                return _finish(items, catalog, r, b, tries, "recommend")
    # does not fit one box: several largest boxes, best of the sort rules
    big = order[-1]
    best = None
    for rule in rules:
        tries += 1
        r = ep.pack(items, catalog[big], sort=rule, allow_rotation=True)
        if best is None or r.num_bins < best.num_bins:
            best = r
    return _finish(items, catalog, best, big, tries, "recommend")


def naive_box(items: list[Item3D], catalog: list[Box]) -> Result:
    total = sum(volume(it) for it in items)
    tries = 0
    order = _by_volume(catalog)
    for b in order:
        box = catalog[b]
        if total > volume(box) or not all(fits_empty(it, box, False) for it in items):
            continue
        tries += 1
        r = naive.pack(items, box)
        if r.num_bins == 1:
            return _finish(items, catalog, r, b, tries, "naive")
    tries += 1
    big = order[-1]
    return _finish(items, catalog, naive.pack(items, catalog[big]), big, tries, "naive")
