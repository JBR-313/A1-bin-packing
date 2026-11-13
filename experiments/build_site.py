"""Build the results website (index.html at the repo root, served by GitHub Pages).

    python -m experiments.build_site

Every number on the page is computed here from the default-mode CSVs with the same
functions that write results/summary.md, so the site, summary.md and the slides agree.
Run it again after re-running any experiment.
"""
from __future__ import annotations

import html
from datetime import date

import numpy as np
import pandas as pd

from experiments import config as cfg
from experiments.common import CSV_DIR, ROOT
from experiments.summary import (b_table, box_table, c_table, exact_agreement, ffd_ratio_table,
                                 gives_up_table)
from packing.viz.animate3d import ANIM_HEIGHT
from packing.viz.view3d import figure_height
from packing.viz.plots import (CONSTRAINED, MAIN_C, ROTATION, STYLE, SUPPORT_SENSITIVITY,
                               extra_bins)

MODE = "default"
REPO = "https://github.com/JBR-313/A1-bin-packing"
FIG = "results/figures"
VIEW = "results/html"

LABEL = {k: v[0] for k, v in STYLE.items()}


# ---------------------------------------------------------------- helpers
def esc(x) -> str:
    return html.escape(str(x))


def fmt(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return ""
    if isinstance(v, (float, np.floating)):
        return np.format_float_positional(float(v), trim="-")
    return str(v)


def table(df: pd.DataFrame, rename: dict | None = None, label_col: str | None = None) -> str:
    d = df.copy()
    if label_col:
        d[label_col] = d[label_col].map(lambda a: LABEL.get(a, a))
    if rename:
        d = d.rename(columns=rename)
    head = "".join(f"<th>{esc(c)}</th>" for c in d.columns)
    body = "".join("<tr>" + "".join(f"<td>{esc(fmt(v))}</td>" for v in r) + "</tr>"
                   for r in d.itertuples(index=False))
    return f'<div class="tw"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def figure(src: str, alt: str, caption: str) -> str:
    return (f'<figure><a href="{src}"><img src="{src}" alt="{esc(alt)}" loading="lazy"></a>'
            f"<figcaption>{caption}</figcaption></figure>")


ONE_ROW = figure_height(1) + 20   # iframe height for 1-2 panel viewers / animations
TWO_ROWS = figure_height(2) + 20  # 2x2 viewers
ANIM = ANIM_HEIGHT + 20            # animations (scene row + buttons + slider)


def viewer(src: str, title: str, caption: str, height: int = ONE_ROW) -> str:
    return (f'<figure class="viewer"><div class="vhead"><span>{esc(title)}</span>'
            f'<a href="{src}" target="_blank" rel="noopener">Open full screen ↗</a></div>'
            f'<iframe src="{src}" title="{esc(title)}" loading="lazy" style="height:{height}px">'
            f"</iframe><figcaption>{caption}</figcaption></figure>")


def tile(value: str, label: str) -> str:
    return f'<div class="tile"><div class="v">{esc(value)}</div><div class="l">{label}</div></div>'


def pct(x: float, digits: int = 1) -> str:
    return f"{x:.{digits}f}%"


def one_or_list(values, unit="n = ") -> str:
    vals = sorted(set(values))
    return f"{unit}{vals[0]} in every distribution" if len(vals) == 1 else \
        ", ".join(f"{unit}{v}" for v in vals)


# ---------------------------------------------------------------- page
def build() -> str:
    a = pd.read_csv(CSV_DIR / f"exp_a_{MODE}.csv")
    b = pd.read_csv(CSV_DIR / f"exp_b_{MODE}.csv")
    c = pd.read_csv(CSV_DIR / f"exp_c_{MODE}.csv")

    # --- experiment A numbers
    gu = gives_up_table(a)
    ex_gave = [int(v) for v in gu[gu.algorithm == "exhaustive"]["gave up at n"] if v != "-"]
    dp_rows = gu[gu.algorithm == "dp"]
    dp_max = int(dp_rows["largest n, all reps answered"].max())
    dp_rt = dp_rows["median runtime at largest answered n (s)"].astype(float)
    agree = exact_agreement(a)
    fr = ffd_ratio_table(a)
    f_all = a[(a.algorithm == "ffd") & a.opt.notna()]
    ffd_opt_share = (f_all.num_bins == f_all.opt).mean() * 100
    ffd_max = float(fr["max"].max())
    mip = gu[gu.algorithm == "mip"].set_index("dist")
    mip_gave = mip["gave up at n"].to_dict()
    mip_proven = mip["largest n, all reps proven optimal"].to_dict()

    # --- experiment B numbers
    bt = b_table(b)
    big = bt[(bt.n == bt.n.max()) & (bt.algorithm != "mip")]
    ffd_big = big[big.algorithm == "ffd"]
    mip_rows = bt[bt.algorithm == "mip"]
    mip_b_fail = mip_rows[(mip_rows.dist == "uniform") & (mip_rows.status == "timeout")].n
    mip_b_fail = int(mip_b_fail.min()) if len(mip_b_fail) else None

    # --- experiment C numbers
    rot = extra_bins(c, ROTATION)
    naive_all = float(rot[(rot.variant == "naive") & (rot.dist == "all")].increase_pct.iloc[0])
    norot_all = float(rot[(rot.variant == "ep_volume_norot") & (rot.dist == "all")].increase_pct.iloc[0])
    cc = extra_bins(c, CONSTRAINED)
    cc_all = {r.variant: r.increase_pct for r in cc[cc.dist == "all"].itertuples()}
    sens = extra_bins(c, SUPPORT_SENSITIVITY)
    sens_all = sens[sens.dist == "all"]
    ct = c_table(c)
    nmax = ct.n.max()
    c_big = ct[(ct.n == nmax) & ct.algorithm.isin(MAIN_C)][
        ["dist", "algorithm", "bins", "L", "bins_over_L", "fill_rate", "runtime_s"]]
    ep_rt_max = float(ct[(ct.n == nmax) & ct.algorithm.str.startswith("ep_")].runtime_s.max())
    rules = c[(c.experiment == "C") & c.algorithm.isin(["ep_volume", "ep_height", "ep_area"])]
    rule_bins = rules.groupby("algorithm").num_bins.sum()
    rule_spread = 100 * (rule_bins.max() / rule_bins.min() - 1)
    cc_d = cc[cc.dist != "all"].pivot(index="dist", columns="variant", values="increase_pct")
    wf_always_lower = bool((cc_d["ep_weight_support_weight"] < cc_d["ep_support_weight"]).all())
    worst_support = cc_d["ep_support"].idxmax()
    worst_heavy = cc_d["ep_support_weight"].idxmax()
    bx = box_table(c)
    rec = bx[bx.algorithm == "box_recommend"].iloc[0]
    nav = bx[bx.algorithm == "box_naive"].iloc[0]

    tiles = "".join([
        tile(f"n = {min(ex_gave)}", "exhaustive search gives up (60 s limit)"),
        tile(f"{agree['disagreements']} / {agree['instances']}",
             "disagreements between exact methods"),
        tile(pct(ffd_opt_share), "of instances where FFD is already optimal"),
        tile(f"+{naive_all:.0f}%", "more bins for 3D Naive than Extreme Point"),
        tile(f"+{cc_all['ep_support_weight']:.1f}% → +{cc_all['ep_weight_support_weight']:.1f}%",
             "cost of heavy-below, just by loading heaviest first"),
        tile(f"{rec.void_median:.0%} vs {nav.void_median:.0%}",
             "median empty space: box recommendation vs naive box"),
    ])

    sec = []

    # ------------------------------------------------------------ 0. overview
    sec.append(f"""
<section id="overview">
<h2>What we compare</h2>
<p>Parcel packing asks: <em>how few boxes do we need for these items?</em> We give the
<strong>same randomly generated items</strong> (fixed seeds) to several algorithms and watch how
<strong>runtime</strong> and <strong>solution quality</strong> split apart as the number of items
<em>n</em> grows. We do it three times: 1D (sizes only), 3D (real boxes), and 3D with
real loading rules, ending with a practical question — which shipping box should one order use?</p>
{table(pd.DataFrame([
    ["Naive", "Exhaustive search (all n! orders × First Fit), Next Fit",
     "Layer stacking in arrival order, no rotation"],
    ["Better (course)", "Bitmask DP, First Fit, Best Fit, FFD",
     "Extreme Point heuristic + sort rules"],
    ["Practical", "MIP solver (OR-Tools + SCIP)", "Box recommendation from a box catalog"],
], columns=["", "1D", "3D"]))}
<p class="note">Every number on this page is generated by
<code>python -m experiments.build_site</code> from the default-mode CSVs (5 reps per setting,
60 s time limit) — the same numbers as <a href="{REPO}/blob/main/results/summary.md">summary.md</a>.</p>
</section>""")

    # ------------------------------------------------------------ 1. experiment A
    sec.append(f"""
<section id="exp-a">
<h2>1 · Exact answers: where does “try everything” give up?</h2>
<p><strong>Question.</strong> Three methods always find the optimal number of bins. How large can
<em>n</em> get before each one runs out of time? And how close does a fast greedy method (FFD) get?</p>
<ul>
<li><strong>Exhaustive search</strong> tries every one of the n! item orders and packs each with First
Fit. It is optimal because the order “items of bin 1, then bin 2, …” of an optimal packing is one of
the orders tried. No pruning — it really tries them all.</li>
<li><strong>Bitmask DP</strong> keeps, for every subset of items, the best (bins used, fill of the last
bin). That is 2<sup>n</sup> states instead of n! orders.</li>
<li><strong>MIP</strong> hands the problem to an industrial solver (SCIP) as an integer program.</li>
<li><strong>FFD</strong> (First Fit Decreasing) sorts items largest first and puts each into the first
bin with room. Not guaranteed optimal, but fast.</li>
</ul>
{figure(f"{FIG}/exp_a_runtime_{MODE}.png", "Runtime versus n for the exact methods and FFD",
        "<strong>How to read:</strong> log–log runtime per method; an ✕ on the dashed line means the "
        "method hit the 60 s limit at that n. Each panel is one item-size distribution "
        "(uniform 1–100, small 1–25, large 34–100; bin capacity 100).")}
<p><strong>Result.</strong> Exhaustive search gives up at {one_or_list(ex_gave)} (n! explodes).
The DP reaches n = {dp_max} in every distribution (about {dp_rt.min():.0f}–{dp_rt.max():.0f} s) — we
stop it there because 2<sup>24</sup> states already need about half a gigabyte of memory.
MIP gives up at n = {mip_gave.get('uniform', '-')} on uniform sizes and n = {mip_gave.get('large', '-')}
on large sizes, but proves the optimum for small items up to n = {mip_proven.get('small', '-')}
(the largest n we tried): difficulty depends on the data, not only on n. FFD stays under a
millisecond.</p>
{table(gives_up_table(a), label_col="algorithm")}
<p><strong>Cross-check.</strong> On {agree['instances']} instances (n = {agree['n_min']}–{agree['n_max']})
at least two exact methods proved the optimum; they disagreed <strong>{agree['disagreements']}</strong>
times. A single disagreement would have stopped the experiment as a bug.</p>
{figure(f"{FIG}/exp_a_ffd_ratio_{MODE}.png", "FFD bins divided by optimal bins",
        "<strong>How to read:</strong> FFD’s bins ÷ the proven optimum, median (solid) and worst (dotted). "
        "1.0 means FFD was optimal.")}
<p>FFD matched the optimum on {pct(ffd_opt_share)} of the instances where the optimum is known; its worst
case was {ffd_max:g}× optimal. The theory only promises ≤ 11/9·OPT + 6/9, so on random items FFD
does far better than its worst case — but that is a statement about <em>these</em> distributions.</p>
{table(ffd_ratio_table(a), rename={"optimal_share": "FFD optimal", "median": "median ratio",
                                     "max": "worst ratio"})}
</section>""")

    # ------------------------------------------------------------ 2. experiment B
    sec.append(f"""
<section id="exp-b">
<h2>2 · Greedy at scale: 10,000 items in milliseconds</h2>
<p><strong>Question.</strong> For large n no exact method finishes. How good are the greedy
heuristics, and does a time-limited MIP still help?</p>
<ul>
<li><strong>Next Fit</strong> keeps one open bin (≤ 2 × optimal). <strong>First Fit</strong> /
<strong>Best Fit</strong> try all open bins (≤ 1.7 × optimal). <strong>FFD</strong> sorts first
(≤ 11/9 × optimal + 6/9).</li>
<li>Quality is measured against the lower bound L = ⌈total size ÷ capacity⌉ (no packing can beat it),
so 1.00 = provably optimal.</li>
<li>MIP gets 10 s per run and is not run above n = 1,000 (its model has n × bins variables).</li>
</ul>
{figure(f"{FIG}/exp_b_bins_over_lb_{MODE}.png", "Bins over lower bound versus n",
        "<strong>How to read:</strong> median bins ÷ lower bound; lower is better, 1.0 is optimal.")}
{figure(f"{FIG}/exp_b_runtime_{MODE}.png", "Runtime versus n for heuristics",
        "<strong>How to read:</strong> median runtime, log–log.")}
<p><strong>Result.</strong> At n = {int(bt.n.max()):,} FFD needs
{", ".join(f"{r.bins_over_L:.3f}× L ({r.dist})" for r in ffd_big.itertuples())}, in about
{ffd_big.runtime_s.max() * 1000:.0f} ms. Next Fit is clearly worse; First Fit and Best Fit sit in between.
The MIP solves small cases{f", but within {cfg.B_MIP_TIME_LIMIT_S[MODE]:g} s it finds no answer at all from n = {mip_b_fail} on uniform items" if mip_b_fail else ""} —
so at scale the heuristics win on both time and quality.</p>
<h3>Largest n</h3>
{table(big[["dist", "algorithm", "bins_over_L", "runtime_s"]], label_col="algorithm",
       rename={"bins_over_L": "bins / L", "runtime_s": "runtime (s)"})}
<h3>MIP with a 10 s limit</h3>
{table(mip_rows[["dist", "n", "status", "bins_over_L", "runtime_s"]],
       rename={"bins_over_L": "bins / L", "runtime_s": "runtime (s)"})}
<p class="note"><code>feasible</code> = answer found but not proven optimal; <code>timeout</code> = no
answer within the limit. Our MIP is the textbook assignment model, which is weak; stronger
formulations (arc-flow, column generation) scale much further.</p>
</section>""")

    # ------------------------------------------------------------ 3. experiment C: 3D
    sec.append(f"""
<section id="exp-c">
<h2>3 · 3D: real boxes</h2>
<p><strong>Question.</strong> Items now have width, depth and height. How much does a smarter
placement rule save over simply stacking items as they arrive?</p>
<ul>
<li><strong>3D Naive</strong> fills a row along x, then a new row behind it, then a new layer on top
(as tall as the tallest item in the layer), then a new bin. It never goes back to fill gaps and
never rotates items.</li>
<li><strong>Extreme Point (EP)</strong> sorts items (by volume, height or base area) and keeps a list of
candidate corners in every open bin. Each item goes to the lowest, back-most corner where it fits,
trying all 6 rotations. It goes back to fill gaps.</li>
<li>Container 100×100×100, item sides 5–50, four item shapes: uniform, flat, long, mixed.</li>
</ul>
{viewer(f"{VIEW}/anim_naive_vs_ep_{MODE}.html", "Animation: same 60 items, two recipes",
        "Press <strong>▶ Play</strong>. Items drop in the order each algorithm places them "
        "(Naive: arrival order; EP: largest first). Colour = weight. Drag to rotate, scroll to zoom.",
        height=ANIM)}
{figure(f"{FIG}/exp_c_bins_over_lb_{MODE}.png", "3D bins over lower bound",
        "<strong>How to read:</strong> median bins ÷ volume lower bound; lower is better.")}
<p><strong>Result.</strong> Over all {int(rot[(rot.variant == 'naive') & (rot.dist == 'all')].instances.iloc[0])}
instances, 3D Naive used <strong>+{naive_all:.0f}%</strong> more bins than EP. Is that just rotation?
Running the same EP <em>without</em> rotation costs only +{norot_all:.1f}% — so most of the gap is the
algorithm (going back to fill gaps), not rotation. The three EP sort rules (volume, height, base
area) differ by only {rule_spread:.1f}% in total bins.</p>
{table(rot, label_col="variant", rename={"variant": "compared with EP (rotation on)",
                                          "increase_pct": "extra bins %",
                                          "share_needing_more_bins": "instances with more bins"})}
<h3>Largest n = {nmax}</h3>
{table(c_big, label_col="algorithm", rename={"bins_over_L": "bins / L", "fill_rate": "fill rate",
                                             "runtime_s": "runtime (s)"})}
{viewer(f"{VIEW}/exp_c_naive_vs_ep_{MODE}.html", "3D viewer: 100 items, every bin",
        "Final packings of the same 100 items (all bins shown, four per row). Hover an item to see its "
        "size and weight.")}
{figure(f"{FIG}/exp_c_runtime_{MODE}.png", "3D runtime",
        "<strong>How to read:</strong> median runtime, log–log. EP is much slower than Naive because it "
        f"checks many candidate positions: up to {ep_rt_max:.1f} s (median) at n = {nmax} in pure "
        "Python, versus well under a millisecond for Naive.")}
</section>""")

    # ------------------------------------------------------------ 4. loading rules
    s70 = sens_all.set_index("variant").increase_pct
    sec.append(f"""
<section id="loading">
<h2>4 · From packing to loading: rules cost boxes</h2>
<p><strong>Question.</strong> Real loading has rules. What does obeying them cost?</p>
<ul>
<li><strong>Support</strong>: an item above the floor needs at least
{cfg.C3_SUPPORT_RATIO:.0%} of its bottom resting on other items — nothing hangs in the air.</li>
<li><strong>Heavy-below</strong>: an item may only rest on items at least as heavy. This is our
simplified stand-in for <em>load-bearing</em> limits used in practice (how much weight a box can carry),
see Bortfeldt &amp; Wäscher (2013).</li>
<li><strong>Heaviest first</strong>: same two rules, but items are sorted by weight instead of volume,
so heavy items take the floor before light ones.</li>
</ul>
{figure(f"{FIG}/exp_c_constraint_cost_{MODE}.png", "Extra bins caused by loading constraints",
        "<strong>How to read:</strong> extra bins compared with EP without rules, on the same instances "
        "(sum of bins with ÷ sum without − 1).")}
<p><strong>Result.</strong> Support alone costs <strong>+{cc_all['ep_support']:.1f}%</strong> bins.
Adding heavy-below raises it to <strong>+{cc_all['ep_support_weight']:.1f}%</strong>. Simply loading
the heaviest items first, with exactly the same rules, brings it down to
<strong>+{cc_all['ep_weight_support_weight']:.1f}%</strong>{" — lower in every item shape" if wf_always_lower else ""}.
Support hurts {worst_support} items most; heavy-below hurts {worst_heavy} items most.</p>
{table(cc, label_col="variant", rename={"variant": "rules", "increase_pct": "extra bins %",
                                         "share_needing_more_bins": "instances with more bins"})}
{viewer(f"{VIEW}/anim_constraints_{MODE}.html", "Animation: no rules vs heaviest first + rules",
        "Colour = weight (dark = heavy). On the right, no item ever rests on a lighter one and "
        "nothing overhangs by more than 30%.", height=ANIM)}
<h3>Is 70% a magic number?</h3>
<p>No — it is our assumption, so we also ran 50% and 90% on the same instances. The cost grows
steadily: +{s70.get('ep_support_50', float('nan')):.1f}% at 50%, +{s70.get('ep_support', float('nan')):.1f}% at
70%, +{s70.get('ep_support_90', float('nan')):.1f}% at 90%.</p>
{table(sens_all, label_col="variant", rename={"variant": "support threshold", "increase_pct": "extra bins %",
                                                "share_needing_more_bins": "instances with more bins"})}
{viewer(f"{VIEW}/exp_c_constraints_{MODE}.html", "3D viewer: rules on / off (100 items)",
        "Four final packings of the same items: no rules, support, support + heavy-below, "
        "and the same rules loaded heaviest first.", height=TWO_ROWS)}
</section>""")

    # ------------------------------------------------------------ 5. box choice
    sec.append(f"""
<section id="boxes">
<h2>5 · Practical: which box should this order go in?</h2>
<p><strong>Question.</strong> An online order of {cfg.ORDER_ITEMS[0]}–{cfg.ORDER_ITEMS[1]} items arrives;
we have {len(cfg.BOX_CATALOG)} box sizes. Too big a box wastes material — Korean rules on excessive
packaging aim for at most {cfg.VOID_LIMIT:.0%} empty space.</p>
<ul>
<li><strong>Naive box choice</strong>: the smallest box with enough total volume, stacked in arrival
order without rotation; if it does not fit, try the next box.</li>
<li><strong>Box recommendation</strong>: try boxes from small to large; in each, run EP with all three sort
rules and rotation (a “multi-start”); take the first box that holds the whole order.</li>
<li>Inspired by the idea behind CJ Logistics’ LoIS O’Pack; our items and catalog are synthetic, so our
numbers are <em>not</em> comparable with theirs.</li>
</ul>
{figure(f"{FIG}/exp_c_void_hist_{MODE}.png", "Void ratio histogram",
        "<strong>How to read:</strong> how empty the chosen box(es) are for each of "
        f"{int(rec.orders)} orders; left of the dashed line meets the {cfg.VOID_LIMIT:.0%} rule.")}
<p><strong>Result.</strong> The recommendation leaves a median of <strong>{rec.void_median:.0%}</strong>
empty space (naive: {nav.void_median:.0%}) and meets the {cfg.VOID_LIMIT:.0%} rule for
<strong>{rec.share_void_le_50}</strong> of orders (naive: {nav.share_void_le_50}). It takes about
{rec.runtime_ms_median:.1f} ms per order including all attempts. The naive rule often fails even in the
largest box and has to split the order ({nav.share_split} of orders).</p>
{table(bx, label_col="algorithm", rename={"void_median": "median void", "void_mean": "mean void",
                                            "share_void_le_50": f"void ≤ {cfg.VOID_LIMIT:.0%}",
                                            "share_split": "split into >1 box",
                                            "runtime_ms_median": "ms per order",
                                            "tries_mean": "packing attempts"})}
{viewer(f"{VIEW}/exp_c_boxes_{MODE}.html", "3D viewer: two orders, naive vs recommended box",
        "Two orders where the recommendation chose a smaller box (one order per row). Panel titles show "
        "box size and void ratio.", height=TWO_ROWS)}
</section>""")

    # ------------------------------------------------------------ 6. method
    sec.append(f"""
<section id="method">
<h2>How we measured</h2>
<ul>
<li>Same instance for every algorithm: items come from a fixed seed per (distribution, n, repetition).</li>
<li>5 repetitions per setting; we report medians. Time limit 60 s per run; if any repetition times out,
that n counts as “gave up” and larger n are skipped.</li>
<li>Runtime covers the algorithm call only (<code>time.perf_counter</code>). Exhaustive search and DP run in
a separate process that is killed at the limit. MIP time includes building the model; box
recommendation time includes all attempts.</li>
<li>Every answer is checked: each item exactly once, no overflow / overlap / item outside the box,
and no rule violations when rules are on.</li>
<li>All algorithms are pure Python except the MIP solver (C++).</li>
</ul>
<h3>Limitations</h3>
<ul>
<li>Random, synthetic items; real parcels are more regular.</li>
<li>Extreme Point is a simplified version of Crainic, Perboli &amp; Tadei (2008).</li>
<li>No load-bearing strength, centre of gravity, fragility or delivery-order rules.</li>
</ul>
<p class="note">Code, tests and raw CSVs: <a href="{REPO}">{REPO}</a>. Parts of the code and text were
written with the help of Claude (Anthropic); the team reviewed everything, and every number here was
produced by the code in the repository.</p>
</section>""")

    nav_links = "".join(f'<a href="#{i}">{t}</a>' for i, t in [
        ("exp-a", "Exact"), ("exp-b", "Greedy at scale"), ("exp-c", "3D"),
        ("loading", "Loading rules"), ("boxes", "Box choice"), ("method", "Method")])

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>From Packing to Loading — Group A1</title>
<meta name="description" content="Naive vs better vs practical bin packing: measured results, 1D to 3D with loading rules.">
<style>
:root {{
  --bg: #fbfbfa; --fg: #1c1d1f; --muted: #5d6168; --line: #e3e4e6; --card: #ffffff;
  --accent: #1f6feb; --accent-soft: #e8f0fe; --code: #f1f2f4;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg: #111214; --fg: #e8e9eb; --muted: #a0a4ab; --line: #2a2c30; --card: #18191c;
          --accent: #6ea8ff; --accent-soft: #1b2738; --code: #222428; }}
  figure img {{ background: #fff; }}
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{ margin: 0; background: var(--bg); color: var(--fg);
       font: 16px/1.65 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }}
header {{ padding: 56px 16px 28px; border-bottom: 1px solid var(--line); }}
.wrap {{ max-width: 980px; margin: 0 auto; }}
h1 {{ font-size: clamp(28px, 4.5vw, 42px); line-height: 1.15; margin: 0 0 10px; letter-spacing: -0.02em; }}
.sub {{ color: var(--muted); margin: 0 0 4px; }}
nav {{ position: sticky; top: 0; z-index: 5; background: var(--bg); border-bottom: 1px solid var(--line);
      overflow-x: auto; white-space: nowrap; }}
nav .wrap {{ display: flex; gap: 18px; padding: 10px 16px; }}
nav a {{ color: var(--muted); text-decoration: none; font-size: 14px; }}
nav a:hover {{ color: var(--accent); }}
main {{ padding: 0 16px 64px; }}
section {{ padding-top: 44px; }}
h2 {{ font-size: 26px; letter-spacing: -0.01em; margin: 0 0 12px; }}
h3 {{ font-size: 17px; margin: 26px 0 8px; }}
p, li {{ max-width: 76ch; }}
a {{ color: var(--accent); }}
code {{ background: var(--code); padding: 1px 5px; border-radius: 4px; font-size: 0.92em; }}
.note {{ color: var(--muted); font-size: 14px; }}
.tiles {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-top: 26px; }}
.tile {{ background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 14px; }}
.tile .v {{ font-size: 22px; font-weight: 650; letter-spacing: -0.01em; }}
.tile .l {{ color: var(--muted); font-size: 13px; line-height: 1.4; margin-top: 4px; }}
figure {{ margin: 22px 0; }}
figure img {{ width: 100%; height: auto; border: 1px solid var(--line); border-radius: 8px; display: block; }}
figcaption {{ color: var(--muted); font-size: 14px; margin-top: 8px; max-width: 76ch; }}
.viewer iframe {{ width: 100%; border: 1px solid var(--line); border-radius: 0 0 8px 8px; background: #fff; display: block; }}
.vhead {{ display: flex; justify-content: space-between; gap: 12px; align-items: center;
         background: var(--accent-soft); border: 1px solid var(--line); border-bottom: 0;
         border-radius: 8px 8px 0 0; padding: 8px 12px; font-size: 14px; font-weight: 600; }}
.vhead a {{ font-weight: 500; white-space: nowrap; }}
.tw {{ overflow-x: auto; margin: 14px 0; border: 1px solid var(--line); border-radius: 8px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 14px; background: var(--card); }}
th, td {{ padding: 7px 10px; text-align: left; border-bottom: 1px solid var(--line); white-space: nowrap; }}
th {{ font-weight: 600; color: var(--muted); }}
tbody tr:last-child td {{ border-bottom: 0; }}
footer {{ border-top: 1px solid var(--line); padding: 20px 16px; color: var(--muted); font-size: 13px; }}
@media (max-width: 640px) {{ .viewer iframe {{ height: 420px !important; }} }}
</style>
</head>
<body>
<header><div class="wrap">
<p class="sub">DCCS309 Algorithms · Group A1 · 전재형, 정진형, 박은혁</p>
<h1>From Packing to Loading</h1>
<p class="sub">Naive vs better vs practical bin packing — what actually changes as the problem grows.</p>
<div class="tiles">{tiles}</div>
</div></header>
<nav><div class="wrap">{nav_links}<a href="{REPO}">GitHub ↗</a></div></nav>
<main><div class="wrap">
{"".join(sec)}
</div></main>
<footer><div class="wrap">Generated {date.today()} from default-mode results ·
<a href="{REPO}/blob/main/results/summary.md">summary.md</a> · <a href="{REPO}">source</a></div></footer>
</body>
</html>
"""


def main() -> None:
    out = ROOT / "index.html"
    out.write_text(build(), encoding="utf-8")
    (ROOT / ".nojekyll").touch()  # serve files as-is on GitHub Pages
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
