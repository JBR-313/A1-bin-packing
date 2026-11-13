"""Build results/summary.md from the experiment CSVs.

Slides and READMEs must take their numbers from this file only.

    python -m experiments.summary            # newest available mode per experiment
    python -m experiments.summary --mode quick
"""
from __future__ import annotations

import argparse
import json
from datetime import date

import numpy as np
import pandas as pd

from experiments import config as cfg
from experiments.common import CSV_DIR, ROOT
from packing.viz.plots import ROTATION, SUPPORT_SENSITIVITY, constraint_cost, extra_bins


def _load(exp: str, mode: str | None) -> tuple[pd.DataFrame | None, str]:
    for m in ([mode] if mode else ["full", "default", "quick"]):
        p = CSV_DIR / f"exp_{exp}_{m}.csv"
        if p.exists():
            return pd.read_csv(p), m
    return None, ""


def _cell(v) -> str:
    if pd.isna(v):
        return ""
    if isinstance(v, float):  # plain decimals, never 4e-05
        return np.format_float_positional(v, trim="-")
    return str(v)


def table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(_cell(v) for v in r) + " |")
    return "\n".join(lines)


def section_a(df: pd.DataFrame, mode: str) -> list[str]:
    out = [f"## Experiment A — exact vs greedy (`{mode}` mode)", ""]
    rows = []
    for (alg, dist), g in df.groupby(["algorithm", "dist"], sort=False):
        # timeout rule: an n counts as finished only if NO rep timed out
        per_n = g.groupby("n").status.agg(set)
        all_ok = [n for n, s in per_n.items() if s == {"ok"}]
        answered = [n for n, s in per_n.items() if "timeout" not in s]
        gave_up = [n for n, s in per_n.items() if "timeout" in s]
        last = max(answered) if answered else None
        rows.append({
            "algorithm": alg, "dist": dist,
            "largest n, all reps proven optimal": max(all_ok) if alg != "ffd" and all_ok else "-",
            "largest n, all reps answered": last if last is not None else "-",
            "gave up at n": min(gave_up) if gave_up else "-",
            "largest n tried": int(g.n.max()),
            "median runtime at largest answered n (s)":
                round(g[g.n == last].runtime_s.median(), 4) if last is not None else "-",
        })
    out += ["### Where each method gives up", "",
            "An n counts as finished only if every rep finished within the time limit "
            "(one timeout → that n is `gave up`, larger n are not run). "
            "`-` under *gave up* means it never timed out up to *largest n tried*; "
            "DP is capped at n = 24 by memory (2^24 states), not by time.", "",
            table(pd.DataFrame(rows)), ""]

    ex = df[df.algorithm.isin(["exhaustive", "dp", "mip"]) & (df.status == "ok")]
    per = ex.groupby(["dist", "n", "seed"]).agg(methods=("algorithm", "nunique"),
                                                 distinct=("num_bins", "nunique"))
    multi = per[per.methods >= 2]
    out += ["### Do the exact methods agree?", "",
            f"Instances solved to proven optimality by 2+ exact methods: **{len(multi)}**, "
            f"disagreements: **{int((multi.distinct > 1).sum())}** "
            f"(n range {multi.index.get_level_values('n').min()}–"
            f"{multi.index.get_level_values('n').max()}).", ""]

    f = df[(df.algorithm == "ffd") & df.opt.notna()].copy()
    f["ratio"] = f.num_bins / f.opt
    r = f.groupby("dist").agg(instances=("ratio", "size"),
                              optimal_share=("ratio", lambda s: f"{(s == 1).mean():.1%}"),
                              median=("ratio", "median"), max=("ratio", "max")).reset_index()
    r[["median", "max"]] = r[["median", "max"]].round(3)
    out += ["### FFD / OPT (instances where OPT is known)", "", table(r), ""]
    return out


def section_b(df: pd.DataFrame, mode: str) -> list[str]:
    out = [f"## Experiment B — heuristics at scale (`{mode}` mode)", ""]
    d = df.copy()
    d["bins/L"] = d.num_bins / d.lower_bound
    g = d.groupby(["dist", "algorithm", "n"], sort=False).agg(
        status=("status", lambda s: ",".join(sorted(set(s)))),
        bins_over_L=("bins/L", "median"), runtime_s=("runtime_s", "median")).reset_index()
    g["bins_over_L"] = g.bins_over_L.round(4)
    g["runtime_s"] = g.runtime_s.round(6)
    out += ["Median over reps. `bins/L` = bins used / lower bound ceil(sum/C).", "", table(g), ""]
    return out


def section_c(df: pd.DataFrame, mode: str) -> list[str]:
    out = [f"## Experiment C — 3D packing and loading (`{mode}` mode)", ""]
    c = df[df.experiment == "C"].copy()
    c["bins_over_L"] = c.num_bins / c.lower_bound
    g = c.groupby(["dist", "algorithm", "n"], sort=False).agg(
        status=("status", lambda s: ",".join(sorted(set(s)))),
        bins=("num_bins", "median"), L=("lower_bound", "median"),
        bins_over_L=("bins_over_L", "median"), fill_rate=("fill_rate", "median"),
        runtime_s=("runtime_s", "median")).reset_index()
    for col, k in [("bins_over_L", 3), ("fill_rate", 3), ("runtime_s", 6)]:
        g[col] = g[col].round(k)
    out += ["### Bins, fill rate and runtime per n", "",
            f"Container {cfg.C3_CONTAINER}, item sides {cfg.C3_DIM_RANGE}, median over reps. "
            "`fill_rate` = item volume / (bins × container volume). "
            "Naive never rotates; all EP variants allow rotation.", "", table(g), ""]

    out += ["### Cost of loading constraints", "",
            "Same instances, EP sorted by volume with vs without constraints. "
            "`increase_pct` = sum(bins with) / sum(bins without) − 1 over all n and seeds. "
            f"Support threshold {cfg.C3_SUPPORT_RATIO:.0%} is an assumption.", "",
            table(constraint_cost(df)), ""]

    sens = extra_bins(df, SUPPORT_SENSITIVITY)
    if len(sens):
        out += ["### Sensitivity of the support threshold", "",
                "Extra bins vs plain EP for support thresholds 50% / 70% / 90% "
                "(same instances, same method as above).", "",
                table(sens[sens.dist == "all"]), "", table(sens[sens.dist != "all"]), ""]

    rot = extra_bins(df, ROTATION)
    if len(rot):
        out += ["### How much of the Naive → EP gap is rotation?", "",
                "Extra bins vs EP with rotation (sort by volume). `ep_volume_norot` = same EP "
                "without rotation; `naive` = 3D Naive (no rotation). The gap between the two "
                "rows is the algorithm; the gap between `ep_volume_norot` and 0% is rotation.",
                "", table(rot), ""]

    b = df[df.experiment == "C-box"].copy()
    if len(b):
        b["void"] = 1 - b.fill_rate
        r = b.groupby("algorithm", sort=False).agg(
            orders=("rep", "nunique"),
            void_median=("void", "median"), void_mean=("void", "mean"),
            share_void_le_50=("void", lambda s: f"{(s <= cfg.VOID_LIMIT).mean():.1%}"),
            share_split=("num_bins", lambda s: f"{(s > 1).mean():.1%}"),
            runtime_ms_median=("runtime_s", lambda s: s.median() * 1000)).reset_index()
        tries = b.extra_json.map(lambda e: json.loads(e)["tries"])
        r["tries_mean"] = r.algorithm.map(tries.groupby(b.algorithm).mean())
        for col in ("void_median", "void_mean"):
            r[col] = r[col].round(3)
        r["runtime_ms_median"] = r.runtime_ms_median.round(3)
        r["tries_mean"] = r.tries_mean.round(2)
        out += ["### Box choice per order", "",
                f"{cfg.NUM_ORDERS} orders of {cfg.ORDER_ITEMS[0]}–{cfg.ORDER_ITEMS[1]} items "
                f"(sides {cfg.ORDER_DIM_RANGE}), catalog {cfg.BOX_CATALOG}. "
                "void = 1 − item volume / box volume used. `share_split` = orders that "
                "needed more than one box. `tries` = packing attempts per order "
                "(multi-start cost; included in runtime).", "", table(r), "",
                "Not comparable with CJ Logistics' published figures (different items and "
                "catalog).", ""]
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["quick", "default", "full"])
    mode = p.parse_args().mode
    lines = ["# Results summary (auto-generated — do not edit by hand)", "",
             f"Generated {date.today()} by `python -m experiments.summary`.", ""]
    used = []
    for exp, section in (("a", section_a), ("b", section_b), ("c", section_c)):
        df, m = _load(exp, mode)
        if df is not None:
            lines += section(df, m)
            used.append(m)
    if "quick" in used:
        lines.insert(4, "> **Warning:** contains `quick`-mode numbers (2 reps, 5 s limit). "
                        "Do not put these in slides.\n")
    out = ROOT / "results" / "summary.md"
    out.write_text("\n".join(lines))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
