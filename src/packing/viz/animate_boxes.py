"""Animated box search: watch the naive rule and the box recommendation try boxes.

One row per order, two panels per row (left: naive box choice, right: box
recommendation), all playing in sync. Each attempt from Result.trace becomes a short
scene:
    skip  -> the box outline and why it was skipped
    fail  -> items drop into the box one by one; the item that does not fit appears in
             red above the box: "✗ box · rule"
    ok    -> all items drop in: "✓ box · rule · void xx%"
Orders have at most ~15 items, so every frame simply carries the whole scene.
"""
from __future__ import annotations

from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from packing.threed.geometry import volume
from packing.types import Item3D, Result
from packing.viz.animate3d import _lines, _mesh
from packing.viz.view3d import bin_offset

DROP = 0.6           # items start this many box heights above their spot
HOLD_SKIP, HOLD_FAIL, HOLD_OK = 3, 5, 8   # frames to pause on each outcome
TRACES_PER_PANEL = 4  # outlines + item edges, placed items, falling item, failed item (red)
ROW_HEIGHT = 520


def box_anim_height(rows: int) -> int:
    return 110 + ROW_HEIGHT * rows + 60  # title + scenes + buttons/slider


def _dims(d) -> str:
    return "×".join(map(str, d))


def panel_states(items: list[Item3D], res: Result, drop_steps: int = 2) -> list[dict]:
    """Scene per frame for one search: outlines, placed boxes, falling, failed, status."""
    states = []
    item_vol = sum(volume(it) for it in items)
    for t in res.trace:
        dims, rule = t["dims"], t["rule"]
        head = f"{_dims(dims)}" + (f" · {rule}" if rule and rule != "naive" else "")
        if t["outcome"] == "skip":
            st = dict(outlines=[(0, 0, 0, *dims)], placed=[], falling=None, failed=None,
                      status=f"skip {_dims(dims)}: {t['reason']}")
            states += [st] * HOLD_SKIP
            continue
        nb = t["num_bins"] or 1
        outlines = [(*bin_offset(b, dims), 0, *dims) for b in range(nb)]
        by_id = {p.item_id: p for p in t["placements"]}
        placed = []
        for k, iid in enumerate(t["order"]):
            p = by_id[iid]
            dx, dy = bin_offset(p.bin_id, dims)
            final = (p.x + dx, p.y + dy, p.z, p.w, p.d, p.h, items[iid][3])
            for s in range(1, drop_steps + 1):
                lift = round(DROP * dims[2] * (1 - s / drop_steps), 1)
                fall = final[:2] + (final[2] + lift,) + final[3:]
                states.append(dict(outlines=outlines, placed=list(placed),
                                   falling=fall if s < drop_steps else None, failed=None,
                                   status=f"{head}: placing {k + 1} of {len(items)}"))
            placed.append(final)
            states[-1]["placed"] = list(placed)
        if t["outcome"] == "fail":
            w, d, h, wt = items[t["failed_item"]]
            failed = (0, 0, dims[2] + 2, w, d, h, wt)  # shown hovering above the box
            st = dict(outlines=outlines, placed=placed, falling=None, failed=failed,
                      status=f"✗ {head}: item {t['failed_item']} ({_dims((w, d, h))}) does not fit")
            states += [st] * HOLD_FAIL
        else:
            void = 1 - item_vol / (nb * volume(dims))
            split = f"{nb} boxes " if nb > 1 else ""
            st = dict(outlines=outlines, placed=placed, falling=None, failed=None,
                      status=f"✓ {split}{head} · void {void:.0%}")
            states += [st] * HOLD_OK
    return states


def _panel_traces(st: dict, wmax: int) -> list:
    lines = _lines(st["placed"] + ([st["falling"]] if st["falling"] else []))
    outl = _lines(st["outlines"], "rgba(60,60,60,0.9)")
    # one Scatter3d for outlines + item edges (NaN-free: just concatenate with a break)
    edges = go.Scatter3d(x=list(outl.x) + [None] + list(lines.x),
                         y=list(outl.y) + [None] + list(lines.y),
                         z=list(outl.z) + [None] + list(lines.z), mode="lines",
                         hoverinfo="skip", showlegend=False,
                         line=dict(color="rgba(50,50,50,0.75)", width=2))
    failed = _mesh([st["failed"]] if st["failed"] else [], wmax)
    failed.update(intensity=None, color="#e5383b", opacity=0.9)
    return [edges, _mesh(st["placed"], wmax),
            _mesh([st["falling"]] if st["falling"] else [], wmax), failed]


def build_box_search(orders: list[tuple[str, list[Item3D], Result, Result]], title: str,
                     drop_steps: int = 2, frame_ms: int = 110) -> go.Figure:
    """orders: (label, items, naive result with trace, recommendation result with trace)."""
    panels = []  # (title, items, states)
    for label, items, nv, rec in orders:
        panels.append((f"{label} — naive box choice", items, panel_states(items, nv, drop_steps)))
        panels.append((f"{label} — box recommendation", items, panel_states(items, rec, drop_steps)))
    total = max(len(s) for _, _, s in panels)
    for _, _, s in panels:  # pad: the shorter search waits on its final scene
        s += [s[-1]] * (total - len(s))

    rows = len(orders)
    fig = make_subplots(rows=rows, cols=2, specs=[[{"type": "scene"}] * 2] * rows,
                        subplot_titles=[t for t, _, _ in panels],
                        horizontal_spacing=0.02, vertical_spacing=0.08)
    base_ann = [a.to_plotly_json() for a in fig.layout.annotations]
    for k, (_, items, states) in enumerate(panels):
        wmax = max(it[3] for it in items)
        for tr in _panel_traces(states[0], wmax):
            fig.add_trace(tr, row=k // 2 + 1, col=k % 2 + 1)
        # fixed ranges: every box tried in this panel, plus the drop / failed-item space
        xs = [o[0] + o[3] for s in states for o in s["outlines"]]
        ys = [o[1] + o[4] for s in states for o in s["outlines"]]
        tops = [o[5] for s in states for o in s["outlines"]]
        tops += [s["failed"][2] + s["failed"][5] for s in states if s["failed"]]
        rx, ry = max(xs), max(ys)
        rz = max(max(tops), max(o[5] for s in states for o in s["outlines"]) * (1 + DROP))
        m = max(rx, ry, rz)
        scene = "scene" if k == 0 else f"scene{k + 1}"
        fig.layout[scene].update(
            xaxis=dict(range=[0, rx], title=""), yaxis=dict(range=[0, ry], title=""),
            zaxis=dict(range=[0, rz], title=""), aspectmode="manual",
            aspectratio=dict(x=rx / m, y=ry / m, z=rz / m))

    def annotations(t: int):
        out = []
        for a, (ptitle, _, states) in zip(base_ann, panels):
            st = states[t]["status"]
            color = "#c1121f" if st.startswith("✗") else "#2b9348" if st.startswith("✓") else "#444"
            out.append({**a, "text": f"<b>{ptitle}</b><br><span style='color:{color}'>{st}</span>"})
        return out

    fig.update_layout(annotations=annotations(0))
    fig.frames = [
        go.Frame(name=str(t), layout=go.Layout(annotations=annotations(t)),
                 data=[tr for _, items, states in panels
                       for tr in _panel_traces(states[t], max(it[3] for it in items))],
                 traces=list(range(TRACES_PER_PANEL * len(panels))))
        for t in range(total)
    ]
    play = dict(label="▶ Play", method="animate",
                args=[None, {"frame": {"duration": frame_ms, "redraw": True},
                             "fromcurrent": True, "transition": {"duration": 0}}])
    pause = dict(label="❚❚ Pause", method="animate",
                 args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}])
    steps = [dict(method="animate", label="", args=[[str(t)], {
        "frame": {"duration": 0, "redraw": True}, "mode": "immediate"}]) for t in range(total)]
    fig.update_layout(
        title=f"{title}  (colour = weight, red = item that does not fit)",
        height=box_anim_height(rows), margin=dict(l=0, r=0, t=110, b=0),
        updatemenus=[dict(type="buttons", direction="left", x=0.0, y=0.0, xanchor="left",
                          yanchor="top", buttons=[play, pause])],
        sliders=[dict(active=0, steps=steps, x=0.15, len=0.85, y=0.0,
                      currentvalue=dict(visible=False))])
    return fig


def write_box_search(path: Path, orders, title: str, **kw) -> Path:
    fig = build_box_search(orders, title, **kw)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(path, include_plotlyjs="cdn", auto_play=False)
    return path
