---
title: "Technology Readiness Levels of AI methods"
date: 2024-10-15T11:07:46-07:00
tags: ["controls", "autonomy", "ml", "research"]
---

Recent news of the SpaceX catching its Starship Super Heavy booster[^1] is quite discussed and marveled upon in the media, and rightly so.
Executing what was done can perhaps be explained as trying to catch a falling stick, then balancing it vertically, all while the stick is over 200 ft tall, weighs over 150 tonnes, spews fire, and costs over tens of millions of dollars.
One cannot but feel a little giddy as a controls engineering enthusiast over this massive success. 
It makes me think why we are closer to automation in certain domains/problems than others? Why, for example, is your vacuum cleaning robot seemingly better at navigating in a cluttered environment than your possibly self-driving car? Why is the tremendous progress in machine learning & AI not permeating outside of our web lives as much as we expected in the early 2000's?

I will be impatient and spill the beans for my argument upfront: *there is a reason why black-box methods still have a way to go from finding wider applications (especially in safety critical components & systems) when compared to their more mature cousins in `classical' automation & control --* **technology readiness** is one way to look at this apparent paradox of why learning-based methods find applications in our daily lives and almost all actions in the cyberspace, but not so much in human-machine teams of cyberphysical or physical spaces.

There is this age-old adage in controls engineering that finds its way into the paper title[^2] -- Give us PID controllers and we can control the world.
It comments on the interesting side of experience with industrial control systems, where most, if not all, automation is carried out by a moving slider that mixes a PID controller with model predictive control (MPC). But more importantly, it references the "Dunning-Kruger of PID" cartoon[^3], which was also a topic of [one of my other posts](/blog/split) on the ubiquity of PID & MPC.
Looking at automation from a technology readiness level (TRL) provides a systems-level view of technology maturity vs. user trust. Going from TRL 0 (concept level) through TRL 9 (production and productization) is a long journey from research labs to products on the shelf.
Typical projects and technologies traverse this TRL journey as[^5]: 
* TRL 0 - first principles,
* TRL 1 - concept formulation,
* TRL 2 - proof-of-principle,
* TRL 3 - proof-of-concept,
* TRL 4 - (sub-)component development & validation,
* TRL 5 - system development & validation,
* TRL 6 - system/subsystem/application development in operating environment,
* TRL 7 - integration stage: prototype demonstration in operating environment,
* TRL 8 - test & demonstration, and
* TRL 9 - deployment and being "mission proven"-ness.

PID and MPC controls have proven to be remarkable in the TRL regard : tried and tested methods, that actuate most actuators around the world.
The PID has had a 100 year history, and MPC has been around for 50 years, both finding eventual industry-wide acceptance. On the contrary, AI and machine learning methods have had a much shorter run from conceptualization (TRL 0) to promises of TRL 7-9 being around the corner.
I highly recommend an enjoyable read on future of AI through TRL[^4]. 
TRL lets us compare at a technology level how AI seems to do exceedingly well in machine translation, object recognition, text & speech recognition, while still having lots to achieve in self-driving, UAV autonomous flight, and context-aware recommendation.
*It also makes sense how many AI/ML projects spend remarkably short durations in TRL 0-3, as most systems build upon existing proven algorithms/subsystems/pretrained models.*
Physical space technologies do not translate well across applications, let alone across hardware.
Many automation technologies need to start from TRL 0.

This also presents an exceptional opportunity for budding researchers.

Leveraging 'black-box' methods (data-driven methods, AI/ML modules) for highly uncertain plants & environments (e.g., self-driving) seems reasonable for black-box plants. Increasing introduction of ML methods into control systems space must not be seen as a perversion of a more analytical field. Instead, as an opportunity of skipping TRLs 0 through 3 to develop/prototype newer control schemes in our increasingly fuzzy operating environments.



[^1]: https://www.reuters.com/technology/space/spacex-launches-fifth-starship-test-eyes-novel-booster-catch-2024-10-13/
[^2]: https://www.sciencedirect.com/science/article/pii/S2405896324007316
[^3]: https://engineeringmedia.com/comics/1
[^4]: https://www.sciencedirect.com/science/article/pii/S0736585320301842
[^5]: https://www.nature.com/articles/s41467-022-33128-9
