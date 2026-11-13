# Results summary (auto-generated — do not edit by hand)

Generated 2026-11-14 by `python -m experiments.summary`.

> **Warning:** contains `quick`-mode numbers (2 reps, 5 s limit). Do not put these in slides.

## Experiment C — 3D packing and loading (`quick` mode)

### Bins, fill rate and runtime per n

Container (100, 100, 100), item sides (5, 50), median over reps. `fill_rate` = item volume / (bins × container volume). Naive never rotates; all EP variants allow rotation.

| dist | algorithm | n | status | bins | L | bins_over_L | fill_rate | runtime_s |
|---|---|---|---|---|---|---|---|---|
| uniform | naive | 20 | ok | 2 | 1 | 2 | 0.226 | 0.000053 |
| uniform | naive | 50 | ok | 4 | 1 | 4 | 0.208 | 0.000098 |
| uniform | naive | 100 | ok | 7.5 | 3 | 2.5 | 0.285 | 0.000226 |
| uniform | naive | 200 | ok | 15 | 4.5 | 3.35 | 0.267 | 0.000371 |
| uniform | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.453 | 0.001654 |
| uniform | ep_volume_norot | 50 | ok | 2 | 1 | 2 | 0.416 | 0.009872 |
| uniform | ep_volume_norot | 100 | ok | 3 | 3 | 1 | 0.711 | 0.01972 |
| uniform | ep_volume_norot | 200 | ok | 5.5 | 4.5 | 1.225 | 0.73 | 0.054677 |
| uniform | ep_volume | 20 | ok | 1 | 1 | 1 | 0.453 | 0.002072 |
| uniform | ep_volume | 50 | ok | 1.5 | 1 | 1.5 | 0.615 | 0.018544 |
| uniform | ep_volume | 100 | ok | 3 | 3 | 1 | 0.711 | 0.041443 |
| uniform | ep_volume | 200 | ok | 5 | 4.5 | 1.125 | 0.8 | 0.144456 |
| uniform | ep_height | 20 | ok | 1 | 1 | 1 | 0.453 | 0.002293 |
| uniform | ep_height | 50 | ok | 2 | 1 | 2 | 0.416 | 0.019161 |
| uniform | ep_height | 100 | ok | 3 | 3 | 1 | 0.711 | 0.049083 |
| uniform | ep_height | 200 | ok | 5.5 | 4.5 | 1.225 | 0.73 | 0.194369 |
| uniform | ep_area | 20 | ok | 1 | 1 | 1 | 0.453 | 0.002846 |
| uniform | ep_area | 50 | ok | 1.5 | 1 | 1.5 | 0.615 | 0.019026 |
| uniform | ep_area | 100 | ok | 3 | 3 | 1 | 0.711 | 0.044605 |
| uniform | ep_area | 200 | ok | 5 | 4.5 | 1.125 | 0.8 | 0.151946 |
| uniform | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.453 | 0.002149 |
| uniform | ep_support_50 | 50 | ok | 1.5 | 1 | 1.5 | 0.615 | 0.022378 |
| uniform | ep_support_50 | 100 | ok | 3 | 3 | 1 | 0.711 | 0.043189 |
| uniform | ep_support_50 | 200 | ok | 5 | 4.5 | 1.125 | 0.8 | 0.162497 |
| uniform | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.453 | 0.002242 |
| uniform | ep_support_90 | 50 | ok | 2 | 1 | 2 | 0.416 | 0.020652 |
| uniform | ep_support_90 | 100 | ok | 3 | 3 | 1 | 0.711 | 0.044159 |
| uniform | ep_support_90 | 200 | ok | 5.5 | 4.5 | 1.225 | 0.73 | 0.168564 |
| uniform | ep_support | 20 | ok | 1 | 1 | 1 | 0.453 | 0.002252 |
| uniform | ep_support | 50 | ok | 2 | 1 | 2 | 0.416 | 0.022756 |
| uniform | ep_support | 100 | ok | 3 | 3 | 1 | 0.711 | 0.044503 |
| uniform | ep_support | 200 | ok | 5 | 4.5 | 1.125 | 0.8 | 0.165655 |
| uniform | ep_support_weight | 20 | ok | 1.5 | 1 | 1.5 | 0.326 | 0.003193 |
| uniform | ep_support_weight | 50 | ok | 2 | 1 | 2 | 0.416 | 0.021645 |
| uniform | ep_support_weight | 100 | ok | 4 | 3 | 1.333 | 0.533 | 0.051678 |
| uniform | ep_support_weight | 200 | ok | 6 | 4.5 | 1.35 | 0.667 | 0.195868 |
| uniform | ep_weight_support_weight | 20 | ok | 1.5 | 1 | 1.5 | 0.326 | 0.001971 |
| uniform | ep_weight_support_weight | 50 | ok | 2 | 1 | 2 | 0.416 | 0.017998 |
| uniform | ep_weight_support_weight | 100 | ok | 3 | 3 | 1 | 0.711 | 0.056522 |
| uniform | ep_weight_support_weight | 200 | ok | 6 | 4.5 | 1.35 | 0.667 | 0.225622 |
| flat | naive | 20 | ok | 1 | 1 | 1 | 0.257 | 0.000043 |
| flat | naive | 50 | ok | 2 | 1 | 2 | 0.319 | 0.000093 |
| flat | naive | 100 | ok | 4 | 2 | 2 | 0.363 | 0.000186 |
| flat | naive | 200 | ok | 7 | 3 | 2.333 | 0.409 | 0.00037 |
| flat | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.257 | 0.001946 |
| flat | ep_volume_norot | 50 | ok | 1.5 | 1 | 1.5 | 0.468 | 0.015126 |
| flat | ep_volume_norot | 100 | ok | 3 | 2 | 1.5 | 0.483 | 0.040699 |
| flat | ep_volume_norot | 200 | ok | 4.5 | 3 | 1.5 | 0.643 | 0.117938 |
| flat | ep_volume | 20 | ok | 1 | 1 | 1 | 0.257 | 0.001868 |
| flat | ep_volume | 50 | ok | 1 | 1 | 1 | 0.638 | 0.026764 |
| flat | ep_volume | 100 | ok | 2 | 2 | 1 | 0.725 | 0.087248 |
| flat | ep_volume | 200 | ok | 4 | 3 | 1.333 | 0.716 | 0.313757 |
| flat | ep_height | 20 | ok | 1 | 1 | 1 | 0.257 | 0.002067 |
| flat | ep_height | 50 | ok | 1.5 | 1 | 1.5 | 0.468 | 0.020495 |
| flat | ep_height | 100 | ok | 2 | 2 | 1 | 0.725 | 0.072533 |
| flat | ep_height | 200 | ok | 4 | 3 | 1.333 | 0.716 | 0.252974 |
| flat | ep_area | 20 | ok | 1 | 1 | 1 | 0.257 | 0.001999 |
| flat | ep_area | 50 | ok | 1 | 1 | 1 | 0.638 | 0.025001 |
| flat | ep_area | 100 | ok | 2 | 2 | 1 | 0.725 | 0.093008 |
| flat | ep_area | 200 | ok | 4 | 3 | 1.333 | 0.716 | 0.383107 |
| flat | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.257 | 0.001948 |
| flat | ep_support_50 | 50 | ok | 1 | 1 | 1 | 0.638 | 0.02972 |
| flat | ep_support_50 | 100 | ok | 2.5 | 2 | 1.25 | 0.604 | 0.099227 |
| flat | ep_support_50 | 200 | ok | 4 | 3 | 1.333 | 0.716 | 0.332063 |
| flat | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.257 | 0.001899 |
| flat | ep_support_90 | 50 | ok | 1 | 1 | 1 | 0.638 | 0.026287 |
| flat | ep_support_90 | 100 | ok | 3 | 2 | 1.5 | 0.483 | 0.097938 |
| flat | ep_support_90 | 200 | ok | 4.5 | 3 | 1.5 | 0.643 | 0.34992 |
| flat | ep_support | 20 | ok | 1 | 1 | 1 | 0.257 | 0.002159 |
| flat | ep_support | 50 | ok | 1.5 | 1 | 1.5 | 0.468 | 0.030521 |
| flat | ep_support | 100 | ok | 3 | 2 | 1.5 | 0.483 | 0.103635 |
| flat | ep_support | 200 | ok | 4 | 3 | 1.333 | 0.716 | 0.334737 |
| flat | ep_support_weight | 20 | ok | 1.5 | 1 | 1.5 | 0.187 | 0.002421 |
| flat | ep_support_weight | 50 | ok | 2.5 | 1 | 2.5 | 0.262 | 0.02075 |
| flat | ep_support_weight | 100 | ok | 3 | 2 | 1.5 | 0.483 | 0.097688 |
| flat | ep_support_weight | 200 | ok | 5 | 3 | 1.667 | 0.573 | 0.347434 |
| flat | ep_weight_support_weight | 20 | ok | 1 | 1 | 1 | 0.257 | 0.002296 |
| flat | ep_weight_support_weight | 50 | ok | 2 | 1 | 2 | 0.319 | 0.020306 |
| flat | ep_weight_support_weight | 100 | ok | 3 | 2 | 1.5 | 0.483 | 0.083352 |
| flat | ep_weight_support_weight | 200 | ok | 4.5 | 3 | 1.5 | 0.643 | 0.363547 |
| long | naive | 20 | ok | 1 | 1 | 1 | 0.089 | 0.000043 |
| long | naive | 50 | ok | 2.5 | 1 | 2.5 | 0.087 | 0.000094 |
| long | naive | 100 | ok | 4 | 1 | 4 | 0.104 | 0.000189 |
| long | naive | 200 | ok | 9 | 1 | 9 | 0.101 | 0.000375 |
| long | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.089 | 0.001576 |
| long | ep_volume_norot | 50 | ok | 1 | 1 | 1 | 0.209 | 0.012789 |
| long | ep_volume_norot | 100 | ok | 1 | 1 | 1 | 0.418 | 0.080952 |
| long | ep_volume_norot | 200 | ok | 2 | 1 | 2 | 0.456 | 0.328311 |
| long | ep_volume | 20 | ok | 1 | 1 | 1 | 0.089 | 0.001808 |
| long | ep_volume | 50 | ok | 1 | 1 | 1 | 0.209 | 0.01708 |
| long | ep_volume | 100 | ok | 1 | 1 | 1 | 0.418 | 0.101857 |
| long | ep_volume | 200 | ok | 2 | 1 | 2 | 0.456 | 0.68511 |
| long | ep_height | 20 | ok | 1 | 1 | 1 | 0.089 | 0.002126 |
| long | ep_height | 50 | ok | 1 | 1 | 1 | 0.209 | 0.016389 |
| long | ep_height | 100 | ok | 1 | 1 | 1 | 0.418 | 0.115959 |
| long | ep_height | 200 | ok | 2 | 1 | 2 | 0.456 | 0.885841 |
| long | ep_area | 20 | ok | 1 | 1 | 1 | 0.089 | 0.001935 |
| long | ep_area | 50 | ok | 1 | 1 | 1 | 0.209 | 0.016377 |
| long | ep_area | 100 | ok | 1 | 1 | 1 | 0.418 | 0.107033 |
| long | ep_area | 200 | ok | 2 | 1 | 2 | 0.456 | 0.777289 |
| long | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.089 | 0.001785 |
| long | ep_support_50 | 50 | ok | 1 | 1 | 1 | 0.209 | 0.016962 |
| long | ep_support_50 | 100 | ok | 1 | 1 | 1 | 0.418 | 0.11144 |
| long | ep_support_50 | 200 | ok | 2 | 1 | 2 | 0.456 | 0.691748 |
| long | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.089 | 0.001828 |
| long | ep_support_90 | 50 | ok | 1 | 1 | 1 | 0.209 | 0.016074 |
| long | ep_support_90 | 100 | ok | 1 | 1 | 1 | 0.418 | 0.112318 |
| long | ep_support_90 | 200 | ok | 2 | 1 | 2 | 0.456 | 0.726393 |
| long | ep_support | 20 | ok | 1 | 1 | 1 | 0.089 | 0.001794 |
| long | ep_support | 50 | ok | 1 | 1 | 1 | 0.209 | 0.016745 |
| long | ep_support | 100 | ok | 1 | 1 | 1 | 0.418 | 0.114017 |
| long | ep_support | 200 | ok | 2 | 1 | 2 | 0.456 | 0.686306 |
| long | ep_support_weight | 20 | ok | 1 | 1 | 1 | 0.089 | 0.001785 |
| long | ep_support_weight | 50 | ok | 1.5 | 1 | 1.5 | 0.156 | 0.020149 |
| long | ep_support_weight | 100 | ok | 2 | 1 | 2 | 0.209 | 0.15861 |
| long | ep_support_weight | 200 | ok | 2 | 1 | 2 | 0.456 | 0.696303 |
| long | ep_weight_support_weight | 20 | ok | 1 | 1 | 1 | 0.089 | 0.00202 |
| long | ep_weight_support_weight | 50 | ok | 1 | 1 | 1 | 0.209 | 0.016083 |
| long | ep_weight_support_weight | 100 | ok | 1 | 1 | 1 | 0.418 | 0.111585 |
| long | ep_weight_support_weight | 200 | ok | 2 | 1 | 2 | 0.456 | 0.744541 |
| mixed | naive | 20 | ok | 2 | 1 | 2 | 0.139 | 0.000042 |
| mixed | naive | 50 | ok | 3.5 | 1 | 3.5 | 0.176 | 0.000091 |
| mixed | naive | 100 | ok | 7 | 2 | 3.5 | 0.177 | 0.000181 |
| mixed | naive | 200 | ok | 14.5 | 3 | 4.833 | 0.18 | 0.000358 |
| mixed | ep_volume_norot | 20 | ok | 1 | 1 | 1 | 0.278 | 0.001823 |
| mixed | ep_volume_norot | 50 | ok | 1 | 1 | 1 | 0.614 | 0.014132 |
| mixed | ep_volume_norot | 100 | ok | 2 | 2 | 1 | 0.621 | 0.031173 |
| mixed | ep_volume_norot | 200 | ok | 4 | 3 | 1.333 | 0.653 | 0.101636 |
| mixed | ep_volume | 20 | ok | 1 | 1 | 1 | 0.278 | 0.002071 |
| mixed | ep_volume | 50 | ok | 1 | 1 | 1 | 0.614 | 0.024011 |
| mixed | ep_volume | 100 | ok | 2 | 2 | 1 | 0.621 | 0.061302 |
| mixed | ep_volume | 200 | ok | 3.5 | 3 | 1.167 | 0.754 | 0.263841 |
| mixed | ep_height | 20 | ok | 1 | 1 | 1 | 0.278 | 0.001928 |
| mixed | ep_height | 50 | ok | 1 | 1 | 1 | 0.614 | 0.02192 |
| mixed | ep_height | 100 | ok | 2 | 2 | 1 | 0.621 | 0.080356 |
| mixed | ep_height | 200 | ok | 3.5 | 3 | 1.167 | 0.754 | 0.273554 |
| mixed | ep_area | 20 | ok | 1 | 1 | 1 | 0.278 | 0.002121 |
| mixed | ep_area | 50 | ok | 1 | 1 | 1 | 0.614 | 0.022518 |
| mixed | ep_area | 100 | ok | 2 | 2 | 1 | 0.621 | 0.071724 |
| mixed | ep_area | 200 | ok | 3.5 | 3 | 1.167 | 0.754 | 0.249865 |
| mixed | ep_support_50 | 20 | ok | 1 | 1 | 1 | 0.278 | 0.002098 |
| mixed | ep_support_50 | 50 | ok | 1 | 1 | 1 | 0.614 | 0.020527 |
| mixed | ep_support_50 | 100 | ok | 2 | 2 | 1 | 0.621 | 0.066129 |
| mixed | ep_support_50 | 200 | ok | 3.5 | 3 | 1.167 | 0.754 | 0.258968 |
| mixed | ep_support_90 | 20 | ok | 1 | 1 | 1 | 0.278 | 0.002178 |
| mixed | ep_support_90 | 50 | ok | 1.5 | 1 | 1.5 | 0.443 | 0.019348 |
| mixed | ep_support_90 | 100 | ok | 2 | 2 | 1 | 0.621 | 0.060998 |
| mixed | ep_support_90 | 200 | ok | 4 | 3 | 1.333 | 0.653 | 0.286863 |
| mixed | ep_support | 20 | ok | 1 | 1 | 1 | 0.278 | 0.002124 |
| mixed | ep_support | 50 | ok | 1 | 1 | 1 | 0.614 | 0.020791 |
| mixed | ep_support | 100 | ok | 2 | 2 | 1 | 0.621 | 0.063724 |
| mixed | ep_support | 200 | ok | 4 | 3 | 1.333 | 0.653 | 0.279391 |
| mixed | ep_support_weight | 20 | ok | 1 | 1 | 1 | 0.278 | 0.003031 |
| mixed | ep_support_weight | 50 | ok | 2 | 1 | 2 | 0.307 | 0.025625 |
| mixed | ep_support_weight | 100 | ok | 3 | 2 | 1.5 | 0.414 | 0.082449 |
| mixed | ep_support_weight | 200 | ok | 4 | 3 | 1.333 | 0.653 | 0.310936 |
| mixed | ep_weight_support_weight | 20 | ok | 1 | 1 | 1 | 0.278 | 0.001936 |
| mixed | ep_weight_support_weight | 50 | ok | 2 | 1 | 2 | 0.307 | 0.019433 |
| mixed | ep_weight_support_weight | 100 | ok | 2.5 | 2 | 1.25 | 0.513 | 0.091922 |
| mixed | ep_weight_support_weight | 200 | ok | 4 | 3 | 1.333 | 0.653 | 0.332388 |

### Cost of loading constraints

Same instances, EP sorted by volume with vs without constraints. `increase_pct` = sum(bins with) / sum(bins without) − 1 over all n and seeds. Support threshold 70% is an assumption.

| variant | dist | instances | bins_ep_volume | bins_variant | increase_pct | share_needing_more_bins |
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
| ep_weight_support_weight | flat | 8 | 16 | 21 | 31.2 | 62% |
| ep_weight_support_weight | long | 8 | 10 | 10 | 0 | 0% |
| ep_weight_support_weight | mixed | 8 | 15 | 19 | 26.7 | 50% |
| ep_weight_support_weight | uniform | 8 | 21 | 25 | 19 | 50% |
| ep_weight_support_weight | all | 32 | 62 | 75 | 21 | 41% |

### Sensitivity of the support threshold

Extra bins vs plain EP for support thresholds 50% / 70% / 90% (same instances, same method as above).

| variant | dist | instances | bins_ep_volume | bins_variant | increase_pct | share_needing_more_bins |
|---|---|---|---|---|---|---|
| ep_support_50 | all | 32 | 62 | 63 | 1.6 | 3% |
| ep_support | all | 32 | 62 | 67 | 8.1 | 16% |
| ep_support_90 | all | 32 | 62 | 69 | 11.3 | 22% |

| variant | dist | instances | bins_ep_volume | bins_variant | increase_pct | share_needing_more_bins |
|---|---|---|---|---|---|---|
| ep_support_50 | flat | 8 | 16 | 17 | 6.2 | 12% |
| ep_support_50 | long | 8 | 10 | 10 | 0 | 0% |
| ep_support_50 | mixed | 8 | 15 | 15 | 0 | 0% |
| ep_support_50 | uniform | 8 | 21 | 21 | 0 | 0% |
| ep_support | flat | 8 | 16 | 19 | 18.8 | 38% |
| ep_support | long | 8 | 10 | 10 | 0 | 0% |
| ep_support | mixed | 8 | 15 | 16 | 6.7 | 12% |
| ep_support | uniform | 8 | 21 | 22 | 4.8 | 12% |
| ep_support_90 | flat | 8 | 16 | 19 | 18.8 | 38% |
| ep_support_90 | long | 8 | 10 | 10 | 0 | 0% |
| ep_support_90 | mixed | 8 | 15 | 17 | 13.3 | 25% |
| ep_support_90 | uniform | 8 | 21 | 23 | 9.5 | 25% |

### How much of the Naive → EP gap is rotation?

Extra bins vs EP with rotation (sort by volume). `ep_volume_norot` = same EP without rotation; `naive` = 3D Naive (no rotation). The gap between the two rows is the algorithm; the gap between `ep_volume_norot` and 0% is rotation.

| variant | dist | instances | bins_ep_volume | bins_variant | increase_pct | share_needing_more_bins |
|---|---|---|---|---|---|---|
| ep_volume_norot | flat | 8 | 16 | 20 | 25 | 50% |
| ep_volume_norot | long | 8 | 10 | 10 | 0 | 0% |
| ep_volume_norot | mixed | 8 | 15 | 16 | 6.7 | 12% |
| ep_volume_norot | uniform | 8 | 21 | 23 | 9.5 | 25% |
| ep_volume_norot | all | 32 | 62 | 69 | 11.3 | 22% |
| naive | flat | 8 | 16 | 28 | 75 | 75% |
| naive | long | 8 | 10 | 33 | 230 | 75% |
| naive | mixed | 8 | 15 | 54 | 260 | 100% |
| naive | uniform | 8 | 21 | 57 | 171.4 | 100% |
| naive | all | 32 | 62 | 172 | 177.4 | 88% |

### Box choice per order

200 orders of 3–15 items (sides (3, 25)), catalog [(20, 15, 10), (30, 20, 15), (35, 25, 20), (40, 30, 25), (50, 40, 30), (60, 45, 40)]. void = 1 − item volume / box volume used. `share_split` = orders that needed more than one box. `tries` = packing attempts per order (multi-start cost; included in runtime).

| algorithm | orders | void_median | void_mean | share_void_le_50 | share_split | runtime_ms_median | tries_mean |
|---|---|---|---|---|---|---|---|
| box_recommend | 200 | 0.47 | 0.466 | 55.0% | 0.0% | 0.581 | 2.24 |
| box_naive | 200 | 0.867 | 0.843 | 0.5% | 27.5% | 0.091 | 2.84 |

Not comparable with CJ Logistics' published figures (different items and catalog).

### Multi-start vs a single sort rule

Same orders. The recommendation tries every sort rule in a box before moving to a bigger box (multi-start); the other rows use only one rule. `orders_multistart_smaller` = orders where multi-start chose a box with less volume than that single rule (`_larger`: the opposite; EP is a heuristic, so this is not guaranteed to be 0).

| method | sort rules | void_median | share_void_le_50 | tries_mean | orders_multistart_smaller | orders_multistart_larger |
|---|---|---|---|---|---|---|
| box_recommend | all 3 | 0.47 | 55.0% | 2.24 | - | - |
| box_recommend_volume | volume | 0.516 | 48.5% | 1.45 | 14 | 0 |
| box_recommend_height | height | 0.555 | 35.5% | 1.58 | 41 | 0 |
| box_recommend_area | area | 0.541 | 40.5% | 1.54 | 31 | 0 |
