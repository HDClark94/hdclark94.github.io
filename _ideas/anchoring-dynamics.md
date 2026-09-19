---
layout: post
title: Anchoring dynamics, and why the null result carries the argument
date: 2026-09-18
description: Grid anchoring helps when an animal has to path integrate, and does nothing when a cue is available. That dissociation is worth more than the positive result alone, and it generalises into a test for whether any representation is actually used.
tags: [grid-cells, path-integration, anchoring, reference-frames]
toc:
  sidebar: left
---

> These are working notes, not a position I am committed to. Sections marked
> **Conjecture** are speculation I have not tested.

## The observation

Grid firing in medial entorhinal cortex is not permanently bound to the world.
Recording from mice running a location memory task on a virtual linear track,
grid activity can be **anchored** to the task environment, or it can encode
distance travelled in a reference frame of its own, independent of the track.
This is not a property of an animal or of a session — it varies _within_ a
session, trial to trial ([Clark & Nolan 2024](https://doi.org/10.7554/eLife.89356)).

That variability is usually a nuisance. Here it is the instrument. If anchoring
fluctuates while everything else is held fixed, you can ask what anchoring is
_for_ by asking when it predicts behaviour.

## The dissociation

The answer is specific, and the specificity is the point.

When the reward location is marked by a visual cue, performance is **the same**
whether or not grid cells are anchored. Remove the cue, so the animal has to
path integrate, and performance is **better** on trials where grid cells are
anchored to the task environment.

So grid anchoring is not a general-purpose localisation signal. It is recruited
when the animal must integrate its own motion, and appears to contribute nothing
when the world supplies the answer directly.

### Why the null result does the heavy lifting

It is worth being explicit about the logic, because this is the part that
transfers.

A positive association on its own is weak. If anchored trials were simply better
trials, every plausible confound would produce the same result: arousal,
engagement, running consistency, time-on-task, satiety. All of these predict
_global_ improvements in performance.

The cued condition is the control that kills them. On cued trials the animal is
just as engaged, just as aroused, running the same track — and anchoring buys
nothing. A confound that improved performance through general mechanisms would
have to improve it on both trial types. None of them can explain an effect that
appears only when path integration is required.

> The structure of the argument is: find a behaviour with two routes to the same
> goal, show the representation's state varies independently of the route, and
> show it predicts success on one route only. The **selectivity** is the evidence.
> The positive result tells you there is an association; the null tells you what
> the association is about.

## What controls the switch?

Calling it "anchoring dynamics" commits to anchoring being a _state_ the circuit
moves into and out of, rather than a fixed property. The obvious question is what
drives the transitions, and it is not answered by the data above.

> **Conjecture: anchoring as reliability-weighted reset.** Path integration
> accumulates error with distance travelled. Sensory landmarks reset it. If the
> circuit does this near-optimally, the weight given to a landmark should scale
> with its reliability relative to the accumulated uncertainty of the internal
> estimate — the standard Kalman picture.
>
> Two predictions follow that the existing framing does not make:
>
> 1. **Anchoring probability should increase with distance since the last
>    anchoring event**, because the internal estimate degrades and the landmark
>    wins by comparison. Anchoring should therefore look like a hazard function,
>    not a coin flip.
> 2. **Degrading the cue should reduce anchoring**, and reduce it more when the
>    path integration estimate is fresh.
>
> This also _explains_ the behavioural dissociation instead of restating it. On
> cued trials the animal can read the goal off the world and bypass the
> integrated estimate, so the state of the grid code is irrelevant to the
> decision. On non-cued trials the integrated estimate is the only estimate
> there is, so whether it is bound to the track is the whole ball game.

The dynamical signature would be visible in the population geometry. If grid
population activity lies on a torus
([Gardner et al. 2022](https://doi.org/10.1038/s41586-021-04268-7)), an anchoring
event is a **discontinuity in toroidal phase** — a jump to the phase the track
frame demands. Anchoring would then be measurable as a discrete event with a
latency and a magnitude, rather than as a per-trial label. Whether the reset is a
jump or a fast continuous slide is a mechanistic question with different
implications for the underlying attractor dynamics
([Burak & Fiete 2009](https://doi.org/10.1371/journal.pcbi.1000291)).

## Two frames at once, and who reads them

Non-grid spatial cells were either coherent with the grid population or stably
anchored to the task environment. So on a given trial the circuit can hold **two
reference frames simultaneously** — one drifting with self-motion, one pinned to
the world.

That raises a question the recordings cannot answer on their own: how does a
downstream reader know which frame to trust on this particular trial? Something
must be doing frame selection, and it must do it fast enough to matter within a
trial.

> **Conjecture.** Frame selection is the same problem as the readout-basis
> problem in the [notes on feature manifolds]({{ '/ideas/llm-feature-manifolds/' | relative_url }}).
> In both cases, a population holds more structure than is being used, and the
> functional question is not what is _represented_ but what is _read_. If the
> hippocampus reads the anchored subpopulation preferentially on trials where the
> track frame is behaviourally relevant, then frame selection is implemented at
> the readout, and the entorhinal population is better thought of as offering
> several candidate frames than as committing to one.

## The version of this for models

The reason I think this dissociation is the most portable result of the three
pages here: it supplies the **control condition** that the anchoring account of
confabulation was missing.

In the [notes on capacity]({{ '/ideas/grid-hippocampal-capacity/' | relative_url }})
I suggested that a model confabulating a citation is not suffering a capacity
failure but an anchoring failure — emitting a well-formed point on a
citation-shaped manifold that is not bound to retrieved evidence. As stated, that
is a reframe, and not obviously testable; any probe that correlates with errors
would seem to confirm it.

The grid result says how to do better. Build the two-route version:

- **Cued trials**: questions answerable from the provided context, where the
  evidence is right there.
- **Uncued trials**: questions requiring the model to rely on its own
  parametric knowledge or to carry information across a long gap, where nothing
  in the immediate context supplies the answer.

Then measure, per token, whether the representation is bound to context or
running on priors — and check whether it predicts errors **only** in the second
condition.

> **Conjecture.** If the measure predicts errors in both conditions, it is an
> arousal analogue: a general difficulty or confidence signal wearing a mechanistic
> costume. It is only evidence for anchoring if it is _selective_. This is a
> sharper bar than most interpretability work sets for itself, and it is cheap —
> it needs a control condition, not an intervention.

The asymmetry is worth noting too. In the mouse, anchoring helps only when the
cue is absent. If the model analogue behaves the same way, then context-binding
measures should be uninformative exactly where retrieval already works — which
would predict that grounding interventions help least on the cases that are
easiest to benchmark.

## Questions I would want answered

1. Does anchoring probability scale with distance since the last anchoring
   event, as a reliability-weighted reset predicts?
2. Is an anchoring event a discrete phase jump on the torus, or a continuous
   slide? Do the two occur under different conditions?
3. Does degrading cue reliability shift the anchoring rate in the direction
   optimal weighting predicts?
4. When grid and non-grid populations disagree about the frame, which one do
   downstream hippocampal representations follow, and does it depend on the
   trial type?
5. Does anchoring on trial $$n$$ predict anchoring on trial $$n+1$$? A
   history dependence would argue for a slow state variable rather than
   moment-to-moment evidence weighting.
6. In a model, does a context-binding measure predict errors selectively on
   items that require context, and not on items answerable from parametric
   knowledge?

## References

- Burak, Y. & Fiete, I. R. (2009). [Accurate path integration in continuous attractor network models of grid cells](https://doi.org/10.1371/journal.pcbi.1000291). _PLoS Computational Biology_.
- Clark, H. & Nolan, M. F. (2024). [Task-anchored grid cell firing is selectively associated with successful path integration-dependent behaviour](https://doi.org/10.7554/eLife.89356). _eLife_.
- Gardner, R. J. et al. (2022). [Toroidal topology of population activity in grid cells](https://doi.org/10.1038/s41586-021-04268-7). _Nature_.
