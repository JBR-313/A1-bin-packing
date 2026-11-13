"""Naive exact algorithm: try EVERY order of the items, pack each with First Fit, keep the best.

Why this is optimal:
    Take any optimal packing B1..Bk. List the items of B1, then B2, ..., then Bk.
    Feeding that order to First Fit never needs more than k bins (each item fits in the
    bin it belongs to, or FF puts it even earlier), so the minimum over all n! orders = OPT.

Complexity: O(n! * n^2). There is deliberately NO pruning and NO symmetry removal —
this is the "try all answers" baseline required by the assignment.
"""
from __future__ import annotations

from itertools import permutations
from math import factorial

from packing.types import Result


def _first_fit_count(order: tuple[int, ...], sizes: list[int], C: int) -> int:
    """Number of bins First Fit uses for this order (no bin contents, for speed)."""
    loads: list[int] = []
    for i in order:
        s = sizes[i]
        for b in range(len(loads)):
            if loads[b] + s <= C:
                loads[b] += s
                break
        else:
            loads.append(s)
    return len(loads)


def _first_fit_bins(order: tuple[int, ...], sizes: list[int], C: int) -> list[list[int]]:
    loads: list[int] = []
    bins: list[list[int]] = []
    for i in order:
        s = sizes[i]
        for b in range(len(loads)):
            if loads[b] + s <= C:
                loads[b] += s
                bins[b].append(i)
                break
        else:
            loads.append(s)
            bins.append([i])
    return bins


def solve(sizes: list[int], C: int) -> Result:
    n = len(sizes)
    best_count = n + 1
    best_order: tuple[int, ...] = tuple(range(n))
    for order in permutations(range(n)):  # all n! orders, no early exit
        k = _first_fit_count(order, sizes, C)
        if k < best_count:
            best_count, best_order = k, order
    return Result(_first_fit_bins(best_order, sizes, C), extra={"orders_tried": factorial(n)})
