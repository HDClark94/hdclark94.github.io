"""
Temporary banner for the about page.

A wide, low-contrast field of overlapping planes in the same visual language as
the manifold schematic, so the front page has something deliberate on it until a
real photograph replaces it.

Drawn in 2D on purpose: mpl3d reserves fixed margins around its box, so at a
16:4.4 aspect the content bunches in the middle however hard you push
`set_box_aspect(zoom=...)`. Here the quads are parallelograms with a manual
skew, which reads as planes in perspective and fills the strip exactly.

To swap in a photo, drop the file in assets/img/ and point `banner:` in
_pages/about.md at it, then delete `banner_dark:`.

Run:  python3 scripts/banner.py [--png]
Out:  assets/img/banner-light.svg, assets/img/banner-dark.svg
"""

import pathlib
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "path"
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

W, H = 16.0, 4.4

THEMES = {
    "light": dict(surface="#fcfcfb", series=("#2a78d6", "#eb6834", "#1baf7a"),
                  neutral="#c2c1ba", alpha=0.15, line_alpha=0.34),
    "dark": dict(surface="#1a1a19", series=("#3987e5", "#d95926", "#199e70"),
                 neutral="#4e4e47", alpha=0.22, line_alpha=0.44),
}


def render(mode):
    T = THEMES[mode]
    rng = np.random.default_rng(11)

    fig = plt.figure(figsize=(W, H), facecolor=T["surface"])
    ax = fig.add_axes([0, 0, 1, 1], facecolor=T["surface"])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    palette = list(T["series"]) + [T["neutral"], T["neutral"]]
    for i in range(26):
        cx = rng.uniform(-0.5, W + 0.5)
        cy = rng.uniform(0.35, H - 0.35)
        length = rng.uniform(1.6, 5.2)
        width = rng.uniform(0.22, 0.85)
        angle = np.deg2rad(rng.uniform(-38, 38))
        skew = rng.uniform(-0.55, 0.55)  # stands in for perspective foreshortening

        u = np.array([np.cos(angle), np.sin(angle)])
        v = np.array([-np.sin(angle) + skew, np.cos(angle)])
        v = v / np.linalg.norm(v)
        c = np.array([cx, cy])
        quad = np.array([
            c - length / 2 * u - width / 2 * v,
            c + length / 2 * u - width / 2 * v,
            c + length / 2 * u + width / 2 * v,
            c - length / 2 * u + width / 2 * v,
        ])

        colour = palette[i % len(palette)]
        ax.add_patch(Polygon(quad, closed=True, facecolor=colour,
                             edgecolor="none", alpha=T["alpha"], zorder=i))
        ax.add_patch(Polygon(quad, closed=True, fill=False, edgecolor=colour,
                             linewidth=0.9, alpha=T["line_alpha"], zorder=i + 0.5))

    out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "img"
    fig.savefig(out / f"banner-{mode}.svg", format="svg", facecolor=T["surface"])
    print("wrote", out / f"banner-{mode}.svg")
    if "--png" in sys.argv:
        fig.savefig(out / f"banner-{mode}.png", dpi=110, facecolor=T["surface"])
    plt.close(fig)


for mode in ("light", "dark"):
    render(mode)
