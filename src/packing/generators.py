"""Random instance generators.

Same (dist, n, seed) -> same items, so every algorithm solves the identical input.
A string seed is used because Python's random.Random(str) is deterministic across runs.
"""
from __future__ import annotations

import random

DISTS_1D = ("uniform", "small", "large")


def size_range_1d(dist: str, C: int) -> tuple[int, int]:
    """Inclusive integer range of item sizes for each distribution."""
    if dist == "uniform":
        return 1, C
    if dist == "small":
        return 1, C // 4
    if dist == "large":
        return -(-C // 3), C  # ceil(C/3) .. C
    raise ValueError(f"unknown 1D distribution: {dist}")


def gen_1d(n: int, C: int, dist: str, seed: int) -> list[int]:
    lo, hi = size_range_1d(dist, C)
    rng = random.Random(f"1d-{dist}-{n}-{seed}")
    return [rng.randint(lo, hi) for _ in range(n)]
