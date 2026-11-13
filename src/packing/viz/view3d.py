"""Interactive 3D viewer: writes a standalone plotly HTML with panels side by side.

Each panel shows the bins of one packing on a grid (at most PER_ROW bins per row).
Item colour = weight (light = light, dark = heavy) so heavy-below can be checked by eye.
Hover over an item to see its id, size and weight.
"""
from __future__ import annotations

from pathlib import Path

import plotly.graph_objects as go
from plotly.colors import sample_colorscale
from plotly.subplots import make_subplots

from packing.types import Box, Item3D, Result

PER_ROW = 4  # bins per row in the grid layout

# 12 triangles of a box, as indices into its 8 corners
_TRI_I = [0, 0, 4, 4, 0, 0, 2, 2, 0, 0, 1, 1]
_TRI_J = [1, 2, 5, 6, 1, 5, 3, 7, 3, 7, 2, 6]
_TRI_K = [2, 3, 6, 7, 5, 4, 7, 6, 7, 4, 6, 5]
_EDGES = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
          (0, 4), (1, 5), (2, 6), (3, 7)]


def _corners(x, y, z, w, d, h):
    return [(x, y, z), (x + w, y, z), (x + w, y + d, z), (x, y + d, z),
            (x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)]


def bin_offset(bin_id: int, box: Box) -> tuple[float, float]:
    """(dx, dy) of a bin in the grid: PER_ROW bins along x, then the next row along y."""
    gap = 0.25 * box[0]
    return (bin_id % PER_ROW) * (box[0] + gap), (bin_id // PER_ROW) * (box[1] + gap)


def item_color(weight: int, wmax: int) -> str:
    return sample_colorscale("YlOrRd", [0.15 + 0.85 * weight / max(wmax, 1)])[0]


def box_traces(boxes, wmax: int, outlines=()) -> list:
    """boxes: (x, y, z, w, d, h, item_id, weight) in world coordinates.
    outlines: (x, y, z, w, d, h) drawn as wireframe only (containers).
    Returns [Mesh3d, Scatter3d]; both always exist (possibly empty) so animation
    frames can replace them one-for-one."""
    vx, vy, vz, I, J, K, colors, hover = [], [], [], [], [], [], [], []
    ex, ey, ez = [], [], []

    def add_edges(cs):
        for a, b in _EDGES:
            ex.extend([cs[a][0], cs[b][0], None])
            ey.extend([cs[a][1], cs[b][1], None])
            ez.extend([cs[a][2], cs[b][2], None])

    for o in outlines:
        add_edges(_corners(*o))
    for x, y, z, w, d, h, iid, wt in boxes:
        cs = _corners(x, y, z, w, d, h)
        base = len(vx)
        for c in cs:
            vx.append(c[0]); vy.append(c[1]); vz.append(c[2])
            hover.append(f"item {iid}<br>{w}×{d}×{h}<br>weight {wt}")
        I += [base + i for i in _TRI_I]
        J += [base + j for j in _TRI_J]
        K += [base + k for k in _TRI_K]
        colors += [item_color(wt, wmax)] * 12
        add_edges(cs)
    mesh = go.Mesh3d(x=vx, y=vy, z=vz, i=I, j=J, k=K, facecolor=colors, opacity=0.95,
                     hovertext=hover, hoverinfo="text", flatshading=True, showscale=False)
    lines = go.Scatter3d(x=ex, y=ey, z=ez, mode="lines", hoverinfo="skip",
                         line=dict(color="rgba(40,40,40,0.6)", width=2), showlegend=False)
    return [mesh, lines]


def container_outlines(box: Box, num_bins: int):
    return [(*bin_offset(b, box), 0, *box) for b in range(num_bins)]


def world_boxes(items: list[Item3D], box: Box, placements, shown: int):
    out = []
    for p in placements:
        if p.bin_id < shown:
            dx, dy = bin_offset(p.bin_id, box)
            out.append((p.x + dx, p.y + dy, p.z, p.w, p.d, p.h, p.item_id, items[p.item_id][3]))
    return out


def write_comparison(path: Path, panels: list[tuple[str, list[Item3D], Box, Result]],
                     title: str, max_bins: int | None = None) -> Path:
    """panels: (title, items, container, result). One 3D scene per panel.
    max_bins=None shows every bin (grid of PER_ROW per row)."""
    fig = make_subplots(rows=1, cols=len(panels), specs=[[{"type": "scene"}] * len(panels)],
                        subplot_titles=[f"{t}<br>{r.num_bins} bins" for t, _, _, r in panels],
                        horizontal_spacing=0.02)
    for c, (_, items, box, res) in enumerate(panels, start=1):
        shown = res.num_bins if max_bins is None else min(res.num_bins, max_bins)
        wmax = max((it[3] for it in items), default=1)
        for tr in box_traces(world_boxes(items, box, res.placements, shown), wmax,
                             container_outlines(box, shown)):
            fig.add_trace(tr, row=1, col=c)
        scene = "scene" if c == 1 else f"scene{c}"
        fig.layout[scene].update(aspectmode="data", xaxis_title="x", yaxis_title="y",
                                 zaxis_title="z")
    note = "all bins shown" if max_bins is None else f"first {max_bins} bins shown"
    fig.update_layout(title=f"{title}  ({note}; colour = weight)",
                      height=700, margin=dict(l=0, r=0, t=90, b=0))
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(path, include_plotlyjs="cdn")
    return path
