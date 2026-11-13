# From Packing to Loading: Naive vs Better vs Practical Bin Packing

**DCCS309 Algorithms — Group A1**: 전재형 (Jaehyeong Jeon), 정진형 (Jinhyeong Jeong), 박은혁 (Eunhyeok Park)

We solve the **same** randomly generated parcel sets with several algorithms ("recipes")
and measure how **runtime** and **solution quality** split apart as the input size *n* grows —
first for 1D bin packing, then for 3D packing with real loading rules, and finally for
choosing a shipping box per order.

## Algorithms

| | 1D | 3D |
|---|---|---|
| **Naive** | Exhaustive search (all n! orders × First Fit), Next Fit | Layer stacking in arrival order, no rotation |
| **Better** (course) | Bitmask DP, First Fit, Best Fit, FFD | Extreme Point + sort rules (volume / height / base area) |
| **Practical** | MIP (Google OR-Tools + SCIP) | Box recommendation (multi-start EP over a box catalog) |

Worst-case guarantees (1D): NF ≤ 2·OPT, FF/BF ≤ 1.7·OPT, FFD ≤ 11/9·OPT + 6/9 (Dósa 2007).

### 3D in one paragraph each

- **3D Naive** (`threed/naive.py`): fill a row along x; when the next item does not fit,
  start a new row (y); then a new layer (z, height = tallest item of the layer); then a new
  bin. Earlier bins are never revisited.
- **Extreme Point** (`threed/extreme_point.py`): sort items; each open bin keeps candidate
  points (starting at the origin). An item goes to the first bin where it fits, at the
  candidate point with the smallest (z, y, x), trying orientations lowest-height first.
  Placing an item adds its three corner points and their projections toward the walls.
- **Loading constraints** (`threed/constraints.py`, switchable):
  *support* — an item above the floor needs ≥ 70% of its bottom face resting on other items;
  *heavy-below* — an item may only rest directly on items at least as heavy (checked both
  when placing on top of items and when sliding an item under an overhang).
- **Box recommendation** (`threed/box_recommend.py`): try catalog boxes from smallest
  volume up; in each, run EP with each of the 3 sort rules (rotation allowed) and take the
  first box that holds the whole order. If no single box works, use several of the largest
  box. Baseline: smallest box with enough volume, packed with 3D Naive, next box if it fails.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate   # Python 3.11+
pip install -r requirements.txt
pip install -e .
pytest                                              # all tests must pass
```

## Running experiments

```bash
python -m experiments.exp_a --quick   # 1D exact vs greedy        (~5 min)
python -m experiments.exp_b --quick   # 1D heuristics at scale    (~20 s)
python -m experiments.exp_c --quick   # 3D packing + box choice   (~30 s)
python -m experiments.summary         # writes results/summary.md

# presentation numbers: drop --quick (exp_a takes about an hour)
```

| mode | reps | time limit per run | notes |
|---|---|---|---|
| `--quick` | 2 | 5 s | pipeline check; experiment C stops at n = 200 |
| default | 5 | 60 s | presentation numbers |
| `--full` | 30 | 60 s | if time allows |

Outputs:
- `results/csv/exp_{a,b,c}_<mode>.csv` — one row per run (columns: experiment, algorithm,
  dist, n, seed, rep, num_bins, lower_bound, opt, runtime_s, status, fill_rate, extra_json)
- `results/figures/*.png` — slide-ready plots
- `results/html/exp_c_*.html` — interactive 3D viewers (Naive vs EP, constraints on/off,
  box choice examples); open in a browser (loads plotly from a CDN)
- `results/summary.md` — **numbers in slides and personal READMEs must come from this file**

Only default-mode results are committed. `--quick` outputs (`*_quick.*`) are a local
pipeline check and are git-ignored.

## Measurement rules

- Every algorithm gets the identical instance for a given (distribution, n, seed).
- Runtime is measured with `time.perf_counter()` around the algorithm call only.
  Exhaustive search and DP run in a child process that is killed at the time limit
  (process start-up is not counted). Polynomial algorithms run in-process; a run longer
  than the limit is still recorded as `timeout`.
- If any rep of (algorithm, distribution, n) times out, it is recorded as `timeout`
  and larger n are skipped for that algorithm and distribution.
- MIP runtime **includes model building** (`model_build_s` is also reported separately
  in `extra_json`). MIP is not run for n > 1000 (`skipped`): the model has
  n × (#bins) binary variables.
- Box recommendation runtime **includes all multi-start attempts**; the number of attempts
  is reported as `tries`.
- Exact methods are cross-checked on every instance: if exhaustive / DP / MIP disagree,
  the experiment stops with an error. Every 3D answer is checked for overlaps, items
  outside the container, and (when switched on) support / heavy-below violations.

## Assumptions

All values live in `experiments/config.py`.

- 1D bin capacity C = 100, integer item sizes; distributions uniform `[1, 100]`,
  small `[1, 25]`, large `[34, 100]`.
- Instance seed = 2025 + rep.
- 3D container 100 × 100 × 100; item sides 5..50; weights 1..20 (integers, uniform).
- 3D item shapes: *uniform* (every side 5..50), *flat* (two sides 23..50, height 5..16),
  *long* (one random side 29..50, others 5..16), *mixed* (shape chosen per item).
- Rotation: 3D Naive never rotates; EP and box recommendation allow all 6 orientations.
- Support threshold 70% of the bottom face — our assumption, not an industry standard.
  Experiment C also runs 50% and 90% on the same instances (sensitivity table in summary).
- Experiment C also runs EP **without** rotation, to separate the effect of rotation from
  the effect of the algorithm when comparing with 3D Naive.
- Heavy-below checks direct contact only (not everything further below). It is a
  simplified stand-in for the **load-bearing (stacking) constraints** used in practice,
  where what matters is how much weight a box's top can carry, not whether it is heavier.
  Real loading also considers delivery order, centre of gravity and axle loads, which we
  do not model (see Bortfeldt & Wäscher 2013 for the taxonomy of practical constraints).
- Experiment C also runs the constrained EP with items sorted **heaviest first**
  (`ep_weight_support_weight`), to see whether the order alone lowers the cost of
  heavy-below (constraint cost table in summary).
- Box catalog (6 boxes): 20×15×10, 30×20×15, 35×25×20, 40×30×25, 50×40×30, 60×45×40.
- Orders: 200 orders of 3..15 items, item sides 3..25, mixed shapes.
- Over-packing threshold: void ratio ≤ 50%.

### Simplifications (3D)

- Extreme Point: candidate points are the 3 corners of each placed item plus their
  straight projections along −x, −y, −z; the paper's full projection rules and
  merit-function bin choice are not implemented. Bins are tried in order (First Fit).
- No load-bearing limits, centre-of-gravity or fragility rules beyond the two above.
- Box recommendation is *inspired by* CJ Logistics' LoIS O'Pack (press release, Jan 2024:
  ~0.04 s per order, ~36% average void). It is not their algorithm, and our numbers are
  not directly comparable (different items and catalog).

## Repository layout

```
src/packing/   types, generators, bounds,
               oned/   exhaustive, dp, heuristics, mip
               threed/ geometry, naive, extreme_point, constraints, box_recommend
               bench/  timeout, runner
               viz/    plots, view3d
experiments/   config, exp_a, exp_b, exp_c, summary
results/       csv/, figures/, html/, summary.md
tests/         correctness tests (pytest)
```

## Use of generative AI

Parts of this code and documentation were written with the help of Claude (Anthropic).
All team members reviewed the code and can explain it; every measured number in this
repository was produced by the code here.

## References

- Google OR-Tools, Bin packing: https://developers.google.com/optimization/pack/bin_packing
- G. Dósa, "The tight bound of First Fit Decreasing bin-packing algorithm is FFD(I) ≤ 11/9 OPT(I) + 6/9", 2007.
- T. G. Crainic, G. Perboli, R. Tadei, "Extreme point-based heuristics for three-dimensional bin packing", INFORMS J. Computing 20(3), 2008.
- CJ대한통운 (CJ Logistics) press release on LoIS O'Pack, January 2024.
- A. Bortfeldt, G. Wäscher, "Constraints in container loading – A state-of-the-art review", European Journal of Operational Research 229(1), 2013.
