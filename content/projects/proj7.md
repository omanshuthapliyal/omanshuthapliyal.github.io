---
title: "Unmanned Aerial Vehicle Safe Autonomous Operations"
status: "completed"
start_date: 2023-01-01
end_date: 2025-12-31
description: "Safety guarantees for autonomous drones and air taxis: learned reachable sets that build collision avoidance into the controller, and camera-based 3D models from neural radiance fields for safe path planning."
organization: "Strategic Data Solutions Lab, Hitachi America Ltd."
tags: ["reachability", "physics-informed-ml", "neural-radiance-fields", "safe-navigation", "urban-air-mobility"]
stack: ["DeepReach", "PyTorch", "hj_reachability", "JAX", "nerfstudio"]
paper: "https://arxiv.org/abs/2604.26899"
patent: "patents/patent-02"
slides: "https://github.com/omanshuthapliyal/ICMCR-2026--OT/blob/main/ICMCR-nerf-reachability.pdf"
related: ["papers/pub16", "papers/pub13", "patents/patent-02"]
image: "/images/projects/proj7-pinn-reach-thumb.jpg"
image_alt: "2D slice of a UAV collision-avoidance value function, with the zero level set drawn in black"
hero_image: "/images/projects/proj7-pinn-reach-sidebyside.gif"
hero_still: "/images/projects/proj7-pinn-reach-still.png"
hero_alt: "Two animations side by side: a 2D slice of the value function for two UAVs avoiding a collision, evolving over time with its zero level set in black, and the matching reachable tube rendered as a rotating 3D volume"
image_caption: "Two UAVs avoiding a collision, a standard benchmark known as Air3D. Left: a 2D slice of the value function as it evolves, with the zero level set (black) marking the boundary of the states that can lead to a collision. Right: the full reachable tube in 3D, over relative position and heading. From [Embedding Safety Requirements into Learning-Based Controllers for Urban Air Mobility Applications](/papers/embedding-safety-requirements-into-learning-based-controllers-for-urban-air-mobility-applications/), AIAA SciTech 2024."
---

## Problem

Air taxis and delivery drones are expected to fly autonomously over cities,
but public trust is low: in one survey cited in this work, only 26% of
respondents trusted autonomous air taxis. Before these vehicles can fly on
their own, their controllers need a clear safety guarantee: the set of states
from which the vehicle can still avoid a collision or reach its landing pad.
Computing that set means solving a Hamilton-Jacobi equation, and grid-based
solvers become impractical for realistic vehicle models with 6 to 12 states.
Learning-based controllers scale better, but they are hard to certify.

## Approach

The first line of work learns the safety guarantee instead of gridding it. A
physics-informed neural network is trained to satisfy the Hamilton-Jacobi
equation and its boundary conditions, building on the open-source
[DeepReach](https://github.com/smlbansal/deepreach) framework. The learned
value function gives the reachable set directly, and the safe control follows
from it. Results are checked against
[hj_reachability](https://github.com/StanfordASL/hj_reachability), a JAX-based
numerical solver.

The second line of work brings camera-based 3D models into path planning. A
neural radiance field, trained with nerfstudio on images from several
viewpoints, turns an object into a 3D point cloud. Its convex hull can stand
for the robot's own shape, an obstacle or the goal. The robot's reachable sets
are computed in closed form as polytopes, so a model predictive controller only
has to satisfy linear inequality constraints to stay clear of every obstacle.

{{< figure src="/images/projects/proj7-nerf-reach.jpg" width="540" alt="Four panels: point clouds of an object recovered from a neural radiance field at four viewing angles, their convex hull, a planned path through a field of box obstacles, and a close-up of the convex hull at the goal" caption="From images to a safe path: (1) an object recovered from a neural radiance field, seen from several angles, (2) wrapped in a convex hull, (3) a collision-free path through randomly placed obstacles to a goal defined by that object, and (4) a close-up of the goal. Adapted from [Safe Navigation using Neural Radiance Fields via Reachable Sets](/papers/safe-navigation-using-neural-radiance-fields-via-reachable-sets/), ICMCR 2026." >}}

## Outcome

- **Learned safety that matches a numerical solver.** On the Air3D benchmark,
  where two UAVs must avoid a collision, the physics-informed network
  reproduces the nonconvex reachable tube computed by a numerical solver.
- **Safe vertiport landing.** The same approach finds every state from which a
  UAV can land safely on a vertiport.
- **Collision-free planning with NeRF models.** Closed-form reachable sets keep
  the planner clear of obstacles in two cluttered scenarios, using a NeRF
  object as the robot's shape in one and as the goal in the other. The NeRF
  model trains in about 18 minutes on a single CPU.
- **Published and patented.** Papers at AIAA SciTech 2024 and ICMCR 2026, and a
  patent application on AI-based safe control for unmanned aerial systems.
