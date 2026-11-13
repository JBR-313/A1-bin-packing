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

# Experiment C: 3D packing and loading
C3_CONTAINER = (100, 100, 100)
C3_DIM_RANGE = (5, 50)      # item size per axis
C3_WEIGHT_RANGE = (1, 20)   # integer weight
C3_SUPPORT_RATIO = 0.7      # share of the bottom face that must rest on items (assumption)
C3_SUPPORT_SENSITIVITY = (0.5, 0.9)  # extra thresholds run to show how much 70% matters
C3_DISTS = ("uniform", "flat", "long", "mixed")
# quick skips n=500 (EP takes ~2-6 s there in pure Python, over the 5 s quick limit)
C3_N = {"quick": [20, 50, 100, 200], "default": [20, 50, 100, 200, 500],
        "full": [20, 50, 100, 200, 500]}
C3_VIEW_DIST, C3_VIEW_N = "mixed", 100  # instance shown in the 3D HTML viewer

# Box recommendation
BOX_CATALOG = [(20, 15, 10), (30, 20, 15), (35, 25, 20), (40, 30, 25), (50, 40, 30), (60, 45, 40)]
ORDER_ITEMS = (3, 15)        # items per order
ORDER_DIM_RANGE = (3, 25)    # item size per axis in orders
NUM_ORDERS = 200
VOID_LIMIT = 0.5             # over-packing rule: void ratio <= 50%
