---
title: "So does your Car fail? (The Counterexample to HRT Conjecture) - Part 2"
date: 2026-08-14T01:02:49-04:00
draft: false
tags: [maths, analysis]
# links:
#     website: "https://omanshuthapliyal.github.io/"
#     alias : "blog/hrt-conjecture-part-2/"

---

In the [previous post](INSERT-PREVIOUS-HRT-POST-LINK), I talked about the HRT conjecture as a rather natural statement about phase space.
A signal can be moved in time. It can also be moved in frequency.
Moving it in time changes where its envelope lives. Moving it in frequency changes the pitch of its oscillations. If we do both, we obtain a time-frequency shifted version of the original signal.

Using a symmetric convention, one writes this operation as

$$
(\rho(x,\omega)f)(t)
=
e^{2\pi i\omega(t-x/2)}
f(t-x).
$$

The point

$$
(x,\omega)
$$

tells us where we moved the function in time-frequency phase space.

The HRT conjecture said that distinct points in phase space should produce distinct, linearly independent copies of a nonzero function.

More explicitly, if

$$
z_1,\ldots,z_N
\in
\mathbb{R}^2
$$

are distinct, and

$$
f
\in
L^2(\mathbb{R})
$$

is nonzero, then one should never be able to find nontrivial coefficients

$$
c_1,\ldots,c_N
$$

for which

$$
\sum_{k=1}^{N}
c_k \rho(z_k)f
=
0.
$$

This was an extremely believable conjecture.

If I shift a wave packet in time, it moves. If I modulate it, the frequency changes. If I do different combinations of both operations, why should a finite number of them somehow arrange themselves into a perfect cancellation over the entire real line?

It feels a little like taking several copies of the same violin note, moving each one to a different place in time and changing the pitch of each one, and then expecting their sum to vanish *everywhere*.

For roughly thirty years, the answer appeared to be: they cannot.

But, in August 2026, a counterexample was constructed.

Not using a pathological function. Not using an object which only barely belongs to $L^2$. The counterexample uses a nonzero Schwartz function: infinitely differentiable, rapidly decaying, and very much the sort of wave packet one would have expected to behave nicely.[^1]

The conjecture, in full generality, is false.

## A lattice is too rigid

The counterexample becomes more interesting once one understands where it cannot live.

There is a theorem of Linnell which says that the HRT conjecture holds if all the phase-space points lie in a discrete lattice-like subgroup.[^2] So if the locations of the shifts sit neatly on a regular grid, there is no way to produce this sort of linear dependence.

This is not merely a convenient technical assumption.

A lattice gives the translation and modulation operators a rather disciplined algebraic structure. The shifted functions can interact, of course, but not in a way which allows a nonzero function to be annihilated by a finite combination of distinct shifts.

So the counterexample has to escape the lattice.

But it cannot escape it entirely.

If one starts from a completely arbitrary cloud of points in phase space, there is no structure to exploit. There is no obvious coordinate system, no return map, and no clear way to organize the interactions among the shifted wave packets.

The construction therefore does something more delicate.

It uses eleven points which sit in an irrationally translated half-lattice, together with one additional point at the origin.

So, in a loose sense, it is an 11+1 configuration.

Most of the points still resemble a structured grid. But the entire configuration is not contained in the type of discrete subgroup where Linnell's theorem applies.

The geometry is close enough to a lattice to remain analyzable, while being far enough from one to escape rigidity.

This seems to be the first crack in the conjecture.

Not disorder.

Not a random collection of phase-space points.

Just a very carefully placed deviation from order.

## Why smoothness does not save the conjecture

One might have expected that any counterexample to HRT would need to use a very strange function.

After all, if a function has sharp discontinuities, slow decay, or some unpleasant irregularity, perhaps one can imagine exploiting that structure to create cancellation.

But the window in the counterexample belongs to the Schwartz space,

$$
\mathcal{S}(\mathbb{R}).
$$

This means that the function is infinitely differentiable, and it decays faster than every inverse polynomial. Its derivatives do the same.

For every nonnegative $m$ and $n$,

$$
\sup_{t \in \mathbb{R}}
\left|
t^m f^{(n)}(t)
\right|
<
\infty.
$$

This is about as far as one can get from a jagged pathological example.

However, this does not mean that every rapidly decaying function behaves the same way.

A Gaussian,

$$
g(t)
=
e^{-t^2},
$$

has a stronger kind of decay. There are positive HRT results for functions with sufficiently strong Gaussian-like decay. Intuitively, the tails of the shifted functions disappear so aggressively that they cannot sustain the long-range interference needed for a global cancellation.[^3]

A Schwartz function is still extremely well behaved. But it leaves a little more room.

The counterexample lives in that room.

It is smooth enough to look harmless, but not so rigid that the geometry of its time-frequency shifts is forced to remain independent.

## The cancellation is not found directly

The authors do not begin by writing down twelve shifted functions and somehow guessing the coefficients which make them vanish.

Instead, they package eleven time-frequency shifts into one operator:

$$
P_*
=
\sum_{k=1}^{11}
c_k\rho(z_k).
$$

Then they seek a function $f_*$ for which

$$
P_*f_*
=
c_*f_*.
$$

In other words, they look for an eigenfunction.

Once this is achieved, the desired twelve-term relation follows immediately:

$$
-c_*f_*
+
\sum_{k=1}^{11}
c_k\rho(z_k)f_*
=
0.
$$

The twelfth point is the origin. It corresponds to the unshifted copy of the function.

I find this reframing useful.

The original question is: can twelve distinct time-frequency shifts cancel?

The new question is: can a specially designed combination of eleven shifts possess a smooth, rapidly decaying eigenfunction?

It is still a difficult question, but it is no longer a completely shapeless one.

## Folding the problem until it becomes visible

The proof then uses something called a Zak transform.

The Zak transform takes a function on the real line and reorganizes it into an object living on a torus. This is useful because translations and modulations, which look global and awkward on the line, become more structured after this transformation.

The actual construction uses a two-component version of this transform. One can think of it as folding the real-line problem into a two-dimensional, periodic phase-space picture.

After this folding, the problem is no longer primarily about twelve wave packets on the line.

It becomes a question about a small matrix which changes as one moves around a torus.

The authors construct this matrix field to be close to a simpler rank-one object. A rank-one map has a preferred direction: it compresses nearly everything onto a line.

The important fact is that this preferred direction survives the perturbation.

So, rather than the geometry of the problem wandering freely across all possible directions, there is a hidden line which is carried consistently along the torus dynamics.

The rest of the proof is essentially about turning this hidden direction into an honest-to-goodness Schwartz function on the real line.

There is an irrational shift involved, and this produces a familiar small-divisor issue. The same irrationality which helps the configuration escape lattice rigidity also has to be controlled carefully enough that the resulting construction remains smooth.

This is where the arithmetic choice of the phase-space translation matters.

The irrationality is not decorative. It is doing two jobs at once.

It breaks the lattice theorem.

And it remains structured enough that the torus dynamics can still be solved.

#### Where the computer enters

There is a computer-assisted component to the proof, but it is worth being precise about what this means.
The computer is not asked to search through a large list of candidate functions and announce that one seems to work.
Instead, interval arithmetic is used to verify a bound uniformly over the torus.

Ordinary floating-point computation might tell us that a quantity appears smaller than some threshold. Interval arithmetic instead returns a guaranteed interval containing the true value, including all rounding errors.
The verification shows that the true matrix field remains sufficiently close to the simple rank-one model.
That closeness is what gives the proof its hidden contracting direction.
So the computer-assisted part is not replacing the mathematics. It is making a particular analytic estimate rigorous in a situation where an ordinary symbolic bound would be rather unpleasant.

I think this is a useful way to understand the role of computation in modern mathematics.
The computation is not the explanation.
The geometry is the explanation.
The computation verifies that the geometry is strong enough.

#### What actually broke?

It would be easy to say that the HRT conjecture failed because phase space is messy.
But this is not really what happened.
The counterexample is not random. It is almost too structured to be called messy.
A pure lattice is too rigid. A completely arbitrary configuration gives us no traction. The 12-point construction sits in the uncomfortable region between the two.
It has enough lattice-like structure to be folded into a tractable torus problem. It has enough irrationality to evade the theorem which protects genuine lattices. And it has a smooth enough function to prevent the counterexample from being dismissed as pathological.

The result is not that time-frequency shifts are generally easy to make dependent.
The result is more unsettling.
There are very smooth wave packets, and very carefully arranged phase-space locations, for which distinct time-frequency shifts can conspire to cancel perfectly.

For thirty years, the conjecture suggested that phase space had a certain kind of rigidity.
The counterexample does not destroy every piece of that rigidity.
It shows that the rigidity had a gap.

> **Update.** The 12-point construction was the first explicit Schwartz-class counterexample. Further recent work claims that four points already suffice. I will return to this separately, since reducing the geometry from twelve points to four is not merely a smaller example; it changes the question of how little structure is needed before HRT can fail.[^3]

## References

[^1]: M. Faulhuber, P. Petersen, J. T. van Velthoven, and F. Voigtlaender, [*Linear dependence of time-frequency shifts of a Schwartz function*](https://arxiv.org/abs/2608.05044), 2026. The original 12-point counterexample.

[^2]: P. A. Linnell, [*von Neumann algebras and linear independence of translates*](https://doi.org/10.1090/S0002-9939-98-04672-8), *Proceedings of the American Mathematical Society*, 127(11), 1999.

[^3]: T. Tao, [*A partial digestion of the HRT counterexample*](https://terrytao.wordpress.com/2026/08/06/a-partial-digestion-of-the-hrt-counterexample/), 2026. A blog-level explanation of the original counterexample and subsequent developments.

> Written with [StackEdit](https://stackedit.io/).