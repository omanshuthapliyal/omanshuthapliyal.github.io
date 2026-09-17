---
title: "So does your Car fail? (A Small Harness for Mathematical Exploration) - Part 3"
date: 2026-09-16T12:02:49-04:00
draft: false
tags: [maths, ml, research]
# links:
#     website: "https://omanshuthapliyal.github.io/"
#     alias : "blog/hrt-conjecture-part-3/"

---

In the [(last couple)](https://omanshuthapliyal.github.io/blog/hrt-conjecture/) [(of posts)](https://omanshuthapliyal.github.io/blog/hrt-conjecture-part-2/) I explained what the recently (dis-)proven HRT conjecture states, and what it implies.
We looked at how a computer-assisted argument can turn a difficult mathematical question into a finite collection of things that can be checked. Here, we try the more mundane inverse problem: how do we set up a small AI harness such that an LLM can suggest where to look, while the things that matter are still checked deterministically?
Here's a speedy recap. The original HRT conjecture asked whether this could ever happen.[^2] For a function $$g$$, define the time-frequency shift
$$
\pi(a,b)g(x) = e^{2\pi i b x}g(x-a).
$$
Given finitely many distinct points
$$
\Lambda = \{(a_k,b_k)\}_{k=1}^{N} \subset \mathbb{R}^{2},
$$
HRT asked whether the collection
$$\{\pi(a_k,b_k)g\}_{k=1}^{N}$$
is always linearly independent whenever $$g\neq 0$$.
Equivalently, can we find nonzero coefficients $$c_k$$ such that
$$
\sum_{k=1}^{N} c_k \pi(a_k,b_k)g = 0?
$$

The recent four-point construction does this with a carefully constructed complex-valued Schwartz window, an exact reduction to a dynamical system on a torus, and validated numerical inequalities.[^1] The numerical part is not a plot or a floating-point singular-value calculation. It uses outward-rounded ball arithmetic together with derivative bounds over a finite cover, so that the computation enters the proof as a validated certificate.[^1]

It is relatively easy to sample a few shifted functions on a grid, form a matrix, and inspect its singular values. It is much harder to know what such a computation has actually established. A small singular value might indicate interesting geometry. It might also be caused by a coarse grid, a truncated domain, a poorly conditioned discretization, or a window that has little to do with the actual construction.
*This post is about a small harness for keeping those possibilities separate.*

The complete code can be found here.[^3] The aim is not to engage in autonomous theorem proving (perhaps for a different day), but to make a simple rule explicit:

**_A model may suggest where to look. Deterministic code decides what was observed._**

#### A finite-dimensional proxy

Let us start with the most naive numerical experiment. We take a Gaussian window
$$
g_\sigma(x) = e^{-(x/\sigma)^2},
$$
sample it over a finite domain, and construct one column for every time-frequency shift. For points
$$
(a_k,b_k),
$$
the resulting matrix is a discretized version of
$$
\pi(a_k,b_k)g_\sigma(x).
$$
The smallest singular value gives a rough measure of how close the sampled columns are to linear dependence.

```python
def sampled_gabor_matrix(points, n, domain, sigma):
    x = np.linspace(-domain, domain, n)
    window = gaussian(x, sigma=sigma)

    columns = [
        tf_shift(window, x, translation=a, modulation=b)
        for a, b in points
    ]

    return np.column_stack(columns)


def svd_diagnostic(points, n, domain, sigma):
    matrix = sampled_gabor_matrix(points, n, domain, sigma)
    singular_values = np.linalg.svd(matrix, compute_uv=False)

    return {
        "grid_size": n,
        "sigma_max": float(singular_values),
        "sigma_min": float(singular_values[-1]),
        "relative_residual": float(
            singular_values[-1] / max(singular_values, 1e-12)
        ),
    }
```

This is already a useful exploratory tool. If a configuration has a comparatively small value of
$$
\sigma_{\min},
$$
across multiple grid sizes, then it may be worth looking at further.

But it is important to be precise about the output of this computation. We have established something about a sampled matrix, not about a collection of functions in \(L^2(\mathbb{R})\).

```python
HRT_CLAIM_BOUNDARY = (
    "Finite-grid singular-value diagnostics are numerical evidence only; "
    "they do not prove or disprove the continuous HRT conjecture."
)
```

The claim boundary is not a disclaimer attached after the experiment. It determines how the rest of the code is written.

#### Candidate generation

There are many ways to generate four-point configurations. We could choose them by hand, sample them randomly, or optimize a low-dimensional parameterization.

An LLM gives us another source of proposals. It can suggest configurations based on descriptions of known geometric regimes, previous failed candidates, or simple patterns such as rectangles and perturbations of lattice points.

The useful part is not the natural-language rationale. The useful part is a candidate represented in a form that ordinary code can inspect.

```python
class TFPoint(BaseModel):
    translation: float
    modulation: float

class HRTProposal(BaseModel):
    points: list[TFPoint] = Field(min_length=4, max_length=4)
    sigma: float
    rationale: str
    requested_checks: list[str] = Field(default_factory=list)
```

This object is deliberately boring.

There are exactly four points. There is one scale parameter. There is a rationale that a human can inspect later. And there is a place to record which follow-up checks the proposer thinks may be useful.
There is no field for `proof`, `confidence`, or `counterexample_found`.
Before evaluating the proxy, the harness checks that the proposal is admissible.

```python
def check_hrt_proposal(proposal, config):
    points = points_from_proposal(proposal)

    if len(points) != config.required_points:
        return {
            "status": "rejected",
            "result": {"reason": "expected exactly four points"},
            "claim_boundary": HRT_CLAIM_BOUNDARY,
        }

    if len(set(points)) != len(points):
        return {
            "status": "rejected",
            "result": {"reason": "points must be distinct"},
            "claim_boundary": HRT_CLAIM_BOUNDARY,
        }

    if not config.sigma_min <= proposal.sigma <= config.sigma_max:
        return {
            "status": "rejected",
            "result": {"reason": "sigma outside configured range"},
            "claim_boundary": HRT_CLAIM_BOUNDARY,
        }

    return {
        "status": "checked",
        "result": refine_hrt_candidate(points, proposal.sigma, config),
        "claim_boundary": HRT_CLAIM_BOUNDARY,
    }
```

This separation is small, but useful. The model does not get to decide whether its points are distinct. It does not get to decide whether a parameter is in range. It does not get to report a singular value.
It proposes a candidate, and the numerical backend evaluates it.

#### Refinement is part of the experiment

A single finite grid is not particularly informative. We therefore repeat the calculation over a sequence of resolutions.

```python
def refine_hrt_candidate(points, sigma, config):
    return [
        svd_diagnostic(
            points,
            n=grid_size,
            domain=config.domain,
            sigma=sigma,
        )
        for grid_size in config.grids
    ]
```

The resulting curve is more useful than one number. We can ask whether the smallest singular value changes substantially as the grid is refined.
This is still not validated numerics. 
In the HRT construction, numerical statements are converted into globally valid inequalities using interval methods and derivative estimates.[^1] Here, grid refinement only tells us whether one particular floating-point proxy behaves consistently under one particular family of discretizations.

That is weaker evidence, but it is still useful evidence, provided we do not pretend otherwise.

#### One bounded critic

There is a natural next question after seeing a refinement curve: what should we perturb?
Maybe the apparent behavior disappears under a larger domain. Maybe it is highly sensitive to the Gaussian width. Maybe moving each point by a small amount changes the diagnostic entirely.
A critic can be useful here, but only if its role is constrained. Otherwise, we have just added a second source of unverified commentary.

```python
HRT_ALLOWED_CHECKS = {
    "wider_grid_refinement",
    "perturb_points_check",
    "perturb_sigma_check",
    "larger_domain_check",
}


def allowed_critic_action(requested_check):
    return requested_check in HRT_ALLOWED_CHECKS
```

The critic is shown an evidence packet containing the checked proposal, its refinement data, and the set of available checks. It may select one additional experiment.
The harness executes that experiment.

```python
def execute_hrt_check(review, proposal, config):
    if not allowed_critic_action(review.requested_check):
        return {
            "status": "invalid_check",
            "reason": "critic requested a disallowed check",
            "claim_boundary": HRT_CLAIM_BOUNDARY,
        }

    if review.requested_check == "wider_grid_refinement":
        return wider_grid_refinement(proposal, config)

    if review.requested_check == "perturb_points_check":
        return perturb_points_check(proposal, config)

    if review.requested_check == "perturb_sigma_check":
        return perturb_sigma_check(proposal, config)

    return larger_domain_check(proposal, config)
```

The point of the allowlist is not that these four checks are privileged. They are simply explicit.

A future experiment might replace them with symmetry tests, exact arithmetic checks, interval bounds, or comparisons against a known construction. The important part is that the menu is specified before the critic sees a candidate.

#### What happens after a promising signal?

Suppose a candidate has a small sampled singular value, and that value remains small as we increase the sampling resolution. What should the harness return?
Not a counterexample.
At most, it should return a reason to leave the numerical search loop and begin a different kind of work.

```python
def hrt_promotion_decision(
    refinement,
    sigma_threshold,
    variation_threshold,
):
    if not refinement:
        return "continue"

    sigma_curve = [row["sigma_min"] for row in refinement]

    last_sigma = sigma_curve[-1]
    baseline = max(abs(sigma_curve), 1e-12)

    variation_ratio = max(
        abs(value - last_sigma)
        for value in sigma_curve
    ) / baseline

    if (
        last_sigma < sigma_threshold
        and variation_ratio < variation_threshold
    ):
        return "promote_to_analytic_proof_obligation"

    return "continue"
```

The thresholds here are not theorems. They are experimental choices. They should therefore be included in the run configuration and recorded with the output.
The phrase

```text
promote_to_analytic_proof_obligation
```
is intentionally awkward. It is supposed to be.

A stable numerical signal creates work. It does not close a mathematical question.

For HRT, that work could mean trying to derive an exact functional relation, identifying a suitable transform-domain representation, proving a uniform bound, or finding a reason that the apparent dependence must disappear in the continuum limit. The specific proof strategy depends on the problem. The harness only records why the candidate was interesting enough to deserve one.

#### Artifacts instead of conversation history
The last part is mundane but important. Each proposal and check is written to an append-only artifact log.

```python
artifact_store.append_artifact(
    record_id=record_id,
    kind="hrt_proposal",
    candidate=proposal_payload,
    result=proposal_record["result"],
    status=proposal_record["status"],
    claim_boundary=proposal_record["claim_boundary"],
    model_name=config.model.model_name,
    configuration=config_payload(config, "hrt"),
    run_id=run_id,
)
```

The log stores the proposed configuration, the numerical output, the configuration used to generate it, the claim boundary, and the final status.
This is more useful than retaining a long agent transcript. A transcript explains what the model said. An artifact record explains what was actually run.
The notebook also supports deterministic fixtures. This means that the entire harness can be inspected without an API key: the explorer and critic return fixed structured objects, while the verifier and policy run normally. A live model can replace the fixtures later without changing the meaning of the deterministic checks.[^3]

#### _Afterword: A note on orchestration_

The plain Python version is the main implementation because the policy is easy to read directly.
There is also a LangChain/LangGraph version of the same example.[^4] It represents the loop as explicit state transitions:

```text
propose -> verify -> critique -> execute_check -> update
```

This is useful when the state becomes large or the graph itself needs to be inspected. It does not alter the numerical backend, the claim boundary, or the evidence labels.

The recent HRT proof is a reminder that there is a large difference between numerical exploration and a computer-assisted proof.[^1] A small harness does not bridge that difference. 
It does something narrower: _it gives exploratory models a place to be useful without letting them narrate a result into existence._



[^1]: Vignon Oussa, “An Intrinsically Subcritical Four-Point Counterexample to the HRT Conjecture,” *arXiv preprint* arXiv:2608.07604 (2026). https://arxiv.org/abs/2608.07604

[^2]: Christopher Heil, Jayakumar Ramanathan, and Pankaj Topiwala, “Linear Independence of Time-Frequency Translates,” *Proceedings of the American Mathematical Society* 124, no. 9 (1996): 2787–2795. https://heil.math.gatech.edu/papers/shifts.pdf

[^3]: https://github.com/omanshuthapliyal/blog-posts_accompanying-code/blob/main/hrt_agentHarness_demo.ipynb

[^4]: https://github.com/omanshuthapliyal/blog-posts_accompanying-code/blob/main/hrt_agentHarness_demo%5BLangchain%5D.ipynb