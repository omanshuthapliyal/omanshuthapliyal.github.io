---
title: "The Industry-Academia split in Control Systems"
date: 2019-09-16T12:32:31-04:00
tags: ["controls"]
---

I often wonder why the "cutting edge" research that we read about in the foremost scientific journals & conferences in Control Systems are never applied in the industry.
Because whenever we read/write papers, Section-I always tries to ground itself to industry and/or practical applications. However, it's pretty well known that a majority of the controllers used in the industry are still tuned PIDs.
Even though sub-fields of modern control -- adaptive, and robust control are very mature and pretty old in their own rights, the real world's inertia against using modern control techniques bears substantial weight.

This not very old paper[^1] from IEEE control systems magazine presents a great, unsurprising account of researchers in controls community on which fields are most prevalent in the industry based on a survey conducted in 2014 IFAC.
Based on the survey (addressed by 23 committee members of the IFAC committee, most affiliated with the industry), control technologies were ranked based on their industry impact ratings as: *PID* > *MPC* > *System Identification* > *Process Data Analytics* > *Soft Sensing* > 50% ratings, while the list was wrapped up by *Nonlinear control* > *Adaptive control* > *Robust control* > *Hybrid systems*.
While researchers would agree that academia interests probably go the other wy around! From my own experience, most of my colleagues work in hybrid systems > adaptive control > robust control, etc. which is surprisingly the opposite of industry driven factors.

The survey also attempted to find the causes for the said split in industry impact, and academia interests.
I would very highly recommend reading the very short paper[^1] itself, but of the causes outlined, the following resounded with me the most.
Most responders agreed that:
* Controls students are unaware of industry driving problems
* A lot of emphasis is placed on advanced mathematics, and not on plant modeling or industry applications

while most disagreed with the following statement:

Advanced controls has little relevance to industry problems

So, advanced problems that we work on definitely have industry relevance, but are still disjoint from industry acceptance as they, perhaps, are not represented well in papers and articles in a practically relevant light.
While this is no epiphany, and stands true for most "high-technology" fields, it still shows an interesting view of the split between academia and the industry in control systems, where they both wish to work together, but somehow find their directions still misaligned.

Exploring the causes of this split from an academia perspective would be a good follow up to [the work][1].

[^1]: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7823045
