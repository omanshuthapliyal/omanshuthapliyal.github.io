---
title: "Can LLM Finetuning be Stateful? Small states for Large Models - Part 1"
date: 2026-07-31T11:57:21-07:00
draft: false
katex: true
tags: ["ml", "controls", "state_space_models", "linear_algebra"]
# links:
#     website: "https://omanshuthapliyal.github.io/"
#     alias : "blog/HRM-part-1/"

---


In the [last post](https://omanshuthapliyal.github.io/blog/hankel-singular-values/) I talked about Hankel operators of simple linear dynamical systems. Such operators, and either eigenvalues, _"can be used as a proxy for how much memory a task actually requires in a state-space model"._ And later we tied their input-output relations empirically tie the memory requirements of a post-trained state space model (SSM) to its Hankel singular value (HSV) rates. Further, HSV-based balanced truncation can offer us to selectively choose 'some' eigenvalues to keep that involve higher input-to-output signal strength over time. 
And so, we used Hankel singular values to decide which states of a dynamical system are worth keeping. 
However, a language model also processes a sequence of tokens over time. 
We saw task-dependent HSV decay rates for various tasks for different SSM-based models.
Similarly, could we give the model a small state, one deliberately built around that same notion of "worth keeping", without retraining the entire model?

Note that this is normally phrased as a model-reduction problem. But it also sounds suspiciously like a memory problem. If one has limited room to remember the past, what is the best use of that room?

The conclusion was, in retrospect, quite intuitive. A state direction is useful when two things are true. First, the input can actually excite it. Second, once excited, it can actually affect what comes out of the system. If either of these is not true, then keeping the direction around is rather pointless. It is either a memory that cannot be written to, or a memory that cannot be read from. This is normally presented as a model-reduction story. We begin with a complicated state-space model, then ask which of its internal coordinates can be discarded without changing the input-output behaviour too much. But I find it useful to phrase the same question differently: 

> If a system has only a small amount of memory available, what should it choose to remember?

This question is not restricted to physical systems. It also appears, perhaps a little unexpectedly, in the fine-tuning of language models. 

#### Attention has access to the past. That is not quite the same as state.

Transformers, of course, already process sequences. A token can attend to tokens that came before it, and this ability is largely why they work as well as they do. However, there is a difference between being able to look at the past and maintaining a small, evolving summary of it. Suppose I have a large collection of notes. I can search through all of them whenever I need something. Alternatively, I can maintain a notebook containing the things which have continued to matter. The first strategy is access. The second is state. The distinction becomes relevant in parameter-efficient fine-tuning. A typical language-model fine-tuning procedure freezes almost all of the pretrained model and trains a small number of additional parameters. LoRA is perhaps the canonical example. In its simplest form, instead of changing a large weight matrix directly, we learn a low-rank correction: $$ W \longrightarrow W + BA, $$ where the rank of $BA$ is much smaller than the dimensions of $W$.

This is a remarkably sensible thing to do. If the pretrained model has learned useful features already, perhaps we only need a small correction to how those features are transformed. But there is something that such a correction does not do by itself. It does not have an internal variable which evolves as the sequence evolves.
At token $t$, a low-rank adapter sees the representation at token $t$ and transforms it. At token $t+1$, it again sees a representation and transforms it. Any memory of the earlier token must have been carried by the frozen model itself. 
This is perfectly adequate for many tasks. But it is a slightly odd inductive bias for tasks which really do require accumulating state. 

Consider a parity task. After reading a sequence of bits, the only question might be whether the number of ones was even or odd. Or consider a deterministic finite automaton. Each symbol changes an internal state, and the current state is the entire relevant summary of the prefix read so far. These are deliberately simple examples, but they capture a broader point. Some problems are not merely about transforming a representation at each position. They are about maintaining an evolving account of the sequence.

#### A small adapter which is itself a dynamical system 

The idea in my recent work was to make the adapter itself stateful. 
Let $$h_t$$ be the representation emitted by a frozen transformer at token $$t$$. We give the adapter a small state $$s_t$$ and update it according to $$ s_t = \bar{A}s_{t-1} + \bar{B}h_t. $$ The state then produces a residual correction, $$ r_t = Cs_t. $$ The model receives this correction in addition to its usual computation.

There are many details one can add here: gating, normalization, discretization, and where exactly the residual is inserted. But the essential idea is almost embarrassingly simple. 
- $$h_t$$ is what the frozen model currently knows. 
- $$s_t$$ is the small amount of history the adapter has decided to carry. 
- $$r_t$$ is the way this remembered history changes the present computation.

The adapter is not just a function of the current token representation. It is a tiny system which has been watching the sequence unfold. 

{{< scale src="hrm-figure-1.png" alt="A finetuning method" scale="30" >}}

*Figure 1. Both LoRA and HRM add a small trainable residual to a frozen model. LoRA modifies a weight map. HRM adds a small dynamical system whose state persists across tokens.* 

I like this comparison because it is not really a story about one method replacing the other. 
A low-rank adapter asks something like: 

> How should I locally correct this representation? 

A stateful adapter asks something different: 

> Given everything I have seen so far, what should I carry forward?

The two questions can have different answers. In particular, when a downstream task requires a sequential state to be accumulated, it seems reasonable to provide the trainable component with an explicit state of its own.

#### But what should the state remember?

Writing down a recurrence does not solve the memory problem. One can always add more state dimensions. This is rather like buying a larger notebook whenever one is unsure what to write down. It may work, but it is not a particularly satisfying principle. A state can be too small. It can fail to retain information which will matter later. But a state can also be unnecessarily large. It can contain directions which are not meaningfully written by the incoming representations, or which have almost no effect on the adapter output. This is exactly where the discussion from the previous post becomes useful again. If the adapter has limited memory, perhaps we should not decide what it retains by choosing an arbitrary state dimension and hoping the optimization procedure sorts things out. Perhaps we should use the same input-output notion of importance that motivated Hankel singular values in the first place. In the next post, I will describe how we do this using empirical controllability and observability Grammians, why this leads naturally to a reduced-order state-space adapter, and why the location at which we insert the adapter into a transformer matters almost as much as the adapter itself.


_Written with [StackEdit](https://stackedit.io/)._