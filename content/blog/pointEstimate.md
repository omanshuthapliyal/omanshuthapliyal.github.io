---
title: "Point Estimation Problem"
date: 2019-07-24T01:34:25+05:30
tags: ["maths", "statistics"]
---

It might seem out of place that in the world of big data, finding a singular parameter's estimate could be interesting. Quite the contrary -- **point estimation problems** are one of the most ubiquitous parametric estimation problems that arise whether you are doing your Stat Inference 101 assignments, or dealing with $$10^8$$ rows in a parquet file. And so, I thought of making this post to look further into the point estimation problems, and when might one want to use which method.

#### Point estimation problem

A generic point estimation problem goes like this:
Consider a random variable $$x\sim f(x;\theta)$$ with the parameter $$\theta\in\Omega$$. Here $$f(x;\theta)$$ corresponds to a *family of distributions* rather than a single probability distribution. We are interested in finding a *point* estimate to the parameter $$\theta$$. In order to do that, we draw a random sample with $$n$$ realizations of the random variable $$x$$ as $$\tilde{X}=\{x_1=X_1,x_2=X_2,\cdots, x_n=X_n\}$$. In shorthand, this realization from the $$n$$ experiments of the given family of distribution is also written as simply $$\{X_1,X_2,\cdots,X_n\}$$.

#### Solution strategies

Our point estimate, in order to capture the information in the realization $$\tilde{X}$$, has to depend on another statistic $$Y=u(\tilde{X})$$, such that our point estimate is:
$$\hat{\theta}=u(\tilde{X})$$
This is a key point and is intuitive to the problem of point estimation.

##### Maximum likelihood

One of the ways to go about finding $$\hat{\theta}$$ is to find *what value of parameter* $$\theta$$ *makes the current realization* $$\tilde{X}$$ *most likely*. In order to do this, observe that the joint-distribution of the observed data is given by
$$f(\theta;x_1=X_1,x_2=X_2,\cdots,x_n=X_n)=\prod_{i=1}^{n} f(x_i;\theta):=L(\theta)$$
This is the likelihood function. An intuitive estimate to the parameter would now be the value that makes the data points observed *most likely* ; simply given by
$$\hat{\theta}_{\mathrm{MLE}}=\underset{\theta}{\mathrm{argmax\,}} L(\theta) = \mathrm{arg}\left\{\frac{dL}{d\theta}=0\right\}$$
Notice that this requires the likelihood function to be differentiable in order to be maximized; and often a log-likelihood is maximized instead of the likelihood function instead.
The Maximum likelihood estimator is [consistent](https://en.wikipedia.org/wiki/Consistent_estimator), and often [unbiased] (https://en.wikipedia.org/wiki/Bias_of_an_estimator). Then the obvious question is:

###### Why do MoM? (or some other estimator)

For this, consider a family of Gamma distribution with parameters $$\theta_1=\alpha, \theta_2=\beta$$ such that $$\theta_1,\theta_2>0$$, be given by:
$$f(x;\theta_1,\theta_2)=\frac{1}{\Gamma(\theta_1)\theta_2^{\theta_1}}x^{\theta_1-1}e^{-\frac{x}{\theta_2}}$$
For a particular sample of data $$\tilde{X}$$ from this family, we get the likelihood function as

$$L(\theta_1,\theta_2;x_1,\cdots,x_n)=\left[\frac{1}{\Gamma(\theta_1)\theta_2^{\theta_1}}\right]^n(x_1 x_2\cdots x_n)^{\theta_1-1}\mathrm{exp}(-\sum_{i=1}^{n} x_i/\theta_2)$$

Not so easy to find the MLE now, is it!
*The gamma function in the likelihood makes it hard to find the MLE in a closed form in this example, and in general.*

##### MoM

MoM is another intuitive way to proceed in such problems where MLE either does not exist, or is hard to calculate.
The underlying principle of an MLE, which is very easy to follow, is:
Equate $$\frac{1}{n}\sum_{i=1}^{n}X_i^k$$ to the expectation $$\mathbb{E}[x^k]$$ for $$k = 1,2,\cdots$$ until you have enough equations to solve for parameters $$\theta$$.
Pretty easy, right!
Then why do we need other estimators?

##### Why do MLE?

Suppose, in the very same example of the gamma-family, you need to find the parameters $$\theta_1$$ and let $$\theta_2=\beta$$ be given, for simplicity.
The likelihood of the observed sample is:

$$L(\theta_1;x_1,\cdots,x_n)=\left[\frac{1}{\Gamma(\theta_1)\beta^{\theta_1}}\right]^n(x_1 x_2\cdots x_n)^{\theta_1-1}\mathrm{exp}(-\sum_{i=1}^{n} x_i/\beta)$$

$$= \left(\left[\frac{1}{\Gamma(\theta_1)\beta^{\theta_1}}\right]^n \mathrm{exp}(-\sum_{i=1}^{n} x_i/\beta)\right) \cdot (\mathrm{exp}\{(\theta_1-1)\sum^n_1 \mathrm{log}(x_i)\})$$

Let me digress for a moment and recall the reader’s attention to the concept of a [sufficient statistic](https://en.wikipedia.org/wiki/Sufficient_statistic). In a broad manner, the sufficient statistic encompasses *all the information* that could possibly be conveyed about the parameter to be estimated $$\theta\in\Omega$$ by the observed data $$\tilde{X}$$. Therefore, it is always great to use this information in our estimate $$\hat{\theta}$$.
By using Factorization theorem on the likelihood expression above, the sufficient statistic for $\theta_1$ is given by some $$Y=u(\tilde{X})=\sum^n_1\mathrm{log}\,x_i$$.
Note that if you use MoM to estimate the parameters here, the estimate $$\hat{\theta}$$ would *not be a function of *$$Y$$; it would always be a function of the sample moments $$\frac{1}{n}\sum_{i=1}^{n}X_i^k$$ (sample mean, sample variance, etc.).
We can conclusively say from this, that

**MoM estimate need not be a function of the sufficient statistic; an MLE, if it exists, is ALWAYS a function of the sufficient statistic**.
This is where MLE shines, and this is why it is used; if it is useful to a problem!
However, MoM estimates are good starting point for numerically complex point estimation problems and can iteratively lead to a good estimate and are consistent estimates.

##### Why MAP?

Coming back to the definition of the point estimation problem, suppose in addition to $$\theta\in\Omega$$, we have some more knowledge about where it could be in $$\Omega$$; this is usually in the form of some *prior knowledge about* $$\theta\sim g(\theta|\theta\in\Omega)$$; hence called the prior.
The MAP estimate is a way to include this knowledge in our estimation as
$$\hat{\theta}_{\mathrm{MAP}}=\underset{\theta}{\mathrm{argmax\,}} f(x;\theta)g(\theta)$$
This is just using the fact that *using more information to find* $$\hat{\theta}$$ *wouldn’t hurt!*

#### So ...
Now that we know about what is going on, I would answer the questions asked here.
What is the difference between MAP, MLE, MoM?
I have already answered in terms of the differences. So I would rather answer “When to use MoM, MLE or MAP?” based on my observations:
1. Do you have a prior knowledge about $\theta$?
2. If yes, is your prior uniform?
   * No  **MAP estimator**
   * Yes; Does a closed form MLE exist?
Yes $$\rightarrow$$ **MLE estimator** 
No $$\rightarrow$$ **MoM estimator**
3. If No, go to 2. (ii) ; use MLE/MoM
This is only to help choose among the given 3 methods.
Are there instances where the MOM and MLE are exactly the same?
Yes.
If your MoM estimate is a function of the sufficient statistic, the two estimates *could* be the same.
If MoM estimate is *not* a function of the sufficient statistic, the two are *definitely* different estimates.
Interestingly enough, as we observed, MoM estimates need not be a function of the sufficient statistic and the estimate need not even lie in the region $$\Omega$$!
Further, the MAP estimate would coincide with the MLE estimate iff $$g(\theta)=\mathrm{Uniform}(\Omega)$$.

Most of the stuff comes from [Introduction to Mathematical Statistics, 7th Edition](https://www.pearsonhighered.com/program/Hogg-Introduction-to-Mathematical-Statistics-7th-Edition/PGM49624.html), which is a great introductory (and almost standard) text on statistics.
