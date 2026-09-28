---
title: "Safety and Cybersecurity of Cyberphysical Systems"
status: "completed"
start_date: 2019-01-01
end_date: 2023-05-31
description: "My doctoral research at Purdue: fast, data-driven ways to prove that learned, networked and multi-agent autonomous systems stay safe, and to expose how attackers could exploit them."
organization: "Flight Dynamics & Control / Hybrid Systems Lab, Purdue University"
tags: ["reachability", "cyberphysical-systems", "cybersecurity", "multi-agent-systems", "koopman-operators", "urban-air-mobility"]
stack: ["MATLAB", "Python", "CVX", "MOSEK", "MATLAB Optimization Toolbox", "CORA"]
links:
  - label: "Dissertation"
    url: "https://docs.lib.purdue.edu/dissertations/AAI30499122/"
  - label: "Code: distributed path planning"
    url: "https://github.com/omanshuthapliyal/LP-pathplan"
  - label: "Code: mixed-monotone reachability (partial)"
    url: "https://github.com/omanshuthapliyal/linearReachExample"
image: "/images/projects/proj4-nn-reach-framework.png"
image_alt: "Framework schematic: windows of past states and inputs excite a neural network model; the learned feature space is approximated by a linear model in a Koopman observable space"
hero_alt: "Framework schematic: windows of past states and control inputs are fed to a learned neural network model of the dynamics; its behavior in a nonlinear feature space is approximated, window by window, by a linear model in a Koopman observable space"
image_caption: "The core idea behind the learned-systems work: excite a neural network model of the dynamics with short windows of data, fit a linear model in a Koopman observable space, and use that linear model for fast safety analysis. From [Approximating Reachable Sets for Neural Network-Based Models in Real Time via Optimal Control](/papers/approximating-reachable-sets-for-neural-network-based-models-in-real-time-via-optimal-control/), IEEE TCST 2023."
related: ["papers/pub19", "papers/pub9", "papers/pub15", "papers/pub5", "papers/pub8", "papers/pub7", "papers/pub12", "papers/pub11", "papers/pub6", "papers/pub4", "papers/pub10", "blog/data-driven-safety"]
resources:
  - label: "Lab page: Secure and Safe Assured Autonomy (S2A2), FD&C/HSL, Purdue"
    url: "https://sites.google.com/view/fdchsl/projects/secure-and-safe-assured-autonomy"
  - label: "S2A2 program website (NASA University Leadership Initiative)"
    url: "https://s2a2.ncat.edu/#/home"
  - label: "Purdue ME news (2025): Purdue and Saab collaborate on autonomous marine vehicles"
    url: "https://engineering.purdue.edu/ME/News/2025/purdue-and-saab-collaborate-on-autonomous-marine-vehicles"
  - label: "Saab newsroom (2024): Saab and Purdue team up on DARPA program for uncrewed sea vessels"
    url: "https://www.saab.com/markets/united-states/us-newsroom/stories/2024/saab-and-purdue-university-team-up-on-darpa-program-to-advance-adaptive-controls-for-uncrewed-sea-vessels"
---

## Problem

Drones, air taxis and robot teams are cyberphysical systems: physical machines
run by software and linked by networks. Before they can be trusted in
safety-critical airspace, we need to know every state they could reach, and
whether any of those states is unsafe. The exact answer comes from solving
high-dimensional partial differential equations, which is out of reach once a
system is nonlinear, learned from data by a neural network, spread across many
agents, or under cyberattack.

My doctoral dissertation, *Data-Driven Safety & Security of Cyberphysical
Systems*,
computes these safety guarantees without solving those equations. It uses
data, Koopman operator theory and optimal control to approximate reachable
sets quickly, and then turns the same tools around to show how an attacker
could exploit such systems. The work has three thrusts.

## Safety of learned systems

When the dynamics are unknown, or learned by a neural network, there is no
model to analyze directly. Two questions drive this thrust:

- **How much can an unknown system reach, judged from data alone?** A Koopman
  model of the system is learned from data and embedded in a structure (mixed
  monotonicity) whose reachable sets are cheap to bound. On a 7-state
  enzymatic benchmark, it over-approximates the reachable set faster than the
  CORA reachability toolbox for longer time horizons
  ([IEEE Access 2022](/papers/approximate-reachability-for-koopman-systems-using-mixed-monotonicity/)).

{{< figure src="/images/projects/proj4-koopman-cora-vs-mm.jpg" alt="Two sets of four projections of the reachable set of a 7-state system: left, the set computed by the CORA toolbox in green; right, the box-shaped over-approximation computed by the proposed method in yellow, enclosing the same trajectories" caption="Reachable set of the 7-state Laub-Loomis model: computed by the CORA toolbox (left, green) and over-approximated by the Koopman mixed-monotonicity method (right, yellow boxes), both enclosing the sampled trajectories. From [Approximate reachability for Koopman systems using mixed monotonicity](/papers/approximate-reachability-for-koopman-systems-using-mixed-monotonicity/), IEEE Access 2022." >}}

- **Can safety be checked in real time when the model is a neural network?**
  A network learns a quadrotor's dynamics offline from trajectory data. Online,
  it is excited with short windows of inputs, and dynamic mode decomposition
  turns its response into a sequence of linear models. Optimal control then
  pushes the edges of the initial set forward in time, giving polytopic
  reachable sets in real time, with accuracy tuned by how many edges are used.
  The same pipeline still works after two of the quadrotor's rotors fail
  ([IEEE TCST 2023](/papers/approximating-reachable-sets-for-neural-network-based-models-in-real-time-via-optimal-control/)).

{{< figure src="/images/projects/proj4-quadrotor-true-learned-dmd.jpg" width="540" alt="Three 3D plots of quadrotor trajectory bundles: the true trajectories in red, the neural network's learned trajectories in blue, and the linear DMD approximations in black, all following the same path" caption="Quadrotor trajectories from the true dynamics (red), the learned neural network (blue) and the linear approximation used for reachability (black)." >}}

{{< figure src="/images/projects/proj4-quadrotor-reach-inputs.png" width="540" alt="Left: reachable-set slices drawn as red polygons along a quadrotor trajectory in the y-z plane. Right: four plots of the optimal rotor inputs, stepping down over time inside shaded bounds" caption="Reachable-set approximations (red) along a quadrotor trajectory in the y–z plane, and the optimal rotor inputs that generate them, inside their limits (right). From [Approximating Reachable Sets for Neural Network-Based Models in Real Time via Optimal Control](/papers/approximating-reachable-sets-for-neural-network-based-models-in-real-time-via-optimal-control/), IEEE TCST 2023." >}}

## Safety of multi-agent systems

In a team of agents, each agent's feedback depends on its neighbors, so their
reachable sets are coupled, yet no agent knows the whole team's dynamics.

- **Can each agent compute its own reachable set using only its neighbors?**
  Yes, and the answer rests on two results
  ([ACC 2025](/papers/an-algorithm-for-distributed-computation-of-reachable-sets-for-multi-agent-systems/)):
  - *Polytopic reachability.* Building on Varaiya's classic result, every flat
    face touching the initial set can be tracked forward in time: its contact
    point follows the system dynamics driven by the solution of a small optimal
    control problem. Together, the tracked faces bound the reachable set, and
    adding faces tightens the bound.
  - *Distributed convergence.* The computation splits into steps each agent
    runs with its neighbors. As long as the communication network, even one
    that changes over time, is connected often enough (repeatedly jointly
    strongly connected), the shared linear-algebra steps converge exponentially
    fast and the optimal control step finishes in finite time.

{{< figure src="/images/projects/proj4-mas-coupled-reach.png" width="540" alt="Left: a network of agents with one agent's neighborhood highlighted. Right: two initial sets whose reachable sets overlap, marked with a question mark" caption="Agent i sees only its neighborhood, but its reachable set is coupled to its neighbors'. From [An Algorithm for Distributed Computation of Reachable Sets for Multi-Agent Systems](/papers/an-algorithm-for-distributed-computation-of-reachable-sets-for-multi-agent-systems/), ACC 2025." >}}

- **How can a team of robots avoid obstacles that only some of them can see?**
  Knowledge of the obstacles is spread across the network, so the planning
  problem is split into small linear programs, one per robot, which is far
  cheaper than solving one large nonlinear problem
  ([ACC 2021](/papers/path-planning-for-a-network-of-robots-with-distributed-multi-objective-linear-programming/)).
- **How fast can a network of agents solve a shared optimization problem?** A
  distributed, fast-tracking version of the ADMM algorithm reaches an optimal
  convergence rate
  ([IEEE SMC 2021](/papers/distributed-fast-tracking-alternating-direction-method-of-multipliers-admm-algorithm-with-optimal-convergence-rate/)).

## Cybersecurity of networked systems

The same data that makes safety analysis possible also helps an attacker. This
thrust asks how networked control systems can be attacked, and how they can be
defended.

### Data-driven attacks on networked control

- **What can an attacker do with nothing but observed data?** By learning a
  model of a networked system from data alone, an attacker can design
  coordinated false-data-injection and denial-of-service attacks, corrupting
  what agents sense and cutting the links between them, that break a
  five-drone formation
  ([IFAC World Congress 2023](/papers/data-driven-cyberattack-synthesis-against-network-control-systems/)).
- **Can an attacker force a switching controller into the wrong mode, and can
  it be stopped?** A neural network learns when the controller switches modes
  and crafts attacks that trigger the wrong one. On the defense side, a
  generative adversarial network detects the injected signals and
  reconstructs clean data, keeping a robot formation on course
  ([ECC 2021](/papers/learning-based-cyberattack-design-and-defense-for-supervisory-control-systems/)).

{{< figure src="/images/projects/proj4-supervisory-attack-defense.png" alt="Left: coordinate scheme for two robots in formation. Middle: three robot trajectories staying in formation with the defense active. Right: robot 3's trajectory looping away under attack with no defense" caption="Left: the formation-control setup. Middle: with the learned defense, all three robots stay in formation. Right: without it, an attack on robot 3 drives it off course. From [Learning Based Cyberattack Design and Defense for Supervisory Control Systems](/papers/learning-based-cyberattack-design-and-defense-for-supervisory-control-systems/), ECC 2021." >}}

- **When will a human misread what the automation is doing?** For systems that
  switch between modes, mode confusion is predicted ahead of time using
  mixed-integer linear programming
  ([IEEE CDC 2019](/papers/predicting-mode-confusion-through-mixed-integer-linear-programming/)).

### Cybersecurity of urban air mobility networks

Air taxis and drones sharing urban airspace will coordinate over networks,
which makes those networks a target.

- **How can a fleet keep working when the networks that tie it together are
  attacked?** A distributed, optimization-based controller keeps a multi-agent
  system working under cyberattack when agents interact through two separate
  networks
  ([AIAA SciTech 2022](/papers/attack-resilient-distributed-optimization-based-control-of-multi-agent-systems-with-dual-interaction-networks/)).
- **How exposed is each aircraft to a distributed denial-of-service attack?** A
  graph-based vulnerability score lets each aircraft assess its own exposure,
  then reorganize with its neighbors to cut collision risk, all without a
  central coordinator. The resulting control provably reduces vulnerability,
  in a probabilistic sense, against an attacker with a known budget
  ([Journal of Aerospace Information Systems, 2023](/papers/distributed-denial-of-service-resilient-control-for-urban-air-mobility-applications/)).

## Outcome

- **Real-time safety checks for learned systems.** Reachable sets for a
  neural-network quadrotor model computed in real time, including after rotor
  failure.
- **Part of a NASA program for safe urban air mobility.** Research carried out
  under NASA's University Leadership Initiative project *Secure and Safe
  Assured Autonomy* (S2A2), on its secured-autonomy challenge.
- **Follow-on DARPA funding.** Co-authored the successful proposal behind
  Purdue's collaboration with Saab on DARPA's Learning Introspective Control
  (LINC) program, developing adaptive, self-correcting control for uncrewed
  sea vessels.
- **Eleven papers,** including journal articles in IEEE Transactions on
  Control Systems Technology, IEEE Access and the Journal of Aerospace
  Information Systems, and the basis of my Ph.D. dissertation (Purdue, 2023).
