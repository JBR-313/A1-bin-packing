# Results summary (auto-generated — do not edit by hand)

Generated 2026-11-14 by `python -m experiments.summary`.

## Experiment A — exact vs greedy (`default` mode)

### Where each method gives up

An n counts as finished only if every rep finished within the time limit (one timeout → that n is `gave up`, larger n are not run). `-` under *gave up* means it never timed out up to *largest n tried*; DP is capped at n = 24 by memory (2^24 states), not by time.

| algorithm | dist | largest n, all reps proven optimal | largest n, all reps answered | gave up at n | largest n tried | median runtime at largest answered n (s) |
|---|---|---|---|---|---|---|
| exhaustive | uniform | 10 | 10 | 11 | 11 | 4.5901 |
| dp | uniform | 24 | 24 | - | 24 | 33.0787 |
| mip | uniform | 20 | 50 | 100 | 100 | 58.5147 |
| ffd | uniform | - | 200 | - | 200 | 0.0003 |
| exhaustive | small | 10 | 10 | 11 | 11 | 3.7847 |
| dp | small | 24 | 24 | - | 24 | 30.6221 |
| mip | small | 200 | 200 | - | 200 | 0.3968 |
| ffd | small | - | 200 | - | 200 | 0.0003 |
| exhaustive | large | 10 | 10 | 11 | 11 | 4.893 |
| dp | large | 24 | 24 | - | 24 | 31.0634 |
| mip | large | 22 | 50 | 100 | 100 | 58.3241 |
| ffd | large | - | 200 | - | 200 | 0.0003 |

### Do the exact methods agree?

Instances solved to proven optimality by 2+ exact methods: **302**, disagreements: **0** (n range 4–24).

### FFD / OPT (instances where OPT is known)

| dist | instances | optimal_share | median | max |
|---|---|---|---|---|
| large | 111 | 100.0% | 1 | 1 |
| small | 130 | 100.0% | 1 | 1 |
| uniform | 110 | 99.1% | 1 | 1.1 |

## Experiment B — heuristics at scale (`default` mode)

Median over reps. `bins/L` = bins used / lower bound ceil(sum/C).

| dist | algorithm | n | status | bins_over_L | runtime_s |
|---|---|---|---|---|---|
| uniform | next_fit | 10 | ok | 1.3333 | 0.000002 |
| uniform | next_fit | 100 | ok | 1.2941 | 0.000008 |
| uniform | next_fit | 1000 | ok | 1.3238 | 0.000084 |
| uniform | next_fit | 10000 | ok | 1.325 | 0.001659 |
| uniform | first_fit | 10 | ok | 1.1667 | 0.000011 |
| uniform | first_fit | 100 | ok | 1.0784 | 0.000132 |
| uniform | first_fit | 1000 | ok | 1.0476 | 0.001841 |
| uniform | first_fit | 10000 | ok | 1.0241 | 0.02685 |
| uniform | best_fit | 10 | ok | 1.1667 | 0.000003 |
| uniform | best_fit | 100 | ok | 1.0625 | 0.000029 |
| uniform | best_fit | 1000 | ok | 1.0357 | 0.000434 |
| uniform | best_fit | 10000 | ok | 1.0148 | 0.007767 |
| uniform | ffd | 10 | ok | 1.1667 | 0.000014 |
| uniform | ffd | 100 | ok | 1.0208 | 0.000134 |
| uniform | ffd | 1000 | ok | 1.0081 | 0.001982 |
| uniform | ffd | 10000 | ok | 1.0059 | 0.029724 |
| uniform | mip | 10 | ok | 1.1667 | 0.007542 |
| uniform | mip | 100 | timeout |  | 10.074613 |
| small | next_fit | 10 | ok | 1 | 0.000002 |
| small | next_fit | 100 | ok | 1.0769 | 0.000006 |
| small | next_fit | 1000 | ok | 1.0859 | 0.000059 |
| small | next_fit | 10000 | ok | 1.088 | 0.001012 |
| small | first_fit | 10 | ok | 1 | 0.00001 |
| small | first_fit | 100 | ok | 1 | 0.000121 |
| small | first_fit | 1000 | ok | 1 | 0.001757 |
| small | first_fit | 10000 | ok | 1.0008 | 0.025672 |
| small | best_fit | 10 | ok | 1 | 0.000002 |
| small | best_fit | 100 | ok | 1 | 0.00002 |
| small | best_fit | 1000 | ok | 1 | 0.000267 |
| small | best_fit | 10000 | ok | 1.0008 | 0.004127 |
| small | ffd | 10 | ok | 1 | 0.000011 |
| small | ffd | 100 | ok | 1 | 0.00013 |
| small | ffd | 1000 | ok | 1 | 0.001842 |
| small | ffd | 10000 | ok | 1 | 0.027445 |
| small | mip | 10 | ok | 1 | 0.003001 |
| small | mip | 100 | ok | 1 | 0.064589 |
| small | mip | 1000 | timeout |  | 10.766957 |
| large | next_fit | 10 | ok | 1.2857 | 0.000002 |
| large | next_fit | 100 | ok | 1.3134 | 0.000008 |
| large | next_fit | 1000 | ok | 1.3591 | 0.000111 |
| large | next_fit | 10000 | ok | 1.3549 | 0.001537 |
| large | first_fit | 10 | ok | 1.1429 | 0.000013 |
| large | first_fit | 100 | ok | 1.1918 | 0.000133 |
| large | first_fit | 1000 | ok | 1.1542 | 0.001917 |
| large | first_fit | 10000 | ok | 1.1357 | 0.028396 |
| large | best_fit | 10 | ok | 1.1429 | 0.000003 |
| large | best_fit | 100 | ok | 1.1791 | 0.00003 |
| large | best_fit | 1000 | ok | 1.1452 | 0.000501 |
| large | best_fit | 10000 | ok | 1.1322 | 0.011246 |
| large | ffd | 10 | ok | 1.1429 | 0.000013 |
| large | ffd | 100 | ok | 1.1765 | 0.000137 |
| large | ffd | 1000 | ok | 1.1335 | 0.002152 |
| large | ffd | 10000 | ok | 1.1268 | 0.035181 |
| large | mip | 10 | ok | 1.1429 | 0.010688 |
| large | mip | 100 | feasible,timeout | 1.1884 | 10.129804 |

## Experiment C — 3D packing and loading (`default` mode)

### Bins, fill rate and runtime per n

Container (100, 100, 100), item sides (5, 50), median over reps. `fill_rate` = item volume / (bins × container volume). Naive never rotates; all EP variants allow rotation.

| dist | algorithm | n | status | bins | L | bins_over_L | fill_rate | runtime_s |
|---|---|---|---|---|---|---|---|---|
| uniform | naive | 20 | ok | 2 | 1 | 2 | 0.199 | 0.000032 |
| uniform | naive | 50 | ok | 4 | 1 | 4 | 0.218 | 0.000073 |
| uniform | naive | 100 | ok | 8 | 3 | 2.667 | 0.261 | 0.00014 |
| uniform | naive | 200 | ok | 14 | 5 | 3.2 | 0.279 | 0.000282 |
| uniform | naive | 500 | ok | 37 | 11 | 3.364 | 0.288 | 0.000717 |
| uniform | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.333 | 0.001723 |
| uniform | ep_volume_norot | 50 | ok | 2 | 1 | 2 | 0.437 | 0.010126 |
| uniform | ep_volume_norot | 100 | ok | 3 | 3 | 1 | 0.696 | 0.018869 |
| uniform | ep_volume_norot | 200 | ok | 6 | 5 | 1.25 | 0.712 | 0.055566 |
| uniform | ep_volume_norot | 500 | ok | 13 | 11 | 1.182 | 0.822 | 0.215707 |
| uniform | ep_volume | 20 | ok | 1 | 1 | 1 | 0.333 | 0.001938 |
| uniform | ep_volume | 50 | ok | 2 | 1 | 2 | 0.495 | 0.015249 |
| uniform | ep_volume | 100 | ok | 3 | 3 | 1 | 0.696 | 0.039741 |
| uniform | ep_volume | 200 | ok | 5 | 5 | 1.2 | 0.828 | 0.142158 |
| uniform | ep_volume | 500 | ok | 12 | 11 | 1.091 | 0.883 | 0.865522 |
| uniform | ep_height | 20 | ok | 1 | 1 | 1 | 0.333 | 0.002025 |
| uniform | ep_height | 50 | ok | 2 | 1 | 2 | 0.437 | 0.016976 |
| uniform | ep_height | 100 | ok | 3 | 3 | 1 | 0.696 | 0.047513 |
| uniform | ep_height | 200 | ok | 5 | 5 | 1.25 | 0.755 | 0.150685 |
| uniform | ep_height | 500 | ok | 13 | 11 | 1.182 | 0.822 | 0.740056 |
| uniform | ep_area | 20 | ok | 1 | 1 | 1 | 0.333 | 0.002288 |
| uniform | ep_area | 50 | ok | 2 | 1 | 2 | 0.495 | 0.016577 |
| uniform | ep_area | 100 | ok | 3 | 3 | 1 | 0.696 | 0.042032 |
| uniform | ep_area | 200 | ok | 5 | 5 | 1.2 | 0.828 | 0.121409 |
| uniform | ep_area | 500 | ok | 13 | 11 | 1.182 | 0.822 | 0.693058 |
| uniform | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.333 | 0.002131 |
| uniform | ep_support_50 | 50 | ok | 2 | 1 | 2 | 0.495 | 0.014376 |
| uniform | ep_support_50 | 100 | ok | 3 | 3 | 1 | 0.696 | 0.0408 |
| uniform | ep_support_50 | 200 | ok | 5 | 5 | 1.2 | 0.828 | 0.14472 |
| uniform | ep_support_50 | 500 | ok | 13 | 11 | 1.182 | 0.835 | 0.918584 |
| uniform | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.333 | 0.002056 |
| uniform | ep_support_90 | 50 | ok | 2 | 1 | 2 | 0.437 | 0.013717 |
| uniform | ep_support_90 | 100 | ok | 3 | 3 | 1 | 0.683 | 0.042633 |
| uniform | ep_support_90 | 200 | ok | 6 | 5 | 1.25 | 0.712 | 0.151218 |
| uniform | ep_support_90 | 500 | ok | 13 | 11 | 1.182 | 0.815 | 0.959205 |
| uniform | ep_support | 20 | ok | 1 | 1 | 1 | 0.333 | 0.001998 |
| uniform | ep_support | 50 | ok | 2 | 1 | 2 | 0.437 | 0.014597 |
| uniform | ep_support | 100 | ok | 3 | 3 | 1 | 0.696 | 0.040992 |
| uniform | ep_support | 200 | ok | 5 | 5 | 1.2 | 0.828 | 0.145114 |
| uniform | ep_support | 500 | ok | 13 | 11 | 1.182 | 0.822 | 0.932525 |
| uniform | ep_support_weight | 20 | ok | 1 | 1 | 1 | 0.326 | 0.00271 |
| uniform | ep_support_weight | 50 | ok | 2 | 1 | 2 | 0.396 | 0.016946 |
| uniform | ep_support_weight | 100 | ok | 4 | 3 | 1.333 | 0.554 | 0.052621 |
| uniform | ep_support_weight | 200 | ok | 6 | 5 | 1.4 | 0.69 | 0.188129 |
| uniform | ep_support_weight | 500 | ok | 14 | 11 | 1.273 | 0.774 | 1.062111 |
| uniform | ep_weight_support_weight | 20 | ok | 1 | 1 | 1 | 0.326 | 0.001831 |
| uniform | ep_weight_support_weight | 50 | ok | 2 | 1 | 2 | 0.437 | 0.018128 |
| uniform | ep_weight_support_weight | 100 | ok | 3 | 3 | 1.333 | 0.603 | 0.059208 |
| uniform | ep_weight_support_weight | 200 | ok | 6 | 5 | 1.4 | 0.69 | 0.180106 |
| uniform | ep_weight_support_weight | 500 | ok | 14 | 11 | 1.273 | 0.763 | 0.947973 |
| flat | naive | 20 | ok | 1 | 1 | 1 | 0.288 | 0.000029 |
| flat | naive | 50 | ok | 2 | 1 | 2 | 0.334 | 0.00007 |
| flat | naive | 100 | ok | 4 | 2 | 2 | 0.362 | 0.000135 |
| flat | naive | 200 | ok | 7 | 3 | 2.333 | 0.401 | 0.000274 |
| flat | naive | 500 | ok | 17 | 8 | 2.125 | 0.418 | 0.000678 |
| flat | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.288 | 0.001814 |
| flat | ep_volume_norot | 50 | ok | 2 | 1 | 2 | 0.34 | 0.014089 |
| flat | ep_volume_norot | 100 | ok | 3 | 2 | 1.5 | 0.482 | 0.040716 |
| flat | ep_volume_norot | 200 | ok | 4 | 3 | 1.333 | 0.693 | 0.116616 |
| flat | ep_volume_norot | 500 | ok | 10 | 8 | 1.25 | 0.709 | 0.556574 |
| flat | ep_volume | 20 | ok | 1 | 1 | 1 | 0.288 | 0.001781 |
| flat | ep_volume | 50 | ok | 1 | 1 | 1 | 0.668 | 0.024817 |
| flat | ep_volume | 100 | ok | 2 | 2 | 1 | 0.724 | 0.079287 |
| flat | ep_volume | 200 | ok | 4 | 3 | 1.333 | 0.702 | 0.284147 |
| flat | ep_volume | 500 | ok | 9 | 8 | 1.125 | 0.788 | 1.817735 |
| flat | ep_height | 20 | ok | 1 | 1 | 1 | 0.288 | 0.001902 |
| flat | ep_height | 50 | ok | 1 | 1 | 1 | 0.663 | 0.019212 |
| flat | ep_height | 100 | ok | 2 | 2 | 1 | 0.724 | 0.063563 |
| flat | ep_height | 200 | ok | 4 | 3 | 1.333 | 0.702 | 0.24502 |
| flat | ep_height | 500 | ok | 9 | 8 | 1.125 | 0.788 | 1.266396 |
| flat | ep_area | 20 | ok | 1 | 1 | 1 | 0.288 | 0.002284 |
| flat | ep_area | 50 | ok | 1 | 1 | 1 | 0.668 | 0.023193 |
| flat | ep_area | 100 | ok | 2 | 2 | 1 | 0.724 | 0.084949 |
| flat | ep_area | 200 | ok | 4 | 3 | 1.333 | 0.702 | 0.327269 |
| flat | ep_area | 500 | ok | 9 | 8 | 1.25 | 0.763 | 1.824319 |
| flat | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.288 | 0.001784 |
| flat | ep_support_50 | 50 | ok | 1 | 1 | 1 | 0.668 | 0.023774 |
| flat | ep_support_50 | 100 | ok | 2 | 2 | 1 | 0.712 | 0.088994 |
| flat | ep_support_50 | 200 | ok | 4 | 3 | 1.333 | 0.702 | 0.307989 |
| flat | ep_support_50 | 500 | ok | 10 | 8 | 1.25 | 0.726 | 1.879755 |
| flat | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.288 | 0.001954 |
| flat | ep_support_90 | 50 | ok | 1 | 1 | 1 | 0.668 | 0.023573 |
| flat | ep_support_90 | 100 | ok | 3 | 2 | 1.5 | 0.484 | 0.087773 |
| flat | ep_support_90 | 200 | ok | 4 | 3 | 1.333 | 0.697 | 0.320181 |
| flat | ep_support_90 | 500 | ok | 10 | 8 | 1.25 | 0.724 | 1.910354 |
| flat | ep_support | 20 | ok | 1 | 1 | 1 | 0.288 | 0.001977 |
| flat | ep_support | 50 | ok | 1 | 1 | 1 | 0.663 | 0.026559 |
| flat | ep_support | 100 | ok | 2 | 2 | 1 | 0.704 | 0.085454 |
| flat | ep_support | 200 | ok | 4 | 3 | 1.333 | 0.702 | 0.319207 |
| flat | ep_support | 500 | ok | 10 | 8 | 1.25 | 0.711 | 1.947132 |
| flat | ep_support_weight | 20 | ok | 2 | 1 | 2 | 0.152 | 0.002436 |
| flat | ep_support_weight | 50 | ok | 2 | 1 | 2 | 0.298 | 0.020176 |
| flat | ep_support_weight | 100 | ok | 3 | 2 | 1.5 | 0.475 | 0.081583 |
| flat | ep_support_weight | 200 | ok | 5 | 3 | 1.667 | 0.562 | 0.318339 |
| flat | ep_support_weight | 500 | ok | 11 | 8 | 1.375 | 0.658 | 2.015756 |
| flat | ep_weight_support_weight | 20 | ok | 1 | 1 | 1 | 0.288 | 0.002069 |
| flat | ep_weight_support_weight | 50 | ok | 2 | 1 | 2 | 0.334 | 0.018822 |
| flat | ep_weight_support_weight | 100 | ok | 3 | 2 | 1.5 | 0.482 | 0.079708 |
| flat | ep_weight_support_weight | 200 | ok | 5 | 3 | 1.667 | 0.564 | 0.356679 |
| flat | ep_weight_support_weight | 500 | ok | 10 | 8 | 1.25 | 0.711 | 1.900883 |
| long | naive | 20 | ok | 2 | 1 | 2 | 0.047 | 0.00003 |
| long | naive | 50 | ok | 2 | 1 | 2 | 0.105 | 0.000068 |
| long | naive | 100 | ok | 4 | 1 | 4 | 0.097 | 0.000134 |
| long | naive | 200 | ok | 9 | 1 | 9 | 0.099 | 0.000264 |
| long | naive | 500 | ok | 21 | 3 | 7 | 0.102 | 0.000677 |
| long | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001631 |
| long | ep_volume_norot | 50 | ok | 1 | 1 | 1 | 0.21 | 0.012492 |
| long | ep_volume_norot | 100 | ok | 1 | 1 | 1 | 0.433 | 0.08011 |
| long | ep_volume_norot | 200 | ok | 2 | 1 | 2 | 0.444 | 0.328483 |
| long | ep_volume_norot | 500 | ok | 4 | 3 | 1.333 | 0.563 | 1.673133 |
| long | ep_volume | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001746 |
| long | ep_volume | 50 | ok | 1 | 1 | 1 | 0.21 | 0.015204 |
| long | ep_volume | 100 | ok | 1 | 1 | 1 | 0.433 | 0.09725 |
| long | ep_volume | 200 | ok | 2 | 1 | 2 | 0.444 | 0.686247 |
| long | ep_volume | 500 | ok | 3 | 3 | 1 | 0.719 | 4.451109 |
| long | ep_height | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001856 |
| long | ep_height | 50 | ok | 1 | 1 | 1 | 0.21 | 0.015989 |
| long | ep_height | 100 | ok | 1 | 1 | 1 | 0.433 | 0.107555 |
| long | ep_height | 200 | ok | 2 | 1 | 2 | 0.444 | 0.946622 |
| long | ep_height | 500 | ok | 3 | 3 | 1 | 0.719 | 5.495228 |
| long | ep_area | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001723 |
| long | ep_area | 50 | ok | 1 | 1 | 1 | 0.21 | 0.014477 |
| long | ep_area | 100 | ok | 1 | 1 | 1 | 0.433 | 0.099322 |
| long | ep_area | 200 | ok | 2 | 1 | 2 | 0.444 | 0.758224 |
| long | ep_area | 500 | ok | 3 | 3 | 1 | 0.719 | 5.019556 |
| long | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001769 |
| long | ep_support_50 | 50 | ok | 1 | 1 | 1 | 0.21 | 0.015767 |
| long | ep_support_50 | 100 | ok | 1 | 1 | 1 | 0.433 | 0.109322 |
| long | ep_support_50 | 200 | ok | 2 | 1 | 2 | 0.444 | 0.732467 |
| long | ep_support_50 | 500 | ok | 3 | 3 | 1 | 0.681 | 4.766496 |
| long | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001732 |
| long | ep_support_90 | 50 | ok | 1 | 1 | 1 | 0.21 | 0.016357 |
| long | ep_support_90 | 100 | ok | 1 | 1 | 1 | 0.433 | 0.106528 |
| long | ep_support_90 | 200 | ok | 2 | 1 | 2 | 0.444 | 0.728196 |
| long | ep_support_90 | 500 | ok | 4 | 3 | 1.333 | 0.563 | 5.409359 |
| long | ep_support | 20 | ok | 1 | 1 | 1 | 0.092 | 0.00174 |
| long | ep_support | 50 | ok | 1 | 1 | 1 | 0.21 | 0.015511 |
| long | ep_support | 100 | ok | 1 | 1 | 1 | 0.433 | 0.112206 |
| long | ep_support | 200 | ok | 2 | 1 | 2 | 0.444 | 0.687756 |
| long | ep_support | 500 | ok | 3 | 3 | 1 | 0.681 | 5.134905 |
| long | ep_support_weight | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001817 |
| long | ep_support_weight | 50 | ok | 1 | 1 | 1 | 0.207 | 0.017351 |
| long | ep_support_weight | 100 | ok | 2 | 1 | 2 | 0.217 | 0.15334 |
| long | ep_support_weight | 200 | ok | 2 | 1 | 2 | 0.44 | 0.665514 |
| long | ep_support_weight | 500 | ok | 4 | 3 | 1.333 | 0.539 | 5.000764 |
| long | ep_weight_support_weight | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001944 |
| long | ep_weight_support_weight | 50 | ok | 1 | 1 | 1 | 0.21 | 0.015763 |
| long | ep_weight_support_weight | 100 | ok | 1 | 1 | 1 | 0.433 | 0.105278 |
| long | ep_weight_support_weight | 200 | ok | 2 | 1 | 2 | 0.444 | 0.695139 |
| long | ep_weight_support_weight | 500 | ok | 4 | 3 | 1.333 | 0.563 | 5.219556 |
| mixed | naive | 20 | ok | 2 | 1 | 2 | 0.151 | 0.000032 |
| mixed | naive | 50 | ok | 3 | 1 | 3 | 0.179 | 0.000071 |
| mixed | naive | 100 | ok | 7 | 2 | 3.5 | 0.183 | 0.000138 |
| mixed | naive | 200 | ok | 14 | 3 | 4.667 | 0.198 | 0.000273 |
| mixed | naive | 500 | ok | 34 | 7 | 4.857 | 0.198 | 0.0007 |
| mixed | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.301 | 0.0016 |
| mixed | ep_volume_norot | 50 | ok | 1 | 1 | 1 | 0.525 | 0.013285 |
| mixed | ep_volume_norot | 100 | ok | 2 | 2 | 1 | 0.639 | 0.030327 |
| mixed | ep_volume_norot | 200 | ok | 4 | 3 | 1.333 | 0.679 | 0.083878 |
| mixed | ep_volume_norot | 500 | ok | 8 | 7 | 1.143 | 0.78 | 0.370907 |
| mixed | ep_volume | 20 | ok | 1 | 1 | 1 | 0.301 | 0.002034 |
| mixed | ep_volume | 50 | ok | 1 | 1 | 1 | 0.599 | 0.019247 |
| mixed | ep_volume | 100 | ok | 2 | 2 | 1 | 0.639 | 0.05537 |
| mixed | ep_volume | 200 | ok | 4 | 3 | 1.333 | 0.744 | 0.244142 |
| mixed | ep_volume | 500 | ok | 8 | 7 | 1.143 | 0.809 | 1.376514 |
| mixed | ep_height | 20 | ok | 1 | 1 | 1 | 0.301 | 0.001971 |
| mixed | ep_height | 50 | ok | 1 | 1 | 1 | 0.599 | 0.018901 |
| mixed | ep_height | 100 | ok | 2 | 2 | 1 | 0.639 | 0.073491 |
| mixed | ep_height | 200 | ok | 4 | 3 | 1.333 | 0.699 | 0.236109 |
| mixed | ep_height | 500 | ok | 8 | 7 | 1.143 | 0.809 | 1.135644 |
| mixed | ep_area | 20 | ok | 1 | 1 | 1 | 0.301 | 0.001959 |
| mixed | ep_area | 50 | ok | 1 | 1 | 1 | 0.599 | 0.020754 |
| mixed | ep_area | 100 | ok | 2 | 2 | 1 | 0.639 | 0.068074 |
| mixed | ep_area | 200 | ok | 4 | 3 | 1.333 | 0.699 | 0.228342 |
| mixed | ep_area | 500 | ok | 8 | 7 | 1.143 | 0.809 | 1.279417 |
| mixed | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.301 | 0.002075 |
| mixed | ep_support_50 | 50 | ok | 1 | 1 | 1 | 0.599 | 0.017909 |
| mixed | ep_support_50 | 100 | ok | 2 | 2 | 1 | 0.639 | 0.058386 |
| mixed | ep_support_50 | 200 | ok | 4 | 3 | 1.333 | 0.699 | 0.236024 |
| mixed | ep_support_50 | 500 | ok | 8 | 7 | 1.143 | 0.809 | 1.485995 |
| mixed | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.301 | 0.001939 |
| mixed | ep_support_90 | 50 | ok | 1 | 1 | 1 | 0.544 | 0.018615 |
| mixed | ep_support_90 | 100 | ok | 2 | 2 | 1 | 0.639 | 0.057023 |
| mixed | ep_support_90 | 200 | ok | 4 | 3 | 1.333 | 0.679 | 0.24445 |
| mixed | ep_support_90 | 500 | ok | 8 | 7 | 1.143 | 0.8 | 1.488484 |
| mixed | ep_support | 20 | ok | 1 | 1 | 1 | 0.301 | 0.001963 |
| mixed | ep_support | 50 | ok | 1 | 1 | 1 | 0.599 | 0.018342 |
| mixed | ep_support | 100 | ok | 2 | 2 | 1 | 0.639 | 0.058984 |
| mixed | ep_support | 200 | ok | 4 | 3 | 1.333 | 0.679 | 0.248638 |
| mixed | ep_support | 500 | ok | 8 | 7 | 1.143 | 0.8 | 1.49561 |
| mixed | ep_support_weight | 20 | ok | 1 | 1 | 1 | 0.301 | 0.002647 |
| mixed | ep_support_weight | 50 | ok | 2 | 1 | 2 | 0.3 | 0.019013 |
| mixed | ep_support_weight | 100 | ok | 3 | 2 | 1.5 | 0.431 | 0.072871 |
| mixed | ep_support_weight | 200 | ok | 4 | 3 | 1.333 | 0.607 | 0.254206 |
| mixed | ep_support_weight | 500 | ok | 9 | 7 | 1.286 | 0.747 | 1.590097 |
| mixed | ep_weight_support_weight | 20 | ok | 1 | 1 | 1 | 0.255 | 0.001935 |
| mixed | ep_weight_support_weight | 50 | ok | 2 | 1 | 2 | 0.342 | 0.018185 |
| mixed | ep_weight_support_weight | 100 | ok | 2 | 2 | 1 | 0.518 | 0.093387 |
| mixed | ep_weight_support_weight | 200 | ok | 4 | 3 | 1.333 | 0.679 | 0.29172 |
| mixed | ep_weight_support_weight | 500 | ok | 9 | 7 | 1.286 | 0.764 | 1.629644 |

### Cost of loading constraints

Same instances, EP sorted by volume with vs without constraints. `increase_pct` = sum(bins with) / sum(bins without) − 1 over all n and seeds. Support threshold 70% is an assumption.

| variant | dist | instances | bins_ep_volume | bins_variant | increase_pct | share_needing_more_bins |
|---|---|---|---|---|---|---|
| ep_support | flat | 25 | 86 | 93 | 8.1 | 28% |
| ep_support | long | 25 | 40 | 42 | 5 | 8% |
| ep_support | mixed | 25 | 78 | 81 | 3.8 | 12% |
| ep_support | uniform | 25 | 116 | 120 | 3.4 | 16% |
| ep_support | all | 100 | 320 | 336 | 5 | 16% |
| ep_support_weight | flat | 25 | 86 | 115 | 33.7 | 92% |
| ep_support_weight | long | 25 | 40 | 52 | 30 | 48% |
| ep_support_weight | mixed | 25 | 78 | 96 | 23.1 | 72% |
| ep_support_weight | uniform | 25 | 116 | 136 | 17.2 | 72% |
| ep_support_weight | all | 100 | 320 | 399 | 24.7 | 71% |
| ep_weight_support_weight | flat | 25 | 86 | 104 | 20.9 | 72% |
| ep_weight_support_weight | long | 25 | 40 | 44 | 10 | 16% |
| ep_weight_support_weight | mixed | 25 | 78 | 90 | 15.4 | 48% |
| ep_weight_support_weight | uniform | 25 | 116 | 133 | 14.7 | 56% |
| ep_weight_support_weight | all | 100 | 320 | 371 | 15.9 | 48% |

### Sensitivity of the support threshold

Extra bins vs plain EP for support thresholds 50% / 70% / 90% (same instances, same method as above).

| variant | dist | instances | bins_ep_volume | bins_variant | increase_pct | share_needing_more_bins |
|---|---|---|---|---|---|---|
| ep_support_50 | all | 100 | 320 | 328 | 2.5 | 8% |
| ep_support | all | 100 | 320 | 336 | 5 | 16% |
| ep_support_90 | all | 100 | 320 | 346 | 8.1 | 26% |

| variant | dist | instances | bins_ep_volume | bins_variant | increase_pct | share_needing_more_bins |
|---|---|---|---|---|---|---|
| ep_support_50 | flat | 25 | 86 | 89 | 3.5 | 12% |
| ep_support_50 | long | 25 | 40 | 42 | 5 | 8% |
| ep_support_50 | mixed | 25 | 78 | 79 | 1.3 | 4% |
| ep_support_50 | uniform | 25 | 116 | 118 | 1.7 | 8% |
| ep_support | flat | 25 | 86 | 93 | 8.1 | 28% |
| ep_support | long | 25 | 40 | 42 | 5 | 8% |
| ep_support | mixed | 25 | 78 | 81 | 3.8 | 12% |
| ep_support | uniform | 25 | 116 | 120 | 3.4 | 16% |
| ep_support_90 | flat | 25 | 86 | 94 | 9.3 | 32% |
| ep_support_90 | long | 25 | 40 | 44 | 10 | 16% |
| ep_support_90 | mixed | 25 | 78 | 82 | 5.1 | 16% |
| ep_support_90 | uniform | 25 | 116 | 126 | 8.6 | 40% |

### How much of the Naive → EP gap is rotation?

Extra bins vs EP with rotation (sort by volume). `ep_volume_norot` = same EP without rotation; `naive` = 3D Naive (no rotation). The gap between the two rows is the algorithm; the gap between `ep_volume_norot` and 0% is rotation.

| variant | dist | instances | bins_ep_volume | bins_variant | increase_pct | share_needing_more_bins |
|---|---|---|---|---|---|---|
| ep_volume_norot | flat | 25 | 86 | 102 | 18.6 | 64% |
| ep_volume_norot | long | 25 | 40 | 44 | 10 | 16% |
| ep_volume_norot | mixed | 25 | 78 | 84 | 7.7 | 24% |
| ep_volume_norot | uniform | 25 | 116 | 123 | 6 | 28% |
| ep_volume_norot | all | 100 | 320 | 353 | 10.3 | 33% |
| naive | flat | 25 | 86 | 156 | 81.4 | 80% |
| naive | long | 25 | 40 | 192 | 380 | 92% |
| naive | mixed | 25 | 78 | 295 | 278.2 | 96% |
| naive | uniform | 25 | 116 | 325 | 180.2 | 96% |
| naive | all | 100 | 320 | 968 | 202.5 | 91% |

### Box choice per order

200 orders of 3–15 items (sides (3, 25)), catalog [(20, 15, 10), (30, 20, 15), (35, 25, 20), (40, 30, 25), (50, 40, 30), (60, 45, 40)]. void = 1 − item volume / box volume used. `share_split` = orders that needed more than one box. `tries` = packing attempts per order (multi-start cost; included in runtime).

| algorithm | orders | void_median | void_mean | share_void_le_50 | share_split | runtime_ms_median | tries_mean |
|---|---|---|---|---|---|---|---|
| box_recommend | 200 | 0.47 | 0.466 | 55.0% | 0.0% | 0.497 | 2.24 |
| box_naive | 200 | 0.867 | 0.843 | 0.5% | 27.5% | 0.072 | 2.84 |

Not comparable with CJ Logistics' published figures (different items and catalog).

### Multi-start vs a single sort rule

Same orders. The recommendation tries every sort rule in a box before moving to a bigger box (multi-start); the other rows use only one rule. `orders_multistart_smaller` = orders where multi-start chose a box with less volume than that single rule. `_larger` must be 0 by construction (multi-start also tries that rule in every box, so it stops at the same box or a smaller one); it is kept as a check.

| method | sort rules | void_median | share_void_le_50 | tries_mean | orders_multistart_smaller | orders_multistart_larger |
|---|---|---|---|---|---|---|
| box_recommend | all 3 | 0.47 | 55.0% | 2.24 | - | - |
| box_recommend_volume | volume | 0.516 | 48.5% | 1.45 | 14 | 0 |
| box_recommend_height | height | 0.555 | 35.5% | 1.58 | 41 | 0 |
| box_recommend_area | area | 0.541 | 40.5% | 1.54 | 31 | 0 |
