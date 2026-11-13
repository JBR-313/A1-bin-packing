"""Shared data types for all packing algorithms."""
from __future__ import annotations

from dataclasses import dataclass, field

# status values
OK = "ok"              # finished; exact algorithms: proven optimal
FEASIBLE = "feasible"  # solver stopped at time limit with a valid (maybe non-optimal) answer
TIMEOUT = "timeout"    # no answer within the time limit
SKIPPED = "skipped"    # we refused to run (e.g. MIP model too large)


@dataclass
class Result:
    """Output of a 1D solver.

    bins: list of bins, each bin is a list of item indices (into `sizes`).
          None when there is no answer (timeout / skipped).
    runtime_s: wall time of the algorithm call only (set by the bench runner).
    """
    bins: list[list[int]] | None
    status: str = OK
    runtime_s: float = 0.0
    extra: dict = field(default_factory=dict)

    @property
    def num_bins(self) -> int | None:
        return None if self.bins is None else len(self.bins)
