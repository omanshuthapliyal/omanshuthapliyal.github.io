---
title: "ML SoTA Resources"
date: 2019-08-18T22:36:00+05:30
tags: ["resource", "ml"]
---

The internet is filled with machine learning resources, and one of the most annoying things about them is the sheer volume. 
There are many attempts at making compilations of papers, code, and current status quo in the vastly active, and fast paced field.
This post is to serve as a collection of my own where I will only post **state of the art** in machine learning.

Most of these links are updated frequently and maintained by the community, and I have collected these *only* for reference. I am not trying to [create a new standard](https://xkcd.com/927/), but I will try to update the list if and when I come around doing that.


1. [Papers with code](https://paperswithcode.com/sota) contains state-of-the-art in machine learning and related topics like NLP, Graphs, and CV. The best part is the reproducibility, and ease of comparing results because of the availability of code.
The data and code is scraped from other sources (some of which are below). Anyone can contribute to the project.

2. [Are we there yet?](http://rodrigob.github.io/are_we_there_yet/build/) seems deprecated, but contains progress made in important classification, estimation, segmentation problems, among others.

3. [Electronic Frontier Foundation (EFF) AI metrics](https://www.eff.org/ai/metrics) contains one of the best maintained sources for state-of-the-art in ML topics run by a big team of researchers. 
Their Jypyter notebook can be found [here](https://github.com/AI-metrics/AI-metrics). They accept donations, and are open to volunteers.

4. [Reddit State-of-the-art](https://github.com/RedditSota/state-of-the-art-result-for-machine-learning-problems) is pretty much how I found most of these resources. The repository claims to have SoTA results for all ML problems, sometimes with code, sometimes not.
They are open to volunteers.

5. [RobustML](https://www.robust-ml.org/defenses/) is very useful for studying SoTA in adversarial attacks and defenses.
The website is open source, very updated, and maintained through [here](https://github.com/robust-ml/robust-ml.github.io).

6. [NLP SoTA](https://nlpprogress.com) is a comprehensive repository for NLP problems SoTA, maintained solely by Sebastian Ruder.
Contributions can be made [here](https://github.com/sebastianruder/NLP-progress/blob/master/README.md).

7. [CleverHans](https://github.com/tensorflow/cleverhans) provides attack methods and related benchmarking (not SoTA), similar to,

8. [robust.vision](https://robust.vision/benchmark/leaderboard/), which  "maintains a comparison between existing defenses by evaluating each one of them against all currently known attacks."

9. [GLUE benchmark](https://gluebenchmark.com/leaderboard/) collects resources for benchmarking and analyzing NLP problems and systems that accepts submissions to its leaderboard.

10. [SuperGLUE](https://super.gluebenchmark.com/leaderboard/) benchmarks NLP problems to more difficult language understanding tasks than its predecessor, GLUE

*Please help the original contributers, or volunteer in maintaining these repositories if they helped you.*
