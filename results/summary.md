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
| large | 43 | 100.0% | 1 | 1 |
| small | 52 | 100.0% | 1 | 1 |
| uniform | 39 | 97.4% | 1 | 1.1 |

## Experiment B — heuristics at scale (`quick` mode)

Median over reps. `bins/L` = bins used / lower bound ceil(sum/C).

| dist | algorithm | n | status | bins_over_L | runtime_s |
|---|---|---|---|---|---|
| uniform | next_fit | 10 | ok | 1.2429 | 0.000005 |
| uniform | next_fit | 100 | ok | 1.3558 | 0.000025 |
| uniform | next_fit | 1000 | ok | 1.3237 | 0.000171 |
| uniform | next_fit | 10000 | ok | 1.3232 | 0.002082 |
| uniform | first_fit | 10 | ok | 1.1714 | 0.00002 |
| uniform | first_fit | 100 | ok | 1.0712 | 0.000129 |
| uniform | first_fit | 1000 | ok | 1.0487 | 0.001856 |
| uniform | first_fit | 10000 | ok | 1.026 | 0.042011 |
| uniform | best_fit | 10 | ok | 1.1714 | 0.00001 |
| uniform | best_fit | 100 | ok | 1.0612 | 0.000035 |
| uniform | best_fit | 1000 | ok | 1.0338 | 0.000519 |
| uniform | best_fit | 10000 | ok | 1.0162 | 0.008696 |
| uniform | ffd | 10 | ok | 1.0714 | 0.000018 |
| uniform | ffd | 100 | ok | 1.0308 | 0.000135 |
| uniform | ffd | 1000 | ok | 1.0099 | 0.001988 |
| uniform | ffd | 10000 | ok | 1.0091 | 0.030402 |
| uniform | mip | 10 | ok | 1.0714 | 0.012681 |
| uniform | mip | 100 | timeout |  | 5.065509 |
| small | next_fit | 10 | ok | 1 | 0.000007 |
| small | next_fit | 100 | ok | 1.0801 | 0.000015 |
| small | next_fit | 1000 | ok | 1.0811 | 0.000065 |
| small | next_fit | 10000 | ok | 1.0875 | 0.000857 |
| small | first_fit | 10 | ok | 1 | 0.000018 |
| small | first_fit | 100 | ok | 1 | 0.000132 |
| small | first_fit | 1000 | ok | 1.0039 | 0.001764 |
| small | first_fit | 10000 | ok | 1 | 0.029124 |
| small | best_fit | 10 | ok | 1 | 0.000014 |
| small | best_fit | 100 | ok | 1 | 0.000025 |
| small | best_fit | 1000 | ok | 1.0039 | 0.000287 |
| small | best_fit | 10000 | ok | 1.0004 | 0.004564 |
| small | ffd | 10 | ok | 1 | 0.000029 |
| small | ffd | 100 | ok | 1 | 0.000134 |
| small | ffd | 1000 | ok | 1 | 0.001937 |
| small | ffd | 10000 | ok | 1 | 0.029059 |
| small | mip | 10 | ok | 1 | 0.003548 |
| small | mip | 100 | ok | 1 | 0.060881 |
| small | mip | 1000 | timeout |  | 6.24645 |
| large | next_fit | 10 | ok | 1.375 | 0.000004 |
| large | next_fit | 100 | ok | 1.3451 | 0.000011 |
| large | next_fit | 1000 | ok | 1.3586 | 0.000104 |
| large | next_fit | 10000 | ok | 1.3534 | 0.01433 |
| large | first_fit | 10 | ok | 1.2292 | 0.000014 |
| large | first_fit | 100 | ok | 1.1982 | 0.000128 |
| large | first_fit | 1000 | ok | 1.1585 | 0.001834 |
| large | first_fit | 10000 | ok | 1.1353 | 0.02705 |
| large | best_fit | 10 | ok | 1.2292 | 0.000023 |
| large | best_fit | 100 | ok | 1.191 | 0.000033 |
| large | best_fit | 1000 | ok | 1.1495 | 0.000514 |
| large | best_fit | 10000 | ok | 1.1316 | 0.009064 |
| large | ffd | 10 | ok | 1.1458 | 0.000017 |
| large | ffd | 100 | ok | 1.1614 | 0.00014 |
| large | ffd | 1000 | ok | 1.1398 | 0.002227 |
| large | ffd | 10000 | ok | 1.1275 | 0.029207 |
| large | mip | 10 | ok | 1.1458 | 0.01206 |
| large | mip | 100 | timeout |  | 5.095159 |

## Experiment C — 3D packing and loading (`quick` mode)

### Bins, fill rate and runtime per n

Container (100, 100, 100), item sides (5, 50), median over reps. `fill_rate` = item volume / (bins × container volume). Naive never rotates; all EP variants allow rotation.

| dist | algorithm | n | status | bins | L | bins_over_L | fill_rate | runtime_s |
|---|---|---|---|---|---|---|---|---|
| uniform | naive | 20 | ok | 2 | 1 | 2 | 0.226 | 0.00005 |
| uniform | naive | 50 | ok | 4 | 1 | 4 | 0.208 | 0.000081 |
| uniform | naive | 100 | ok | 7.5 | 3 | 2.5 | 0.285 | 0.000152 |
| uniform | naive | 200 | ok | 15 | 4.5 | 3.35 | 0.267 | 0.000472 |
| uniform | ep_volume | 20 | ok | 1 | 1 | 1 | 0.453 | 0.002259 |
| uniform | ep_volume | 50 | ok | 1.5 | 1 | 1.5 | 0.615 | 0.0202 |
| uniform | ep_volume | 100 | ok | 3 | 3 | 1 | 0.711 | 0.047066 |
| uniform | ep_volume | 200 | ok | 5 | 4.5 | 1.125 | 0.8 | 0.163948 |
| uniform | ep_height | 20 | ok | 1 | 1 | 1 | 0.453 | 0.002474 |
| uniform | ep_height | 50 | ok | 2 | 1 | 2 | 0.416 | 0.020773 |
| uniform | ep_height | 100 | ok | 3 | 3 | 1 | 0.711 | 0.054069 |
| uniform | ep_height | 200 | ok | 5.5 | 4.5 | 1.225 | 0.73 | 0.201196 |
| uniform | ep_area | 20 | ok | 1 | 1 | 1 | 0.453 | 0.002399 |
| uniform | ep_area | 50 | ok | 1.5 | 1 | 1.5 | 0.615 | 0.019734 |
| uniform | ep_area | 100 | ok | 3 | 3 | 1 | 0.711 | 0.042473 |
| uniform | ep_area | 200 | ok | 5 | 4.5 | 1.125 | 0.8 | 0.157143 |
| uniform | ep_support | 20 | ok | 1 | 1 | 1 | 0.453 | 0.00279 |
| uniform | ep_support | 50 | ok | 2 | 1 | 2 | 0.416 | 0.025014 |
| uniform | ep_support | 100 | ok | 3 | 3 | 1 | 0.711 | 0.046857 |
| uniform | ep_support | 200 | ok | 5 | 4.5 | 1.125 | 0.8 | 0.184887 |
| uniform | ep_support_weight | 20 | ok | 1.5 | 1 | 1.5 | 0.326 | 0.004214 |
| uniform | ep_support_weight | 50 | ok | 2 | 1 | 2 | 0.416 | 0.030444 |
| uniform | ep_support_weight | 100 | ok | 4 | 3 | 1.333 | 0.533 | 0.05854 |
| uniform | ep_support_weight | 200 | ok | 6 | 4.5 | 1.35 | 0.667 | 0.233071 |
| flat | naive | 20 | ok | 1 | 1 | 1 | 0.257 | 0.000065 |
| flat | naive | 50 | ok | 2 | 1 | 2 | 0.319 | 0.000073 |
| flat | naive | 100 | ok | 4 | 2 | 2 | 0.363 | 0.000155 |
| flat | naive | 200 | ok | 7 | 3 | 2.333 | 0.409 | 0.00042 |
| flat | ep_volume | 20 | ok | 1 | 1 | 1 | 0.257 | 0.00199 |
| flat | ep_volume | 50 | ok | 1 | 1 | 1 | 0.638 | 0.031178 |
| flat | ep_volume | 100 | ok | 2 | 2 | 1 | 0.725 | 0.105125 |
| flat | ep_volume | 200 | ok | 4 | 3 | 1.333 | 0.716 | 0.385076 |
| flat | ep_height | 20 | ok | 1 | 1 | 1 | 0.257 | 0.002496 |
| flat | ep_height | 50 | ok | 1.5 | 1 | 1.5 | 0.468 | 0.024455 |
| flat | ep_height | 100 | ok | 2 | 2 | 1 | 0.725 | 0.075135 |
| flat | ep_height | 200 | ok | 4 | 3 | 1.333 | 0.716 | 0.25328 |
| flat | ep_area | 20 | ok | 1 | 1 | 1 | 0.257 | 0.002024 |
| flat | ep_area | 50 | ok | 1 | 1 | 1 | 0.638 | 0.02533 |
| flat | ep_area | 100 | ok | 2 | 2 | 1 | 0.725 | 0.093783 |
| flat | ep_area | 200 | ok | 4 | 3 | 1.333 | 0.716 | 0.380574 |
| flat | ep_support | 20 | ok | 1 | 1 | 1 | 0.257 | 0.001986 |
| flat | ep_support | 50 | ok | 1.5 | 1 | 1.5 | 0.468 | 0.035267 |
| flat | ep_support | 100 | ok | 3 | 2 | 1.5 | 0.483 | 0.107307 |
| flat | ep_support | 200 | ok | 4 | 3 | 1.333 | 0.716 | 0.331863 |
| flat | ep_support_weight | 20 | ok | 1.5 | 1 | 1.5 | 0.187 | 0.002577 |
| flat | ep_support_weight | 50 | ok | 2.5 | 1 | 2.5 | 0.262 | 0.020548 |
| flat | ep_support_weight | 100 | ok | 3 | 2 | 1.5 | 0.483 | 0.10405 |
| flat | ep_support_weight | 200 | ok | 5 | 3 | 1.667 | 0.573 | 0.376512 |
| long | naive | 20 | ok | 1 | 1 | 1 | 0.089 | 0.000036 |
| long | naive | 50 | ok | 2.5 | 1 | 2.5 | 0.087 | 0.000096 |
| long | naive | 100 | ok | 4 | 1 | 4 | 0.104 | 0.000179 |
| long | naive | 200 | ok | 9 | 1 | 9 | 0.101 | 0.000306 |
| long | ep_volume | 20 | ok | 1 | 1 | 1 | 0.089 | 0.002185 |
| long | ep_volume | 50 | ok | 1 | 1 | 1 | 0.209 | 0.019552 |
| long | ep_volume | 100 | ok | 1 | 1 | 1 | 0.418 | 0.114463 |
| long | ep_volume | 200 | ok | 2 | 1 | 2 | 0.456 | 0.763675 |
| long | ep_height | 20 | ok | 1 | 1 | 1 | 0.089 | 0.002186 |
| long | ep_height | 50 | ok | 1 | 1 | 1 | 0.209 | 0.017719 |
| long | ep_height | 100 | ok | 1 | 1 | 1 | 0.418 | 0.120452 |
| long | ep_height | 200 | ok | 2 | 1 | 2 | 0.456 | 0.987926 |
| long | ep_area | 20 | ok | 1 | 1 | 1 | 0.089 | 0.001975 |
| long | ep_area | 50 | ok | 1 | 1 | 1 | 0.209 | 0.016165 |
| long | ep_area | 100 | ok | 1 | 1 | 1 | 0.418 | 0.110755 |
| long | ep_area | 200 | ok | 2 | 1 | 2 | 0.456 | 0.819315 |
| long | ep_support | 20 | ok | 1 | 1 | 1 | 0.089 | 0.002065 |
| long | ep_support | 50 | ok | 1 | 1 | 1 | 0.209 | 0.01736 |
| long | ep_support | 100 | ok | 1 | 1 | 1 | 0.418 | 0.119274 |
| long | ep_support | 200 | ok | 2 | 1 | 2 | 0.456 | 0.739469 |
| long | ep_support_weight | 20 | ok | 1 | 1 | 1 | 0.089 | 0.00179 |
| long | ep_support_weight | 50 | ok | 1.5 | 1 | 1.5 | 0.156 | 0.022922 |
| long | ep_support_weight | 100 | ok | 2 | 1 | 2 | 0.209 | 0.171183 |
| long | ep_support_weight | 200 | ok | 2 | 1 | 2 | 0.456 | 0.739782 |
| mixed | naive | 20 | ok | 2 | 1 | 2 | 0.139 | 0.000048 |
| mixed | naive | 50 | ok | 3.5 | 1 | 3.5 | 0.176 | 0.000084 |
| mixed | naive | 100 | ok | 7 | 2 | 3.5 | 0.177 | 0.0002 |
| mixed | naive | 200 | ok | 14.5 | 3 | 4.833 | 0.18 | 0.000372 |
| mixed | ep_volume | 20 | ok | 1 | 1 | 1 | 0.278 | 0.002159 |
| mixed | ep_volume | 50 | ok | 1 | 1 | 1 | 0.614 | 0.025167 |
| mixed | ep_volume | 100 | ok | 2 | 2 | 1 | 0.621 | 0.059809 |
| mixed | ep_volume | 200 | ok | 3.5 | 3 | 1.167 | 0.754 | 0.256493 |
| mixed | ep_height | 20 | ok | 1 | 1 | 1 | 0.278 | 0.001983 |
| mixed | ep_height | 50 | ok | 1 | 1 | 1 | 0.614 | 0.021261 |
| mixed | ep_height | 100 | ok | 2 | 2 | 1 | 0.621 | 0.08177 |
| mixed | ep_height | 200 | ok | 3.5 | 3 | 1.167 | 0.754 | 0.308419 |
| mixed | ep_area | 20 | ok | 1 | 1 | 1 | 0.278 | 0.002191 |
| mixed | ep_area | 50 | ok | 1 | 1 | 1 | 0.614 | 0.023284 |
| mixed | ep_area | 100 | ok | 2 | 2 | 1 | 0.621 | 0.075416 |
| mixed | ep_area | 200 | ok | 3.5 | 3 | 1.167 | 0.754 | 0.242485 |
| mixed | ep_support | 20 | ok | 1 | 1 | 1 | 0.278 | 0.002031 |
| mixed | ep_support | 50 | ok | 1 | 1 | 1 | 0.614 | 0.020272 |
| mixed | ep_support | 100 | ok | 2 | 2 | 1 | 0.621 | 0.061118 |
| mixed | ep_support | 200 | ok | 4 | 3 | 1.333 | 0.653 | 0.282978 |
| mixed | ep_support_weight | 20 | ok | 1 | 1 | 1 | 0.278 | 0.002416 |
| mixed | ep_support_weight | 50 | ok | 2 | 1 | 2 | 0.307 | 0.026009 |
| mixed | ep_support_weight | 100 | ok | 3 | 2 | 1.5 | 0.414 | 0.085623 |
| mixed | ep_support_weight | 200 | ok | 4 | 3 | 1.333 | 0.653 | 0.317215 |

### Cost of loading constraints

Same instances, EP sorted by volume with vs without constraints. `increase_pct` = sum(bins with) / sum(bins without) − 1 over all n and seeds. Support threshold 70% is an assumption.

| constraint | dist | instances | bins_without | bins_with | increase_pct | share_needing_more_bins |
|---|---|---|---|---|---|---|
| ep_support | flat | 8 | 16 | 19 | 18.8 | 38% |
| ep_support | long | 8 | 10 | 10 | 0 | 0% |
| ep_support | mixed | 8 | 15 | 16 | 6.7 | 12% |
| ep_support | uniform | 8 | 21 | 22 | 4.8 | 12% |
| ep_support | all | 32 | 62 | 67 | 8.1 | 16% |
| ep_support_weight | flat | 8 | 16 | 24 | 50 | 88% |
| ep_support_weight | long | 8 | 10 | 13 | 30 | 38% |
| ep_support_weight | mixed | 8 | 15 | 20 | 33.3 | 62% |
| ep_support_weight | uniform | 8 | 21 | 27 | 28.6 | 75% |
| ep_support_weight | all | 32 | 62 | 84 | 35.5 | 66% |

### Box choice per order

200 orders of 3–15 items (sides (3, 25)), catalog [(20, 15, 10), (30, 20, 15), (35, 25, 20), (40, 30, 25), (50, 40, 30), (60, 45, 40)]. void = 1 − item volume / box volume used. `share_split` = orders that needed more than one box. `tries` = packing attempts per order (multi-start cost; included in runtime).

| algorithm | orders | void_median | void_mean | share_void_le_50 | share_split | runtime_ms_median | tries_mean |
|---|---|---|---|---|---|---|---|
| box_recommend | 200 | 0.47 | 0.466 | 55.0% | 0.0% | 0.549 | 2.24 |
| box_naive | 200 | 0.867 | 0.843 | 0.5% | 27.5% | 0.078 | 2.84 |

Not comparable with CJ Logistics' published figures (different items and catalog).
