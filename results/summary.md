# Results summary (auto-generated — do not edit by hand)

Generated 2026-11-13 by `python -m experiments.summary`.

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
| uniform | naive | 20 | ok | 2 | 1 | 2 | 0.199 | 0.00003 |
| uniform | naive | 50 | ok | 4 | 1 | 4 | 0.218 | 0.000101 |
| uniform | naive | 100 | ok | 8 | 3 | 2.667 | 0.261 | 0.000138 |
| uniform | naive | 200 | ok | 14 | 5 | 3.2 | 0.279 | 0.000266 |
| uniform | naive | 500 | ok | 37 | 11 | 3.364 | 0.288 | 0.000719 |
| uniform | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.333 | 0.001692 |
| uniform | ep_volume_norot | 50 | ok | 2 | 1 | 2 | 0.437 | 0.009681 |
| uniform | ep_volume_norot | 100 | ok | 3 | 3 | 1 | 0.696 | 0.018138 |
| uniform | ep_volume_norot | 200 | ok | 6 | 5 | 1.25 | 0.712 | 0.05163 |
| uniform | ep_volume_norot | 500 | ok | 13 | 11 | 1.182 | 0.822 | 0.209551 |
| uniform | ep_volume | 20 | ok | 1 | 1 | 1 | 0.333 | 0.00193 |
| uniform | ep_volume | 50 | ok | 2 | 1 | 2 | 0.495 | 0.015398 |
| uniform | ep_volume | 100 | ok | 3 | 3 | 1 | 0.696 | 0.039853 |
| uniform | ep_volume | 200 | ok | 5 | 5 | 1.2 | 0.828 | 0.139215 |
| uniform | ep_volume | 500 | ok | 12 | 11 | 1.091 | 0.883 | 0.910021 |
| uniform | ep_height | 20 | ok | 1 | 1 | 1 | 0.333 | 0.002226 |
| uniform | ep_height | 50 | ok | 2 | 1 | 2 | 0.437 | 0.01633 |
| uniform | ep_height | 100 | ok | 3 | 3 | 1 | 0.696 | 0.046447 |
| uniform | ep_height | 200 | ok | 5 | 5 | 1.25 | 0.755 | 0.15263 |
| uniform | ep_height | 500 | ok | 13 | 11 | 1.182 | 0.822 | 0.796793 |
| uniform | ep_area | 20 | ok | 1 | 1 | 1 | 0.333 | 0.002158 |
| uniform | ep_area | 50 | ok | 2 | 1 | 2 | 0.495 | 0.019201 |
| uniform | ep_area | 100 | ok | 3 | 3 | 1 | 0.696 | 0.057738 |
| uniform | ep_area | 200 | ok | 5 | 5 | 1.2 | 0.828 | 0.159272 |
| uniform | ep_area | 500 | ok | 13 | 11 | 1.182 | 0.822 | 0.761136 |
| uniform | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.333 | 0.002269 |
| uniform | ep_support_50 | 50 | ok | 2 | 1 | 2 | 0.495 | 0.015791 |
| uniform | ep_support_50 | 100 | ok | 3 | 3 | 1 | 0.696 | 0.059552 |
| uniform | ep_support_50 | 200 | ok | 5 | 5 | 1.2 | 0.828 | 0.168039 |
| uniform | ep_support_50 | 500 | ok | 13 | 11 | 1.182 | 0.835 | 1.060457 |
| uniform | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.333 | 0.002055 |
| uniform | ep_support_90 | 50 | ok | 2 | 1 | 2 | 0.437 | 0.018243 |
| uniform | ep_support_90 | 100 | ok | 3 | 3 | 1 | 0.683 | 0.04304 |
| uniform | ep_support_90 | 200 | ok | 6 | 5 | 1.25 | 0.712 | 0.16984 |
| uniform | ep_support_90 | 500 | ok | 13 | 11 | 1.182 | 0.815 | 1.017396 |
| uniform | ep_support | 20 | ok | 1 | 1 | 1 | 0.333 | 0.002041 |
| uniform | ep_support | 50 | ok | 2 | 1 | 2 | 0.437 | 0.014926 |
| uniform | ep_support | 100 | ok | 3 | 3 | 1 | 0.696 | 0.040389 |
| uniform | ep_support | 200 | ok | 5 | 5 | 1.2 | 0.828 | 0.148894 |
| uniform | ep_support | 500 | ok | 13 | 11 | 1.182 | 0.822 | 1.003967 |
| uniform | ep_support_weight | 20 | ok | 1 | 1 | 1 | 0.326 | 0.002617 |
| uniform | ep_support_weight | 50 | ok | 2 | 1 | 2 | 0.396 | 0.019724 |
| uniform | ep_support_weight | 100 | ok | 4 | 3 | 1.333 | 0.554 | 0.050893 |
| uniform | ep_support_weight | 200 | ok | 6 | 5 | 1.4 | 0.69 | 0.181587 |
| uniform | ep_support_weight | 500 | ok | 14 | 11 | 1.273 | 0.774 | 1.175472 |
| flat | naive | 20 | ok | 1 | 1 | 1 | 0.288 | 0.000036 |
| flat | naive | 50 | ok | 2 | 1 | 2 | 0.334 | 0.000075 |
| flat | naive | 100 | ok | 4 | 2 | 2 | 0.362 | 0.000136 |
| flat | naive | 200 | ok | 7 | 3 | 2.333 | 0.401 | 0.000296 |
| flat | naive | 500 | ok | 17 | 8 | 2.125 | 0.418 | 0.000697 |
| flat | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.288 | 0.001962 |
| flat | ep_volume_norot | 50 | ok | 2 | 1 | 2 | 0.34 | 0.014488 |
| flat | ep_volume_norot | 100 | ok | 3 | 2 | 1.5 | 0.482 | 0.042274 |
| flat | ep_volume_norot | 200 | ok | 4 | 3 | 1.333 | 0.693 | 0.131715 |
| flat | ep_volume_norot | 500 | ok | 10 | 8 | 1.25 | 0.709 | 0.62809 |
| flat | ep_volume | 20 | ok | 1 | 1 | 1 | 0.288 | 0.002392 |
| flat | ep_volume | 50 | ok | 1 | 1 | 1 | 0.668 | 0.029812 |
| flat | ep_volume | 100 | ok | 2 | 2 | 1 | 0.724 | 0.079918 |
| flat | ep_volume | 200 | ok | 4 | 3 | 1.333 | 0.702 | 0.333829 |
| flat | ep_volume | 500 | ok | 9 | 8 | 1.125 | 0.788 | 2.0573 |
| flat | ep_height | 20 | ok | 1 | 1 | 1 | 0.288 | 0.001966 |
| flat | ep_height | 50 | ok | 1 | 1 | 1 | 0.663 | 0.024448 |
| flat | ep_height | 100 | ok | 2 | 2 | 1 | 0.724 | 0.065267 |
| flat | ep_height | 200 | ok | 4 | 3 | 1.333 | 0.702 | 0.264612 |
| flat | ep_height | 500 | ok | 9 | 8 | 1.125 | 0.788 | 1.389389 |
| flat | ep_area | 20 | ok | 1 | 1 | 1 | 0.288 | 0.002147 |
| flat | ep_area | 50 | ok | 1 | 1 | 1 | 0.668 | 0.025262 |
| flat | ep_area | 100 | ok | 2 | 2 | 1 | 0.724 | 0.086665 |
| flat | ep_area | 200 | ok | 4 | 3 | 1.333 | 0.702 | 0.355123 |
| flat | ep_area | 500 | ok | 9 | 8 | 1.25 | 0.763 | 2.005282 |
| flat | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.288 | 0.001982 |
| flat | ep_support_50 | 50 | ok | 1 | 1 | 1 | 0.668 | 0.024404 |
| flat | ep_support_50 | 100 | ok | 2 | 2 | 1 | 0.712 | 0.095599 |
| flat | ep_support_50 | 200 | ok | 4 | 3 | 1.333 | 0.702 | 0.334538 |
| flat | ep_support_50 | 500 | ok | 10 | 8 | 1.25 | 0.726 | 1.999415 |
| flat | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.288 | 0.001822 |
| flat | ep_support_90 | 50 | ok | 1 | 1 | 1 | 0.668 | 0.023821 |
| flat | ep_support_90 | 100 | ok | 3 | 2 | 1.5 | 0.484 | 0.095001 |
| flat | ep_support_90 | 200 | ok | 4 | 3 | 1.333 | 0.697 | 0.34923 |
| flat | ep_support_90 | 500 | ok | 10 | 8 | 1.25 | 0.724 | 2.011064 |
| flat | ep_support | 20 | ok | 1 | 1 | 1 | 0.288 | 0.001857 |
| flat | ep_support | 50 | ok | 1 | 1 | 1 | 0.663 | 0.027167 |
| flat | ep_support | 100 | ok | 2 | 2 | 1 | 0.704 | 0.083766 |
| flat | ep_support | 200 | ok | 4 | 3 | 1.333 | 0.702 | 0.325414 |
| flat | ep_support | 500 | ok | 10 | 8 | 1.25 | 0.711 | 2.041675 |
| flat | ep_support_weight | 20 | ok | 2 | 1 | 2 | 0.152 | 0.002597 |
| flat | ep_support_weight | 50 | ok | 2 | 1 | 2 | 0.298 | 0.020746 |
| flat | ep_support_weight | 100 | ok | 3 | 2 | 1.5 | 0.475 | 0.089102 |
| flat | ep_support_weight | 200 | ok | 5 | 3 | 1.667 | 0.562 | 0.348577 |
| flat | ep_support_weight | 500 | ok | 11 | 8 | 1.375 | 0.658 | 2.118405 |
| long | naive | 20 | ok | 2 | 1 | 2 | 0.047 | 0.00003 |
| long | naive | 50 | ok | 2 | 1 | 2 | 0.105 | 0.000068 |
| long | naive | 100 | ok | 4 | 1 | 4 | 0.097 | 0.000132 |
| long | naive | 200 | ok | 9 | 1 | 9 | 0.099 | 0.000264 |
| long | naive | 500 | ok | 21 | 3 | 7 | 0.102 | 0.000703 |
| long | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001529 |
| long | ep_volume_norot | 50 | ok | 1 | 1 | 1 | 0.21 | 0.012325 |
| long | ep_volume_norot | 100 | ok | 1 | 1 | 1 | 0.433 | 0.082853 |
| long | ep_volume_norot | 200 | ok | 2 | 1 | 2 | 0.444 | 0.333182 |
| long | ep_volume_norot | 500 | ok | 4 | 3 | 1.333 | 0.563 | 1.800587 |
| long | ep_volume | 20 | ok | 1 | 1 | 1 | 0.092 | 0.00177 |
| long | ep_volume | 50 | ok | 1 | 1 | 1 | 0.21 | 0.015738 |
| long | ep_volume | 100 | ok | 1 | 1 | 1 | 0.433 | 0.116089 |
| long | ep_volume | 200 | ok | 2 | 1 | 2 | 0.444 | 0.713317 |
| long | ep_volume | 500 | ok | 3 | 3 | 1 | 0.719 | 4.814264 |
| long | ep_height | 20 | ok | 1 | 1 | 1 | 0.092 | 0.002203 |
| long | ep_height | 50 | ok | 1 | 1 | 1 | 0.21 | 0.017919 |
| long | ep_height | 100 | ok | 1 | 1 | 1 | 0.433 | 0.120511 |
| long | ep_height | 200 | ok | 2 | 1 | 2 | 0.444 | 1.041536 |
| long | ep_height | 500 | ok | 3 | 3 | 1 | 0.719 | 5.954692 |
| long | ep_area | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001772 |
| long | ep_area | 50 | ok | 1 | 1 | 1 | 0.21 | 0.014278 |
| long | ep_area | 100 | ok | 1 | 1 | 1 | 0.433 | 0.098754 |
| long | ep_area | 200 | ok | 2 | 1 | 2 | 0.444 | 0.794536 |
| long | ep_area | 500 | ok | 3 | 3 | 1 | 0.719 | 5.363503 |
| long | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001762 |
| long | ep_support_50 | 50 | ok | 1 | 1 | 1 | 0.21 | 0.017062 |
| long | ep_support_50 | 100 | ok | 1 | 1 | 1 | 0.433 | 0.106486 |
| long | ep_support_50 | 200 | ok | 2 | 1 | 2 | 0.444 | 0.74363 |
| long | ep_support_50 | 500 | ok | 3 | 3 | 1 | 0.681 | 5.030771 |
| long | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001794 |
| long | ep_support_90 | 50 | ok | 1 | 1 | 1 | 0.21 | 0.016877 |
| long | ep_support_90 | 100 | ok | 1 | 1 | 1 | 0.433 | 0.118988 |
| long | ep_support_90 | 200 | ok | 2 | 1 | 2 | 0.444 | 0.746439 |
| long | ep_support_90 | 500 | ok | 4 | 3 | 1.333 | 0.563 | 5.842655 |
| long | ep_support | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001919 |
| long | ep_support | 50 | ok | 1 | 1 | 1 | 0.21 | 0.016369 |
| long | ep_support | 100 | ok | 1 | 1 | 1 | 0.433 | 0.119792 |
| long | ep_support | 200 | ok | 2 | 1 | 2 | 0.444 | 0.736496 |
| long | ep_support | 500 | ok | 3 | 3 | 1 | 0.681 | 5.43653 |
| long | ep_support_weight | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001788 |
| long | ep_support_weight | 50 | ok | 1 | 1 | 1 | 0.207 | 0.017623 |
| long | ep_support_weight | 100 | ok | 2 | 1 | 2 | 0.217 | 0.191172 |
| long | ep_support_weight | 200 | ok | 2 | 1 | 2 | 0.44 | 0.689522 |
| long | ep_support_weight | 500 | ok | 4 | 3 | 1.333 | 0.539 | 5.397437 |
| mixed | naive | 20 | ok | 2 | 1 | 2 | 0.151 | 0.000037 |
| mixed | naive | 50 | ok | 3 | 1 | 3 | 0.179 | 0.00007 |
| mixed | naive | 100 | ok | 7 | 2 | 3.5 | 0.183 | 0.000141 |
| mixed | naive | 200 | ok | 14 | 3 | 4.667 | 0.198 | 0.000267 |
| mixed | naive | 500 | ok | 34 | 7 | 4.857 | 0.198 | 0.000696 |
| mixed | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.301 | 0.001662 |
| mixed | ep_volume_norot | 50 | ok | 1 | 1 | 1 | 0.525 | 0.013553 |
| mixed | ep_volume_norot | 100 | ok | 2 | 2 | 1 | 0.639 | 0.040553 |
| mixed | ep_volume_norot | 200 | ok | 4 | 3 | 1.333 | 0.679 | 0.082078 |
| mixed | ep_volume_norot | 500 | ok | 8 | 7 | 1.143 | 0.78 | 0.392124 |
| mixed | ep_volume | 20 | ok | 1 | 1 | 1 | 0.301 | 0.002914 |
| mixed | ep_volume | 50 | ok | 1 | 1 | 1 | 0.599 | 0.022276 |
| mixed | ep_volume | 100 | ok | 2 | 2 | 1 | 0.639 | 0.063929 |
| mixed | ep_volume | 200 | ok | 4 | 3 | 1.333 | 0.744 | 0.274167 |
| mixed | ep_volume | 500 | ok | 8 | 7 | 1.143 | 0.809 | 1.59972 |
| mixed | ep_height | 20 | ok | 1 | 1 | 1 | 0.301 | 0.002041 |
| mixed | ep_height | 50 | ok | 1 | 1 | 1 | 0.599 | 0.019625 |
| mixed | ep_height | 100 | ok | 2 | 2 | 1 | 0.639 | 0.073475 |
| mixed | ep_height | 200 | ok | 4 | 3 | 1.333 | 0.699 | 0.245885 |
| mixed | ep_height | 500 | ok | 8 | 7 | 1.143 | 0.809 | 1.219758 |
| mixed | ep_area | 20 | ok | 1 | 1 | 1 | 0.301 | 0.002251 |
| mixed | ep_area | 50 | ok | 1 | 1 | 1 | 0.599 | 0.021623 |
| mixed | ep_area | 100 | ok | 2 | 2 | 1 | 0.639 | 0.078277 |
| mixed | ep_area | 200 | ok | 4 | 3 | 1.333 | 0.699 | 0.232494 |
| mixed | ep_area | 500 | ok | 8 | 7 | 1.143 | 0.809 | 1.338884 |
| mixed | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.301 | 0.001921 |
| mixed | ep_support_50 | 50 | ok | 1 | 1 | 1 | 0.599 | 0.017996 |
| mixed | ep_support_50 | 100 | ok | 2 | 2 | 1 | 0.639 | 0.062567 |
| mixed | ep_support_50 | 200 | ok | 4 | 3 | 1.333 | 0.699 | 0.252536 |
| mixed | ep_support_50 | 500 | ok | 8 | 7 | 1.143 | 0.809 | 1.515446 |
| mixed | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.301 | 0.001887 |
| mixed | ep_support_90 | 50 | ok | 1 | 1 | 1 | 0.544 | 0.018885 |
| mixed | ep_support_90 | 100 | ok | 2 | 2 | 1 | 0.639 | 0.057122 |
| mixed | ep_support_90 | 200 | ok | 4 | 3 | 1.333 | 0.679 | 0.240942 |
| mixed | ep_support_90 | 500 | ok | 8 | 7 | 1.143 | 0.8 | 1.546742 |
| mixed | ep_support | 20 | ok | 1 | 1 | 1 | 0.301 | 0.002972 |
| mixed | ep_support | 50 | ok | 1 | 1 | 1 | 0.599 | 0.019253 |
| mixed | ep_support | 100 | ok | 2 | 2 | 1 | 0.639 | 0.058314 |
| mixed | ep_support | 200 | ok | 4 | 3 | 1.333 | 0.679 | 0.267927 |
| mixed | ep_support | 500 | ok | 8 | 7 | 1.143 | 0.8 | 1.604447 |
| mixed | ep_support_weight | 20 | ok | 1 | 1 | 1 | 0.301 | 0.002929 |
| mixed | ep_support_weight | 50 | ok | 2 | 1 | 2 | 0.3 | 0.025319 |
| mixed | ep_support_weight | 100 | ok | 3 | 2 | 1.5 | 0.431 | 0.087027 |
| mixed | ep_support_weight | 200 | ok | 4 | 3 | 1.333 | 0.607 | 0.258103 |
| mixed | ep_support_weight | 500 | ok | 9 | 7 | 1.286 | 0.747 | 1.738962 |

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
| box_recommend | 200 | 0.47 | 0.466 | 55.0% | 0.0% | 0.518 | 2.24 |
| box_naive | 200 | 0.867 | 0.843 | 0.5% | 27.5% | 0.075 | 2.84 |

Not comparable with CJ Logistics' published figures (different items and catalog).
