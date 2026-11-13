"""Repeat runs over (distribution, n, rep), apply the timeout rule, write a CSV.

Timeout rule: if ANY rep of (algorithm, dist, n) times out, that n is recorded as
timeout and all larger n are skipped for that algorithm and distribution.

The same loop serves 1D and 3D; a `Problem` says how to generate an instance, call a
solver, validate its answer and compute the lower bound / fill rate.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable

import pandas as pd

from packing.bench.timeout import run_with_timeout
from packing.bounds import lower_bound_1d, validate_1d
from packing.generators import gen_1d
from packing.types import TIMEOUT, Result

COLUMNS = ["experiment", "algorithm", "dist", "n", "seed", "rep", "num_bins", "lower_bound",
           "opt", "runtime_s", "status", "fill_rate", "extra_json"]


@dataclass
class AlgoSpec:
    func: Callable
    ns: list[int]
    exact: bool = False          # proven-optimal when status == "ok"
    isolate: bool = True         # run in a killable child process
    kwargs: dict = field(default_factory=dict)
    hard_timeout_s: float | None = None  # defaults to the mode's timeout


@dataclass
class Problem:
    gen: Callable[[int, str, int], Any]                  # (n, dist, seed) -> instance
    args: Callable[[Any], tuple]                         # instance -> solver positional args
    validate: Callable[[Any, Result, AlgoSpec], None]    # raise if the answer is invalid
    lower_bound: Callable[[Any], int]
    fill_rate: Callable[[Any, int], float]               # (instance, bins) -> used share


def problem_1d(C: int) -> Problem:
    return Problem(
        gen=lambda n, dist, seed: gen_1d(n, C, dist, seed),
        args=lambda sizes: (sizes, C),
        validate=lambda sizes, res, spec: validate_1d(sizes, C, res.bins),
        lower_bound=lambda sizes: lower_bound_1d(sizes, C),
        fill_rate=lambda sizes, k: sum(sizes) / (k * C),
    )


def sweep(experiment: str, problem: Problem, algos: dict[str, AlgoSpec], dists, reps: int,
          base_seed: int, timeout_s: float) -> pd.DataFrame:
    rows = []
    for dist in dists:
        for name, spec in algos.items():
            limit = spec.hard_timeout_s or timeout_s
            for n in spec.ns:
                timed_out = False
                for rep in range(reps):
                    seed = base_seed + rep
                    inst = problem.gen(n, dist, seed)
                    res = run_with_timeout(spec.func, problem.args(inst), spec.kwargs, limit,
                                           spec.isolate)
                    if res.bins is not None:
                        problem.validate(inst, res, spec)
                    k = res.num_bins
                    rows.append({
                        "experiment": experiment, "algorithm": name, "dist": dist, "n": n,
                        "seed": seed, "rep": rep, "num_bins": k,
                        "lower_bound": problem.lower_bound(inst), "opt": None,
                        "runtime_s": res.runtime_s, "status": res.status,
                        "fill_rate": problem.fill_rate(inst, k) if k else None,
                        "extra_json": json.dumps(res.extra),
                    })
                    if res.status == TIMEOUT:
                        timed_out = True
                        break
                print(f"[{experiment}] {dist:8s} {name:18s} n={n:<6d} "
                      f"{'TIMEOUT' if timed_out else rows[-1]['status']:8s} "
                      f"last={rows[-1]['runtime_s']:.3f}s", flush=True)
                if timed_out:
                    break
    df = pd.DataFrame(rows, columns=COLUMNS)
    return fill_opt(df, [n for n, s in algos.items() if s.exact])


def sweep_1d(experiment: str, algos: dict[str, AlgoSpec], dists, reps: int, base_seed: int,
             timeout_s: float, C: int) -> pd.DataFrame:
    return sweep(experiment, problem_1d(C), algos, dists, reps, base_seed, timeout_s)


def fill_opt(df: pd.DataFrame, exact_algos: list[str]) -> pd.DataFrame:
    """opt = bin count proven optimal by any exact algorithm on the same instance.
    If two exact algorithms disagree, that is a bug -> stop."""
    key = ["dist", "n", "seed"]
    ok = df[df.algorithm.isin(exact_algos) & (df.status == "ok")]
    agg = ok.groupby(key)["num_bins"].agg(["min", "max"])
    bad = agg[agg["min"] != agg["max"]]
    if len(bad):
        raise AssertionError(f"exact algorithms disagree (bug!):\n{bad}")
    opt = agg["min"].rename("opt_fill")
    df = df.drop(columns="opt").join(opt, on=key).rename(columns={"opt_fill": "opt"})
    df["opt"] = df["opt"].astype("Int64")
    df["num_bins"] = df["num_bins"].astype("Int64")
    return df[COLUMNS]
