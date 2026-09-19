"""
Schematic for /ideas/manifolds-in-disease/.

Cognition drawn as a set of rectangular manifolds intersecting at a common
origin. Three panels: a typical state, a disrupted state (contracted extent),
and a neuromodulated state (extent pushed past its default bound).

The manifolds are flat, zero-thickness planes drawn with transparency, so
crossing planes blend rather than occlude. Depth comes from the perspective
projection and from the planes' orientation, with no axes, panes or grid.

Draw order is pinned. `computed_zorder = False` disables matplotlib's
per-artist depth sort, so each manifold keeps the same explicit zorder in all
three panels; otherwise changing a plane's length changes its average depth and
the stacking flips between panels, which reads as the planes having swapped
places rather than changed size.

Each plane carries ticks along its principal axis whose *spacing* stands for
resolution. That is the non-obvious part of the figure: extending an axis
without adding capacity buys range at the cost of precision, so the extended
plane in panel C is drawn both longer and coarser.

Colours are categorical slots 1-4 of the validated reference palette
(blue / orange / aqua / violet), which clears the all-pairs CVD and
normal-vision separation floors on a light surface. Planes are direct-labelled
in panel A, satisfying the relief rule for the low-contrast aqua slot.

Run:  python3 scripts/manifold_schematic.py [--png]
Out:  assets/img/ideas/manifold-states.svg
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

FILL_ALPHA = 0.38  # transparent enough that crossing planes blend
LIGHT = np.array([0.45, 0.75, 0.50])
LIGHT = LIGHT / np.linalg.norm(LIGHT)

# label, colour, principal axis (length), width direction, half-len, half-wid, short
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


def shade(colour, facing, floor=0.78):
    """Mild orientation tint - enough to separate planes, not enough to muddy them."""
    rgb = np.array(matplotlib.colors.to_rgb(colour))
    k = floor + (1.0 - floor) * float(abs(facing))
    return tuple(np.clip(rgb * k, 0, 1))


def corners(u, v, half_len, half_wid):
    return [
        -half_len * u - half_wid * v,
        half_len * u - half_wid * v,
        half_len * u + half_wid * v,
        -half_len * u + half_wid * v,
    ]


def outline(u, v, half_len, half_wid):
    c = corners(u, v, half_len, half_wid)
    return [[c[i], c[(i + 1) % 4]] for i in range(4)]


def axis_ticks(u, v, half_len, half_wid, spacing):
    """Cross-lines along the principal axis; spacing encodes resolution."""
    segs, x = [], spacing
    while x < half_len - 1e-9:
        for s in (1, -1):
            segs.append([s * x * u - half_wid * v, s * x * u + half_wid * v])
        x += spacing
    return segs


def draw_plane(ax, u, v, n, half_len, half_wid, colour, spacing, z, dashed=False, ticks=True):
    ax.add_collection3d(
        Poly3DCollection(
            [corners(u, v, half_len, half_wid)],
            facecolor=shade(colour, np.dot(n, LIGHT)),
            edgecolor="none",
            alpha=FILL_ALPHA,
            zorder=z,
        )
    )
    if ticks:
        ax.add_collection3d(
            Line3DCollection(
                axis_ticks(u, v, half_len, half_wid, spacing),
                colors=colour,
                linewidths=0.7,
                alpha=0.7,
                zorder=z + 1,
            )
        )
    ax.add_collection3d(
        Line3DCollection(
            outline(u, v, half_len, half_wid),
            colors=colour,
            linewidths=1.5,
            linestyles=(0, (4, 2)) if dashed else "-",
            zorder=z + 2,
        )
    )


def draw_ghost(ax, u, v, half_len, half_wid, colour, z):
    ax.add_collection3d(
        Line3DCollection(
            outline(u, v, half_len, half_wid),
            colors=colour,
            linewidths=0.9,
            linestyles=(0, (1.5, 2.5)),
            alpha=0.6,
            zorder=z,
        )
    )


def panel(ax, subtitle, scales, spacings, ghosts, label=False):
    # Pinned draw order, identical in every panel.
    ax.computed_zorder = False

    for idx, (name, colour, axis, width_dir, half_len, half_wid, short) in enumerate(
        MANIFOLDS + [NEUROMOD]
    ):
        u, v, n = frame(axis, width_dir)
        k = scales.get(idx, 1.0)
        z = 10 + idx * 10
        if idx in ghosts:
            draw_ghost(ax, u, v, half_len, half_wid, colour, z - 4)
        draw_plane(
            ax, u, v, n, half_len * k, half_wid, colour,
            spacings.get(idx, TICK), z, dashed=(idx == 4), ticks=(idx != 4),
        )
        if label:
            tip = u * (half_len * k + 0.07)
            ax.text(
                tip[0], tip[1], tip[2], short,
                color=shade(colour, 0.0, floor=0.62), fontsize=7.8,
                ha="center", va="center", fontweight="bold", zorder=100, clip_on=False,
            )

    lim = 1.05
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    ax.set_box_aspect((1, 1, 1), zoom=1.28)
    ax.view_init(elev=22, azim=-58)
    ax.set_proj_type("persp", focal_length=0.42)  # real convergence, not near-flat
    ax.set_axis_off()
    ax.scatter([0], [0], [0], color=INK, s=13, depthshade=False, zorder=90)
    ax.text2D(
        0.5, 0.02, subtitle, transform=ax.transAxes, ha="center",
        color=INK_SOFT, fontsize=8.7,
    )


fig = plt.figure(figsize=(12.6, 4.4), facecolor=SURFACE)

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
        (i + 0.5) / 3, 0.965, title, ha="center", va="top",
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

fig.subplots_adjust(left=0.0, right=1.0, top=0.95, bottom=0.09, wspace=0.0)

out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "img" / "ideas"
out.mkdir(parents=True, exist_ok=True)
fig.savefig(out / "manifold-states.svg", format="svg", facecolor=SURFACE)
print("wrote", out / "manifold-states.svg")

# Raster copy is for eyeballing locally; only the SVG is committed.
if "--png" in sys.argv:
    fig.savefig(out / "manifold-states.png", dpi=200, facecolor=SURFACE)
    print("wrote", out / "manifold-states.png")
