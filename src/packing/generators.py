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


# ---------------------------------------------------------------- 3D
DISTS_3D = ("uniform", "flat", "long", "mixed")


def _item_3d(rng: random.Random, shape: str, lo: int, hi: int, wt: tuple[int, int]):
    """One item (w, d, h, weight). lo..hi is the allowed size range per axis.

    uniform: every axis in [lo, hi]
    flat:    two axes in the upper 60% of the range, height in the lower 25%
    long:    one random axis in the upper 45%, the other two in the lower 25%
    """
    span = hi - lo
    big = (lo + int(0.4 * span), hi)
    long_ = (lo + int(0.55 * span), hi)
    small = (lo, lo + int(0.25 * span))
    if shape == "uniform":
        dims = [rng.randint(lo, hi) for _ in range(3)]
    elif shape == "flat":
        dims = [rng.randint(*big), rng.randint(*big), rng.randint(*small)]
    elif shape == "long":
        dims = [rng.randint(*small), rng.randint(*small), rng.randint(*small)]
        dims[rng.randrange(3)] = rng.randint(*long_)
    else:
        raise ValueError(f"unknown 3D shape: {shape}")
    return (dims[0], dims[1], dims[2], rng.randint(*wt))


def gen_3d(n: int, dist: str, seed: int, dim_range=(5, 50), weight_range=(1, 20)):
    """n items for experiment C. "mixed" picks uniform / flat / long per item."""
    rng = random.Random(f"3d-{dist}-{n}-{seed}")
    out = []
    for _ in range(n):
        shape = rng.choice(("uniform", "flat", "long")) if dist == "mixed" else dist
        out.append(_item_3d(rng, shape, *dim_range, weight_range))
    return out


def gen_order(order_id: int, seed: int, k_range=(3, 15), dim_range=(3, 25), weight_range=(1, 20)):
    """One e-commerce order for box recommendation: k items of mixed shapes."""
    rng = random.Random(f"order-{order_id}-{seed}")
    k = rng.randint(*k_range)
    return [_item_3d(rng, rng.choice(("uniform", "flat", "long")), *dim_range, weight_range)
            for _ in range(k)]
