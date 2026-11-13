"""Build results/summary.md from the experiment CSVs.

Slides and READMEs must take their numbers from this file only.

    python -m experiments.summary            # uses default-mode CSVs, falls back to quick
    python -m experiments.summary --mode quick
"""
from __future__ import annotations

import argparse
from datetime import date

import pandas as pd

from experiments.common import CSV_DIR, ROOT

def _load(exp: str, mode: str) -> tuple[pd.DataFrame | None, str]:
    for m in ([mode] if mode else ["full", "default", "quick"]):
        p = CSV_DIR / f"exp_{exp}_{m}.csv"
        if p.exists():
            return pd.read_csv(p), m
    return None, ""

def table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join("" if pd.isna(v) else str(v) for v in r) + " |")
    return "\n".join(lines)

def section_a(df: pd.DataFrame, mode: str) -> list[str]:
    out = [f"## Experiment A — exact vs greedy (`{mode}` mode)", ""]
    # largest n finished and first n that gave up
    rows = []
    for (alg, dist), g in df.groupby(["algorithm", "dist"], sort=False):
        done = g[g.status.isin(["ok", "feasible"])]
        proven = g[g.status == "ok"]
        to = g[g.status == "timeout"]
        rows.append({
            "algorithm": alg, "dist": dist,
            "largest n proven optimal": int(proven.n.max()) if alg != "ffd" and len(proven) else "-",
            "largest n with an answer": int(done.n.max()) if len(done) else "-",
            "gave up at n": int(to.n.min()) if len(to) else "-",
            "median runtime at that largest n (s)":
                round(done[done.n == done.n.max()].runtime_s.median(), 4) if len(done) else "-",
        })
    out += ["### Where each method gives up", "", table(pd.DataFrame(rows)), ""]

    # agreement of exact methods on the same instance
    ex = df[df.algorithm.isin(["exhaustive", "dp", "mip"]) & (df.status == "ok")]
    per = ex.groupby(["dist", "n", "seed"]).agg(methods=("algorithm", "nunique"),
                                                 distinct=("num_bins", "nunique"))
    multi = per[per.methods >= 2]
    out += ["### Do the exact methods agree?", "",
            f"Instances solved to proven optimality by 2+ exact methods: **{len(multi)}**, "
            f"disagreements: **{int((multi.distinct > 1).sum())}** "
            f"(n range {multi.index.get_level_values('n').min()}–"
            f"{multi.index.get_level_values('n').max()}).", ""]

    # FFD / OPT
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
    g["runtime_s"] = g.runtime_s.round(4)
    out += ["Median over reps. `bins/L` = bins used / lower bound ceil(sum/C).", "", table(g), ""]
    return out

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["quick", "default", "full"])
    mode = p.parse_args().mode
    lines = ["# Results summary (auto-generated — do not edit by hand)", "",
             f"Generated {date.today()} by `python -m experiments.summary`.", ""]
    a, ma = _load("a", mode)
    b, mb = _load("b", mode)
    if a is not None:
        lines += section_a(a, ma)
    if b is not None:
        lines += section_b(b, mb)
    if "quick" in (ma, mb):
        lines.insert(4, "> **Warning:** contains `quick`-mode numbers (2 reps, 5 s limit). "
                        "Do not put these in slides.\n")
    out = ROOT / "results" / "summary.md"
    out.write_text("\n".join(lines))
    print(f"wrote {out}")

if __name__ == "__main__":
    main()
