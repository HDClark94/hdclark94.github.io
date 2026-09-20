# Asset generation scripts

Everything in `assets/` that is generated rather than photographed or drawn by
hand is produced by a script in this directory. The generated files are
committed, so the site builds without running any of this — you only need these
when you want to **change** a figure rather than recreate it from scratch.

This directory is listed under `exclude:` in `_config.yml`, so it is tracked in
git but never published to the site.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
```

## The scripts

| Script                  | Produces                                            | Re-run when                                            |
| ----------------------- | --------------------------------------------------- | ------------------------------------------------------ |
| `manifold_schematic.py` | `assets/img/ideas/manifold-states-{light,dark}.svg` | Changing the manifold figure on the disease ideas page |
| `banner.py`             | `assets/img/banner-{light,dark}.svg`                | Changing the about-page banner placeholder             |
| `fetch_github.py`       | `_data/github.yml`                                  | Adding a repository, or to refresh stars/followers     |

Each takes `--png` (except `fetch_github.py`) to additionally write a raster
copy for eyeballing locally. Those PNGs are gitignored; only the SVGs are
served.

```bash
make assets          # regenerate everything
make figures         # just the manifold schematic
make banner          # just the banner
make github          # just refresh _data/github.yml
```

## Output is deterministic

Regenerating an unchanged figure produces a **byte-identical** file, so any diff
in git means the design actually changed. This is not matplotlib's default and
takes three deliberate measures:

- `svg.hashsalt` is pinned, so element ids are derived from a fixed salt rather
  than a random uuid.
- `metadata={"Date": None}` on save, so no timestamp is embedded.
- The banner's patches use `clip_on=False`. The axes already fills the whole
  figure so the clip is redundant, and matplotlib derives clip-path ids
  unstably — leaving it on produced a spurious ~100-line diff on every run.

If you change a script and get a much larger diff than you expected, check these
first.

## Decisions baked into the figures

These are easy to undo by accident, so they are worth knowing before editing.

### Colours are validated, not chosen by eye

Both figure scripts use a categorical palette checked against colour-vision
deficiency and normal-vision separation floors on each background:

| Slot     | Light     | Dark      |
| -------- | --------- | --------- |
| 1 blue   | `#2a78d6` | `#3987e5` |
| 2 orange | `#eb6834` | `#d95926` |
| 3 aqua   | `#1baf7a` | `#199e70` |

Light and dark are **separately selected steps of the same hues**, not an
automatic flip — a colour that passes on white frequently fails on near-black.

**The manifold figure carries three manifolds plus a neutral grey, not four
manifolds, and this is deliberate.** A fourth categorical hue cannot clear the
all-pairs separation floors against the dark background with this palette: dark
violet against dark blue scores ΔE 1.9 for protanopia, which is effectively
identical. If you add a fourth manifold, it needs a different palette rather
than a fourth colour bolted on.

The aqua slot sits below 3:1 contrast on the light background, which is why the
planes carry direct labels in the first panel rather than relying on the legend
alone. Keep the labels if you keep the colour.

### The manifold schematic

- **Planes, not solids.** Zero-thickness quads with transparent fills so
  crossing manifolds blend rather than occlude.
- **Draw order is pinned.** `computed_zorder = False` plus an explicit `zorder`
  per manifold. Without it, changing a plane's length changes its average depth
  and matplotlib re-sorts, so the stacking flips between panels — which reads as
  the manifolds having swapped places rather than changed size. This is the
  single most important line in the file.
- **Tick spacing encodes resolution.** Plane length is representational extent;
  the ticks ruled across each plane are spaced by precision. That is what makes
  the third panel say "range bought at the cost of precision" rather than
  "bigger is better". Do not widen a plane without widening its ticks.
- No axes, panes or grid; depth comes from the perspective projection alone.

### The banner

Drawn in **2D**, deliberately. `mpl3d` reserves fixed margins around its box, so
at a 16:4.4 aspect the content bunches in the middle however hard you push
`set_box_aspect(zoom=...)`. The quads are parallelograms with a manual skew,
which reads as planes in perspective and fills the strip exactly.

It is a placeholder. To replace it with a photograph: drop the file in
`assets/img/`, point `banner:` in `_pages/about.md` at it, and delete
`banner_dark:`. The layout handles a single image fine. Sizing is
`object-fit: cover` so a photo crops sensibly at any width.

### The GitHub cards

`_data/github.yml` exists because the repositories page used to hotlink cards
from `github-readme-stats.vercel.app` and `github-profile-trophy.vercel.app`.
Both went down — 503 and 402 respectively — taking every image on the page with
them. The cards are now rendered by the site itself from this data, styled
against the theme's CSS variables so they follow the light/dark toggle.

`fetch_github.py` reads the user and repo lists from `_data/repositories.yml`,
so **that file stays the only place you edit**. Add a repo there, re-run the
script, commit both files.

It uses the unauthenticated GitHub API (60 requests/hour), which is ample for a
handful of repositories.

## Theme-aware images

Anything baked into an image file cannot follow the CSS light/dark toggle, so
the figures and banner ship in both themes and are swapped with the classes the
theme already provides:

```html
<img src="...-light.svg" class="repo-img-light" /> <img src="...-dark.svg" class="repo-img-dark" />
```

`repo-img-light` / `repo-img-dark` are defined in `_sass/_themes.scss` and
switch on `html[data-theme="dark"]`. Both files download, so use this for
figures rather than for large photographs.
