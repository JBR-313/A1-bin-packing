"""Animated 3D packing: items drop from above into their final spot, one at a time.

Several packings of the SAME item set are shown side by side and play in sync:
in every panel, item k falls for `drop_steps` frames and then lands. Items appear in
the order each algorithm placed them (Result.order): Naive shows arrival order, EP its
sorted order.

Size control (an HTML file holds every frame):
  * each panel has separate traces for "placed items" (+ their edges) and "the falling
    item";
    a frame only carries the traces that change, so the (large) placed-items trace
    is stored only on landing frames, the falling item (one box) on the others;
  * container outlines are a static trace, never repeated in frames;
  * colour is one number (weight) per triangle on a colour scale, no hover text;
  * axis ranges are fixed so the camera does not jump between frames.
The slider jumps only to landing frames, which always carry the full placed state.
"""
from __future__ import annotations

from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from packing.types import Box, Item3D, Result
from packing.viz.view3d import _EDGES, _TRI_I, _TRI_J, _TRI_K, _corners, bin_offset

DROP_HEIGHT = 0.6  # items start this many container heights above their final spot
TRACES_PER_PANEL = 4  # 0: outlines (static), 1: placed items, 2: their edges, 3: falling item


def landing_boxes(items: list[Item3D], box: Box, res: Result):
    """Final boxes (x, y, z, w, d, h, weight) in world coordinates, in placement order."""
    by_id = {p.item_id: p for p in res.placements}
    out = []
    for iid in res.order:
        p = by_id[iid]
        dx, dy = bin_offset(p.bin_id, box)
        out.append((p.x + dx, p.y + dy, p.z, p.w, p.d, p.h, items[iid][3]))
    return out


def frame_boxes(items: list[Item3D], box: Box, res: Result, drop_steps: int = 3):
    """Full scene per frame (placed boxes + falling box), for tests and inspection.
    The last frame is exactly the final packing."""
    final = landing_boxes(items, box, res)
    frames = []
    for k, f in enumerate(final):
        for s in range(1, drop_steps + 1):
            lift = round(DROP_HEIGHT * box[2] * (1 - s / drop_steps))
            frames.append(final[:k] + [f[:2] + (f[2] + lift,) + f[3:]])
    return frames


def _mesh(boxes, wmax: int) -> go.Mesh3d:
    vx, vy, vz, I, J, K, inten = [], [], [], [], [], [], []
    for x, y, z, w, d, h, wt in boxes:
        base = len(vx)
        for c in _corners(x, y, z, w, d, h):
            vx.append(c[0]); vy.append(c[1]); vz.append(c[2])
        I += [base + i for i in _TRI_I]
        J += [base + j for j in _TRI_J]
        K += [base + k for k in _TRI_K]
        inten += [wt] * 12
    return go.Mesh3d(x=vx, y=vy, z=vz, i=I, j=J, k=K, intensity=inten, intensitymode="cell",
                     colorscale="YlOrRd", cmin=0, cmax=wmax, showscale=False, opacity=0.95,
                     flatshading=True, hoverinfo="skip")


def _lines(boxes, color="rgba(40,40,40,0.6)") -> go.Scatter3d:
    ex, ey, ez = [], [], []
    for x, y, z, w, d, h, *_ in boxes:
        cs = _corners(x, y, z, w, d, h)
        for a, b in _EDGES:
            ex += [cs[a][0], cs[b][0], None]
            ey += [cs[a][1], cs[b][1], None]
            ez += [cs[a][2], cs[b][2], None]
    return go.Scatter3d(x=ex, y=ey, z=ez, mode="lines", hoverinfo="skip", showlegend=False,
                        line=dict(color=color, width=2))


def build_animation(panels: list[tuple[str, list[Item3D], Box, Result]], title: str,
                    drop_steps: int = 3, frame_ms: int = 60) -> go.Figure:
    """panels: (title, items, container, result); all panels must pack the same items."""
    n = len(panels[0][1])
    assert all(len(p[1]) == n for p in panels), "panels must use the same item set"
    finals = [landing_boxes(items, box, res) for _, items, box, res in panels]
    wmax = max(it[3] for it in panels[0][1])

    fig = make_subplots(rows=1, cols=len(panels), specs=[[{"type": "scene"}] * len(panels)],
                        subplot_titles=[f"{t}: {r.num_bins} bins" for t, _, _, r in panels],
                        horizontal_spacing=0.02)
    for c, (_, items, box, res) in enumerate(panels, start=1):
        outl = [(*bin_offset(b, box), 0, *box) for b in range(res.num_bins)]
        fig.add_trace(_lines(outl, "rgba(80,80,80,0.8)"), row=1, col=c)  # static
        fig.add_trace(_mesh([], wmax), row=1, col=c)   # placed items
        fig.add_trace(_lines([]), row=1, col=c)        # their edges
        fig.add_trace(_mesh([], wmax), row=1, col=c)   # falling item
        rx = max(o[0] + o[3] for o in outl)
        ry = max(o[1] + o[4] for o in outl)
        top = box[2] * (1 + DROP_HEIGHT)
        m = max(rx, ry, top)
        scene = "scene" if c == 1 else f"scene{c}"
        fig.layout[scene].update(
            xaxis=dict(range=[0, rx], title="x"), yaxis=dict(range=[0, ry], title="y"),
            zaxis=dict(range=[0, top], title="z"), aspectmode="manual",
            aspectratio=dict(x=rx / m, y=ry / m, z=top / m))

    frames = []
    for k in range(n):
        for s in range(1, drop_steps + 1):
            data, idx = [], []
            for p, final in enumerate(finals):
                base = p * TRACES_PER_PANEL
                f = final[k]
                if s < drop_steps:  # falling: only the single falling box changes
                    lift = round(DROP_HEIGHT * panels[p][2][2] * (1 - s / drop_steps))
                    data.append(_mesh([f[:2] + (f[2] + lift,) + f[3:]], wmax))
                    idx.append(base + 3)
                else:  # landed: placed set grows by one, falling trace empties
                    placed = final[:k + 1]
                    data += [_mesh(placed, wmax), _lines(placed), _mesh([], wmax)]
                    idx += [base + 1, base + 2, base + 3]
            frames.append(go.Frame(name=f"{k}-{s}", data=data, traces=idx))
    fig.frames = frames

    play = dict(label="▶ Play", method="animate",
                args=[None, {"frame": {"duration": frame_ms, "redraw": True},
                             "fromcurrent": True, "transition": {"duration": 0}}])
    pause = dict(label="❚❚ Pause", method="animate",
                 args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}])
    steps = [dict(method="animate", label=str(k + 1),
                  args=[[f"{k}-{drop_steps}"],
                        {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}])
             for k in range(n)]  # landing frames only: they carry the full placed state
    fig.update_layout(
        title=f"{title}  (colour = weight)", height=700, margin=dict(l=0, r=0, t=90, b=0),
        updatemenus=[dict(type="buttons", direction="left", x=0.0, y=0.0, xanchor="left",
                          yanchor="top", buttons=[play, pause])],
        sliders=[dict(active=0, steps=steps, x=0.15, len=0.85, y=0.0,
                      currentvalue=dict(prefix="items placed: "))])
    return fig


def write_animation(path: Path, panels, title: str, drop_steps: int = 3,
                    frame_ms: int = 60) -> Path:
    fig = build_animation(panels, title, drop_steps, frame_ms)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(path, include_plotlyjs="cdn", auto_play=False)
    return path
