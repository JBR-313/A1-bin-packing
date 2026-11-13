"""Practical 3D: pick the smallest shipping box from a catalog for one order.

Inspired by the idea behind CJ Logistics' LoIS O'Pack (choose the box per order
automatically). This is our own simplified version, NOT a re-implementation of
their system, and the numbers are not directly comparable.

recommend():   boxes from smallest to largest volume; skip a box if the items' total
               volume exceeds it or an item cannot fit in any orientation; otherwise
               run Extreme Point once per sort rule (multi-start, rotation allowed)
               and return the first box where ALL items fit. If no single box works,
               split the order over several copies of the largest box.
               Why multi-start: EP is greedy and never moves an item once placed, so the
               result depends on the order items arrive in. One order can fail in a box
               where another order fits; trying 3 orders is cheap for 3-15 items.
naive_box():   baseline — smallest box whose volume >= total item volume, packed with
               3D Naive (arrival order, no rotation); if it needs more than one box,
               try the next box. Same fallback to the largest box.

Metric: void ratio = 1 - (item volume / total volume of the boxes used).
extra["tries"] counts packing attempts (= the multi-start cost).

trace=True records every attempt in Result.trace (for the search animation):
    {"box": index, "dims": (W, D, H), "rule": sort rule or "naive",
     "outcome": "ok" | "fail" | "skip", "reason": text,
     "placements": placements of this attempt (partial when it failed),
     "order": item ids in placement order, "failed_item": id or None,
     "num_bins": bins used (ok only)}
"""
from __future__ import annotations

from packing.threed import extreme_point as ep
from packing.threed import naive
from packing.threed.geometry import fits_empty, volume
from packing.types import OK, Box, Item3D, Result


def _finish(items, catalog, res: Result, box_idx: int, tries: int, method: str,
            trace: list | None) -> Result:
    item_vol = sum(volume(it) for it in items)
    used = res.num_bins * volume(catalog[box_idx])
    res.extra = {"method": method, "box": box_idx, "num_boxes": res.num_bins,
                 "box_dims": list(catalog[box_idx]), "tries": tries,
                 "item_volume": item_vol, "box_volume": used,
                 "void_ratio": 1 - item_vol / used}
    res.trace = trace
    return res


def _by_volume(catalog: list[Box]) -> list[int]:
    return sorted(range(len(catalog)), key=lambda b: volume(catalog[b]))


def _skip_reason(items, box, total, allow_rotation) -> str | None:
    if total > volume(box):
        return "items' total volume is larger than the box"
    if not all(fits_empty(it, box, allow_rotation) for it in items):
        return "an item is too large for this box"
    return None


def _log(trace, b, box, rule, outcome, reason="", res: Result | None = None, failed=None):
    if trace is None:
        return
    trace.append({"box": b, "dims": tuple(box), "rule": rule, "outcome": outcome,
                  "reason": reason,
                  "placements": list(res.placements) if res and res.placements else [],
                  "order": list(res.order) if res and res.order else [],
                  "failed_item": failed,
                  "num_bins": res.num_bins if res is not None and outcome == "ok" else None})


def recommend(items: list[Item3D], catalog: list[Box],
              rules: tuple[str, ...] = ep.SORT_RULES, trace: bool = False) -> Result:
    total = sum(volume(it) for it in items)
    tries = 0
    log = [] if trace else None
    method = "recommend" if len(rules) > 1 else f"recommend_{rules[0]}"
    order = _by_volume(catalog)
    for b in order:
        box = catalog[b]
        why = _skip_reason(items, box, total, True)
        if why:
            _log(log, b, box, None, "skip", why)
            continue
        for rule in rules:
            tries += 1
            r = ep.pack(items, box, sort=rule, allow_rotation=True, max_bins=1,
                        record_failure=trace)
            if r.status == OK:
                _log(log, b, box, rule, "ok", res=r)
                return _finish(items, catalog, r, b, tries, method, log)
            _log(log, b, box, rule, "fail", "an item did not fit", res=r,
                 failed=r.extra.get("failed_item"))
    # does not fit one box: several largest boxes, best of the sort rules
    big = order[-1]
    best = None
    for rule in rules:
        tries += 1
        r = ep.pack(items, catalog[big], sort=rule, allow_rotation=True)
        if best is None or r.num_bins < best.num_bins:
            best, best_rule = r, rule
    _log(log, big, catalog[big], best_rule, "ok", "split over several boxes", res=best)
    return _finish(items, catalog, best, big, tries, method, log)


def naive_box(items: list[Item3D], catalog: list[Box], trace: bool = False) -> Result:
    total = sum(volume(it) for it in items)
    tries = 0
    log = [] if trace else None
    order = _by_volume(catalog)
    for b in order:
        box = catalog[b]
        why = _skip_reason(items, box, total, False)
        if why:
            _log(log, b, box, None, "skip", why)
            continue
        tries += 1
        r = naive.pack(items, box)
        if r.num_bins == 1:
            _log(log, b, box, "naive", "ok", res=r)
            return _finish(items, catalog, r, b, tries, "naive", log)
        if log is not None:  # the first item that opened bin 2 is where it failed
            failed = r.bins[1][0]
            k = r.order.index(failed)
            part = Result(None, placements=[p for p in r.placements if p.bin_id == 0],
                          order=r.order[:k])
            _log(log, b, box, "naive", "fail", "an item did not fit", res=part, failed=failed)
    tries += 1
    big = order[-1]
    r = naive.pack(items, catalog[big])
    _log(log, big, catalog[big], "naive", "ok", "split over several boxes", res=r)
    return _finish(items, catalog, r, big, tries, "naive", log)
