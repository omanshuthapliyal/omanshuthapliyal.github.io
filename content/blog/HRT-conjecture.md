---
title: "So does your Car fail? (An \"Uninteresting\" Implication of HRT Conjecture) - Part 1"
date: 2026-08-10T01:02:49-04:00
draft: false
tags: [maths, abstract]
# links:
#     website: "https://omanshuthapliyal.github.io/"
#     alias : "blog/hrt-conjecture/"

---

The mathematics community has recently been effervescing with plenty of AI usage stories (notably Terence Tao, nonetheless) [^1]. In the latest such development, a long-standing conjecture was disproved by a counterexample found using AI. 
The Heil-Ramanathan-Topiwala (HRT) conjecture itself turns 30 years old next month, and while numerous interesting questions come up in my mind after its AI-assisted counterexample, for now I will contain myself to: 

_1) What is the HRT conjecture and What does it mean? And,_

_2) What does HRT being disproven by a counterexample mean materially?_

To this end, let's take a brief walk followed by a brisk mathematical jog.
Based on your appetite for such a trip, you can absolutely cut short before the math begins and still walk away with a (sufficiently) decent understanding of the conjecture.

The HRT conjecture states that "any finite collection of distinct time-frequency shifts of a nonzero square-integrable function $$L^2(\mathbb{R})$$ is always linearly independent" [^2].
In terms of a temporal signal $$f(t)$$, a _temporal shift_ $$f(t-x)$$ is a delaying by $$x$$, and its _frequency-shift_ is a "change in pitch" $$e^{2\pi i(\omega,t)}f(t)$$ or modulation of the signal by $$\omega$$.
Intuitively, delaying or modulating the signal's waveform should produce a fundamentally distinct waveform.
The HRT conjecture claims that **no matter what shape your original** (finite, non-zero energy) **wave has, and no matter how you choose a finite number of distinct time-frequency shifts** (delay + modulate operations), **the resulting collection of waves will always be linearly independent** [^3].

We can make this more formal in the form of defining the delayed operator $$\circ$$ original signal as $$(T_xf)(t)=f(t-x)$$, and the modulated operator $$\circ$$ original signal as $$(M_\omega f)(t)=e^{2\pi i(\omega,t)}f(t)$$.
Using this, a combined "delay+modulate" operator can be written as $$(M_\omega T_xf)(t)=e^{2\pi i(\omega,t)}f(t-x)$$.
We can construct a finite set of $$n$$ distinct frequency-time phase space points $$A=\{\omega_i,x_i\}_{i=1}^n$$.
The set $$A$$ generates a finite collection of shifted (in time, or in frequency) signals as: $$\mathscr{F}(f,A)=\{M_{\omega_i}T_{x_i}f\}_{i=1}^n$$.
The HRT statement can now be written as: _for any non-zero energy measurable $$f$$ ($$\in L^2(\mathbb{R}\setminus \{0\})$$), and finite set $$A$$,  the set $$\mathscr{F}(f,A)$$ is linearly independent over complex numbers._ 
In other words, if one can find $$c_1,c_2,\cdots,c_n\in \mathbb{C}$$ such that $$\sum^{n}_{i=1}c_i M_{\omega_i}T_{x_i}f=0$$, then $$c_1=c_2=\cdots=c_N=0$$.

**Remark:** Existing works in HRT have Lattice configuration based proofs of the conjecture's statement.
In the 90's, mathematicians found that if the phase space points in the set $$A$$ all lie on a uniform lattice (that is, the points are not randomly scattered in the phase space, but restricted to some equidistant lattice $$\{\cdots,-2a,-1a,0,1a,2a,\cdots\}\times \{\cdots,-2b,-1b,0,1b,2b,\cdots\}$$), then the HRT conjecture holds!
The proof itself is beyond me as it utilizes abstract algebra .


This immediately looks very interesting already!
There are many implications for _if_ this does not always hold.

Having answered our first questions, we are armed to move to the next, and more interesting question of the two!
Let's look at a specific use case.

##### Scattermaps on Self-driving Vehicles

Suppose you are designing a self-driving system for an autonomous vehicle. 
It is equipped with, for simplicity, a radar that helps it echolocate itself with respect to its surroundings (it could be LiDAR, but then we have more rays, so probably higher dimensional waveforms in $$L^2(\mathbb{R}^d)$$).
It does so by transmitting a pulse wave $$f(t)$$ into the environment, and notes the scattermap (waveforms that bounce back).
Now the environment itself acts as a linear time-varying (LTV) system in this case, delaying and/or modulating the originally transmitted waveform $$f(t)$$.
This LTV system returns back a different signal:
$$y(t)=\sum^{n}_{i=1}c_i e^{2\pi i \omega_i t}f(t-x_i) + w(t)$$
where,
$$x_i$$ is the time delay (depending on the target's distance), $$\omega_i$$ is the Doppler shift (proportional to the target's velocity), $$w(t)$$ is the ambient measurement noise, and
$$c_i$$ represents the reflectivity / size of the target and _this is the system's parameter you need to identify._

Let's make it simple first and let $$\mathbf{x}=[c_1,\cdots,c_n]^T$$, contain the unknown reflection coefficients. 
Then, we can set up a 'vectorized' discrete-time state-space estimation framework (just like a Kalman Filter!) or an empirical observability framework to extract this model.
The vectorized observation equation at time step $$t$$ can be written as:
$$\mathbf{y}_t=\mathbf{H}_t\mathbf{x}_t+\mathbf{w}_t$$.

Now for us to be able to accurately find $$\mathbf{x}_t$$, the system above needs to be **observable**, which means, the columns of $$\mathbf{H}_t$$ need to be linearly independent!
If HRT conjecture holds, $$\mathbf{H}_t$$ linear independence is guaranteed and the vehicle can perfectly distinguish moving targets - be they small or large or slow or fast!

However, now that HRT conjecture is disproven using a counterexample, _there is a **mathematical blind spot** in the autonomous vehicle's, as some targets may not be discernible from others!_

In reality, engineers utilize multitudes of solutions such as sensing system redundancies. 
This isn't a pathological limitation of autonomous vehicles (it was merely an interesting problem to motivate this discussion) as such, but rather a mathematical limitation.

[^1]: https://www.reddit.com/r/math/comments/1vj9fm8/hrt_conjecture_disproven_by_ai/
[^2]: https://math.umd.edu/~rvbalan/TEACHING/RIT2023/RemarksOnHRT_DanielStrook.pdf
[^3]: https://terrytao.wordpress.com/2026/08/06/a-partial-digestion-of-the-hrt-counterexample/

> Written with [StackEdit](https://stackedit.io/).