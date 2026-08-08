---
title: "Can LLM Finetuning be Stateful? Small states for Large Models - Part 2"
date: 2026-08-07T11:57:21-07:00
draft: false
katex: true
tags: ["ml", "controls", "state_space_models", "linear_algebra"]
# links:
#     website: "https://omanshuthapliyal.github.io/"
#     alias : "blog/HRM-part-2/"

---
The code for this project can be found at: [https://github.com/omanshuthapliyal/HRM-adapter](https://github.com/omanshuthapliyal/HRM-adapter).
And the paper can be found at: [https://arxiv.org/pdf/2606.26290](https://arxiv.org/pdf/2606.26290).

In the [previous post](https://omanshuthapliyal.github.io/blog/hrm-part-1/), I introduced the basic idea behind a stateful adapter. Instead of asking a small trainable module to only modify the current transformer representation, we allow it to maintain a state: $$ s_t = \bar{A}s_{t-1} + \bar{B}h_t, $$ and use that state to generate a residual correction, $$ r_t = Cs_t. $$ The important unresolved question was: if this adapter gets a small amount of memory, what should it remember? The answer I want to explore is the same one that appeared in the discussion of Hankel singular values: 

> Retain state directions which are both meaningfully excited by the input and capable of meaningfully affecting the output.

### A state is useful only when it can be written to and read from 

Suppose an adapter has a state direction that the input sequence can never excite. It exists mathematically, but it will not store anything useful. Conversely, suppose the input can excite a state direction quite easily, but changing that direction barely changes the adapter output. Then the direction is a kind of private diary: information goes in, but nothing useful ever comes out. Controllability asks whether the first thing happens. Observability asks whether the second thing happens. The nice thing about the Hankel-singular-value perspective is that it refuses to treat these questions independently. A direction is important if it lies where controllability and observability meet. In a usual balanced-truncation setting, we would construct controllability and observability Gramians for a system, find balanced coordinates, and discard the directions associated with small Hankel singular values. Here, the setting is slightly different. The system is an adapter sitting beside a frozen language model. The inputs are not arbitrary control signals; they are the representations produced by the host model. So we estimate the relevant Gramians empirically from the representation stream the adapter actually sees. This gives us a way to initialize a reduced state-space adapter. The emphasis here is important. We are not simply saying that a small state is efficient. We are saying that the state should be small in a particular way: it should preserve directions which matter for the adapter's empirical input-output behaviour.

### A reduced state is a claim about useful forgetting 
A language model has far more history available than any small adapter state could hope to retain. So the goal cannot be to reproduce the full sequence in $s_t$. That would be silly. The goal is to carry forward an abstraction of the sequence which remains useful. This is perhaps the most satisfying interpretation of balanced truncation in this setting. It is not merely a compression trick applied after the interesting work is done. It is a proposal for how the adapter should forget. It forgets directions which are weakly coupled to what enters it, weakly coupled to what leaves it, or both. It retains directions which can absorb relevant information from the sequence and later alter the correction supplied to the frozen transformer. 

{{< scale src="DFA-figure.png" alt="A finetuning method - on a Deterministic Finite Automaton (DFA)" scale="70" >}}

*Figure 2. A task may permit a 32-dimensional adapter state without requiring 32 meaningful dynamical directions. In our DFA experiments, the relevant solution was intrinsically much lower dimensional.*

This figure is useful because it makes a distinction that is easy to lose in notation. The number of coordinates we allocate to a state is not necessarily the number of degrees of freedom the task needs. A model can be given a large state and still settle into a much smaller effective dynamical system. Hankel reduction is a way of making that preference explicit rather than leaving it entirely to optimization.

### Where should such an adapter live? 

There is another question which sounds implementation-specific but is actually conceptual: where do we inject the adapter? The standard PEFT instinct is often to modify attention projections. Attention is, after all, where the transformer mixes information across positions. But an SSM adapter is doing something different. It is already a mechanism for accumulating information across positions. The incoming transformer representations give it a stream to summarize; its own state update provides the temporal structure. In our experiments, the adapter is placed in parallel with an MLP sublayer. This should not be read as a universal claim that MLPs are the only reasonable home for recurrence. It is a hypothesis about division of labour. The frozen attention mechanism continues to route and contextualize token representations. The recurrent adapter receives a tokenwise feature stream and maintains a compact account of the aspects which should persist. Where an adapter is inserted is therefore not just a software choice. It is a statement about which part of the computation we think needs adapting. 

### A recurrence need not be evaluated one token at a time

There is an obvious objection to adding recurrence to a transformer: is this not sequential, and therefore slow? For a time-invariant state-space model, we can unroll the recurrence: $$ s_t = \sum_{k=0}^{t-1} \bar{A}^{k}\bar{B}h_{t-k}. $$ This is a convolution. The sequence is being filtered by the impulse response $$ \bar{B}, \quad \bar{A}\bar{B}, \quad \bar{A}^2\bar{B}, \quad \ldots $$ The system is still recurrent in the sense that its state summarizes the past. But the computation can be viewed over the entire sequence and evaluated using a parallel FFT-based scan. I find this to be one of those small facts from linear systems which remains useful in surprising places. A recurrence has not disappeared just because we stopped computing it one step at a time. 

### Does the extra state actually help? 

The cleanest tests are tasks where a state is not merely helpful but unavoidable. Parity and deterministic-finite-automaton tasks require the model to update an internal summary as it reads each symbol. They are toy tasks, certainly, but they isolate the question rather well: does an adapter with an explicit evolving state help when the problem itself is explicitly stateful? The answer in our experiments was yes. The same pattern then carried into character-level language modelling on enwik8 and long-context language tasks from LongBench. On the Mistral-7B experiments, the HRM adapter and LoRA variants were compared with the same 8.4 million trainable parameters. 
HRM improved on several long-context tasks, including relative gains of 34.8% on QuALITY accuracy and 71.6% on QMSum ROUGE-1. 

I do not think the correct conclusion is that every fine-tuning problem secretly wants a state-space model. 

Sometimes a low-rank correction is exactly what is needed. But when the downstream task is fundamentally about accumulating a compact, task-relevant summary of a long sequence, it seems unnecessarily restrictive to require the adaptation mechanism itself to be memoryless. 

The point of a state is not to preserve the past. 

It is to forget the past correctly.

---
_Written with [StackEdit](https://stackedit.io/)._