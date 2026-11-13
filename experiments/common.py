"""Command-line handling shared by the experiment scripts."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_DIR = ROOT / "results" / "csv"
FIG_DIR = ROOT / "results" / "figures"


def parse_mode(description: str) -> str:
    p = argparse.ArgumentParser(description=description)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--quick", action="store_true", help="2 reps, 5 s limit (minutes)")
    g.add_argument("--full", action="store_true", help="30 reps, 60 s limit")
    a = p.parse_args()
    return "quick" if a.quick else "full" if a.full else "default"
