# From Packing to Loading: Naive vs Better vs Practical Bin Packing

**DCCS309 Algorithms — Group A1**: 전재형 (Jaehyeong Jeon), 정진형 (Jinhyeong Jeong), 박은혁 (Eunhyeok Park)

We solve the **same** randomly generated parcel sets with several algorithms ("recipes")
and measure how **runtime** and **solution quality** split apart as the input size *n* grows.

> Status (2026-11-13): 1D part (experiments A and B) is done. 3D (experiment C) is next.

## Algorithms

| | 1D | 3D (planned) |
|---|---|---|
| **Naive** | Exhaustive search (all n! orders × First Fit), Next Fit | Stack in arrival order, no rotation |
| **Better** (course) | Bitmask DP, First Fit, Best Fit, FFD | Extreme Point + sort rules |
| **Practical** | MIP (Google OR-Tools + SCIP) | Box recommendation (inspired by CJ Logistics LoIS O'Pack) |

Worst-case guarantees: NF ≤ 2·OPT, FF/BF ≤ 1.7·OPT, FFD ≤ 11/9·OPT + 6/9 (Dósa 2007).

## Setup

```bash
python -m venv .venv && source .venv/bin/activate   # Python 3.11+
pip install -r requirements.txt
pip install -e .
pytest                                              # all tests must pass
```

## Running experiments

```bash
python -m experiments.exp_a --quick   # pipeline check (~5 min)
python -m experiments.exp_a           # presentation numbers (5 reps, 60 s limit; ~1 h)
python -m experiments.exp_b --quick
python -m experiments.exp_b
python -m experiments.summary         # writes results/summary.md
```

| mode | reps | time limit per run |
|---|---|---|
| `--quick` | 2 | 5 s |
| default | 5 | 60 s |
| `--full` | 30 | 60 s |

Outputs: `results/csv/*.csv`, `results/figures/*.png`, `results/summary.md`.
**Numbers in slides and personal READMEs must come from `results/summary.md`.**

## Measurement rules

- Every algorithm gets the identical instance for a given (distribution, n, seed).
- Runtime is measured with `time.perf_counter()` around the algorithm call only.
  Exhaustive search and DP run in a child process that is killed at the time limit
  (process start-up is not counted).
- If any rep of (algorithm, distribution, n) times out, it is recorded as `timeout`
  and larger n are skipped for that algorithm and distribution.
- MIP runtime **includes model building** (`model_build_s` is also reported separately
  in `extra_json`). MIP is not run for n > 1000 (`skipped`): the model has
  n × (#bins) binary variables.
- Exact methods are cross-checked on every instance: if exhaustive / DP / MIP disagree,
  the experiment stops with an error.

## Assumptions

- 1D bin capacity C = 100, integer item sizes.
- Size distributions: uniform `[1, 100]`, small `[1, 25]`, large `[34, 100]`.
- Instance seed = 2025 + rep.
- (All assumptions live in `experiments/config.py`.)

## Repository layout

```
src/packing/   types, generators, bounds, oned/ (exhaustive, dp, heuristics, mip),
               bench/ (timeout, runner), viz/ (plots)
experiments/   config, exp_a, exp_b, summary
results/       csv/, figures/, summary.md
tests/         correctness tests (pytest)
```

## Use of generative AI

Parts of this code and documentation were written with the help of Claude (Anthropic).
All team members reviewed the code and can explain it; every measured number in this
repository was produced by the code here.

## References

- Google OR-Tools, Bin packing: https://developers.google.com/optimization/pack/bin_packing
- G. Dósa, "The tight bound of First Fit Decreasing bin-packing algorithm is FFD(I) ≤ 11/9 OPT(I) + 6/9", 2007.
- T. G. Crainic, G. Perboli, R. Tadei, "Extreme point-based heuristics for three-dimensional bin packing", INFORMS J. Computing, 2008.
