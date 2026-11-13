"""Experiment B — 1D heuristics at scale (NF, FF, BF, FFD) vs time-limited MIP.

    python -m experiments.exp_b --quick
    python -m experiments.exp_b
"""
from __future__ import annotations

from experiments import config as cfg
from experiments.common import CSV_DIR, FIG_DIR, parse_mode
from packing.bench.runner import AlgoSpec, sweep_1d
from packing.oned import heuristics, mip
from packing.viz import plots


def main() -> None:
    mode = parse_mode(__doc__)
    m = cfg.MODES[mode]
    mip_t = cfg.B_MIP_TIME_LIMIT_S[mode]
    fast = dict(ns=cfg.B_N, isolate=False)
    algos = {
        "next_fit": AlgoSpec(heuristics.next_fit, **fast),
        "first_fit": AlgoSpec(heuristics.first_fit, **fast),
        "best_fit": AlgoSpec(heuristics.best_fit, **fast),
        "ffd": AlgoSpec(heuristics.ffd, **fast),
        # MIP: n > 1000 returns "skipped" without building the model
        "mip": AlgoSpec(mip.solve, cfg.B_N, exact=True, isolate=False,
                        kwargs={"time_limit_s": mip_t}, hard_timeout_s=2 * mip_t + 60),
    }
    df = sweep_1d("B", algos, cfg.DISTS_1D, m["reps"], cfg.BASE_SEED, m["timeout_s"], cfg.C)
    out = CSV_DIR / f"exp_b_{mode}.csv"
    df.to_csv(out, index=False)
    print(f"wrote {out}")
    plots.plot_exp_b(df, FIG_DIR, mode)


if __name__ == "__main__":
    main()
