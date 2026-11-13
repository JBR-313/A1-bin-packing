"""Experiment A — 1D exact methods (exhaustive, bitmask DP, MIP) vs FFD.

    python -m experiments.exp_a --quick     # check the pipeline
    python -m experiments.exp_a             # presentation numbers
"""
from __future__ import annotations

from experiments import config as cfg
from experiments.common import CSV_DIR, FIG_DIR, parse_mode
from packing.bench.runner import AlgoSpec, sweep_1d
from packing.oned import dp, exhaustive, heuristics, mip
from packing.viz import plots


def main() -> None:
    mode = parse_mode(__doc__)
    m = cfg.MODES[mode]
    t = m["timeout_s"]
    algos = {
        "exhaustive": AlgoSpec(exhaustive.solve, cfg.A_N_EXHAUSTIVE, exact=True),
        "dp": AlgoSpec(dp.solve, cfg.A_N_DP, exact=True),
        # MIP stops itself at the time limit; hard kill only as a safety net
        "mip": AlgoSpec(mip.solve, cfg.A_N_ALL, exact=True, isolate=False,
                        kwargs={"time_limit_s": t}, hard_timeout_s=2 * t + 30),
        "ffd": AlgoSpec(heuristics.ffd, cfg.A_N_ALL, isolate=False),
    }
    df = sweep_1d("A", algos, cfg.DISTS_1D, m["reps"], cfg.BASE_SEED, t, cfg.C)
    out = CSV_DIR / f"exp_a_{mode}.csv"
    df.to_csv(out, index=False)
    print(f"wrote {out}")
    plots.plot_exp_a(df, FIG_DIR, mode, t)


if __name__ == "__main__":
    main()
