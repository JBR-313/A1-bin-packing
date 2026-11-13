# Results summary (auto-generated — do not edit by hand)

Generated 2026-11-13 by `python -m experiments.summary`.

> **Warning:** contains `quick`-mode numbers (2 reps, 5 s limit). Do not put these in slides.

## Experiment A — exact vs greedy (`quick` mode)

### Where each method gives up

| algorithm | dist | largest n proven optimal | largest n with an answer | gave up at n | median runtime at that largest n (s) |
|---|---|---|---|---|---|
| exhaustive | uniform | 10 | 10 | 11 | 4.4974 |
| dp | uniform | 21 | 21 | 22 | 3.3849 |
| mip | uniform | 24 | 50 | 100 | 4.7376 |
| ffd | uniform | - | 200 | - | 0.0003 |
| exhaustive | small | 10 | 10 | 11 | 3.7811 |
| dp | small | 21 | 21 | 22 | 3.3946 |
| mip | small | 200 | 200 | - | 0.3618 |
| ffd | small | - | 200 | - | 0.0003 |
| exhaustive | large | 9 | 9 | 10 | 0.4449 |
| dp | large | 21 | 21 | 22 | 3.4637 |
| mip | large | 50 | 50 | 100 | 2.7082 |
| ffd | large | - | 200 | - | 0.0003 |

### Do the exact methods agree?

Instances solved to proven optimality by 2+ exact methods: **106**, disagreements: **0** (n range 4–21).

### FFD / OPT (instances where OPT is known)

| dist | instances | optimal_share | median | max |
|---|---|---|---|---|
| large | 43 | 100.0% | 1.0 | 1.0 |
| small | 52 | 100.0% | 1.0 | 1.0 |
| uniform | 39 | 97.4% | 1.0 | 1.1 |

## Experiment B — heuristics at scale (`quick` mode)

Median over reps. `bins/L` = bins used / lower bound ceil(sum/C).

| dist | algorithm | n | status | bins_over_L | runtime_s |
|---|---|---|---|---|---|
| uniform | next_fit | 10 | ok | 1.2429 | 0.0 |
| uniform | next_fit | 100 | ok | 1.3558 | 0.0 |
| uniform | next_fit | 1000 | ok | 1.3237 | 0.0002 |
| uniform | next_fit | 10000 | ok | 1.3232 | 0.0021 |
| uniform | first_fit | 10 | ok | 1.1714 | 0.0 |
| uniform | first_fit | 100 | ok | 1.0712 | 0.0001 |
| uniform | first_fit | 1000 | ok | 1.0487 | 0.0019 |
| uniform | first_fit | 10000 | ok | 1.026 | 0.042 |
| uniform | best_fit | 10 | ok | 1.1714 | 0.0 |
| uniform | best_fit | 100 | ok | 1.0612 | 0.0 |
| uniform | best_fit | 1000 | ok | 1.0338 | 0.0005 |
| uniform | best_fit | 10000 | ok | 1.0162 | 0.0087 |
| uniform | ffd | 10 | ok | 1.0714 | 0.0 |
| uniform | ffd | 100 | ok | 1.0308 | 0.0001 |
| uniform | ffd | 1000 | ok | 1.0099 | 0.002 |
| uniform | ffd | 10000 | ok | 1.0091 | 0.0304 |
| uniform | mip | 10 | ok | 1.0714 | 0.0127 |
| uniform | mip | 100 | timeout |  | 5.0655 |
| small | next_fit | 10 | ok | 1.0 | 0.0 |
| small | next_fit | 100 | ok | 1.0801 | 0.0 |
| small | next_fit | 1000 | ok | 1.0811 | 0.0001 |
| small | next_fit | 10000 | ok | 1.0875 | 0.0009 |
| small | first_fit | 10 | ok | 1.0 | 0.0 |
| small | first_fit | 100 | ok | 1.0 | 0.0001 |
| small | first_fit | 1000 | ok | 1.0039 | 0.0018 |
| small | first_fit | 10000 | ok | 1.0 | 0.0291 |
| small | best_fit | 10 | ok | 1.0 | 0.0 |
| small | best_fit | 100 | ok | 1.0 | 0.0 |
| small | best_fit | 1000 | ok | 1.0039 | 0.0003 |
| small | best_fit | 10000 | ok | 1.0004 | 0.0046 |
| small | ffd | 10 | ok | 1.0 | 0.0 |
| small | ffd | 100 | ok | 1.0 | 0.0001 |
| small | ffd | 1000 | ok | 1.0 | 0.0019 |
| small | ffd | 10000 | ok | 1.0 | 0.0291 |
| small | mip | 10 | ok | 1.0 | 0.0035 |
| small | mip | 100 | ok | 1.0 | 0.0609 |
| small | mip | 1000 | timeout |  | 6.2465 |
| large | next_fit | 10 | ok | 1.375 | 0.0 |
| large | next_fit | 100 | ok | 1.3451 | 0.0 |
| large | next_fit | 1000 | ok | 1.3586 | 0.0001 |
| large | next_fit | 10000 | ok | 1.3534 | 0.0143 |
| large | first_fit | 10 | ok | 1.2292 | 0.0 |
| large | first_fit | 100 | ok | 1.1982 | 0.0001 |
| large | first_fit | 1000 | ok | 1.1585 | 0.0018 |
| large | first_fit | 10000 | ok | 1.1353 | 0.0271 |
| large | best_fit | 10 | ok | 1.2292 | 0.0 |
| large | best_fit | 100 | ok | 1.191 | 0.0 |
| large | best_fit | 1000 | ok | 1.1495 | 0.0005 |
| large | best_fit | 10000 | ok | 1.1316 | 0.0091 |
| large | ffd | 10 | ok | 1.1458 | 0.0 |
| large | ffd | 100 | ok | 1.1614 | 0.0001 |
| large | ffd | 1000 | ok | 1.1398 | 0.0022 |
| large | ffd | 10000 | ok | 1.1275 | 0.0292 |
| large | mip | 10 | ok | 1.1458 | 0.0121 |
| large | mip | 100 | timeout |  | 5.0952 |
