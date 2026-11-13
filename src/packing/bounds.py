"""Lower bounds on the number of bins."""
from __future__ import annotations


def lower_bound_1d(sizes: list[int], C: int) -> int:
    """L = ceil(sum(sizes) / C): no packing can use fewer bins than total volume allows."""
    return -(-sum(sizes) // C)


def validate_1d(sizes: list[int], C: int, bins: list[list[int]]) -> None:
    """Raise AssertionError unless every item appears exactly once and no bin overflows."""
    seen = sorted(i for b in bins for i in b)
    assert seen == list(range(len(sizes))), "each item must be packed exactly once"
    for b in bins:
        assert b, "empty bin"
        assert sum(sizes[i] for i in b) <= C, f"bin overflow: {b}"
