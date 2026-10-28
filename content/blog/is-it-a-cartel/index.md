---
title: "When AI Agents Run the Shop - Part 1"
date: 2026-10-27T09:00:00-07:00
draft: false
tags: ["AI", "AI-Safety", "ai-control", "research"]
---

In April this year, a small café opened on Norrbackagatan in Stockholm with a rather unusual manager.
The baristas are human, but most of the decisions behind the counter are made by an AI agent called ***Mona***, which Andon Labs built on top of Google's Gemini.
Mona registered the business with the authorities, signed the electricity and broadband contracts, set up accounts with a wholesaler and a bakery, and hired its two baristas through LinkedIn, whom it now manages over Slack.
It has also made some memorable mistakes, which the café keeps on display on a shelf that includes 6,000 napkins and a large order of canned tomatoes that no item on the menu uses.[^1]

![Andon Café in Stockholm, run by the AI agent Mona](https://andonlabs.com/andon-cafe-og.webp)

*Figure 1. Andon Café in Stockholm, managed by the AI agent Mona. Image: [Andon Labs](https://andonlabs.com/cafe).*

The café is an experiment, and a fairly charming one, but it is not an isolated one.
A year earlier, Anthropic and Andon Labs let a Claude agent run a small shop inside Anthropic's office, where it decided what to stock and set its own prices; it sold some items below cost and handed out discount codes rather freely.[^2]
More recently, in Anthropic's Project Deal, 69 employees each gave a Claude agent a small budget and let it buy and sell their belongings in a marketplace where every buyer and seller was another agent. The people represented by the stronger model got noticeably better deals, and the people represented by the weaker one did not notice.[^3]
Outside of experiments, software that sets prices with no human in the loop has been part of real markets for some time, for example at petrol stations in Germany, where margins rose once competing stations had both adopted it.[^4]

So it seems reasonable to expect that, before long, the café down the street from Mona will be run by an agent too, and that the two agents will be setting their prices with each other in plain view, which raises the question of what happens to those prices.
Fish, Gonczarowski and Shorrer gave pairs of language-model agents the job of pricing competing products in a simulated market, and found that prices drifted well above the competitive level, even though neither agent was ever told to coordinate with the other.[^5]

#### Why should we care?

The most direct reason is that customers pay the difference.
If two agents settle on prices above what competition would give, the people buying coffee or paying rent pay more, and it is possible that nobody ever decided that they should.

A less direct reason is that our tools for dealing with this were built for people.
Competition law has traditionally looked for an agreement between firms, and courts have so far been reluctant to treat the independent use of the same pricing software as one.[^6]
With agents, there may be no agreement to find at all. Two businesses could each choose the same general-purpose model, ask it for nothing more than to run the shop well, and still end up with high prices.
When there is no agreement to point to, the only evidence left is how the agents behave, so it becomes important to know which behaviour should count as evidence.

There is a reason to care that goes beyond prices as well.
Pricing is perhaps the simplest setting in which AI agents interact with each other repeatedly, each pursuing its own goal, with nobody overseeing the interaction as a whole.
If we cannot tell whether two pricing agents are coordinating against their customers, we are unlikely to do much better for agents that negotiate contracts or bid against each other in auctions.
In that sense, collusion between agents is a multi-agent safety problem, and pricing is a good place to learn how to detect it.

#### What exactly is the problem?

Return to the two cafés, and suppose both have charged well above their costs for months without either one ever undercutting the other. Two quite different stories fit this picture.

In the first story, each café knows that if it lowers its price, the other will answer with a cut of its own and both will lose money, so neither of them tries.
The high price is *enforced*: a deviation is noticed and punished, and that pattern of reward and punishment is what economists and competition lawyers mean by collusion.[^7] Simple learning algorithms are known to discover it on their own.[^8]

In the second story, neither café has ever seriously tried a lower price.
The price was set early on, it seems to work well enough, and it stays where it is because nothing ever moves it. Calvano and co-authors call a high price of this kind *spurious*,[^9] and I will describe an agent in this state as *anchored*, since it holds on to its own price and pays little attention to its rival.

The problem this series is about is how to tell these two stories apart when all we can observe is the agents' behaviour.
It matters which one we are in, because the right response differs between them.
An enforced price is a cartel, and it calls for competition enforcement.
An anchored price may need nothing more than a nudge, for instance making one agent try a lower price once, so that it discovers the lower price pays. A real cartel, however, would punish exactly that nudge.
So a wrong diagnosis is costly either way: it spends enforcement effort on agents that would have competed had anyone pushed them, or it sets off the retaliation that holds a real cartel together.

#### Why is this hard?

The first difficulty is that watching the market does not help.
Once prices settle, an enforced price and an anchored price produce the same flat line, and nothing in that line reveals what is holding it in place, however long we observe it.

The obvious experiment is to force one firm to cut its price and see whether the other follows. This has long been the standard test,[^8] and recent work has applied it to language models and found that some of them do follow a cut.[^10]
The difficulty is that a rival can follow a cut for reasons that have nothing to do with punishment. It may simply copy whatever price it sees, or it may lower its own price out of plain self-interest because the cut took some of its customers, and part of what looks like punishment can turn out to be the latter.[^11]

Language-model agents add a difficulty of their own.
They write plans and notes as they go, and it is tempting to read these for signs of a deliberate scheme, but what an agent writes about its reasoning and what it actually does can come apart.[^12]

What the problem seems to call for is something closer to system identification: we push on the market in carefully chosen ways and measure how it responds, for example by forcing a price raise as well as a cut, or by hiding one agent's price from the other, and then ask whether a cut ends up costing the firm that made it. Agents make this unusually practical, since a game between them can be saved, rewound and replayed with exactly one thing changed. The [next post](https://omanshuthapliyal.github.io/blog/is-it-a-cartel-part-2/) describes such an audit and what it found for four language models.

*A high price tells us where a market sits; it takes a push to learn what is holding it there.*

---

*This series grew out of a research question posed by Apart Research in their [AI Collusion Research Sprint](https://apartresearch.com/sprints/ai-collusion-research-sprint-2026-10-23-to-2026-10-25), which provided a [market environment and starter code](https://github.com/poseidon-research/collusion_hackathon) by Peist, Romero and Sauer. My code and data are at [github.com/omanshuthapliyal/llm-collusion-audit](https://github.com/omanshuthapliyal/llm-collusion-audit).*

[^1]: Associated Press (2026). [The barista is human but an AI agent runs this experimental Swedish cafe](https://wtop.com/lifestyle/2026/05/the-barista-is-human-but-an-ai-agent-runs-this-experimental-swedish-cafe). 11 May 2026.

[^2]: Anthropic (2025). [Project Vend](https://www.anthropic.com/research/project-vend-1).

[^3]: Anthropic (2026). [Project Deal](https://www.anthropic.com/features/project-deal).

[^4]: Assad, Clark, Ershov and Xu (2024). [Algorithmic Pricing and Competition: Empirical Evidence from the German Retail Gasoline Market](https://doi.org/10.1086/726906). *Journal of Political Economy* 132(3).

[^5]: Fish, Gonczarowski and Shorrer (2024). [Algorithmic Collusion by Large Language Models](https://arxiv.org/abs/2404.00806). arXiv:2404.00806.

[^6]: Baker McKenzie (2025). [United States: Ninth Circuit on algorithmic pricing](https://www.bakermckenzie.com/en/insight/publications/alerts/2025/08/united-states-ninth-circuit-on-algorithmic-pricing) (summary of *Gibson v. Cendyn Group*, 9th Cir., 15 August 2025).

[^7]: Harrington (2018). [Developing Competition Law for Collusion by Autonomous Artificial Agents](https://doi.org/10.1093/joclec/nhy016). *Journal of Competition Law & Economics* 14(3): 331-363.

[^8]: Calvano, Calzolari, Denicolò and Pastorello (2020). [Artificial Intelligence, Algorithmic Pricing, and Collusion](https://doi.org/10.1257/aer.20190623). *American Economic Review* 110(10): 3267-97.

[^9]: Calvano, Calzolari, Denicolò and Pastorello (2023). [Algorithmic collusion: Genuine or spurious?](https://doi.org/10.1016/j.ijindorg.2023.102973) *International Journal of Industrial Organization* 90: 102973.

[^10]: Tran and Yu (2026). [Is Anyone Enforcing the Cartel? What Reinforcement Learning Teaches LLM Agents in Markets](https://arxiv.org/abs/2610.28787). arXiv:2610.28787.

[^11]: Arslan, Kim and Xiao (2026). [Persistent Partners Raise Prices Among Learning Agents](https://arxiv.org/abs/2609.35402). arXiv:2609.35402.

[^12]: Lee and Park (2026). [Faithful yet Collusive](https://arxiv.org/abs/2609.18346). arXiv:2609.18346.
