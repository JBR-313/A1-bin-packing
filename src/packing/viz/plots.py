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
    "naive": ("3D Naive (layers)", "#d62728", "o"),
    "ep_volume": ("EP, sort by volume", "#1f77b4", "s"),
    "ep_height": ("EP, sort by height", "#17becf", "^"),
    "ep_area": ("EP, sort by base area", "#9467bd", "D"),
    "ep_support": ("EP + support 70%", "#ff7f0e", "v"),
    "ep_support_weight": ("EP + support + heavy-below", "#8c564b", "P"),
    "ep_volume_norot": ("EP, sort by volume, no rotation", "#7f7f7f", "X"),
    "ep_support_50": ("EP + support 50%", "#ffbb78", "v"),
    "ep_support_90": ("EP + support 90%", "#d62728", "v"),
    "box_recommend": ("Box recommendation", "#2ca02c", "s"),
    "box_naive": ("Naive box choice", "#d62728", "o"),
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
        # timeout rule: an n with any timed-out rep is shown only as an X, not as a point
        timed = d[d.status == "timeout"][["algorithm", "n"]].drop_duplicates()
        keep = ~d.set_index(["algorithm", "n"]).index.isin(timed.set_index(["algorithm", "n"]).index)
        done = _median(d[keep & d.status.isin(["ok", "feasible"])], "runtime_s")
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
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=len(labels), frameon=False)
    fig.suptitle(f"Exact vs greedy: runtime  (X = gave up at {timeout_s:g}s)")
    fig.tight_layout(rect=(0, 0.08, 1, 1))
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


# ---------------------------------------------------------------- experiment C
CONSTRAINED = ("ep_support", "ep_support_weight")
SUPPORT_SENSITIVITY = ("ep_support_50", "ep_support", "ep_support_90")
ROTATION = ("ep_volume_norot", "naive")
# lines drawn in the per-n plots (sensitivity variants only go to summary.md)
MAIN_C = ("naive", "ep_volume_norot", "ep_volume", "ep_height", "ep_area",
          "ep_support", "ep_support_weight")


def extra_bins(df: pd.DataFrame, variants=CONSTRAINED, base: str = "ep_volume") -> pd.DataFrame:
    """Extra bins of each variant compared with `base`, per distribution and overall.

    Default: loading constraints vs plain EP (both sorted by volume, rotation on).
    Only instances (dist, n, seed) where both finished are compared.
    increase = sum(bins of variant) / sum(bins of base) - 1, which is steadier than a
    median of small integers.
    """
    c = df[(df.experiment == "C") & (df.status == "ok")]
    key = ["dist", "n", "seed"]
    b = c[c.algorithm == base].set_index(key).num_bins.rename("base")
    rows = []
    for alg in variants:
        j = c[c.algorithm == alg].set_index(key).num_bins.rename("var").to_frame().join(b, how="inner")
        if j.empty:
            continue
        for dist, g in list(j.groupby(level="dist")) + [("all", j)]:
            rows.append({"variant": alg, "dist": dist, "instances": len(g),
                         f"bins_{base}": int(g.base.sum()), "bins_variant": int(g["var"].sum()),
                         "increase_pct": round(100 * (g["var"].sum() / g.base.sum() - 1), 1),
                         "share_needing_more_bins": f"{(g['var'] > g.base).mean():.0%}"})
    return pd.DataFrame(rows)


def constraint_cost(df: pd.DataFrame) -> pd.DataFrame:
    return extra_bins(df, CONSTRAINED)


def plot_exp_c(df: pd.DataFrame, out_dir: Path, mode: str, void_limit: float) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    c = df[(df.experiment == "C") & df.status.isin(["ok"]) & df.algorithm.isin(MAIN_C)].copy()
    c["ratio"] = c.num_bins.astype(float) / c.lower_bound
    dists = list(dict.fromkeys(c.dist))

    for col, ylabel, fname, logy in [("ratio", "bins / lower bound (median)", "bins_over_lb", False),
                                     ("runtime_s", "runtime (s, median)", "runtime", True)]:
        fig, axes = plt.subplots(1, len(dists), figsize=(5.5 * len(dists), 5), sharey=True)
        med = _median(c, col)
        for ax, dist in zip(axes, dists):
            d = med[med.dist == dist]
            for alg in dict.fromkeys(d.algorithm):
                label, color, marker = STYLE[alg]
                a = d[d.algorithm == alg]
                ax.plot(a.n, a[col], marker=marker, color=color, label=label)
            ax.set_xscale("log")
            ns = sorted(c.n.unique())
            ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
            ax.set_xticks(ns, [str(n) for n in ns])
            if logy:
                ax.set_yscale("log")
            ax.set_title(f"{dist} items")
            ax.set_xlabel("number of items n")
            ax.grid(True, which="both", alpha=0.3)
        axes[0].set_ylabel(ylabel)
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="lower center", ncol=len(labels), fontsize=12,
                   frameon=False)
        fig.suptitle("3D packing" + (" — quality (1.0 = volume lower bound)" if col == "ratio"
                                     else " — runtime"))
        fig.tight_layout(rect=(0, 0.08, 1, 1))
        fig.savefig(out_dir / f"exp_c_{fname}_{mode}.png")
        plt.close(fig)

    # constraint cost bars
    cc = constraint_cost(df)
    if len(cc):
        fig, ax = plt.subplots(figsize=(9, 5))
        groups = list(dict.fromkeys(cc.dist))
        width = 0.38
        for k, alg in enumerate(CONSTRAINED):
            s = cc[cc.variant == alg].set_index("dist").reindex(groups)
            xs = [i + (k - 0.5) * width for i in range(len(groups))]
            bars = ax.bar(xs, s.increase_pct, width, label=STYLE[alg][0], color=STYLE[alg][1])
            ax.bar_label(bars, fmt="%.1f%%", fontsize=11)
        ax.set_xticks(range(len(groups)), groups)
        ax.set_ylabel("extra bins vs plain EP (%)")
        ax.set_title("Cost of loading constraints")
        ax.grid(True, axis="y", alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(out_dir / f"exp_c_constraint_cost_{mode}.png")
        plt.close(fig)

    # void ratio histogram for box choice
    b = df[df.experiment == "C-box"].copy()
    if len(b):
        b["void"] = 1 - b.fill_rate
        fig, ax = plt.subplots(figsize=(9, 5))
        bins = [i / 20 for i in range(21)]
        for alg in ("box_naive", "box_recommend"):
            v = b[b.algorithm == alg].void
            ax.hist(v, bins=bins, alpha=0.6, color=STYLE[alg][1],
                    label=f"{STYLE[alg][0]} (median {v.median():.0%})")
        ax.axvline(void_limit, color="black", ls="--", lw=2)
        ax.text(void_limit + 0.01, ax.get_ylim()[1] * 0.92, f"{void_limit:.0%} limit", fontsize=12)
        ax.set_xlabel("void ratio = 1 - item volume / box volume")
        ax.set_ylabel("number of orders")
        ax.set_title(f"Box choice for {b.rep.nunique()} orders")
        ax.legend()
        fig.tight_layout()
        fig.savefig(out_dir / f"exp_c_void_hist_{mode}.png")
        plt.close(fig)
