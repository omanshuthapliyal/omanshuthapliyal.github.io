---
title: "Provable Safety and Efficient Memory for Language Models"
status: "active"
aliases: ["/projects/control-theoretic-ai-safety-for-language-models/", "/projects/control-theoretic-ai-in-language-models-safety-and-enhancing-memory/"]
weight: 1                   # among ongoing projects with the same start date, lower weight is listed first
start_date: 2025-01-01
description: "Using control theory to make language-model components predictable enough for safety-critical deployment: safety classifiers that can prove their decisions, and fine-tuning adapters whose memory can be analyzed and compressed with guarantees."
organization: "Strategic Data Solutions Lab, Hitachi America Ltd."
collaborators: ["Malarvizhi Sankaranarayanasamy"]
tags: ["ai-safety", "jailbreak-detection", "certified-robustness", "reachability", "state-space-models", "parameter-efficient-fine-tuning", "model-reduction"]
stack: ["PyTorch", "mamba-ssm", "Transformers", "PEFT", "SciPy", "scikit-learn", "TextAttack", "JailbreakBench", "HarmBench", "LongBench"]
links:
  - label: "Paper: certified safety head (arXiv)"
    url: "https://arxiv.org/abs/2610.02853"
  - label: "Code: certified safety head"
    url: "https://github.com/omanshuthapliyal/contraction_constrained-safety-head"
  - label: "Code: HRM adapter"
    url: "https://github.com/omanshuthapliyal/HRM-adapter"
image: "/images/projects/proj9-hrm-vs-lora-thumb.png"
image_alt: "Block diagrams comparing LoRA, a low-rank update beside frozen attention weights, with the HRM adapter, a small state space model beside the frozen MLP"
hero_image: "/images/projects/proj9-reach-tube.png"
hero_alt: "Six panels of classifier score over 64 tokens. Left column, contraction-constrained model: the shaded band of reachable scores stays narrow and two of three examples are certified. Right column, unconstrained model: the band widens over the sequence and crosses the decision boundary, so none are certified"
image_caption: "Reach tubes: every score a safety classifier could output while reading a prompt whose token embeddings are nudged within a small bound. With contraction (left), the tube settles and the decision can be certified. Without it (right), uncertainty keeps growing until it crosses the decision boundary. From [Bounded Reachability & Jailbreak Detection via Contraction-Constrained State Space Models](/papers/bounded-reachability-jailbreak-detection-via-contraction-constrained-state-space-models/), AIMS @ COLM 2026."
related: ["papers/pub20", "papers/pub18", "blog/safety-classifier-ssm", "blog/hrm-part-1", "blog/hrm-part-2", "blog/hankel-singular-values"]
---

## Problem

Putting language models into safety-critical operations raises questions that
accuracy benchmarks do not answer. If a safety filter says a prompt is safe,
will it still say so when the prompt is changed slightly? When a model is
adapted to a new task, what has the added component learned to remember, and
can that be bounded?

Both are questions about dynamics. State space models (SSMs), the recurrent
architecture behind Mamba and S4, are dynamical systems, so the tools used to
certify controllers apply to them directly: reachability, contraction and
model reduction. This project uses those tools to build language-model
components whose behavior can be checked, not just measured.

## Certifiable safety classifiers

A safety head is a small classifier that screens prompts before a model
responds. The question is whether it can promise not to change its mind.

- **Can a safety classifier prove its decision holds under small input
  changes?** For a linear SSM classifier, the full set of scores it could
  produce, while every token embedding is nudged within a fixed bound, can be
  computed exactly. That set stays bounded, whatever the prompt length, if
  and only if the state transition is contracting. A simple training penalty
  enforces contraction, and on toxic-comment data it raises the share of
  certified decisions from 41% to 59%, with a sharp transition exactly where
  the theory predicts
  ([AIMS @ COLM 2026](/papers/bounded-reachability-jailbreak-detection-via-contraction-constrained-state-space-models/)).
- **Does the idea carry over to jailbreak detection?** A 54,000-parameter,
  contraction-regularized S4 head reads only the prompt's token embeddings
  from Mamba-130M, so it runs in about 5 ms on a CPU, before any response is
  generated. Trained on JailbreakBench, it detects all six attack families and
  transfers zero-shot to AdvBench and HarmBench.
- **What does the guarantee cover, and what not?** A linear probe on the same
  embeddings detects jailbreaks just as well, so the head's value is the
  certificate, which no probe provides. The certificate holds in embedding
  space: adaptive attackers who swap whole tokens can still evade the head,
  which sets the next problem.

## Adapters with analyzable memory

Parameter-efficient fine-tuning such as LoRA corrects each token's
representation independently, so the adapter itself has no memory. Tasks such
as long-document question answering need an evolving summary of what has been
read.

{{< figure src="/images/projects/proj9-hrm-vs-lora.png" alt="Two block diagrams of a transformer layer. Left: LoRA adds a low-rank update beside a frozen weight matrix in attention. Right: the HRM adapter adds a small state space model beside the frozen MLP, gated into the residual stream, while attention stays frozen" caption="LoRA (left) adds a low-rank correction to a frozen weight matrix. The Hankel reduced-order model (HRM) adapter (right) adds a small state space model beside the frozen MLP, whose state carries information across tokens. From [SSM Adapters via Hankel Reduced-order Modeling](/papers/ssm-adapters-via-hankel-reduced-order-modeling-injection-site-determines-task-suitability-in-long-context-fine-tuning/), HiLD @ ICML 2026." >}}

- **Can a fine-tuning adapter carry state?** The HRM adapter is a small SSM
  added beside the MLP of a frozen transformer. Because its dynamics are
  linear and time-invariant, the recurrence runs as an FFT convolution, with
  wall-clock cost on par with LoRA
  ([HiLD @ ICML 2026](/papers/ssm-adapters-via-hankel-reduced-order-modeling-injection-site-determines-task-suitability-in-long-context-fine-tuning/)).
- **What should a small memory keep?** Directions of the state that the input
  can excite and that also affect the output. These are ranked by Hankel
  singular values from Gramians estimated on the data, and balanced truncation
  keeps only the important ones, with a certified bound on the error this
  introduces. The spectrum doubles as a fingerprint of how much memory a task
  needs.

{{< figure src="/images/projects/proj9-dfa-hsv.png" alt="Left: bar chart of validation accuracy on a state-tracking task at four sequence lengths, with HRM and its truncated version above LoRA at every length. Right: Hankel singular values falling steeply, with only five above the cutoff" caption="Left: on a finite-state-machine tracking task, HRM and its balanced-truncation reduction (HRM-BT) beat LoRA at every sequence length. Right: the Hankel singular value spectrum shows that only 5 of 32 state directions matter for this task. From [SSM Adapters via Hankel Reduced-order Modeling](/papers/ssm-adapters-via-hankel-reduced-order-modeling-injection-site-determines-task-suitability-in-long-context-fine-tuning/), HiLD @ ICML 2026." >}}

- **Where in the network should memory go?** The injection site decides which
  tasks an adapter suits: adapters in attention help retrieval, while an
  adapter beside the MLP integrates information over the sequence.
- **Does it help at scale?** On Mistral-7B, at the same 8.4 million trainable
  parameters as LoRA, AdaLoRA, DoRA and QLoRA, HRM gives the best results on
  the tasks that need sequential integration (QuALITY and QMSum), and trails
  on retrieval-heavy NarrativeQA.

## Outcome

- **Safety filters that can prove their decisions.** A training recipe that
  makes a lightweight safety classifier certifiably stable under bounded input
  perturbations, with the threshold predicted by theory.
- **Jailbreaks caught before the model answers.** Zero-shot, the head flags
  over 98% of held-out harmful prompts from AdvBench and HarmBench, from the
  prompt alone.
- **Fine-tuning that remembers.** A stateful adapter that beats LoRA-family
  methods on long-document tasks, including 35% higher relative accuracy on
  QuALITY with Mistral-7B at an equal parameter budget.
- **Published and open-sourced.** Papers at the HiLD workshop at ICML 2026 and
  the AIMS workshop at COLM 2026, with code for both.
