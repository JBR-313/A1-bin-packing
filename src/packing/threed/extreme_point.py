"""3D Better: Extreme Point heuristic (after Crainic, Perboli & Tadei 2008).

1. Sort items by a rule (volume / height / bottom area, all largest first).
2. Every open bin keeps a list of candidate points ("extreme points"); a new bin
   starts with (0, 0, 0).
3. For each item, try the open bins in order (First Fit over bins). Inside a bin take
   the candidate point with the smallest (z, y, x) where some allowed orientation fits
   (inside the bin, no overlap, loading constraints if switched on). Orientations are
   tried lowest-height first. If no open bin works, open a new bin.
4. After placing an item at (x, y, z) with size (w, d, h), add the three corner points
   (x+w, y, z), (x, y+d, z), (x, y, z+h), and each of them projected along -x, -y and
   -z until it hits a wall or another item. Points outside the bin or inside an item
   are dropped.

Simplifications compared with the paper (also listed in README):
    - projections are straight-line along one axis from the three corner points
      (the paper projects each corner along the two OTHER axes only);
    - bins are tried in order (First Fit), not chosen by a merit function;
    - no "residual space" bookkeeping; occupancy is checked against all items in the bin.
"""
from __future__ import annotations

from bisect import insort

from packing.threed import constraints as cons
from packing.threed.geometry import fits_empty, orientations, overlaps, volume
from packing.types import INFEASIBLE, Box, Item3D, Placement, Result

SORT_RULES = ("volume", "height", "area")


def sort_order(items: list[Item3D], rule: str) -> list[int]:
    keys = {
        "volume": lambda i: (-volume(items[i]), -items[i][2]),
        "height": lambda i: (-items[i][2], -volume(items[i])),
        "area": lambda i: (-items[i][0] * items[i][1], -items[i][2]),
        "arrival": lambda i: 0,
    }
    if rule not in keys:
        raise ValueError(f"unknown sort rule {rule}")
    return sorted(range(len(items)), key=keys[rule])  # stable: ties keep arrival order


class _Bin:
    def __init__(self, bin_id: int, box: Box):
        self.id = bin_id
        self.box = box
        self.placed: list[Placement] = []
        self.points: list[tuple[int, int, int]] = [(0, 0, 0)]  # stored as (z, y, x), sorted
        self.free = volume(box)

    def occupied(self, x: int, y: int, z: int) -> bool:
        return any(q.x <= x < q.x + q.w and q.y <= y < q.y + q.d and q.z <= z < q.z + q.h
                   for q in self.placed)

    def find(self, item_id: int, item: Item3D, allow_rotation: bool,
             support_ratio: float | None, heavy_below: bool, weights) -> Placement | None:
        W, D, H = self.box
        ors = orientations(*item[:3], allow_rotation)
        for z, y, x in self.points:
            for w, d, h in ors:
                if x + w > W or y + d > D or z + h > H:
                    continue
                cand = Placement(item_id, self.id, x, y, z, w, d, h)
                if any(overlaps(cand, q) for q in self.placed):
                    continue
                if support_ratio is not None or heavy_below:
                    below = cons.contacts_below(cand, self.placed) if z > 0 else []
                    if support_ratio is not None and not cons.support_ok(cand, below, support_ratio):
                        continue
                    if heavy_below and not (
                            cons.weight_ok(item[3], below, weights) and
                            cons.weight_ok_above(item[3], cons.contacts_above(cand, self.placed),
                                                 weights)):
                        continue
                return cand
        return None

    def _project(self, x: int, y: int, z: int, axis: int) -> tuple[int, int, int]:
        """Slide the point toward 0 along `axis` until it hits a wall or an item face."""
        p = [x, y, z]
        stop = 0
        for q in self.placed:
            lo = (q.x, q.y, q.z)
            size = (q.w, q.d, q.h)
            # q blocks the slide if the point's other two coordinates lie in q's face
            if all(lo[k] <= p[k] < lo[k] + size[k] for k in range(3) if k != axis):
                top = lo[axis] + size[axis]
                if top <= p[axis]:
                    stop = max(stop, top)
        p[axis] = stop
        return tuple(p)

    def place(self, cand: Placement) -> None:
        self.placed.append(cand)
        self.free -= cand.w * cand.d * cand.h
        x, y, z = cand.x, cand.y, cand.z
        corners = [(x + cand.w, y, z), (x, y + cand.d, z), (x, y, z + cand.h)]
        new = set()
        for c in corners:
            new.add(c)
            for axis in range(3):
                new.add(self._project(*c, axis))
        W, D, H = self.box
        keep = [p for p in self.points if not self.occupied(p[2], p[1], p[0])]
        existing = set(keep)
        for px, py, pz in new:
            if px < W and py < D and pz < H and (pz, py, px) not in existing \
                    and not self.occupied(px, py, pz):
                insort(keep, (pz, py, px))
                existing.add((pz, py, px))
        self.points = keep


def pack(items: list[Item3D], box: Box, sort: str = "volume", allow_rotation: bool = True,
         support_ratio: float | None = None, heavy_below: bool = False,
         max_bins: int | None = None) -> Result:
    """Pack all items. With max_bins set, return status "infeasible" if more are needed."""
    for i, it in enumerate(items):
        if not fits_empty(it, box, allow_rotation):
            raise ValueError(f"item {i} {it[:3]} does not fit container {box}")
    weights = [it[3] for it in items]
    bins: list[_Bin] = []
    for i in sort_order(items, sort):
        vol = volume(items[i])
        for b in bins:
            if b.free < vol:
                continue
            cand = b.find(i, items[i], allow_rotation, support_ratio, heavy_below, weights)
            if cand:
                b.place(cand)
                break
        else:
            if max_bins is not None and len(bins) >= max_bins:
                return Result(None, INFEASIBLE)
            b = _Bin(len(bins), box)
            bins.append(b)
            # the floor point (0,0,0) always works in an empty bin (z = 0: no constraints)
            b.place(b.find(i, items[i], allow_rotation, support_ratio, heavy_below, weights))
    placements = sorted((p for b in bins for p in b.placed), key=lambda p: p.item_id)
    return Result([[p.item_id for p in b.placed] for b in bins], placements=placements,
                  extra={"sort": sort, "rotation": allow_rotation,
                         "support_ratio": support_ratio, "heavy_below": heavy_below})
