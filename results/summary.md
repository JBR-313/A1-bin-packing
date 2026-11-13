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
| uniform | naive | 20 | ok | 2 | 1 | 2 | 0.199 | 0.00004 |
| uniform | naive | 50 | ok | 4 | 1 | 4 | 0.218 | 0.000089 |
| uniform | naive | 100 | ok | 8 | 3 | 2.667 | 0.261 | 0.000162 |
| uniform | naive | 200 | ok | 14 | 5 | 3.2 | 0.279 | 0.000351 |
| uniform | naive | 500 | ok | 37 | 11 | 3.364 | 0.288 | 0.000779 |
| uniform | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.333 | 0.00184 |
| uniform | ep_volume_norot | 50 | ok | 2 | 1 | 2 | 0.437 | 0.010565 |
| uniform | ep_volume_norot | 100 | ok | 3 | 3 | 1 | 0.696 | 0.021742 |
| uniform | ep_volume_norot | 200 | ok | 6 | 5 | 1.25 | 0.712 | 0.055707 |
| uniform | ep_volume_norot | 500 | ok | 13 | 11 | 1.182 | 0.822 | 0.246339 |
| uniform | ep_volume | 20 | ok | 1 | 1 | 1 | 0.333 | 0.002312 |
| uniform | ep_volume | 50 | ok | 2 | 1 | 2 | 0.495 | 0.017005 |
| uniform | ep_volume | 100 | ok | 3 | 3 | 1 | 0.696 | 0.048435 |
| uniform | ep_volume | 200 | ok | 5 | 5 | 1.2 | 0.828 | 0.170386 |
| uniform | ep_volume | 500 | ok | 12 | 11 | 1.091 | 0.883 | 1.156232 |
| uniform | ep_height | 20 | ok | 1 | 1 | 1 | 0.333 | 0.002598 |
| uniform | ep_height | 50 | ok | 2 | 1 | 2 | 0.437 | 0.020742 |
| uniform | ep_height | 100 | ok | 3 | 3 | 1 | 0.696 | 0.059041 |
| uniform | ep_height | 200 | ok | 5 | 5 | 1.25 | 0.755 | 0.185105 |
| uniform | ep_height | 500 | ok | 13 | 11 | 1.182 | 0.822 | 0.891095 |
| uniform | ep_area | 20 | ok | 1 | 1 | 1 | 0.333 | 0.002672 |
| uniform | ep_area | 50 | ok | 2 | 1 | 2 | 0.495 | 0.018575 |
| uniform | ep_area | 100 | ok | 3 | 3 | 1 | 0.696 | 0.04962 |
| uniform | ep_area | 200 | ok | 5 | 5 | 1.2 | 0.828 | 0.148559 |
| uniform | ep_area | 500 | ok | 13 | 11 | 1.182 | 0.822 | 0.878147 |
| uniform | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.333 | 0.002314 |
| uniform | ep_support_50 | 50 | ok | 2 | 1 | 2 | 0.495 | 0.015237 |
| uniform | ep_support_50 | 100 | ok | 3 | 3 | 1 | 0.696 | 0.045753 |
| uniform | ep_support_50 | 200 | ok | 5 | 5 | 1.2 | 0.828 | 0.164094 |
| uniform | ep_support_50 | 500 | ok | 13 | 11 | 1.182 | 0.835 | 1.136971 |
| uniform | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.333 | 0.002329 |
| uniform | ep_support_90 | 50 | ok | 2 | 1 | 2 | 0.437 | 0.018376 |
| uniform | ep_support_90 | 100 | ok | 3 | 3 | 1 | 0.683 | 0.052005 |
| uniform | ep_support_90 | 200 | ok | 6 | 5 | 1.25 | 0.712 | 0.172793 |
| uniform | ep_support_90 | 500 | ok | 13 | 11 | 1.182 | 0.815 | 1.130598 |
| uniform | ep_support | 20 | ok | 1 | 1 | 1 | 0.333 | 0.002432 |
| uniform | ep_support | 50 | ok | 2 | 1 | 2 | 0.437 | 0.016649 |
| uniform | ep_support | 100 | ok | 3 | 3 | 1 | 0.696 | 0.04754 |
| uniform | ep_support | 200 | ok | 5 | 5 | 1.2 | 0.828 | 0.182761 |
| uniform | ep_support | 500 | ok | 13 | 11 | 1.182 | 0.822 | 1.171209 |
| uniform | ep_support_weight | 20 | ok | 1 | 1 | 1 | 0.326 | 0.003264 |
| uniform | ep_support_weight | 50 | ok | 2 | 1 | 2 | 0.396 | 0.017731 |
| uniform | ep_support_weight | 100 | ok | 4 | 3 | 1.333 | 0.554 | 0.058239 |
| uniform | ep_support_weight | 200 | ok | 6 | 5 | 1.4 | 0.69 | 0.21596 |
| uniform | ep_support_weight | 500 | ok | 14 | 11 | 1.273 | 0.774 | 1.232446 |
| uniform | ep_weight_support_weight | 20 | ok | 1 | 1 | 1 | 0.326 | 0.002039 |
| uniform | ep_weight_support_weight | 50 | ok | 2 | 1 | 2 | 0.437 | 0.022404 |
| uniform | ep_weight_support_weight | 100 | ok | 3 | 3 | 1.333 | 0.603 | 0.07193 |
| uniform | ep_weight_support_weight | 200 | ok | 6 | 5 | 1.4 | 0.69 | 0.215404 |
| uniform | ep_weight_support_weight | 500 | ok | 14 | 11 | 1.273 | 0.763 | 1.140229 |
| flat | naive | 20 | ok | 1 | 1 | 1 | 0.288 | 0.000072 |
| flat | naive | 50 | ok | 2 | 1 | 2 | 0.334 | 0.000087 |
| flat | naive | 100 | ok | 4 | 2 | 2 | 0.362 | 0.000181 |
| flat | naive | 200 | ok | 7 | 3 | 2.333 | 0.401 | 0.00031 |
| flat | naive | 500 | ok | 17 | 8 | 2.125 | 0.418 | 0.000959 |
| flat | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.288 | 0.002492 |
| flat | ep_volume_norot | 50 | ok | 2 | 1 | 2 | 0.34 | 0.017108 |
| flat | ep_volume_norot | 100 | ok | 3 | 2 | 1.5 | 0.482 | 0.04858 |
| flat | ep_volume_norot | 200 | ok | 4 | 3 | 1.333 | 0.693 | 0.138672 |
| flat | ep_volume_norot | 500 | ok | 10 | 8 | 1.25 | 0.709 | 0.663059 |
| flat | ep_volume | 20 | ok | 1 | 1 | 1 | 0.288 | 0.001954 |
| flat | ep_volume | 50 | ok | 1 | 1 | 1 | 0.668 | 0.027914 |
| flat | ep_volume | 100 | ok | 2 | 2 | 1 | 0.724 | 0.092912 |
| flat | ep_volume | 200 | ok | 4 | 3 | 1.333 | 0.702 | 0.325923 |
| flat | ep_volume | 500 | ok | 9 | 8 | 1.125 | 0.788 | 2.225521 |
| flat | ep_height | 20 | ok | 1 | 1 | 1 | 0.288 | 0.002264 |
| flat | ep_height | 50 | ok | 1 | 1 | 1 | 0.663 | 0.023767 |
| flat | ep_height | 100 | ok | 2 | 2 | 1 | 0.724 | 0.080523 |
| flat | ep_height | 200 | ok | 4 | 3 | 1.333 | 0.702 | 0.300178 |
| flat | ep_height | 500 | ok | 9 | 8 | 1.125 | 0.788 | 1.478881 |
| flat | ep_area | 20 | ok | 1 | 1 | 1 | 0.288 | 0.002141 |
| flat | ep_area | 50 | ok | 1 | 1 | 1 | 0.668 | 0.029551 |
| flat | ep_area | 100 | ok | 2 | 2 | 1 | 0.724 | 0.102251 |
| flat | ep_area | 200 | ok | 4 | 3 | 1.333 | 0.702 | 0.379974 |
| flat | ep_area | 500 | ok | 9 | 8 | 1.25 | 0.763 | 2.175946 |
| flat | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.288 | 0.002363 |
| flat | ep_support_50 | 50 | ok | 1 | 1 | 1 | 0.668 | 0.02929 |
| flat | ep_support_50 | 100 | ok | 2 | 2 | 1 | 0.712 | 0.108525 |
| flat | ep_support_50 | 200 | ok | 4 | 3 | 1.333 | 0.702 | 0.361642 |
| flat | ep_support_50 | 500 | ok | 10 | 8 | 1.25 | 0.726 | 2.240404 |
| flat | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.288 | 0.002172 |
| flat | ep_support_90 | 50 | ok | 1 | 1 | 1 | 0.668 | 0.029007 |
| flat | ep_support_90 | 100 | ok | 3 | 2 | 1.5 | 0.484 | 0.107192 |
| flat | ep_support_90 | 200 | ok | 4 | 3 | 1.333 | 0.697 | 0.410349 |
| flat | ep_support_90 | 500 | ok | 10 | 8 | 1.25 | 0.724 | 2.299724 |
| flat | ep_support | 20 | ok | 1 | 1 | 1 | 0.288 | 0.002434 |
| flat | ep_support | 50 | ok | 1 | 1 | 1 | 0.663 | 0.02968 |
| flat | ep_support | 100 | ok | 2 | 2 | 1 | 0.704 | 0.096951 |
| flat | ep_support | 200 | ok | 4 | 3 | 1.333 | 0.702 | 0.386031 |
| flat | ep_support | 500 | ok | 10 | 8 | 1.25 | 0.711 | 2.390838 |
| flat | ep_support_weight | 20 | ok | 2 | 1 | 2 | 0.152 | 0.002548 |
| flat | ep_support_weight | 50 | ok | 2 | 1 | 2 | 0.298 | 0.021627 |
| flat | ep_support_weight | 100 | ok | 3 | 2 | 1.5 | 0.475 | 0.109504 |
| flat | ep_support_weight | 200 | ok | 5 | 3 | 1.667 | 0.562 | 0.376674 |
| flat | ep_support_weight | 500 | ok | 11 | 8 | 1.375 | 0.658 | 2.466672 |
| flat | ep_weight_support_weight | 20 | ok | 1 | 1 | 1 | 0.288 | 0.002353 |
| flat | ep_weight_support_weight | 50 | ok | 2 | 1 | 2 | 0.334 | 0.022091 |
| flat | ep_weight_support_weight | 100 | ok | 3 | 2 | 1.5 | 0.482 | 0.092432 |
| flat | ep_weight_support_weight | 200 | ok | 5 | 3 | 1.667 | 0.564 | 0.413552 |
| flat | ep_weight_support_weight | 500 | ok | 10 | 8 | 1.25 | 0.711 | 2.251125 |
| long | naive | 20 | ok | 2 | 1 | 2 | 0.047 | 0.000035 |
| long | naive | 50 | ok | 2 | 1 | 2 | 0.105 | 0.000075 |
| long | naive | 100 | ok | 4 | 1 | 4 | 0.097 | 0.000146 |
| long | naive | 200 | ok | 9 | 1 | 9 | 0.099 | 0.0004 |
| long | naive | 500 | ok | 21 | 3 | 7 | 0.102 | 0.000933 |
| long | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001785 |
| long | ep_volume_norot | 50 | ok | 1 | 1 | 1 | 0.21 | 0.015291 |
| long | ep_volume_norot | 100 | ok | 1 | 1 | 1 | 0.433 | 0.094116 |
| long | ep_volume_norot | 200 | ok | 2 | 1 | 2 | 0.444 | 0.372919 |
| long | ep_volume_norot | 500 | ok | 4 | 3 | 1.333 | 0.563 | 1.983811 |
| long | ep_volume | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001912 |
| long | ep_volume | 50 | ok | 1 | 1 | 1 | 0.21 | 0.017786 |
| long | ep_volume | 100 | ok | 1 | 1 | 1 | 0.433 | 0.115313 |
| long | ep_volume | 200 | ok | 2 | 1 | 2 | 0.444 | 0.788815 |
| long | ep_volume | 500 | ok | 3 | 3 | 1 | 0.719 | 5.326446 |
| long | ep_height | 20 | ok | 1 | 1 | 1 | 0.092 | 0.002162 |
| long | ep_height | 50 | ok | 1 | 1 | 1 | 0.21 | 0.018548 |
| long | ep_height | 100 | ok | 1 | 1 | 1 | 0.433 | 0.129998 |
| long | ep_height | 200 | ok | 2 | 1 | 2 | 0.444 | 1.226311 |
| long | ep_height | 500 | ok | 3 | 3 | 1 | 0.719 | 6.740941 |
| long | ep_area | 20 | ok | 1 | 1 | 1 | 0.092 | 0.002183 |
| long | ep_area | 50 | ok | 1 | 1 | 1 | 0.21 | 0.016445 |
| long | ep_area | 100 | ok | 1 | 1 | 1 | 0.433 | 0.12446 |
| long | ep_area | 200 | ok | 2 | 1 | 2 | 0.444 | 0.902691 |
| long | ep_area | 500 | ok | 3 | 3 | 1 | 0.719 | 6.193906 |
| long | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.092 | 0.002088 |
| long | ep_support_50 | 50 | ok | 1 | 1 | 1 | 0.21 | 0.020358 |
| long | ep_support_50 | 100 | ok | 1 | 1 | 1 | 0.433 | 0.139435 |
| long | ep_support_50 | 200 | ok | 2 | 1 | 2 | 0.444 | 0.894496 |
| long | ep_support_50 | 500 | ok | 3 | 3 | 1 | 0.681 | 5.868496 |
| long | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.092 | 0.002018 |
| long | ep_support_90 | 50 | ok | 1 | 1 | 1 | 0.21 | 0.019792 |
| long | ep_support_90 | 100 | ok | 1 | 1 | 1 | 0.433 | 0.146563 |
| long | ep_support_90 | 200 | ok | 2 | 1 | 2 | 0.444 | 0.938559 |
| long | ep_support_90 | 500 | ok | 4 | 3 | 1.333 | 0.563 | 6.621138 |
| long | ep_support | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001825 |
| long | ep_support | 50 | ok | 1 | 1 | 1 | 0.21 | 0.017122 |
| long | ep_support | 100 | ok | 1 | 1 | 1 | 0.433 | 0.123775 |
| long | ep_support | 200 | ok | 2 | 1 | 2 | 0.444 | 0.79168 |
| long | ep_support | 500 | ok | 3 | 3 | 1 | 0.681 | 5.806113 |
| long | ep_support_weight | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001654 |
| long | ep_support_weight | 50 | ok | 1 | 1 | 1 | 0.207 | 0.01636 |
| long | ep_support_weight | 100 | ok | 2 | 1 | 2 | 0.217 | 0.14157 |
| long | ep_support_weight | 200 | ok | 2 | 1 | 2 | 0.44 | 0.614966 |
| long | ep_support_weight | 500 | ok | 4 | 3 | 1.333 | 0.539 | 4.926638 |
| long | ep_weight_support_weight | 20 | ok | 1 | 1 | 1 | 0.092 | 0.001904 |
| long | ep_weight_support_weight | 50 | ok | 1 | 1 | 1 | 0.21 | 0.01524 |
| long | ep_weight_support_weight | 100 | ok | 1 | 1 | 1 | 0.433 | 0.100054 |
| long | ep_weight_support_weight | 200 | ok | 2 | 1 | 2 | 0.444 | 0.627812 |
| long | ep_weight_support_weight | 500 | ok | 4 | 3 | 1.333 | 0.563 | 5.074126 |
| mixed | naive | 20 | ok | 2 | 1 | 2 | 0.151 | 0.000031 |
| mixed | naive | 50 | ok | 3 | 1 | 3 | 0.179 | 0.000069 |
| mixed | naive | 100 | ok | 7 | 2 | 3.5 | 0.183 | 0.000136 |
| mixed | naive | 200 | ok | 14 | 3 | 4.667 | 0.198 | 0.000269 |
| mixed | naive | 500 | ok | 34 | 7 | 4.857 | 0.198 | 0.000682 |
| mixed | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.301 | 0.001644 |
| mixed | ep_volume_norot | 50 | ok | 1 | 1 | 1 | 0.525 | 0.013339 |
| mixed | ep_volume_norot | 100 | ok | 2 | 2 | 1 | 0.639 | 0.029233 |
| mixed | ep_volume_norot | 200 | ok | 4 | 3 | 1.333 | 0.679 | 0.082425 |
| mixed | ep_volume_norot | 500 | ok | 8 | 7 | 1.143 | 0.78 | 0.365381 |
| mixed | ep_volume | 20 | ok | 1 | 1 | 1 | 0.301 | 0.001932 |
| mixed | ep_volume | 50 | ok | 1 | 1 | 1 | 0.599 | 0.019243 |
| mixed | ep_volume | 100 | ok | 2 | 2 | 1 | 0.639 | 0.055131 |
| mixed | ep_volume | 200 | ok | 4 | 3 | 1.333 | 0.744 | 0.227128 |
| mixed | ep_volume | 500 | ok | 8 | 7 | 1.143 | 0.809 | 1.265697 |
| mixed | ep_height | 20 | ok | 1 | 1 | 1 | 0.301 | 0.001989 |
| mixed | ep_height | 50 | ok | 1 | 1 | 1 | 0.599 | 0.019155 |
| mixed | ep_height | 100 | ok | 2 | 2 | 1 | 0.639 | 0.073804 |
| mixed | ep_height | 200 | ok | 4 | 3 | 1.333 | 0.699 | 0.226239 |
| mixed | ep_height | 500 | ok | 8 | 7 | 1.143 | 0.809 | 1.078417 |
| mixed | ep_area | 20 | ok | 1 | 1 | 1 | 0.301 | 0.002063 |
| mixed | ep_area | 50 | ok | 1 | 1 | 1 | 0.599 | 0.020894 |
| mixed | ep_area | 100 | ok | 2 | 2 | 1 | 0.639 | 0.070442 |
| mixed | ep_area | 200 | ok | 4 | 3 | 1.333 | 0.699 | 0.225316 |
| mixed | ep_area | 500 | ok | 8 | 7 | 1.143 | 0.809 | 1.270316 |
| mixed | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.301 | 0.001853 |
| mixed | ep_support_50 | 50 | ok | 1 | 1 | 1 | 0.599 | 0.018181 |
| mixed | ep_support_50 | 100 | ok | 2 | 2 | 1 | 0.639 | 0.05948 |
| mixed | ep_support_50 | 200 | ok | 4 | 3 | 1.333 | 0.699 | 0.239512 |
| mixed | ep_support_50 | 500 | ok | 8 | 7 | 1.143 | 0.809 | 1.415528 |
| mixed | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.301 | 0.001856 |
| mixed | ep_support_90 | 50 | ok | 1 | 1 | 1 | 0.544 | 0.018269 |
| mixed | ep_support_90 | 100 | ok | 2 | 2 | 1 | 0.639 | 0.056253 |
| mixed | ep_support_90 | 200 | ok | 4 | 3 | 1.333 | 0.679 | 0.223307 |
| mixed | ep_support_90 | 500 | ok | 8 | 7 | 1.143 | 0.8 | 1.34361 |
| mixed | ep_support | 20 | ok | 1 | 1 | 1 | 0.301 | 0.001738 |
| mixed | ep_support | 50 | ok | 1 | 1 | 1 | 0.599 | 0.017097 |
| mixed | ep_support | 100 | ok | 2 | 2 | 1 | 0.639 | 0.055877 |
| mixed | ep_support | 200 | ok | 4 | 3 | 1.333 | 0.679 | 0.233107 |
| mixed | ep_support | 500 | ok | 8 | 7 | 1.143 | 0.8 | 1.504871 |
| mixed | ep_support_weight | 20 | ok | 1 | 1 | 1 | 0.301 | 0.002628 |
| mixed | ep_support_weight | 50 | ok | 2 | 1 | 2 | 0.3 | 0.018669 |
| mixed | ep_support_weight | 100 | ok | 3 | 2 | 1.5 | 0.431 | 0.071781 |
| mixed | ep_support_weight | 200 | ok | 4 | 3 | 1.333 | 0.607 | 0.247913 |
| mixed | ep_support_weight | 500 | ok | 9 | 7 | 1.286 | 0.747 | 1.533889 |
| mixed | ep_weight_support_weight | 20 | ok | 1 | 1 | 1 | 0.255 | 0.001922 |
| mixed | ep_weight_support_weight | 50 | ok | 2 | 1 | 2 | 0.342 | 0.01752 |
| mixed | ep_weight_support_weight | 100 | ok | 2 | 2 | 1 | 0.518 | 0.09033 |
| mixed | ep_weight_support_weight | 200 | ok | 4 | 3 | 1.333 | 0.679 | 0.283821 |
| mixed | ep_weight_support_weight | 500 | ok | 9 | 7 | 1.286 | 0.764 | 1.593264 |

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
| box_recommend | 200 | 0.47 | 0.466 | 55.0% | 0.0% | 0.488 | 2.24 |
| box_naive | 200 | 0.867 | 0.843 | 0.5% | 27.5% | 0.071 | 2.84 |

Not comparable with CJ Logistics' published figures (different items and catalog).
