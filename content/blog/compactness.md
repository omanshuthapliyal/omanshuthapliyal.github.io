---
title: "Compactness"
date: 2019-08-10T15:44:20+05:30
tags: ["maths", "real analysis", "compactness"]
---

This is a non-mathematical note on what I understand about compactness and what it means for a set or a space to be compact. 
The open cover definition is one that can be found in any textbook, but what does it *mean* for a set to be *compact?* Why are such sets called compact? And how do compact sets differ from those which are not?

I think the terminology here is very carefully chosen. For once, mathematicians came up with a term that paints a succinct, abstract picture. To understand compactness,let us look at two other  properties: *limit points*, and *closed sets*.

Consider a metric space $$X$$ and some arbitrary point in $$p\in X$$. Using the usual shorthand 
$$\mathcal{N}_r(p)$$ for an $$r$$-neighbourhood around $$p$$. Now if there exists some neighbourhood with $$r>0$$ such that $$\mathcal{N}_r(p)\subset E\subset X$$, $$p$$ is an interior point of $$E$$. This is just a fancy way of saying that $$p$$ lies inside $$E$$, and nout just on its 'boundary'. There could be two more cases though. If *every* 'punched neighbourhood' of $$p$$ (i.e., $$\mathcal{N}_r(p)\setminus \{p\}$$) contains some points, it is a *limit point* of $$E$$. 
So to speak, the decreasing neighbourhoods around $$p$$ can be 'approximated' by the point limit point $$p$$ itself.
The sequential [definition of limit points](https://en.wikipedia.org/wiki/Limit_point) best helps understand this.
Otherwise, if not a limit point, $$p$$ is an isolated point.
Clearly, interior points are limit points.

Now I could have a set with isolated points like a ball of radius $$1$$ around $$(0,0)$$, and the isolated points $$\{(2,0),(3,0),\cdots\}$$. It looks, well, like a ball and some discrete points in 2D!
This doesn't look very 'compact' in the physical sense. 
We can't 'mould', or 'play around' the set, pick it up and throw it around.
It doesn't 'feel' compact in 2D, right?!
Similarly, think of the open set which is all the points in the interior of the ball of radius $$1$$ around $$(0,0)$$.
We can't mould this set either as it has no 'surfaces'.
It is not immediately visible how this seemingly benign set could have hidden infinities. 
It is better to think of this set of interior points of the ball as the ball itself, without its skin.
However, the skin is not a tangible object that we removed; it has a zero thickness. So no matter how close we approach the skin from the interior, we always find infinite points around us.
In this manner, this set is not literally compact because it seems, feels, and touches more like a ball of gas.
Compactness (at least in Euclidean spaces), for a lack of a better word, makes sure the sets we deal with are '**compact**'!
It allows us to deal with sets that we can mould. 
If a set is compact, it would not be one with isolated points like the first, or a ball of gas like the second.

This very crude understanding works well in Euclidean spaces, and I like to think of compactness as a property before we dive into the open cover definition of compactness.

If we think about it, we tried to understand compactness by seeing what doesn't feel compact.
So, in some sense, it was easier to rule out stuff (in Euclidean spaces) that is *not* compact by touching it, trying to mould it.
This goes in line with the difficulty in proving compactness and the relative ease in proving non-compactness if we go by the standard open cover definition of compactness!

This is a crude and vulgar understanding of why compactness as a mathematical property was named so (probably by Fréchet). 
The [limit point definition of compactness](https://en.wikipedia.org/wiki/Limit_point_compact) was given by Fréchet, whose original French paper on the [history of compactness](https://www.sciencedirect.com/science/article/pii/0315086080900063) is definitely worth a read.
 
