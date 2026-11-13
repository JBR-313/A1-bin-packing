"""Online / offline greedy heuristics (Module 4, Module 6).

Worst-case guarantees (OPT = optimal bin count):
    Next Fit  <= 2 * OPT
    First Fit <= 1.7 * OPT
    Best Fit  <= 1.7 * OPT
    FFD       <= 11/9 * OPT + 6/9   (Dósa 2007, tight)

First Fit uses a segment tree and Best Fit a sorted list, so both run in about
O(n log n) instead of the textbook O(n * bins). The packing they produce is exactly
the same as the simple loop version; only the search for "which bin" is faster.
This matters for experiment B (n = 10,000).
"""
from __future__ import annotations

from bisect import bisect_left, insort

from packing.types import Result


def next_fit(sizes: list[int], C: int) -> Result:
    """Keep one open bin; if the item does not fit, close it and open a new one."""
    bins: list[list[int]] = []
    load = C + 1  # forces a new bin for the first item
    for i, s in enumerate(sizes):
        if load + s > C:
            bins.append([])
            load = 0
        bins[-1].append(i)
        load += s
    return Result(bins)


def first_fit(sizes: list[int], C: int, order: list[int] | None = None) -> Result:
    """Put each item into the lowest-index bin with enough room.

    Segment tree over bin slots 0..n-1 stores the max remaining capacity in each range.
    Unopened slots have remaining = C, so "leftmost slot with remaining >= s" is either
    an open bin (true First Fit) or the next new bin.
    """
    if order is None:
        order = list(range(len(sizes)))
    n = len(order)
    if n == 0:
        return Result([])
    size = 1
    while size < n:
        size *= 2
    tree = [0] * (2 * size)
    for leaf in range(n):
        tree[size + leaf] = C
    for node in range(size - 1, 0, -1):
        tree[node] = max(tree[2 * node], tree[2 * node + 1])

    bins: list[list[int]] = []
    for i in order:
        s = sizes[i]
        node = 1
        while node < size:  # descend, preferring the left child
            node = 2 * node if tree[2 * node] >= s else 2 * node + 1
        b = node - size
        if b == len(bins):
            bins.append([])
        bins[b].append(i)
        tree[node] -= s
        node //= 2
        while node:  # update maxima up to the root
            tree[node] = max(tree[2 * node], tree[2 * node + 1])
            node //= 2
    return Result(bins)


def best_fit(sizes: list[int], C: int) -> Result:
    """Put each item into the bin that leaves the least room (ties: lowest index).

    `rem` is a sorted list of (remaining_capacity, bin_index); bisect finds the
    tightest bin with remaining >= s.
    """
    bins: list[list[int]] = []
    rem: list[tuple[int, int]] = []
    for i, s in enumerate(sizes):
        pos = bisect_left(rem, (s, -1))
        if pos == len(rem):
            bins.append([i])
            insort(rem, (C - s, len(bins) - 1))
        else:
            r, b = rem.pop(pos)
            bins[b].append(i)
            insort(rem, (r - s, b))
    return Result(bins)


def ffd(sizes: list[int], C: int) -> Result:
    """First Fit Decreasing: sort by size (largest first), then First Fit."""
    order = sorted(range(len(sizes)), key=lambda i: -sizes[i])
    return first_fit(sizes, C, order)
