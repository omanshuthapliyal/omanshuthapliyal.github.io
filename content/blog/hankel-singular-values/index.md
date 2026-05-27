---
title: "What Hankel Spectra Reveal About Memory"
date: 2026-05-26T11:09:02-07:00
draft: false

katex: true
tags: [statistics, ml, maths]
# links:
#     website: "https://omanshuthapliyal.github.io/"
#     alias : "blog/hsv-memory"
---

Suppose we are given a linear dynamical system $$G=(A,B,C,D)$$ (recall that a linear system is an input $$x$$ to output $$y$$ map such that $$y_k = Cx_k + Du_k, x_{k+1}=Ax_k+Bu_k$$), and $$G$$ has some dimension $$d$$.
Often times one has to find an "equivalent" system $$\hat{G}$$-- one that has an input-output behavior as close to $$G$$ as possible, while ideally having a lower dimension $$\hat{d}$$.
This very vital demand from the new system $$\hat{G}$$ to model the original (higher dimensional) system as closely as possible has many applications:  building smaller plants for controller synthesis, reduced order system modeling, compressing fluid or other PDE-derived dynamical systems into manageable surrogate models, etc.

One of the ways to do so is via the _Hankel Operator_ of the system. 
We saw in one of the earlier posts how the [Controllability](https://omanshuthapliyal.github.io/blog/state-space-models/)  $$W_c$$ (and Observability, $$W_o$$) matrices help encode if one can drive a given system to any desired state (or observe the state given its output history).
The Hankel operator is somewhat of a Frankenstein: $$H=W_cW_o$$. 
However, its key property is that it maps the full causal history of the inputs to the future outputs. 

An obvious question for dimensionality reduction of linear systems would be, why not simply do Singular value decomposition (SVD), or PCA, or something more linear algebra-esque?
While SVD on a single matrix does do dimensionality reduction, an SVD is static - while Hankel matrix's singular values contain a lot more insight about all the underlying input-output relations of $$G$$ and $$\hat{G}$$.
The Hankel singular values _measure which state directions are both controllable and observable, so they capture dynamical importance rather than just parameter magnitude_.
Naturally, a system's "more important" Hankel singular values tend to capture "more net excitation" in the dynamics.

A seemingly fundamentally distinct, but deeply related aspect of the Hankel singular values (HSV) is actually found in state space models (SSMs)!
Yes - the same SSMs that form a backbone of the Mamba models for long range audio tasks, hybrid SSMs that are a part of the "agentic-first" Nemotron 3 foundational model, and edge applications of Mamba-3's MIMO architecture stacks.
SSMs are fundamentally identical to linear dynamical systems (linear time invariant, in case of S4-type SSMs, and linear parameter varying in case of Mamba-type SSMs).
Therefore, ignoring inter-layer nonlinearities, a lot of results from mature linear systems & controls are very amenable for application to SSMs (deep SSM stacks often involve LayerNorm, or other types of trivial nonlinearities -- I really want to emphasize the fact that these are still systems well within the realm of linear dynamical system; see [Lur'e type systems; Chapter 3](https://web.stanford.edu/~boyd/lmibook/lmibook.pdf)).
Equivalent HSVs of the SSMs, therefore, have a peculiar property that I have found empirically: _HSV decay can be used as a proxy for how much memory a task actually requires in a state-space model._
A steep HSV drop suggests the task is compressible into a small latent state, while a slower decay suggests the task needs richer recurrent memory.
This makes total sense when viewed from the control theory lens, but sounds peculiar as to why an arbitrary, post-trained SSM when trained to a given task, would have its HSVs dictate how much it can remember in the deep past!
This is primarily because even though a linear system's controllability and observability properties depend on the choice of the coordinates, the Hankel singular values are independent of the state-space coordinates!

{{< scale src="HSV-decay-tasks.png" alt="HSV decay rates for various tasks" scale="70" >}}
---
The figure above is taken from a preprint currently in progress on uncovering more such properties of SSMs.
For the purposes of this discussion, it shows 5 different tasks of varying memory requirements - and a steeper HSV decay rate signifies that the task likely has a low intrinsic memory dimension; if it decays gradually, the model may need more state capacity.
While it's a useful empirical diagnostic, HSV decay rate is not as a perfect ground-truth measure of task memory.
Despite that, it is rather cool that this concept from system identification for linear systems shows up in a seemingly (not so) disparate place.

---
> *Written with [StackEdit](https://stackedit.io/).*
