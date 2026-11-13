"""Slide-ready matplotlib figures (English labels, large fonts)."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

plt.rcParams.update({"font.size": 14, "axes.titlesize": 16, "axes.labelsize": 15,
                     "legend.fontsize": 12, "figure.dpi": 120})

STYLE = {  # algorithm -> (label, color, marker)
    "exhaustive": ("Exhaustive (all orders)", "#d62728", "o"),
    "dp": ("Bitmask DP", "#1f77b4", "s"),
    "mip": ("MIP (OR-Tools SCIP)", "#2ca02c", "^"),
    "ffd": ("FFD", "#9467bd", "D"),
    "next_fit": ("Next Fit", "#8c564b", "v"),
    "first_fit": ("First Fit", "#ff7f0e", "<"),
    "best_fit": ("Best Fit", "#17becf", ">"),
}


def _median(df: pd.DataFrame, col: str) -> pd.DataFrame:
    return df.groupby(["algorithm", "dist", "n"], as_index=False)[col].median()


def plot_exp_a(df: pd.DataFrame, out_dir: Path, mode: str, timeout_s: float) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    dists = list(dict.fromkeys(df.dist))

    # 1) runtime vs n (log), timeouts marked with X on the limit line
    fig, axes = plt.subplots(1, len(dists), figsize=(6 * len(dists), 5), sharey=True)
    for ax, dist in zip(axes, dists):
        d = df[df.dist == dist]
        done = _median(d[d.status.isin(["ok", "feasible"])], "runtime_s")
        for alg in dict.fromkeys(d.algorithm):
            label, color, marker = STYLE[alg]
            a = done[done.algorithm == alg]
            ax.plot(a.n, a.runtime_s, marker=marker, color=color, label=label)
            to = d[(d.algorithm == alg) & (d.status == "timeout")]
            if len(to):
                ax.scatter(to.n.unique(), [timeout_s] * to.n.nunique(), marker="x", s=150,
                           color=color, linewidths=3, zorder=5)
        ax.axhline(timeout_s, ls="--", color="gray")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(f"{dist} sizes")
        ax.set_xlabel("number of items n")
        ax.grid(True, which="both", alpha=0.3)
    axes[0].set_ylabel("runtime (s, median)")
    axes[0].legend(loc="upper left")
    fig.suptitle(f"Exact vs greedy: runtime  (X = gave up at {timeout_s:g}s)")
    fig.tight_layout()
    fig.savefig(out_dir / f"exp_a_runtime_{mode}.png")
    plt.close(fig)

    # 2) FFD / OPT vs n
    f = df[(df.algorithm == "ffd") & df.opt.notna()].copy()
    f["ratio"] = f.num_bins.astype(float) / f.opt.astype(float)
    fig, ax = plt.subplots(figsize=(8, 5))
    for dist in dists:
        g = f[f.dist == dist].groupby("n").ratio
        line, = ax.plot(g.median().index, g.median().values, marker="o", label=f"{dist} (median)")
        ax.plot(g.max().index, g.max().values, ls=":", color=line.get_color(), label=f"{dist} (max)")
    ax.axhline(1.0, color="black", lw=1)
    ax.set_xscale("log")
    ax.set_xlabel("number of items n")
    ax.set_ylabel("FFD bins / optimal bins")
    ax.set_title("How far is FFD from optimal?")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / f"exp_a_ffd_ratio_{mode}.png")
    plt.close(fig)


def plot_exp_b(df: pd.DataFrame, out_dir: Path, mode: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    dists = list(dict.fromkeys(df.dist))
    ok = df[df.status.isin(["ok", "feasible"])].copy()
    ok["ratio"] = ok.num_bins.astype(float) / ok.lower_bound

    for col, ylabel, fname, logy in [("ratio", "bins / lower bound (median)", "bins_over_lb", False),
                                     ("runtime_s", "runtime (s, median)", "runtime", True)]:
        fig, axes = plt.subplots(1, len(dists), figsize=(6 * len(dists), 5), sharey=True)
        med = _median(ok, col)
        for ax, dist in zip(axes, dists):
            d = med[med.dist == dist]
            for alg in dict.fromkeys(d.algorithm):
                label, color, marker = STYLE[alg]
                a = d[d.algorithm == alg]
                ax.plot(a.n, a[col], marker=marker, color=color, label=label)
            ax.set_xscale("log")
            if logy:
                ax.set_yscale("log")
            ax.set_title(f"{dist} sizes")
            ax.set_xlabel("number of items n")
            ax.grid(True, which="both", alpha=0.3)
        axes[0].set_ylabel(ylabel)
        axes[0].legend()
        fig.suptitle("Heuristics at scale" + (" — quality" if col == "ratio" else " — runtime"))
        fig.tight_layout()
        fig.savefig(out_dir / f"exp_b_{fname}_{mode}.png")
        plt.close(fig)
