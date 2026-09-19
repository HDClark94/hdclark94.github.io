---
layout: post
title: Do language models carve the world into overlapping manifolds?
date: 2026-09-18
description: If representations in a language model are low-dimensional manifolds superposed in one activation space, the brain tells us where to look for them — and warns us about the basis we use to find them.
tags: [representation-geometry, interpretability, manifolds]
toc:
  sidebar: left
---

> These are working notes, not a position I am committed to. Sections marked
> **Conjecture** are speculation I have not tested.

## The claim

The usual picture of a language model's residual stream is a bag of directions:
each feature is a vector, features are roughly orthogonal, and a representation
is a sparse sum of them. The alternative I want to take seriously is that the
organising unit is not a direction but a **manifold** — a low-dimensional surface
whose axes parameterise a specific feature landscape, with many such manifolds
superposed in the same activation space.

This is how we describe population activity in the brain. Head direction cells
in the fly and mouse lie on a ring, and the angular coordinate on that ring
_is_ the represented heading ([Chaudhuri et al. 2019](https://doi.org/10.1038/s41593-019-0460-x)).
Grid cell populations lie on a torus, and the two toroidal phases _are_ the
encoded position ([Gardner et al. 2022](https://doi.org/10.1038/s41586-021-04268-7)).
Motor cortex operates in a low-dimensional subspace whose axes relate to movement
parameters ([Gallego et al. 2017](https://doi.org/10.1016/j.neuron.2017.05.025)).

The important property in every one of these cases: **the topology is not a
modelling choice**. It is forced by the structure of the variable being encoded.
Heading is circular, so the manifold is a ring. That is the part of the analogy
worth chasing.

## What is already established

The ingredients exist, scattered across separate literatures.

- **Superposition.** Networks represent more features than they have dimensions
  by placing them in almost-orthogonal directions, tolerating a little
  interference ([Elhage et al. 2022](https://transformer-circuits.pub/2022/toy_model/index.html)).
  This is the "overlapping" half of the idea, already formalised.
- **Features as directions.** The linear representation hypothesis, and the fact
  that probing and steering work at all ([Park et al. 2023](https://arxiv.org/abs/2311.03658)).
- **Sparse dictionaries.** Sparse autoencoders recover interpretable features at
  scale ([Bricken et al. 2023](https://transformer-circuits.pub/2023/monosemantic-features/index.html);
  [Templeton et al. 2024](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html)).
- **Structured world variables.** Models carry linear representations of space
  and time ([Gurnee & Tegmark 2023](https://arxiv.org/abs/2310.02207)).
- **The direct evidence.** Not every feature is one-dimensional. Engels et al.
  found genuinely multi-dimensional, _circular_ features — days of the week,
  months of the year — recovered from real models
  ([Engels et al. 2024](https://arxiv.org/abs/2405.14860)).

That last result matters most. A circular feature for days of the week is a ring
attractor's representational signature without the attractor. It is the first
hard evidence that the manifold framing describes something real rather than
being a borrowed metaphor.

The open question is not _whether_ manifolds occur. It is whether they are the
**organising principle** or an occasional special case.

## Where the brain analogy is tight, and where it is not

### The density asymmetry

This is the disanalogy I keep coming back to, because it turns into a prediction.

Superposition works **because features are sparse**. You can pack many features
into few dimensions only if few are active at once; interference stays rare
enough to tolerate. The whole scheme is built on an "off" state.

The brain manifolds we actually measure are the opposite. A grid module is
_always_ on. At every moment the population sits somewhere on the torus — there
is no off state, no spare capacity for a second manifold to borrow the same
subspace. So the brain cannot superpose grid modules the way a model superposes
rare features. Its solution is **segregation**: anatomically discrete modules,
each with its own scale, each with its own population.

> **Conjecture.** Density predicts geometry. Features that are _always_ active in
> a language model — position in sequence, syntactic role, register, language
> identity — should be geometrically segregated, occupying a near-dedicated
> subspace with low interference. Features that are rare and semantic should be
> superposed and polysemantic.
>
> This is testable with tools that already exist. Compute the activation density
> of each SAE feature, then measure how much each feature's direction is shared
> with others. If density predicts subspace isolation, and if the dense features
> are the ones that turn out to be low-dimensional and often periodic, that is
> real evidence for the manifold picture — and it tells you _which_ features to
> look at instead of searching the whole dictionary.

### The basis problem

"Manifold axes designed to encode specific feature landscapes" — the word _axes_
is carrying a lot of weight, and this is where neuroscience has already made the
mistake so the field does not have to repeat it.

Principal components are not functional axes. Motor cortex has **output-potent**
and **output-null** subspaces: the same population, comparable variance, but only
some dimensions are read by downstream muscles, which is how preparatory activity
can be large and yet cause no movement
([Kaufman et al. 2014](https://doi.org/10.1038/nn.3643)). The meaningful basis is
defined by what the readout reads, not by what explains variance.

> **Conjecture.** The same critique applies to sparse autoencoders, and mostly
> is not made. An SAE fit to activations finds a basis that reconstructs
> activation variance under a sparsity prior. It has no knowledge of what the
> rest of the network actually _reads_. The functional basis at layer $$L$$ is
> set by the read matrices of everything downstream — the query, key and value
> projections and the MLP input weights of layers $$>L$$.
>
> So: project activations onto the row space of the downstream read matrices
> first, and ask whether the clean low-dimensional structure lives _there_. In
> the brain, the variance basis and the readout basis can differ substantially.
> There is no reason to expect a model to be kinder. A manifold that is obvious
> in the readout basis could be smeared across many SAE features, and a crisp
> SAE feature could be partly output-null.

### Where it probably breaks

Worth stating plainly, so the analogy does not get oversold:

- **Attractors versus geometry.** A grid torus is maintained by recurrent
  dynamics — it is a continuous attractor, and states off the manifold are pulled
  back onto it ([Burak & Fiete 2009](https://doi.org/10.1371/journal.pcbi.1000291)).
  A transformer's forward pass has no such recurrence. Its "manifold" is a set of
  reachable points, not a dynamical attractor. Nothing corrects a state that
  falls off it. This distinction — representational geometry versus attractor
  dynamics — is doing quiet work in a lot of loose brain/model comparisons.
  The caveat on the caveat: across _tokens_, the residual stream plus attention
  does give something recurrence-shaped, so this is not a clean kill.
- **"Designed to" is the wrong verb.** Nothing designs these. They are whatever
  minimises loss. The real question is what makes manifold geometry the
  loss-minimising solution.

## A candidate organising principle

> **Conjecture.** Manifold structure appears precisely where the feature set
> carries **group structure** — where the features are related by a symmetry
> rather than merely being many.
>
> Cyclic groups give rings: days of the week, months, clock positions, pitch
> class. This is exactly where Engels et al. found circular features, which I
> take as confirmation rather than coincidence. Ordinal or metric structure gives
> a line or a filament: magnitude, date, sentiment intensity. Product structure
> gives a torus or a product manifold: tense × number × person, or any
> factorisable grammatical paradigm.
>
> The reason this would be the loss-minimising solution is generalisation. If
> "Tuesday" and "Wednesday" are unrelated directions, the model must learn every
> fact about every day separately. If they are adjacent points on a ring, the
> operation "next day" is a single rotation that works everywhere on the manifold
> — learn it once, apply it to every point, including combinations never seen in
> training. Sparse directions buy capacity; manifolds buy **generalisation**.
> These are different things and a model should want both, in different places.
>
> The sharp version, which is what makes it worth testing: **manifold geometry
> should be predictable in advance from the group structure of the feature set,
> before you look at the model at all.** Pick a paradigm with known structure,
> predict the topology, then go looking. A failure would be informative.

This also connects the idea to the other thread on this page — the entorhinal
system's answer to representing a group (translations in the plane) is a product
of tori, and that is a very specific choice that buys a very specific kind of
generalisation. See [grid–hippocampal circuits and embedding capacity]({{ '/ideas/grid-hippocampal-capacity/' | relative_url }}).

## Questions I would want answered

1. Does activation density predict subspace isolation across SAE features?
2. Do manifolds found in the activation basis survive projection into the
   downstream readout basis, or are they partly output-null?
3. Can the topology of a feature family be predicted from its group structure
   _before_ looking at the model?
4. Are there manifolds with non-trivial topology beyond rings — tori, cylinders,
   spheres, or anything with genus > 1? A torus would be the strongest possible
   echo of the entorhinal result.
5. Does the same feature family occupy the same topology across model scales and
   across architectures? Convergent geometry would argue the structure is forced
   by the task rather than by the inductive bias.
6. Is there anything in a transformer that plays the error-correcting role that
   attractor dynamics play in the brain — anything that pulls an off-manifold
   state back on?

## References

- Bricken, T. et al. (2023). [Towards Monosemanticity](https://transformer-circuits.pub/2023/monosemantic-features/index.html). _Transformer Circuits_.
- Burak, Y. & Fiete, I. R. (2009). [Accurate path integration in continuous attractor network models of grid cells](https://doi.org/10.1371/journal.pcbi.1000291). _PLoS Computational Biology_.
- Chaudhuri, R. et al. (2019). [The intrinsic attractor manifold and population dynamics of a canonical cognitive circuit across waking and sleep](https://doi.org/10.1038/s41593-019-0460-x). _Nature Neuroscience_.
- Elhage, N. et al. (2022). [Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html). _Transformer Circuits_.
- Engels, J. et al. (2024). [Not All Language Model Features Are One-Dimensionally Linear](https://arxiv.org/abs/2405.14860). _arXiv:2405.14860_.
- Gallego, J. A. et al. (2017). [Neural manifolds for the control of movement](https://doi.org/10.1016/j.neuron.2017.05.025). _Neuron_.
- Gardner, R. J. et al. (2022). [Toroidal topology of population activity in grid cells](https://doi.org/10.1038/s41586-021-04268-7). _Nature_.
- Gurnee, W. & Tegmark, M. (2023). [Language Models Represent Space and Time](https://arxiv.org/abs/2310.02207). _arXiv:2310.02207_.
- Kaufman, M. T. et al. (2014). [Cortical activity in the null space: permitting preparation without movement](https://doi.org/10.1038/nn.3643). _Nature Neuroscience_.
- Park, K. et al. (2023). [The Linear Representation Hypothesis and the Geometry of Large Language Models](https://arxiv.org/abs/2311.03658). _arXiv:2311.03658_.
- Templeton, A. et al. (2024). [Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html). _Transformer Circuits_.
