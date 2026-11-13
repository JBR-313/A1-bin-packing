"""Practical exact method: Mixed Integer Programming with Google OR-Tools + SCIP.

Model (https://developers.google.com/optimization/pack/bin_packing):
    x[i][j] = 1 if item i goes to bin j,  y[j] = 1 if bin j is used
    min  sum_j y[j]
    s.t. sum_j x[i][j] = 1                 for every item i
         sum_i s_i x[i][j] <= C * y[j]     for every bin j
         y[j] >= y[j+1]                    (symmetry breaking: use bins in order)
Number of candidate bins = FFD result (an upper bound on OPT).

runtime_s (measured by the runner) includes model building; extra["model_build_s"]
reports that part separately.
"""
from __future__ import annotations

import time

from ortools.linear_solver import pywraplp

from packing.oned.heuristics import ffd
from packing.types import FEASIBLE, OK, SKIPPED, TIMEOUT, Result

MAX_N = 1000  # n * (#bins) variables; beyond this the model alone blows up memory


def solve(sizes: list[int], C: int, time_limit_s: float = 60.0, max_n: int = MAX_N) -> Result:
    n = len(sizes)
    if n == 0:
        return Result([])
    if n > max_n:
        return Result(None, SKIPPED, extra={"reason": f"n > {max_n}"})

    t0 = time.perf_counter()
    m = ffd(sizes, C).num_bins  # upper bound on bins
    solver = pywraplp.Solver.CreateSolver("SCIP")
    x = [[solver.BoolVar(f"x_{i}_{j}") for j in range(m)] for i in range(n)]
    y = [solver.BoolVar(f"y_{j}") for j in range(m)]
    for i in range(n):
        solver.Add(sum(x[i][j] for j in range(m)) == 1)
    for j in range(m):
        solver.Add(sum(sizes[i] * x[i][j] for i in range(n)) <= C * y[j])
    for j in range(m - 1):
        solver.Add(y[j] >= y[j + 1])
    solver.Minimize(sum(y))
    build_s = time.perf_counter() - t0

    solver.SetTimeLimit(int(time_limit_s * 1000))
    code = solver.Solve()
    extra = {"model_build_s": build_s, "num_vars": solver.NumVariables(), "ub_bins": m}

    if code not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        return Result(None, TIMEOUT, extra=extra)

    bins = [[i for i in range(n) if x[i][j].solution_value() > 0.5] for j in range(m)]
    bins = [b for b in bins if b]
    obj = len(bins)
    bound = solver.Objective().BestBound()
    extra["best_bound"] = bound
    extra["gap"] = (obj - bound) / obj
    return Result(bins, OK if code == pywraplp.Solver.OPTIMAL else FEASIBLE, extra=extra)
