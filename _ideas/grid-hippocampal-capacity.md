---
layout: post
title: Grid–hippocampal circuits and the capacity to build embedding manifolds
date: 2026-09-17
description: The entorhinal–hippocampal system solves a capacity problem that embedding spaces also face. One of its solutions — a multi-scale phase code — already appears in transformers, under a different name.
tags: [grid-cells, hippocampus, capacity, representation-geometry]
toc:
  sidebar: left
---

> These are working notes, not a position I am committed to. Sections marked
> **Conjecture** are speculation I have not tested.

## The claim

The entorhinal–hippocampal circuit faces a problem that sounds a lot like the one
an embedding space solves: build a very large number of distinguishable
population states from a limited number of neurons, such that nearby states are
meaningfully similar, distant states do not interfere, and the whole scheme
generalises to environments never encountered before.

If that framing is right, the circuit is not merely _analogous_ to an embedding
space. It is a worked example, with the advantage that we can record from it and
we know roughly what it is for.

## Why grid codes have unusual capacity

A place cell code is close to unary. Each cell fires in one location, so the
number of distinguishable positions scales roughly linearly with the number of
cells. Serviceable, expensive.

A grid code is a **modular phase code**, and it behaves completely differently.
Position is represented as a tuple of phases, one per module, each module having
its own spatial period. Two modules with incommensurate periods disambiguate a
range far larger than either alone; the unambiguous range grows roughly with the
_product_ of the periods. Capacity is therefore exponential in the **number of
modules**, not linear in the number of neurons, and the redundancy buys error
correction as a side effect
([Sreenivasan & Fiete 2011](https://doi.org/10.1038/nn.2901)).

The toroidal geometry this implies is not a theoretical convenience — it has been
measured directly in the population activity
([Gardner et al. 2022](https://doi.org/10.1038/s41586-021-04268-7)).

Two further pieces matter for the capacity story:

- **Conjunction.** Place fields can be built from a grid basis set
  ([Solstad et al. 2006](https://doi.org/10.1002/hipo.20244)). In the
  Tolman–Eichenbaum Machine this becomes an explicit factorisation: grid cells
  carry _structure_, sensory input carries _content_, and place cells are the
  conjunction ([Whittington et al. 2020](https://doi.org/10.1016/j.cell.2020.10.024)).
- **Remapping.** The hippocampus stores many near-orthogonal maps in one
  population — eleven rooms, eleven statistically independent maps
  ([Alme et al. 2014](https://doi.org/10.1073/pnas.1421056111)). This is already
  "many overlapping manifolds in one population", measured, in CA3.

## Two different routes to exponential capacity

It is worth being precise about this, because the two mechanisms get conflated
and they have different consequences.

**Factorisation (grid modules).** Capacity is exponential in the number of
modules. It requires the encoded variable to have metric or group structure, and
it generalises: a displacement is the same phase update everywhere in the
environment, so you learn the operation once and apply it anywhere.

**Sparse near-orthogonality (superposition, Johnson–Lindenstrauss).** Capacity is
exponential in dimension. It requires sparsity, not structure, and it does not
generalise: each item is its own direction and tells you nothing about its
neighbours.

The interesting thing is that the hippocampal formation appears to use **both**,
for different jobs. Grid modules give a factorised structural code that transfers
across environments. Hippocampal remapping gives an arbitrary, sparse, separating
code that keeps environments from bleeding into each other. That combination —
a structural code that generalises, bound to a content code that separates — is
close to what you would design if you wanted both capacity and transfer.

> **Conjecture.** If a language model needs both properties too, they should be
> visibly separated in the same way: structural features (position, syntactic
> role, relational frames) carried by factorised, low-dimensional, periodic codes,
> and content features carried by sparse near-orthogonal directions. That is the
> same prediction arrived at from the other direction in
> [the notes on feature manifolds]({{ '/ideas/llm-feature-manifolds/' | relative_url }}),
> which I take as mild evidence it is worth testing.

## Rotary position embeddings are a multi-scale phase code

This is the concrete bridge, and I think it is closer than an analogy.

Rotary position embeddings encode sequence position by rotating pairs of
embedding dimensions by an angle $$\theta_i = p \cdot \omega_i$$, with
geometrically spaced frequencies $$\omega_i$$
([Su et al. 2021](https://arxiv.org/abs/2104.09864)). Position is therefore
represented as a **set of phases at multiple scales** — a point on a torus,
built from circles of different periods.

That is the same code class as a grid code. Different substrate, different
dimensionality, same scheme: a modular residue code on a product of circles,
where multi-scale periodicity buys a large unambiguous range from few parameters.

Two things transfer immediately:

**Range versus resolution.** In a grid code the unambiguous range is set by the
largest module, and resolution by the smallest. In RoPE the effective context
range is set by the lowest frequency and local precision by the highest. The
existing analysis of how many modules you need for a given range, and how the
trade-off behaves, applies directly to choosing a frequency spectrum.

**Rescaling.** Grid modules rescale when a familiar environment is resized, and
the rescaling partially reverts with experience
([Barry et al. 2007](https://doi.org/10.1038/nn1905)). Long-context methods
extend a model's context by rescaling RoPE frequencies
([Peng et al. 2023](https://arxiv.org/abs/2309.00071)). These are the same
operation on the same kind of code.

> **Conjecture, and it runs both ways.** YaRN's central empirical finding is that
> you should _not_ scale all frequencies uniformly — high-frequency components
> should be left largely intact while low frequencies are interpolated, because
> uniform scaling destroys local precision to buy range.
>
> The prediction back into neuroscience: grid rescaling under environmental
> deformation should likewise be non-uniform across modules, with small modules
> preserving local metric structure while large modules absorb most of the
> rescaling. There is evidence that rescaling differs across modules; whether it
> follows the specific pattern that works best for RoPE is, as far as I know, not
> something anyone has looked at with this framing. It is answerable with
> existing multi-module recordings.
>
> And the prediction forward: if the entorhinal solution is the better one, the
> reversion-with-experience result suggests context extension should be
> _transient_ — a model should re-learn a native scale with continued training at
> the new length rather than keeping the interpolation indefinitely.

Where the parallel is weaker, to be fair to it: RoPE frequencies are fixed by
design while grid scales are learned and plastic; RoPE encodes one-dimensional
sequence position while grid cells encode two-dimensional space; and RoPE has no
attractor dynamics maintaining the phase. The _code_ is shared even though the
mechanism that produces it is not.

## Capacity is not the binding problem

Here is the part I think is most underrated, and it comes out of the recording
data rather than theory.

Grid firing is not always bound to the world. It can be anchored to the task
environment, or it can run free as a path-integration code that encodes distance
travelled independently of the task frame — and **which of these is happening
predicts whether the animal gets the answer right**
([Clark & Nolan 2024](https://doi.org/10.7554/eLife.89356)).

So capacity is not the whole story. An unanchored manifold has lost none of its
representational capacity and is nonetheless useless for the task. The variable
that matters is whether the internal coordinate is correctly **bound** to
external evidence, and that binding fluctuates from trial to trial within a
single session.

Crucially, the benefit is _selective_: anchoring improves performance when the
animal must path integrate, and makes no difference when a visual cue marks the
goal. Capacity is silent about this. Two codes with identical capacity behave
differently depending only on whether they are currently bound to the world.

> **Conjecture.** This is the variable missing from most discussions of embedding
> geometry in models, and it reframes a familiar failure. When a model
> confabulates a citation, it is not suffering a capacity failure — it emits a
> well-formed point on a citation-shaped manifold, with correct structure,
> plausible authors, a plausible year. What has failed is _anchoring_: the
> representation is generated from the structural prior rather than bound to
> retrieved evidence. That is the exact signature of a grid code that has slipped
> into path integration and is confidently reporting a position the animal is
> not at.

The dissociation, what might drive the switch between frames, and how to turn
this reframe into something testable are taken up separately in
[anchoring dynamics]({{ '/ideas/anchoring-dynamics/' | relative_url }}).

## The bridge already exists formally

The two threads on this page are not only analogically related. A transformer
with an appropriate recurrent position encoding has been shown to correspond
closely to the Tolman–Eichenbaum Machine, and to develop grid-like and place-like
representations ([Whittington et al. 2021](https://arxiv.org/abs/2112.04035)).
The successor-representation account of place and grid coding
([Stachenfeld et al. 2017](https://doi.org/10.1038/nn.4650)) supplies the
predictive objective that makes such a code the sensible solution.

So the interesting work is not in establishing that the analogy holds. It is in
taking the quantitative results that exist on one side — capacity bounds,
rescaling behaviour, anchoring statistics — and asking what they predict on the
other.

## Questions I would want answered

1. Does non-uniform rescaling across grid modules follow the pattern that works
   best for frequency interpolation in RoPE?
2. Is there a per-token anchoring measure in a language model that predicts
   factual error better than confidence does?
3. How many near-orthogonal maps can one population hold before interference
   degrades them, and does the measured hippocampal number sit near that bound
   or well below it?
4. Does a model trained on tasks with genuine metric structure develop modular,
   multi-scale codes without being architecturally given them?
5. Grid modules have discrete, ratio-related scales rather than a continuum. Is
   that ratio optimal for capacity, and does the geometric spacing of RoPE
   frequencies land anywhere near the same ratio?

## References

- Alme, C. B. et al. (2014). [Place cells in the hippocampus: eleven maps for eleven rooms](https://doi.org/10.1073/pnas.1421056111). _PNAS_.
- Barry, C. et al. (2007). [Experience-dependent rescaling of entorhinal grids](https://doi.org/10.1038/nn1905). _Nature Neuroscience_.
- Burak, Y. & Fiete, I. R. (2009). [Accurate path integration in continuous attractor network models of grid cells](https://doi.org/10.1371/journal.pcbi.1000291). _PLoS Computational Biology_.
- Clark, H. & Nolan, M. F. (2024). [Task-anchored grid cell firing is selectively associated with successful path integration-dependent behaviour](https://doi.org/10.7554/eLife.89356). _eLife_.
- Gardner, R. J. et al. (2022). [Toroidal topology of population activity in grid cells](https://doi.org/10.1038/s41586-021-04268-7). _Nature_.
- Peng, B. et al. (2023). [YaRN: Efficient Context Window Extension of Large Language Models](https://arxiv.org/abs/2309.00071). _arXiv:2309.00071_.
- Solstad, T. et al. (2006). [From grid cells to place cells: a mathematical model](https://doi.org/10.1002/hipo.20244). _Hippocampus_.
- Sreenivasan, S. & Fiete, I. (2011). [Grid cells generate an analog error-correcting code for singularly precise neural computation](https://doi.org/10.1038/nn.2901). _Nature Neuroscience_.
- Stachenfeld, K. L. et al. (2017). [The hippocampus as a predictive map](https://doi.org/10.1038/nn.4650). _Nature Neuroscience_.
- Su, J. et al. (2021). [RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864). _arXiv:2104.09864_.
- Whittington, J. C. R. et al. (2020). [The Tolman-Eichenbaum Machine](https://doi.org/10.1016/j.cell.2020.10.024). _Cell_.
- Whittington, J. C. R. et al. (2021). [Relating transformers to models and neural representations of the hippocampal formation](https://arxiv.org/abs/2112.04035). _arXiv:2112.04035_.
