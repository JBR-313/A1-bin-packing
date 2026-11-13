"""All experiment assumptions in one place (mirror changes in README "Assumptions")."""

C = 100          # 1D bin capacity
BASE_SEED = 2025  # instance seed = BASE_SEED + rep

MODES = {
    #          reps, per-run time limit (s)
    "quick": {"reps": 2, "timeout_s": 5.0},
    "default": {"reps": 5, "timeout_s": 60.0},
    "full": {"reps": 30, "timeout_s": 60.0},
}

DISTS_1D = ("uniform", "small", "large")

# Experiment A: exact vs greedy
A_N_SMALL = list(range(4, 25))          # 4..24
A_N_LARGE = [30, 50, 100, 150, 200]
A_N_EXHAUSTIVE = list(range(4, 13))     # 4..12
A_N_DP = A_N_SMALL                      # 4..24 (2^24 states ~ 0.5 GB RAM; do not go higher)
A_N_ALL = A_N_SMALL + A_N_LARGE         # FFD, MIP

# Experiment B: heuristics at scale
B_N = [10, 100, 1000, 10000]
B_MIP_TIME_LIMIT_S = {"quick": 5.0, "default": 10.0, "full": 10.0}
