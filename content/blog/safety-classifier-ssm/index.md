---
title: "Contraction can Help Safety Classifiers keep their Promise"
date: 2026-08-12T01:02:49-04:00
draft: false
tags: [ml, controls]
# links:
#     website: "https://omanshuthapliyal.github.io/"
#     alias : "blog/safety-classifier-ssm/"

---

A safety classifier can tell us that a prompt looks harmful.
That is useful. But it is perhaps not the question we should stop at.
Suppose a classifier sees a prompt and says that it is safe. Now suppose we change the prompt slightly. Perhaps we substitute a few words. Perhaps we phrase the same request differently. Perhaps, more abstractly, we nudge the token embeddings of the prompt by a very small amount.
Would the classifier still say safe?

There are two ways one might answer this question. The first is to collect a rather large set of perturbed prompts, run the classifier on all of them, and report how often it changes its mind. This is empirical robustness. It is certainly better than not testing at all.
The second answer is more ambitious. We ask whether the classification remains unchanged for *every* input within some precisely defined neighbourhood of the original prompt. This is a certification question.

In some recent work, I have been thinking about when such a certificate is possible for a small state-space-model-based safety classifier. The short answer is pleasantly control-theoretic:

> The classifier must forget uncertainty quickly enough.

Or, more precisely, its state transition must be contracting.

#### A classifier does not see words

To be clear, the perturbations I will discuss here are perturbations in *embedding space*, not direct replacements of individual tokens. This matters. A language model turns tokens into vectors. So, if the input is a sequence of token embeddings
$$
u_1, u_2, \ldots, u_T,
$$
we can imagine an adversary replacing each $$u_t$$ by a nearby vector $$u_t'$$ satisfying $$
\lVert u_t' - u_t \rVert_\infty \leq \delta.
$$
The quantity $\delta$ tells us how large a perturbation we allow in any coordinate of any embedding.
This does **not** immediately mean that every point in this embedding-space box corresponds to a meaningful piece of text. Nor does it prove robustness to arbitrary token substitutions. It is instead a particular threat model: a continuous neighbourhood around the original embedded prompt.

Still, it gives us a concrete question to ask:

> If every token embedding is allowed to move a little, can we prove that the classifier's label does not change?

#### A very small state-space safety head

Consider a lightweight classifier which reads token embeddings one at a time and maintains an internal state:
$$
x_t = A x_{t-1} + B u_t.
$$
At time $$t$$, the state $$x_t$$ is a summary of the tokens the classifier has seen so far.
The classifier then produces a scalar score,
$$
s_t = Cx_t + D u_t.
$$

We can imagine that a positive score means "harmful" and a negative score means "benign." The final decision is made from the score after the full sequence has been read.
This is simply a linear time-invariant state-space model.
But recurrence creates an issue which does not appear in the same way for a feed-forward classifier.
If an early input embedding is perturbed, the resulting error enters the state. At the next step, that error is carried forward by $$A$$. Then it is carried forward again. And again.
So a small perturbation is not merely added once to the classifier's final score. It becomes part of a dynamical system.

For a fixed prompt, the classifier produces one nominal score.
Under perturbations, though, there is no longer only one score. There is a whole set of scores which the classifier could produce, depending on how the embeddings are nudged inside the allowed box.
For this linear model, that set can be tracked exactly as an interval.
Suppose that after reading $$t$$ tokens, the state might lie anywhere between a lower bound $$x_t^{\ell}$$ and an upper bound $$x_t^{h}$$. We can propagate these bounds forward through the dynamics instead of enumerating every possible perturbation.

At the end, the classifier produces an output interval:
$$
[s_T^{\ell}, s_T^{h}].
$$

The certification rule is then almost disappointingly simple.

- If the true label is harmful and
$$
s_T^{\ell} > 0,
$$
then every permitted perturbation is still classified as harmful.

- If the true label is benign and
$$
s_T^{h} < 0,
$$
then every permitted perturbation is still classified as benign.

- If the interval crosses zero, then some allowed perturbation *may* change the label. We cannot certify the example.

It is important to be careful with that last statement. An uncertified example is not necessarily incorrectly classified. It may even be robust in practice. We are merely unable to make a worst-case promise about it.

#### The reach tube

Instead of looking only at the final interval, we can watch the entire interval evolve as the classifier reads the prompt.
This time-indexed collection of possible scores is sometimes called a *reach tube*.

{{< scale src="reach-tube-contraction.png" alt="Reach tubes for a contraction-constrained and unconstrained LTI safety classifier" scale="50" >}}

*Figure 1. The shaded region is the set of scores reachable under bounded embedding perturbations as a sequence is processed. Under contraction, the uncertainty tube settles. Without contraction, uncertainty can continue widening and eventually cross the decision boundary.*

I find this picture more helpful than a single certification number.
The nominal score might look confident. But if the surrounding tube spreads across zero, the classifier's apparent confidence is not enough. A small uncertainty at the beginning of a sequence has been allowed to accumulate until the eventual label is no longer guaranteed.
So the question becomes: what determines whether the tube settles down or keeps widening?

Let $r_t$ denote the half-width of the possible state interval after step $t$. For the linear system above, its growth is bounded by a recurrence of the form
$$
r_t
\leq
\lVert A \rVert_\infty r_{t-1}
+
\delta \lVert B \rVert_\infty.
$$
There are two terms here: the first tells us what happens to uncertainty already stored in the state, and the second tells us how much new uncertainty arrives from the next input.
Now consider the quantity
$$
\lVert A \rVert_\infty.
$$
This is the largest absolute row sum of $A$. In this setting, it tells us how much existing uncertainty can be amplified by a single state update.

If
$$
\lVert A \rVert_\infty < 1,
$$
then every update shrinks the uncertainty already present in the state before the next input adds some more.
The system is contracting and the resulting uncertainty has a finite long-run bound:
$$
r_\infty
\leq
\frac{
\delta \lVert B \rVert_\infty
}{
1 - \lVert A \rVert_\infty
}.
$$
If, on the other hand,
$$
\lVert A \rVert_\infty \geq 1,
$$
then the existing uncertainty is not forced to shrink. In the worst-case interval recursion, its effect can continue accumulating with sequence length. We lose the clean, horizon-independent guarantee which made certification meaningful in the first place.

This is why the boundary at one is not merely an aesthetic stability condition. For this linear setting, it separates a regime where uncertainty can settle from one where it need not.

#### Training a classifier that can make the promise

The most straightforward way to encourage contraction is to add a penalty to the ordinary classification objective:

$$
\mathcal{L} =
\mathcal{L}_{\mathrm{BCE}}
+
\lambda
\operatorname{relu}
\left(
\lVert A \rVert_\infty - 1
\right).
$$

The first term asks the classifier to distinguish harmful from benign examples.
The second term only activates if the state transition crosses the contraction boundary. Once
$$
\lVert A \rVert_\infty < 1,
$$
the penalty is zero.
This is a small modification, but it changes the question the model is trained to answer. We are not only asking it to classify correctly. We are also asking it to organize its dynamics so that uncertainty from small input changes does not endlessly compound.
There is, of course, a catch. Contraction alone does not certify anything.
A classifier can be perfectly contracting and still have a score very close to zero. Certification requires both a bounded uncertainty interval and a sufficiently large margin between that interval and the decision boundary.
In other words, stability keeps the tube narrow. The classifier still has to place the tube on the correct side of zero.

#### The scope of the promise

The result here is deliberately narrow.
It applies exactly to a linear time-invariant safety classifier under a bounded embedding-space perturbation model. It is not yet a guarantee against arbitrary discrete jailbreaks, paraphrases, adaptive token-substitution attacks, or the full nonlinear behaviour of a large language model.
But I think the narrowness is useful.
Safety evaluation often asks whether a detector worked on a collection of attacks. Certification asks a different question: under a stated model of perturbation, can the detector promise that it will not change its mind?
For a recurrent classifier, that question eventually becomes a question about dynamics.

Can uncertainty enter the state?
Certainly.
Can it persist?
Perhaps.

But does it have to grow forever?
_Not if the system has learned to forget it._