---
title: "Replicating Expert Behavior via Imitation Learning"
status: "completed"
start_date: 2023-01-01
end_date: 2024-12-31
description: "An imitation-learning system that learns how expert operators make decisions in Oil & Gas SCADA operations from multi-sensor data, so those decisions can be made autonomously."
organization: "Big Data Analytics & Solutions Lab, Hitachi America Ltd."
tags: ["imitation-learning", "generative-adversarial-networks", "industrial-automation", "scada"]
patent: "patents/patent-05"
related: ["patents/patent-05"]
---

## Problem

Oil & Gas production assets are run through SCADA systems, where experienced
operators read many sensor streams and decide how to act. That know-how is
hard to write down as rules. This project set out to learn those decisions
directly from recorded expert behavior, so that they can be made
autonomously.

## Approach

The system is built on Generative Adversarial Imitation Learning (GAIL).
Instead of hand-designing a reward, two networks are trained against each
other on multi-sensor SCADA data: a discriminator learns to tell the experts'
recorded decisions apart from the policy's, and the policy learns to make
decisions the discriminator cannot tell apart from the experts'. The trained
policy then reproduces expert behavior.

## Outcome

- **Validated in a pilot deployment.** The system reached over 85% accuracy on
  its first run.
- **Scaled to production.** After the pilot, it was rolled out across multiple
  production assets.
- **A patent and a paper.** A filed patent application on industrial automation
  that learns from, and works with, human operators, and a paper under review.
