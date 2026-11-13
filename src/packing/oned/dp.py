"""Better exact algorithm: bitmask DP over subsets (Module 3 style).

State: for each subset S of items, best (bins_used, fill_of_last_bin), minimized
lexicographically. Items are added one at a time; an item goes into the last (open)
bin if it fits, otherwise opens a new bin.

Why comparing (bins, fill) lexicographically is safe:
    For the same packed set S, using fewer bins is never worse. With the same number of
    bins, a less-filled last bin can accept everything a fuller one can, so it is never
    worse either. Closed bins never matter again.

Complexity: O(2^n * n) time, O(2^n) memory.
"""
from __future__ import annotations

from packing.types import Result


def solve(sizes: list[int], C: int) -> Result:
    n = len(sizes)
    if n == 0:
        return Result([])
    full = (1 << n) - 1
    INF = n + 2
    nbins = [INF] * (full + 1)  # bins used for subset S
    fill = [0] * (full + 1)     # fill of the last bin for subset S
    parent = [-1] * (full + 1)  # item added last to reach S (for reconstruction)
    nbins[0] = 1                # start with one empty open bin

    # Increasing S works: every transition goes S -> S | bit, a larger number.
    for S in range(full + 1):
        k, f = nbins[S], fill[S]
        for i in range(n):
            bit = 1 << i
            if S & bit:
                continue
            s = sizes[i]
            if f + s <= C:
                k2, f2 = k, f + s
            else:
                k2, f2 = k + 1, s
            T = S | bit
            if k2 < nbins[T] or (k2 == nbins[T] and f2 < fill[T]):
                nbins[T], fill[T], parent[T] = k2, f2, i

    # Walk parents back to get the insertion order, then replay it.
    order = []
    S = full
    while S:
        i = parent[S]
        order.append(i)
        S ^= 1 << i
    order.reverse()

    bins: list[list[int]] = [[]]
    load = 0
    for i in order:
        if load + sizes[i] <= C:
            bins[-1].append(i)
            load += sizes[i]
        else:
            bins.append([i])
            load = sizes[i]
    assert len(bins) == nbins[full]
    return Result(bins, extra={"states": full + 1})
