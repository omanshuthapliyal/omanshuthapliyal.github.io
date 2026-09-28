---
title: "But why is Compactness important?"
date: 2019-08-15T01:34:25+05:30
tags: ["maths", "real analysis", "compactness"]
---

In my [last post](/blog/compactness) I touched upon the intuition behind topological compactness. We as engineers often hear about the word 'compact' as a soft gatekeeping tool from doing serious mathematics. In this post we see why the understanding is very important for doing any mathematics, *especially* as engineers.

Recall the open cover definition of a compact set as the existence of a finite open subcover for any given open cover of the set. Note that the key words here are that the subcover is going to be finite, no matter which infinite cover we begin with. Let us keep that in mind. Now we often hear about compactness being a more subtle form of finiteness, or compactness abstracting the idea of being finite, or the two being related. The open cover definition lets us understand that slightly better. Open sets, being the building blocks of topology, give us a way to interact with *a specific class of sets in a finite manner* [^1]. It is this class of sets that we call compact.

Now when ever dealing with sets in engineering problems, they are almost always accompanied with some function operating on them.
If the problem at hand deals with the properties of the set itself (think of the [reachable set](http://planning.cs.uiuc.edu/node731.html) problem in controls), and the set is compact, it comes with some other properties for free.
For example, in Euclidean spaces, if a set is compact, it is guaranteed to be closed and bound, and have limit points in itself [^2] by Bolzano-Weierstrass.
Else, if the problem deals with the functions operating on those sets (think of literally any function value maximization problem), compactness is an even more paramount property. 
Terry Tao's post explain why this is the case[^3] and that for finite sets, the following will always hold:
* *all* functions are bounded
* *all* functions attain a maximum
* *all* sequences have constant subsequences

It is not hard to see how none of these need to hold for infinite sets.[^3]
However, if the sets in question are compact, we have:
* *all continuous* functions are bounded
* *all continuous* functions attain a maximum
* *all* sequences have convergent subsequences
In addition, we get a bunch of other properties for continuous functions on compact sets, for free!


Compactness allows us to swap limits, interchange integrals with limits, blatantly assume infima are attained, and do all sorts of 'engineering hocus pocus', but with the surity, that none of it breaks down mathematically!
One of the most useful properties of compactness, which almost all engineering problems utilize, is the existence of a maximum of a continuous function on a compact set. 
It doesn't take a lot of insight to see how optimization problems make up a bit chunk of engineering problems.
Compactness is our best friend, in order to speak anything mathematically meaningful about our problems.

I would highly recommend reading Terry Tao's very short and very accessible note on compactness [^3], and a pedagogical note on compactness [^4].

[^1]: https://blogs.scientificamerican.com/roots-of-unity/what-does-compactness-really-mean/
[^2]: https://www.math.upenn.edu/~kazdan/508F14/Notes/compactness.pdf
[^3]: https://www.math.ucla.edu/~tao/preprints/compactness.pdf
[^4]: https://arxiv.org/pdf/1006.4131.pdf
 
