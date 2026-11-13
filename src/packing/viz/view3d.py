"""Interactive 3D viewer: writes a standalone plotly HTML with panels side by side.

Each panel shows the first few bins of one packing, laid out left to right.
Item colour = weight (light = light, dark = heavy) so heavy-below can be checked by eye.
Hover over an item to see its id, size and weight.
"""
from __future__ import annotations

from pathlib import Path

import plotly.graph_objects as go
from plotly.colors import sample_colorscale
from plotly.subplots import make_subplots

from packing.types import Box, Item3D, Result

# 12 triangles of a box, as indices into its 8 corners
_TRI_I = [0, 0, 4, 4, 0, 0, 2, 2, 0, 0, 1, 1]
_TRI_J = [1, 2, 5, 6, 1, 5, 3, 7, 3, 7, 2, 6]
_TRI_K = [2, 3, 6, 7, 5, 4, 7, 6, 7, 4, 6, 5]
_EDGES = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
          (0, 4), (1, 5), (2, 6), (3, 7)]


def _corners(x, y, z, w, d, h):
    return [(x, y, z), (x + w, y, z), (x + w, y + d, z), (x, y + d, z),
            (x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)]


def _panel_traces(items: list[Item3D], box: Box, res: Result, max_bins: int):
    gap = box[0] * 0.25
    wmax = max((it[3] for it in items), default=1)
    vx, vy, vz, I, J, K, colors, hover = [], [], [], [], [], [], [], []
    ex, ey, ez = [], [], []

    def add_edges(cs):
        for a, b in _EDGES:
            ex.extend([cs[a][0], cs[b][0], None])
            ey.extend([cs[a][1], cs[b][1], None])
            ez.extend([cs[a][2], cs[b][2], None])

    shown = min(res.num_bins or 0, max_bins)
    for b in range(shown):  # container outlines
        add_edges(_corners(b * (box[0] + gap), 0, 0, *box))
    for p in res.placements or []:
        if p.bin_id >= shown:
            continue
        off = p.bin_id * (box[0] + gap)
        cs = _corners(p.x + off, p.y, p.z, p.w, p.d, p.h)
        base = len(vx)
        for c in cs:
            vx.append(c[0]); vy.append(c[1]); vz.append(c[2])
            hover.append(f"item {p.item_id}<br>{p.w}×{p.d}×{p.h}<br>weight {items[p.item_id][3]}")
        I += [base + i for i in _TRI_I]
        J += [base + j for j in _TRI_J]
        K += [base + k for k in _TRI_K]
        col = sample_colorscale("YlOrRd", [0.15 + 0.85 * items[p.item_id][3] / wmax])[0]
        colors += [col] * 12
        add_edges(cs)
    mesh = go.Mesh3d(x=vx, y=vy, z=vz, i=I, j=J, k=K, facecolor=colors, opacity=0.95,
                     hovertext=hover, hoverinfo="text", flatshading=True, showscale=False)
    lines = go.Scatter3d(x=ex, y=ey, z=ez, mode="lines", hoverinfo="skip",
                         line=dict(color="rgba(40,40,40,0.6)", width=2), showlegend=False)
    return [mesh, lines], shown


def write_comparison(path: Path, panels: list[tuple[str, list[Item3D], Box, Result]],
                     title: str, max_bins: int = 3) -> Path:
    """panels: (title, items, container, result). One 3D scene per panel."""
    fig = make_subplots(rows=1, cols=len(panels), specs=[[{"type": "scene"}] * len(panels)],
                        subplot_titles=[f"{t}<br>{r.num_bins} bins" for t, _, _, r in panels],
                        horizontal_spacing=0.02)
    for c, (_, items, box, res) in enumerate(panels, start=1):
        traces, shown = _panel_traces(items, box, res, max_bins)
        for tr in traces:
            fig.add_trace(tr, row=1, col=c)
        scene = "scene" if c == 1 else f"scene{c}"
        fig.layout[scene].update(aspectmode="data", xaxis_title="x", yaxis_title="y",
                                 zaxis_title="z")
    fig.update_layout(title=f"{title}  (first {max_bins} bins shown; colour = weight)",
                      height=650, margin=dict(l=0, r=0, t=90, b=0))
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(path, include_plotlyjs="cdn")
    return path
