---
title: "State Estimation under Communication Uncertainties"
status: "completed"
start_date: 2015-01-01
end_date: 2017-12-31
description: "Estimators that keep tracking accurate when sensor data is lost in transit, including losses that cluster in predictable regions, and that let a network of sensors agree on one estimate. Demonstrated on aircraft tracking."
organization: "Flight Dynamics & Control / Hybrid Systems Lab, Purdue University"
tags: ["state-estimation", "kalman-filtering", "networked-control-systems", "sensor-networks", "air-traffic-control"]
paper: "papers/pub3"
links:
  - label: "M.S. thesis slides"
    url: "https://github.com/omanshuthapliyal/KF-MS-dissertation/blob/main/MS-dissertationSlides_Omanshu__print_friendly_.pdf"
resources:
  - label: "Lab page: State estimation with packet losses"
    url: "https://sites.google.com/view/fdchsl/research/air-traffic-control/done-state-estimation-with-packet-losses"
  - label: "Lab page: Distributed state estimation for a network of agents"
    url: "https://sites.google.com/view/fdchsl/research/air-traffic-control/done-distributed-state-estimation-for-a-network-of-agents"
related: ["papers/pub3", "papers/pub2", "papers/pub1"]
image: "/images/projects/proj3-packet-loss-thumb.png"
image_alt: "Aircraft trajectory passing through three radio-jammer regions"
hero_image: "/images/projects/proj3-packet-loss-overview.png"
hero_alt: "Left: an aircraft trajectory passing through three jammer regions. Top right: a two-mode measurement model that switches off inside those regions. Bottom right: the estimator predicting through missed measurements and updating when they arrive."
image_caption: "An aircraft flies past radio jammers (left). Losing measurements inside the jammed regions is modeled as a switching measurement model (top right), and the estimator predicts through the gaps and updates whenever a measurement gets through (bottom right). Adapted from [Kalman filtering with state-dependent packet losses](/papers/kalman-filtering-with-statedependent-packet-losses/), IET Control Theory & Applications, 2019."
---

## Problem

Air traffic surveillance, like many tracking systems, relies on measurements
sent over imperfect communication links. Packets get dropped, sometimes at
random and sometimes in predictable places, such as regions with poor coverage
or radio jamming. A standard Kalman filter assumes every measurement arrives,
so its estimates degrade exactly where losses cluster. When many sensors track
the same aircraft, each sees only part of the picture and has to agree with its
neighbours over a network whose connections keep changing.

## Approach

The first line of work models packet arrival explicitly. For random losses
typical of real communication channels, and for losses that depend on where
the tracked object is, the estimator keeps the familiar Kalman filter structure
but updates its uncertainty to reflect the chance that each measurement
arrives, using prior knowledge of where losses are likely.

The second line of work spreads estimation across a sensor network. Each sensor
runs a local estimator for a system that switches between operating modes and
shares its estimates with neighbouring sensors, so the whole network reaches
agreement even as its connections change over time.

{{< figure src="/images/projects/proj3-consensus-schematic.png" width="540" alt="Three stacked sensor nodes. Each runs two mode-matched filters, mixes them, and updates and combines its estimate, while exchanging initial estimates and edge-error covariances with the nodes above and below." caption="How one sensor (center) updates its estimate: it runs one filter per operating mode, mixes and combines them, and trades estimates and error covariances with neighbouring sensors (above and below). Adapted from [Distributed state estimation for a stochastic linear hybrid system over a sensor network](/papers/distributed-state-estimation-for-a-stochastic-linear-hybrid-system-over-a-sensor-network/), IET Control Theory & Applications, 2018." >}}

## Outcome

- **More accurate tracking under patchy communication.** On an aircraft
  tracking example with location-dependent packet losses, the new filter
  outperforms the baseline packet-loss filter at similar computational cost.
- **Distributed estimation on changing networks.** The consensus-based
  estimator outperforms existing hybrid estimators at comparable per-sensor
  complexity, while allowing the network's connections to change.
- **Published.** Two IET Control Theory & Applications papers (2018, 2019) and
  an IEEE CDC 2017 paper. The packet-loss work formed the basis of an M.S.
  thesis at Purdue, and the distributed estimation work was supported by the
  NSF (CMMI 1335084).
