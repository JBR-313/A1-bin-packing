"""Shared data types for all packing algorithms (1D and 3D)."""
from __future__ import annotations

from dataclasses import dataclass, field

# status values
OK = "ok"                  # finished; exact algorithms: proven optimal
FEASIBLE = "feasible"      # solver stopped at time limit with a valid (maybe non-optimal) answer
TIMEOUT = "timeout"        # no answer within the time limit
SKIPPED = "skipped"        # we refused to run (e.g. MIP model too large)
INFEASIBLE = "infeasible"  # does not fit within the allowed number of bins (3D, max_bins)

# 3D item = (w, d, h, weight); container = (W, D, H). All integers.
Item3D = tuple[int, int, int, int]
Box = tuple[int, int, int]


@dataclass(frozen=True)
class Placement:
    """Item `item_id` sits in bin `bin_id` with its min corner at (x, y, z) and
    (possibly rotated) size w × d × h along x, y, z."""
    item_id: int
    bin_id: int
    x: int
    y: int
    z: int
    w: int
    d: int
    h: int


@dataclass
class Result:
    """Output of any solver.

    bins: list of bins, each a list of item indices. None when there is no answer
          (timeout / skipped / infeasible).
    placements: 3D only — position and orientation of every item, sorted by item id.
    runtime_s: wall time of the algorithm call only (set by the bench runner).
    """
    bins: list[list[int]] | None
    status: str = OK
    runtime_s: float = 0.0
    extra: dict = field(default_factory=dict)
    placements: list[Placement] | None = None
    order: list[int] | None = None  # 3D: item ids in the order they were placed (animation)
    # box recommendation with trace=True: one dict per attempt (box, rule, outcome, partial
    # placements). Kept out of `extra` because extra is written to the CSV as JSON.
    trace: list[dict] | None = None

    @property
    def num_bins(self) -> int | None:
        return None if self.bins is None else len(self.bins)
