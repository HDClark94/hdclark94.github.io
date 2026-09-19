"""
Schematic for /ideas/manifolds-in-disease/.

Cognition drawn as a set of rectangular manifolds intersecting at a common
origin. Three panels: a typical state, a disrupted state (contracted extent),
and a neuromodulated state (extent pushed past its default bound).

Each plane carries ticks along its principal axis whose *spacing* stands for
resolution. That is the non-obvious part of the figure: extending an axis
without adding capacity buys range at the cost of precision, so the extended
plane in panel C is drawn both longer and coarser.

Colours are categorical slots 1-4 of the validated reference palette
(blue / orange / aqua / violet), which clears the all-pairs CVD and
normal-vision separation floors on a light surface. Planes are direct-labelled
in panel A, satisfying the relief rule for the low-contrast aqua slot.

Run:  python3 scripts/manifold_schematic.py
Out:  assets/img/ideas/manifold-states.svg  (+ .png fallback)
"""

import pathlib
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"  # embed glyphs so rendering is stable
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SOFT = "#52514e"
GHOST = "#b6b5af"
PANE = "#f2f2ee"
PANE_EDGE = "#dededa"
GRIDLINE = "#e4e3dd"

THICK = 0.042  # slab half-thickness: gives each manifold visible side faces
LIGHT = np.array([0.45, 0.75, 0.50])  # key light direction
LIGHT = LIGHT / np.linalg.norm(LIGHT)


def shade(colour, facing):
    """Lambertian-ish tint: face-on reads light, edge-on reads dark."""
    rgb = np.array(matplotlib.colors.to_rgb(colour))
    k = 0.58 + 0.42 * float(abs(facing))
    return tuple(np.clip(rgb * k + (1.0 - k) * 0.16, 0, 1))

# label, colour, principal axis (length), width direction, half-len, half-wid
MANIFOLDS = [
    ("spatial coding", "#2a78d6", (1.00, 0.08, 0.10), (0.00, 0.30, 1.00), 1.00, 0.17, "spatial"),
    ("episodic memory", "#eb6834", (0.10, 1.00, 0.06), (0.00, 0.00, 1.00), 0.94, 0.16, "episodic"),
    ("reward valuation", "#1baf7a", (0.06, 0.10, 1.00), (1.00, 0.20, 0.00), 0.88, 0.15, "reward"),
    ("attentional selection", "#4a3aa7", (0.80, 0.66, -0.52), (0.30, -0.60, -0.30), 0.86, 0.15, "attention"),
]
NEUROMOD = ("neuromodulatory tone", "#93928c", (-0.70, 0.58, 0.62), (0.60, 0.75, -0.02), 0.78, 0.13, "neuromod.")

TICK = 0.16  # default spacing between axis ticks = default resolution


def frame(axis, width_dir):
    """Orthonormal (u, v, n): u along the principal axis, v across, n normal."""
    u = np.array(axis, float)
    u /= np.linalg.norm(u)
    v = np.array(width_dir, float)
    v = v - np.dot(v, u) * u
    v /= np.linalg.norm(v)
    return u, v, np.cross(u, v)


def slab_faces(u, v, n, half_len, half_wid, nu=13, nv=2):
    """A thin box as (quad, outward normal) pairs.

    The broad faces are tessellated so matplotlib's per-polygon depth sort
    behaves where slabs intersect; the four narrow sides are what make the
    solid read as solid.
    """
    us = np.linspace(-half_len, half_len, nu + 1)
    vs = np.linspace(-half_wid, half_wid, nv + 1)
    t = THICK * n
    faces = []
    for sign in (1, -1):
        for i in range(nu):
            for j in range(nv):
                faces.append((
                    [
                        us[i] * u + vs[j] * v + sign * t,
                        us[i + 1] * u + vs[j] * v + sign * t,
                        us[i + 1] * u + vs[j + 1] * v + sign * t,
                        us[i] * u + vs[j + 1] * v + sign * t,
                    ],
                    sign * n,
                ))
    for sign in (1, -1):  # ends
        e = sign * half_len * u
        faces.append((
            [e - half_wid * v - t, e + half_wid * v - t,
             e + half_wid * v + t, e - half_wid * v + t],
            sign * u,
        ))
    for sign in (1, -1):  # long sides
        w = sign * half_wid * v
        faces.append((
            [w - half_len * u - t, w + half_len * u - t,
             w + half_len * u + t, w - half_len * u + t],
            sign * v,
        ))
    return faces


def outline(u, v, half_len, half_wid):
    c = [
        -half_len * u - half_wid * v,
        half_len * u - half_wid * v,
        half_len * u + half_wid * v,
        -half_len * u + half_wid * v,
    ]
    return [[c[i], c[(i + 1) % 4]] for i in range(4)]


def axis_ticks(u, v, half_len, half_wid, spacing):
    """Cross-lines along the principal axis; spacing encodes resolution."""
    segs, x = [], spacing
    while x < half_len - 1e-9:
        for s in (1, -1):
            segs.append([s * x * u - half_wid * v, s * x * u + half_wid * v])
        x += spacing
    return segs


def draw_plane(ax, u, v, n, half_len, half_wid, colour, spacing, dashed=False, ticks=True):
    faces = slab_faces(u, v, n, half_len, half_wid)
    polys = [f for f, _ in faces]
    colours = [shade(colour, np.dot(nn, LIGHT)) for _, nn in faces]
    ax.add_collection3d(
        Poly3DCollection(
            polys,
            facecolors=colours,
            edgecolor="none",
            alpha=0.80,
            zsort="average",
        )
    )
    for sign in (1, -1):
        ax.add_collection3d(
            Line3DCollection(
                [[a + sign * THICK * n, b + sign * THICK * n]
                 for a, b in outline(u, v, half_len, half_wid)],
                colors=colour,
                linewidths=1.1,
                linestyles=(0, (4, 2)) if dashed else "-",
            )
        )
    if ticks:
        segs = axis_ticks(u, v, half_len, half_wid, spacing)
        for sign in (1, -1):
            ax.add_collection3d(
                Line3DCollection(
                    [[a + sign * THICK * n, b + sign * THICK * n] for a, b in segs],
                    colors=shade(colour, 0.0),
                    linewidths=0.85,
                    alpha=0.95,
                )
            )


def draw_ghost(ax, u, v, half_len, half_wid, colour=GHOST):
    ax.add_collection3d(
        Line3DCollection(
            outline(u, v, half_len, half_wid),
            colors=colour,
            linewidths=0.9,
            linestyles=(0, (1.5, 2.5)),
            alpha=0.55,
        )
    )


def panel(ax, subtitle, scales, spacings, ghosts, label=False):
    entries = MANIFOLDS + [NEUROMOD]
    for idx, (name, colour, axis, width_dir, half_len, half_wid, short) in enumerate(entries):
        u, v, n = frame(axis, width_dir)
        k = scales.get(idx, 1.0)
        if idx in ghosts:
            draw_ghost(ax, u, v, half_len, half_wid, colour)
        draw_plane(
            ax, u, v, n, half_len * k, half_wid, colour,
            spacings.get(idx, TICK), dashed=(idx == 4), ticks=(idx != 4),
        )
        if label:
            tip = u * (half_len * k + 0.07)
            ax.text(
                tip[0], tip[1], tip[2], short,
                color=shade(colour, 0.0), fontsize=7.8, ha="center", va="center",
                fontweight="bold", zorder=30, clip_on=False,
            )

    lim = 1.05
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    ax.set_box_aspect((1, 1, 1), zoom=1.16)
    ax.view_init(elev=22, azim=-58)
    ax.set_proj_type("persp", focal_length=0.42)  # real convergence, not near-flat

    # A faint room: panes and grid give the eye something to read depth against.
    for pane_axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        pane_axis.pane.set_facecolor(PANE)
        pane_axis.pane.set_edgecolor(PANE_EDGE)
        pane_axis.pane.set_alpha(1.0)
        pane_axis._axinfo["grid"].update(color=GRIDLINE, linewidth=0.6)
        pane_axis.line.set_color(PANE_EDGE)
    ax.grid(True)
    for setter in (ax.set_xticks, ax.set_yticks, ax.set_zticks):
        setter([-1, -0.5, 0, 0.5, 1])
    for setter in (ax.set_xticklabels, ax.set_yticklabels, ax.set_zticklabels):
        setter([])
    ax.tick_params(length=0)
    ax.scatter([0], [0], [0], color=INK, s=13, depthshade=False)
    ax.text2D(
        0.5, -0.02, subtitle, transform=ax.transAxes, ha="center",
        color=INK_SOFT, fontsize=8.7,
    )


fig = plt.figure(figsize=(12.6, 4.5), facecolor=SURFACE)

specs = [
    ("Typical", "default extent, default resolution", {}, {}, set(), True),
    ("Disrupted", "two manifolds contract; spacing unchanged", {0: 0.50, 1: 0.38}, {}, {0, 1}, False),
    ("Neuromodulated", "one axis extends past its bound; ticks coarsen",
     {2: 1.36, 4: 1.28}, {2: TICK * 1.55}, {2, 4}, False),
]

for i, (title, subtitle, scales, spacings, ghosts, label) in enumerate(specs):
    ax = fig.add_subplot(1, 3, i + 1, projection="3d", facecolor=SURFACE)
    panel(ax, subtitle, scales, spacings, ghosts, label=label)
    fig.text(
        (i + 0.5) / 3, 0.945, title, ha="center", va="top",
        color=INK, fontsize=12, fontweight="semibold",
    )

handles = [
    plt.Line2D([], [], color=c, lw=3, ls=(0, (4, 2)) if n == NEUROMOD[0] else "-", label=n)
    for n, c, *_ in MANIFOLDS + [NEUROMOD]
] + [plt.Line2D([], [], color=GHOST, lw=1, ls=(0, (1.5, 2.5)), label="default extent")]

fig.legend(
    handles=handles, loc="lower center", ncol=6, frameon=False, fontsize=8.8,
    labelcolor=INK_SOFT, bbox_to_anchor=(0.5, 0.005), handlelength=2.1,
    columnspacing=1.6,
)

fig.subplots_adjust(left=0.0, right=1.0, top=0.93, bottom=0.10, wspace=0.0)

out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "img" / "ideas"
out.mkdir(parents=True, exist_ok=True)
fig.savefig(out / "manifold-states.svg", format="svg", facecolor=SURFACE)
print("wrote", out / "manifold-states.svg")

# Raster copy is for eyeballing locally; only the SVG is committed.
if "--png" in sys.argv:
    fig.savefig(out / "manifold-states.png", dpi=200, facecolor=SURFACE)
    print("wrote", out / "manifold-states.png")
