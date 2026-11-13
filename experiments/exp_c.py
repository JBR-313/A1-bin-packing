"""Experiment C — 3D packing and loading, plus box recommendation for orders.

    python -m experiments.exp_c --quick
    python -m experiments.exp_c

Part 1: n items into identical 100x100x100 containers.
        3D Naive vs Extreme Point (3 sort rules) vs EP + support vs EP + support + weight.
Part 2: 200 orders (3-15 items) -> pick a box from the 6-box catalog.
        Box recommendation (multi-start EP) vs naive box choice.
Outputs: results/csv/exp_c_<mode>.csv, figures, and 3D HTML viewers.
"""
from __future__ import annotations

import json
import time

import pandas as pd

from experiments import config as cfg
from experiments.common import CSV_DIR, FIG_DIR, ROOT, parse_mode
from packing.bench.runner import COLUMNS, AlgoSpec, Problem, sweep
from packing.generators import gen_3d, gen_order
from packing.threed import box_recommend, extreme_point, naive
from packing.threed.constraints import support_violations, weight_violations
from packing.threed.geometry import lower_bound_3d, validate_3d, volume
from packing.viz import plots
from packing.viz.animate3d import write_animation
from packing.viz.view3d import write_comparison

BOX = cfg.C3_CONTAINER
HTML_DIR = ROOT / "results" / "html"


def make_instance(n: int, dist: str, seed: int):
    return gen_3d(n, dist, seed, cfg.C3_DIM_RANGE, cfg.C3_WEIGHT_RANGE)


def validate(items, res, spec: AlgoSpec) -> None:
    kw = spec.kwargs
    validate_3d(items, BOX, res.placements, allow_rotation=kw.get("allow_rotation", True))
    if kw.get("support_ratio") is not None:
        assert not support_violations(res.placements, kw["support_ratio"]), "support violated"
    if kw.get("heavy_below"):
        assert not weight_violations(items, res.placements), "heavy-below violated"


PROBLEM_3D = Problem(
    gen=make_instance,
    args=lambda items: (items, BOX),
    validate=validate,
    lower_bound=lambda items: lower_bound_3d(items, BOX),
    fill_rate=lambda items, k: sum(volume(it) for it in items) / (k * volume(BOX)),
)


def algorithms(ns: list[int]) -> dict[str, AlgoSpec]:
    """All run in-process (polynomial; a run longer than the limit is marked timeout)."""
    sup = cfg.C3_SUPPORT_RATIO
    algos = {"naive": AlgoSpec(naive.pack, ns, isolate=False)}
    # same EP without rotation: separates "better algorithm" from "allowed to rotate"
    algos["ep_volume_norot"] = AlgoSpec(extreme_point.pack, ns, isolate=False,
                                        kwargs={"sort": "volume", "allow_rotation": False})
    for rule in extreme_point.SORT_RULES:
        algos[f"ep_{rule}"] = AlgoSpec(extreme_point.pack, ns, isolate=False,
                                       kwargs={"sort": rule, "allow_rotation": True})
    # sensitivity of the (assumed) support threshold
    for r in cfg.C3_SUPPORT_SENSITIVITY:
        algos[f"ep_support_{round(r * 100)}"] = AlgoSpec(
            extreme_point.pack, ns, isolate=False,
            kwargs={"sort": "volume", "allow_rotation": True, "support_ratio": r})
    algos["ep_support"] = AlgoSpec(extreme_point.pack, ns, isolate=False,
                                   kwargs={"sort": "volume", "allow_rotation": True,
                                           "support_ratio": sup})
    algos["ep_support_weight"] = AlgoSpec(extreme_point.pack, ns, isolate=False,
                                          kwargs={"sort": "volume", "allow_rotation": True,
                                                  "support_ratio": sup, "heavy_below": True})
    # same constraints, heaviest items first (cheaper way to respect heavy-below?)
    algos["ep_weight_support_weight"] = AlgoSpec(
        extreme_point.pack, ns, isolate=False,
        kwargs={"sort": "weight", "allow_rotation": True, "support_ratio": sup,
                "heavy_below": True})
    return algos


def run_orders() -> tuple[pd.DataFrame, dict]:
    """Box recommendation vs naive box choice on NUM_ORDERS fixed orders."""
    rows, kept = [], {}
    for oid in range(cfg.NUM_ORDERS):
        items = gen_order(oid, cfg.BASE_SEED, cfg.ORDER_ITEMS, cfg.ORDER_DIM_RANGE,
                          cfg.C3_WEIGHT_RANGE)
        for name, f, rot in [("box_recommend", box_recommend.recommend, True),
                             ("box_naive", box_recommend.naive_box, False)]:
            t0 = time.perf_counter()
            res = f(items, cfg.BOX_CATALOG)
            dt = time.perf_counter() - t0
            validate_3d(items, cfg.BOX_CATALOG[res.extra["box"]], res.placements, rot)
            kept[(oid, name)] = (items, res)
            rows.append({
                "experiment": "C-box", "algorithm": name, "dist": "order", "n": len(items),
                "seed": cfg.BASE_SEED, "rep": oid, "num_bins": res.num_bins, "lower_bound": 1,
                "opt": None, "runtime_s": dt, "status": res.status,
                "fill_rate": 1 - res.extra["void_ratio"], "extra_json": json.dumps(res.extra),
            })
    print(f"[C-box] {cfg.NUM_ORDERS} orders done", flush=True)
    return pd.DataFrame(rows, columns=COLUMNS), kept


def write_views(mode: str, kept: dict) -> None:
    items = make_instance(cfg.C3_VIEW_N, cfg.C3_VIEW_DIST, cfg.BASE_SEED)
    sup = cfg.C3_SUPPORT_RATIO
    nv = naive.pack(items, BOX)
    epv = extreme_point.pack(items, BOX)
    eps = extreme_point.pack(items, BOX, support_ratio=sup)
    epw = extreme_point.pack(items, BOX, support_ratio=sup, heavy_below=True)
    epww = extreme_point.pack(items, BOX, sort="weight", support_ratio=sup, heavy_below=True)
    tag = f"{cfg.C3_VIEW_DIST}, n={cfg.C3_VIEW_N}, seed={cfg.BASE_SEED}"
    write_comparison(HTML_DIR / f"exp_c_naive_vs_ep_{mode}.html",
                     [("3D Naive", items, BOX, nv), ("Extreme Point", items, BOX, epv)],
                     f"Same items, two recipes ({tag})")
    write_comparison(HTML_DIR / f"exp_c_constraints_{mode}.html",
                     [("EP (no constraints)", items, BOX, epv),
                      (f"EP + support {sup:.0%}", items, BOX, eps),
                      ("EP + support + heavy-below", items, BOX, epw),
                      ("same, heaviest first", items, BOX, epww)],
                     f"Loading constraints on / off ({tag})")
    # orders where the recommendation picked a smaller box than the naive choice
    better = [oid for oid in range(cfg.NUM_ORDERS)
              if kept[(oid, "box_recommend")][1].extra["box_volume"]
              < kept[(oid, "box_naive")][1].extra["box_volume"]][:2]
    panels = []
    for oid in better:
        for name, label in [("box_naive", "naive"), ("box_recommend", "recommend")]:
            it, res = kept[(oid, name)]
            e = res.extra
            dims = "x".join(map(str, e["box_dims"]))
            panels.append((f"order {oid} {label}: {dims} void {e['void_ratio']:.0%}",
                           it, tuple(e["box_dims"]), res))
    if panels:
        write_comparison(HTML_DIR / f"exp_c_boxes_{mode}.html", panels,
                         "Box choice per order: naive vs recommendation", max_bins=2)


def write_animations(mode: str) -> None:
    """Drop-in animations on one fixed instance (same items in every panel)."""
    items = make_instance(cfg.C3_ANIM_N, cfg.C3_ANIM_DIST, cfg.BASE_SEED)
    sup = cfg.C3_SUPPORT_RATIO
    tag = f"{cfg.C3_ANIM_DIST}, n={cfg.C3_ANIM_N}, seed={cfg.BASE_SEED}"
    epv = extreme_point.pack(items, BOX)
    write_animation(HTML_DIR / f"anim_naive_vs_ep_{mode}.html",
                    [("3D Naive", items, BOX, naive.pack(items, BOX)),
                     ("Extreme Point", items, BOX, epv)],
                    f"Packing order, one item at a time ({tag})")
    write_animation(HTML_DIR / f"anim_constraints_{mode}.html",
                    [("EP (no constraints)", items, BOX, epv),
                     ("EP heaviest first + support + heavy-below", items, BOX,
                      extreme_point.pack(items, BOX, sort="weight", support_ratio=sup,
                                         heavy_below=True))],
                    f"Loading rules on / off ({tag})")


def main() -> None:
    mode = parse_mode(__doc__)
    m = cfg.MODES[mode]
    t0 = time.perf_counter()
    df = sweep("C", PROBLEM_3D, algorithms(cfg.C3_N[mode]), cfg.C3_DISTS, m["reps"],
               cfg.BASE_SEED, m["timeout_s"])
    boxes, kept = run_orders()
    df = pd.concat([df, boxes], ignore_index=True)
    out = CSV_DIR / f"exp_c_{mode}.csv"
    df.to_csv(out, index=False)
    print(f"wrote {out}")
    plots.plot_exp_c(df, FIG_DIR, mode, cfg.VOID_LIMIT)
    write_views(mode, kept)
    write_animations(mode)
    print(f"done in {time.perf_counter() - t0:.1f}s")


if __name__ == "__main__":
    main()
