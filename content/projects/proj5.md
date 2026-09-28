---
title: "Behind-the-Meter Energy Hub Dispatch for Data Centers"
status: "active"
start_date: 2026-01-01
resources:
  - label: "Hitachi Review article (Dec 2024): From Supply Chain to Operations, A Portfolio Approach to Capacity Expansion in Colocation Data Centers"
    url: "https://www.hitachihyoron.com/rev/contents/202412/tech_docs/08/index.html"
description: "Data Center Behind-the-meter Energy Hub dispatch problem formulated as two interacting world models, one for the gas-turbine fleet and one for the AI data hall, planned jointly through a differentiable rollout for MPC and RL control."
tags: ["world-models", "physics-informed-ml", "differentiable-mpc", "reinforcement-learning", "energy-systems", "data-centers"]
organization: "Strategic Data Solutions Lab, Hitachi America Ltd."
patent: "patents/patent-07"
image: "/images/projects/proj5-wm-predict-thumb.jpg"
image_alt: "Demo screen showing the turbine forecast and the data hall prediction surface"
hero_image: "/images/projects/proj5-wm-encode-predict.gif"
hero_still: "/images/projects/proj5-wm-encode-predict-still.jpg"
hero_alt: "Animated capture of the demo's encode and predict steps"
image_caption: "Demo excerpt: live data from the turbines and the data hall is encoded into a shared state, then each world model forecasts ahead."
stack: ["PyTorch", "Stable-Baselines3", "Gymnasium", "RAPS", "Streamlit", "FastAPI"]
related: ["patents/patent-07"]
---

## Problem

AI workloads can push a data center's power demand up by tens of megawatts in
minutes, often faster than its grid connection can supply. On-site gas turbines
can cover the gap, but they respond over minutes while computing load changes
in seconds. Keeping the two in balance without tripping any plant limit is a
hard control problem.

## Approach

Each side of the facility gets its own learned world model: one for the turbine
fleet and one for the AI data hall. A single planner looks ahead across both at
once and decides how far the turbines should ramp and how much work the data
hall can safely defer. Every command is checked against the turbines' physical
limits before it reaches the plant, so the learned components never act
unchecked.

## Outcome

- **Real-time decisions on ordinary hardware.** The planner decides in 10–50
  milliseconds on a CPU, fast enough for live plant control with no GPU.
- **Accurate forecasts of both sides.** Both world models met their accuracy
  targets, trained on nearly 650,000 examples that include real job traces from
  NREL's Kestrel supercomputer augmented with [RAPS simulator](https://github.com/ExaDigiT/RAPS).
- **Better than conventional control.** The learned control policy outperforms
  a standard fixed-setpoint controller.
- **A working end-to-end demo.** The full loop runs interactively, from
  prediction to actuation, including an islanding mode for grid disconnects.
- **Patent filed** on the interacting world models approach.

<!-- ## What's next

Results so far come from simulation. Next come a full-scale surge benchmark,
battery storage as a third world model, and tuning the turbine model on real
plant data. -->
