"""3D Naive: stack items in arrival order, no rotation, one open bin at a time.

Fill a row along x; when the next item does not fit, start a new row behind it
(y += depth of the deepest item in the row); when the row does not fit, start a new
layer on top (z += height of the tallest item in the layer); when the layer does not
fit, close the bin and open a new one. Earlier bins are never revisited (like Next Fit).
"""
from __future__ import annotations

from packing.threed.geometry import fits_empty
from packing.types import Box, Item3D, Placement, Result


def pack(items: list[Item3D], box: Box) -> Result:
    W, D, H = box
    for i, it in enumerate(items):
        if not fits_empty(it, box, allow_rotation=False):
            raise ValueError(f"item {i} {it[:3]} does not fit container {box} without rotation")

    placements: list[Placement] = []
    bins: list[list[int]] = []
    x = y = z = 0
    row_d = layer_h = 0
    for i, (w, d, h, _wt) in enumerate(items):
        if bins and x + w > W:      # new row
            x, y, row_d = 0, y + row_d, 0
        if bins and y + d > D:      # new layer
            x, y, z, row_d, layer_h = 0, 0, z + layer_h, 0, 0
        if not bins or z + h > H:   # new bin
            bins.append([])
            x = y = z = row_d = layer_h = 0
        placements.append(Placement(i, len(bins) - 1, x, y, z, w, d, h))
        bins[-1].append(i)
        x += w
        row_d = max(row_d, d)
        layer_h = max(layer_h, h)
    return Result(bins, placements=placements, order=list(range(len(items))))
