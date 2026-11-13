"""Run a solver with a hard time limit.

isolate=True: run in a fresh child process (multiprocessing "spawn") and kill it when
the limit passes. The clock (time.perf_counter) runs INSIDE the child around the solver
call only, so process start-up and imports are not counted. The limit starts after
the child reports it is ready.

isolate=False: run in this process (for fast polynomial heuristics where spawning a
process per run would cost more than the algorithm). A run longer than the limit is
still recorded as timeout afterwards.
"""
from __future__ import annotations

import multiprocessing as mp
import time
from typing import Callable

from packing.types import TIMEOUT, Result

_STARTUP_WAIT_S = 120.0


def _timed_call(func: Callable[..., Result], args: tuple, kwargs: dict) -> Result:
    t0 = time.perf_counter()
    res = func(*args, **kwargs)
    res.runtime_s = time.perf_counter() - t0
    return res


def _child(conn, func, args, kwargs) -> None:
    conn.send("ready")
    conn.send(_timed_call(func, args, kwargs))
    conn.close()


def run_with_timeout(func: Callable[..., Result], args: tuple = (), kwargs: dict | None = None,
                     timeout_s: float = 60.0, isolate: bool = True) -> Result:
    kwargs = kwargs or {}
    if not isolate:
        res = _timed_call(func, args, kwargs)
        if res.runtime_s > timeout_s:
            return Result(None, TIMEOUT, runtime_s=res.runtime_s, extra={"post_hoc": True})
        return res

    ctx = mp.get_context("spawn")
    recv, send = ctx.Pipe(duplex=False)
    proc = ctx.Process(target=_child, args=(send, func, args, kwargs), daemon=True)
    proc.start()
    send.close()
    try:
        if not recv.poll(_STARTUP_WAIT_S):
            raise RuntimeError("child process did not start")
        recv.recv()  # "ready"
        if recv.poll(timeout_s):
            return recv.recv()
        return Result(None, TIMEOUT, runtime_s=timeout_s)
    except EOFError:
        raise RuntimeError(f"solver process crashed (exit code {proc.exitcode})") from None
    finally:
        if proc.is_alive():
            proc.terminate()
        proc.join()
        recv.close()


def _debug_sleep(seconds: float) -> Result:
    """Used by tests to check that timeouts work."""
    time.sleep(seconds)
    return Result([])
