---
title: "Mechanistic Interpretability of State Space Models"
status: "active"
start_date: 2026-06-01
description: "Using control theory to say which part of a state space model's recurrent state carries a behaviour: directions ranked by how strongly the past writes them and the future reads them, tested by removing a direction at every step."
organization: "Strategic Data Solutions Lab, Hitachi America Ltd."
tags: ["mechanistic-interpretability", "state-space-models", "model-reduction", "ai-safety"]
stack: ["PyTorch", "Transformers", "mamba-ssm", "NumPy", "SciPy", "pandas", "Hugging Face Hub"]
links:
  - label: "Blog post"
    url: "/blog/privileged-basis-ssm-state/"
  - label: "Code: analysis library"
    url: "https://github.com/omanshuthapliyal/ssm-interp"
  - label: "Code: experiment runs"
    url: "https://github.com/omanshuthapliyal/ssm-interp-runs"
  - label: "Data: Gramian statistics"
    url: "https://huggingface.co/xero91/ssm-mech-gramians"
image: "/images/projects/proj10-gramians-thumb.png"
image_alt: "Two Gramian ellipses pointing in different directions in the original coordinates, and a single shared ellipse with axes sigma 1 and sigma 2 after balancing"
hero_image: "/images/projects/proj10-unrolled-channel.png"
hero_alt: "One SSM channel unrolled along the sequence: inputs up to time t write into the state through B, the state is carried forward by A, and outputs after t read it through C; a dashed line marks the cut between past and future, and one path from the input at t minus 2 to the output at t plus 1 is highlighted with weight CA times A squared B"
image_caption: "One channel of the SSM inside a Mamba block, unrolled along the sequence. Every path from a past input to a future output passes through the state, and the weights of these paths form the Hankel operator, whose singular directions are the candidate features. From [A Privileged Basis for the Recurrent State of SSMs](/blog/privileged-basis-ssm-state/)."
related: ["blog/privileged-basis-ssm-state", "blog/hankel-singular-values", "blog/safety-classifier-ssm"]
---

## Problem

Hybrid language models such as NVIDIA's Nemotron-H and TII's Falcon-H1 now
combine attention with state space model (SSM) layers at tens of billions of
parameters. Interpretability tools can already find the layer where an SSM
computes a behaviour, but not which part of its recurrent state carries it.
Two properties stand in the way. An intervention at a single step is undone
as later inputs rebuild the state, and any change of coordinates gives an
equally valid state, so a single state coordinate has no fixed meaning.

## Approach

Control theory has a coordinate-free answer to the question of which state
directions matter. Balanced realization ranks them by how strongly the past
writes into them and the future reads from them, and the ranking, given by the
Hankel singular values, does not depend on the coordinates we start from. This
project treats the top balanced directions as candidate features of the
recurrent state, much as transformer interpretability treats subspaces of the
residual stream, and tests them by removing a direction at every step of the
sequence.

{{< figure src="/images/projects/proj10-mamba-block.png" width="540" alt="A Mamba layer on the residual stream: the block reads the stream through W_in, splits it into a signal and a gate, passes the signal through a causal convolution and a selective SSM whose state h_t is carried along the sequence, multiplies by the gate and writes back through W_out" caption="A Mamba layer reads the residual stream through an input projection and writes back through an output projection, much as an attention head does; the selective SSM between them keeps a small state in each channel. From [A Privileged Basis for the Recurrent State of SSMs](/blog/privileged-basis-ssm-state/)." >}}

- **Do the top balanced directions carry a behaviour?** In small linear SSMs
  trained on synthetic tasks with well-separated timescales, removing the top
  balanced direction affects its own output channel about 250 times more than
  the others, while an intervention at a single step is far less selective
  ([blog post](/blog/privileged-basis-ssm-state/)).
- **Can the picture be carried over to Mamba?** In each channel of a Mamba
  layer, the input-dependent parameters are averaged over a corpus to give a
  fixed linear system. A first proxy, which keeps only each channel's most
  controllable direction, locates the layers that matter for indirect object
  identification and induction from 130M to 2.8B parameters. The test of the
  balanced directions themselves is in progress.
- **How do attention and SSM layers divide the work in hybrids?** Layer
  knockouts suggest that the arrangement matters: attention carries most of
  the IOI effect in Falcon-H1, where the two run side by side, while early SSM
  layers carry the largest single effects in Nemotron-H-56B.

## Outcome

- **A principled candidate for the features of a recurrent state.** Balanced
  directions from control theory, proposed as a privileged basis for the state
  of an SSM, with a test that can show the idea is wrong.
- **Early evidence at small scale.** In linear SSMs, removing the top balanced
  direction disrupts the output it carries about 250 times more than the
  others.
- **Experiments across nine models.** Pure Mamba from 130M to 2.8B parameters,
  and two hybrid families up to 56B.
- **Released early.** Open-source analysis code, and per-layer statistics for
  Mamba models from 130M to 2.8B on Hugging Face.
