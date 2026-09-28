---
title: "MLP Approximation"
date: 2019-09-12T10:27:01-04:00
tags: ["ml", "maths", "analysis"]
---

Almost always we hear about classification or machine learning problems, the go-to methods to solve the problem are neural networks, or multi-layered percetrons (MLP).
Now function approximation problems, which is what classification is, are very well defined in terms of consistency, accuracy, and other abilities of the approximator.
Why are MLPs then able to approximate functions well? Especially given the fact that most of the problems in coming up with candidate architectures, activation functions, etc. are 'design problems'.

Herein comes the [Universal Approximation Theorem](https://en.wikipedia.org/wiki/Universal_approximation_theorem), which says that [MLPs with a single hidden layer](/mlp-approximation/1-hiddenlayer.png) can approximate Borel measurable functions a finite set to arbitrary degrees of accuracy. That is, if you need an $$\epsilon$$ level of accuracy, there exists some finite number $$k$$ of units in the hidden layer that will be able to achieve the said accuracy.
This looks awfully similar to Stone-Weierstrass theorem!
And if we think of rectified lineaer unit (ReLU) activations {$$\sigma(z) = \max{\{0,z\}}$$}, it indeed is convincing.

Think of just a 1-d function $$f(x)$$ that we want to approximate on $$[a,b]$$. 
We do so by usinga single hidden layer activated by ReLUs. That is, $$y(x)=\sum^k_{j=1}\sigma(w_jx+\theta_j)+b_j$$. In order to convince ourselves that $$f(x)$$ can indeed be written as a finite sum of ReLUs given some degree of accuracy, we can look at an individual ReLU unit's output as $$\sigma(w_jx+\theta_j)$$. This would have an intercept at $$\theta_j$$. Without any loss, let $$\varphi_j$$'s be $$\theta_j$$'s sorted on the real line. This way we can split the sum [as shown](/mlp-approximation/relus.png).

Note that if we choose $$\varphi_1=a$$ and $$\varphi_k=b$$ for some $$k$$ that we would determine later, the sum of the activation functions is essentially of a piecewise linear on the interval $$[a,b]$$ where $$y(a)=f(a)$$ and $$y(b)=f(b)$$by designing the $$b_j$$'s appropriately.
That is, now we have $$k-$$segments of piecewise linear functions, for each of which, we still have appropriate flexibility to choose the slope and height from the x-axis by manipulating $$w_j$$'s and $$b_j$$'s.
The end result would be a [piecewise linear function with $$k-$$ segments on $$[a,b]$$](/mlp-approximation/approx.png). Recall that we can still manipulate individual segments to obtain an arbitrary level of accuracy, if we keep making $$k$$ large.
That's it.
This is a simple consequence of the Stone-Weierstrass theorem that we used to approximate a continuous function on $$[a,b]$$ to a fixed level of accuracy using a finite $$k$$ number of units in the single hidden layer.

In reality, proving the actual universal approximation theorem is much more involved, *and* is proven for more general activation functions, *and* for inputs and parameters in a higher dimension, *and* for a wider class of functions.

