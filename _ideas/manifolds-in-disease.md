---
layout: post
title: Cognition as overlapping manifolds, and what disease does to the geometry
date: 2026-09-19
description: If cognition is a set of manifolds sharing a state space, disease is a change in the geometry of particular ones and neuromodulation is a change in their bounds. Drawing it makes the vague parts obvious.
tags: [manifolds, neuromodulation, disease, representation-geometry]
toc:
  sidebar: left
---

> These are working notes, not a position I am committed to. Sections marked
> **Conjecture** are speculation I have not tested.

## The picture

Take the manifold framing seriously across the whole brain rather than one
circuit at a time. Cognition is then a large set of manifolds sharing a state
space: a spatial code, an episodic code, a valuation code, an attentional
selection code, and so on. They intersect, because the same neurons participate
in more than one, and each has an extent — a range over which it can represent
distinctions.

On that picture, two things follow immediately. **Disease** is not a global
failure but a change in the geometry of particular manifolds, leaving others
intact. **Neuromodulation** changes the bounds of a manifold rather than its
identity — the same code, operating over a different range.

<div class="row mt-3 mb-1">
  <div class="col-sm-12">
    <img
      src="{{ '/assets/img/ideas/manifold-states.svg' | relative_url }}"
      class="img-fluid rounded"
      alt="Three 3D panels, each showing five transparent rectangular planes intersecting at a common origin at different angles. In the typical panel the five labelled planes sit at default lengths. In the disrupted panel the spatial and episodic planes are visibly shorter, with dotted outlines marking the extent they had before. In the neuromodulated panel the reward valuation and neuromodulatory planes extend past their dotted default outlines, and the tick marks ruled across them are more widely spaced."
    />
  </div>
</div>
<div class="caption">
  Each plane is a manifold, intersecting the others at a common origin. Plane
  length is representational extent; the ticks ruled across each plane are spaced
  by resolution. <strong>Disrupted</strong>: two manifolds contract while tick
  spacing stays fixed, so fewer distinctions fit. <strong>Neuromodulated</strong>:
  one axis is driven past its default bound and the ticks coarsen — range is
  bought with precision. Dotted outlines mark default extent. Schematic, not data.
</div>

The neuromodulatory plane is drawn dashed because it has an ambiguous status,
which is the most interesting part of the idea and is taken up below.

## What drawing it actually commits you to

The value of making the figure is that it forces decisions that prose lets you
dodge. Three of them are worth flagging before the picture gets used for
anything.

**Planes through a common origin means linear subspaces sharing a zero.** That
is a strong claim. It implies a privileged "null" state that all manifolds pass
through, and that manifolds are flat. Real neural manifolds are curved, and
often have topology that no plane has — the grid torus being the obvious case
([Gardner et al. 2022](https://doi.org/10.1038/s41586-021-04268-7)). The figure
is a cartoon of _relationships between extents_, not of the manifolds themselves.

**"Overlapping" in the figure is intersection, not superposition.** Two planes
crossing share a line — a genuinely shared set of states. That is a different
claim from two codes occupying the same space with minimal interference, which
is what superposition means. Both are real; they are not the same thing, and the
figure only shows the first.

**Extent and resolution are separate quantities.** This is why the ticks are in
the figure at all. A plane can be long and coarse or short and fine, and those
are different clinical pictures.

## What "shortened" could mean

The figure encodes disease as a contracted plane. That reads as one claim but is
at least three, and they are experimentally distinguishable.

> **Conjecture — decompose the contraction.** A manifold can lose capacity in
> three ways, with different behavioural signatures:
>
> 1. **Reduced range.** Same dimensionality, same precision, less extent. The
>    code works normally in the middle of its range and fails at the extremes.
>    Predicts a _ceiling effect_: intact performance on easy items, sharp failure
>    on demanding ones, with no loss of fine discrimination where the code still
>    reaches.
> 2. **Reduced dimensionality.** An axis collapses entirely. A whole class of
>    distinctions becomes unavailable while everything else is untouched.
>    Predicts a _categorical_ deficit — not graded difficulty but a specific
>    discrimination that has gone.
> 3. **Reduced precision.** Same extent, coarser spacing. Predicts _graded_
>    degradation everywhere, worst where fine discrimination is required, with no
>    particular boundary.
>
> These make different predictions about the _shape_ of the psychometric
> function, not just its height, which is what makes them separable. The figure
> as drawn shows only the first. A more honest version would need three disrupted
> panels.

Entorhinal cortex is among the earliest regions affected in Alzheimer's
pathology ([Braak & Braak 1991](https://doi.org/10.1007/BF00308809)), and
grid-cell-like representations are reduced in young adults at genetic risk, long
before symptoms ([Kunz et al. 2015](https://doi.org/10.1126/science.aac8128)).
That is a real case where a specific manifold is compromised while most of
cognition is intact — and as far as I know, the question of _which_ of the three
contractions it is has not been posed in these terms.

## Neuromodulators are axes and manifolds, and the contradiction is only apparent

The intuition that a neuromodulatory pathway is both a modulatory axis _for_
other manifolds and a manifold in its own right looks like it cannot be both.
I think it can, and the resolution is timescale.

> **Conjecture — fast/slow separation.** This is the standard move in dynamical
> systems: a variable that evolves slowly relative to a subsystem appears to that
> subsystem as a _parameter_, not a state.
>
> On the fast timescale of a decision, neuromodulatory tone is approximately
> constant. It therefore acts as a parameter that sets the gain, extent or
> curvature of the manifolds being used — it looks like an **axis of** those
> manifolds, a knob rather than a coordinate.
>
> On slow timescales — minutes, hours, a circadian cycle, a course of
> medication — the neuromodulatory system has its own state, its own dynamics and
> its own geometry. It is a **manifold in its own right**.
>
> The falsifiable part: whether neuromodulation looks like an axis or a manifold
> should depend _entirely on the length of your recording window_, and the
> crossover should sit at the system's autocorrelation time. Two labs studying
> the same pathway with different session structures should disagree in a
> predictable direction. That is a slightly uncomfortable prediction, which is
> what makes it worth making.

This also says something about the figure. Drawing the neuromodulatory plane
alongside the others is only correct on the slow view. On the fast view it should
not be a plane at all — it should be a property of the other planes, which is
awkward to draw. The dashed outline is a hedge standing in for a genuine
ambiguity.

## Extension is not free

The drug panel is the one most likely to be over-read, because a longer plane
looks straightforwardly like more.

> **Conjecture.** If a manifold's extent is bounded by a capacity constraint
> rather than by an arbitrary limit, then extending its range without adding
> neurons has to cost resolution. This is the same range-versus-resolution
> trade-off that governs modular codes in the
> [capacity notes]({{ '/ideas/grid-hippocampal-capacity/' | relative_url }}):
> a fixed number of units distributed over a larger space means coarser
> distinctions within it.
>
> The prediction is specific and falsifiable: a pharmacological manipulation that
> measurably extends a representational range should produce a measurable
> _loss of precision within that range_, in the same subjects, in the same
> session. If range extends with no precision cost, the original bound was not a
> capacity bound — which would itself be informative, because it would mean the
> brain was leaving capacity unused and the interesting question becomes why.
>
> This is why the ticks coarsen in the third panel. A version of the figure with
> the extended plane keeping its fine spacing would be claiming something much
> stronger, and probably false.

The clinical texture fits. Dopamine agonists in Parkinson's disease are
associated with impulse control disorders in a substantial minority of patients
([Weintraub et al. 2010](https://doi.org/10.1001/archneurol.2010.65)) — which
reads naturally as a valuation range extended past its usual bound, with the
discriminations _within_ that range coarsened. Stated that way it is a
hypothesis with a measurement attached rather than a metaphor.

## Two ways to be broken

There is a second failure mode the figure cannot draw at all, and it is the one
the rest of these notes keep running into.

A manifold can have entirely intact geometry — full extent, full resolution — and
still be useless, because it is not **bound** to the world. That is exactly what
unanchored grid firing is: a code doing its job perfectly in its own reference
frame while reporting a position the animal is not at
([anchoring dynamics]({{ '/ideas/anchoring-dynamics/' | relative_url }})).

> **Conjecture.** Geometric degradation and binding failure are distinct axes of
> dysfunction, and should dissociate clinically. Conditions involving progressive
> structural loss should show contracted or collapsed manifolds with anchoring
> intact for whatever remains. Conditions involving disordered inference, with
> structurally intact circuits, should show the opposite — normal manifold
> geometry with a failure to bind it to evidence.
>
> If that holds, the two need different measurements and different treatments,
> and a therapy that restores extent would do nothing for a binding failure. The
> figure only depicts the first kind, which is a limitation worth stating
> whenever it gets shown.

## Questions I would want answered

1. In a population recording, can reduced range, reduced dimensionality and
   reduced precision be separated within a single manifold?
2. For a disease with a known early focus, which of the three does the
   contraction turn out to be?
3. Does neuromodulatory state behave as a parameter or as a state variable, and
   does the crossover sit at the predicted autocorrelation time?
4. Does pharmacologically extending a representational range cost precision
   within it, in the same session?
5. Do manifolds contract independently, or does losing one pull its neighbours
   in, as sharing a substrate would imply?
6. Can geometric degradation and anchoring failure be dissociated in the same
   population, and do they map onto different conditions?

## References

- Braak, H. & Braak, E. (1991). [Neuropathological stageing of Alzheimer-related changes](https://doi.org/10.1007/BF00308809). _Acta Neuropathologica_.
- Gardner, R. J. et al. (2022). [Toroidal topology of population activity in grid cells](https://doi.org/10.1038/s41586-021-04268-7). _Nature_.
- Kunz, L. et al. (2015). [Reduced grid-cell-like representations in adults at genetic risk for Alzheimer's disease](https://doi.org/10.1126/science.aac8128). _Science_.
- Weintraub, D. et al. (2010). [Impulse control disorders in Parkinson disease](https://doi.org/10.1001/archneurol.2010.65). _Archives of Neurology_.

_The figure is generated by `scripts/manifold_schematic.py` in the
[site repository](https://github.com/hdclark94/hdclark94.github.io)._
