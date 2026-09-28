---
title: "Contract-Aware SLA Compliance Monitoring"
status: "active"
start_date: 2025-01-01
description: "AI agents turn colocation SLA contracts into verifiable compliance rules, and a per-customer attention model watches power and temperature data to flag likely breaches 30 minutes before they happen."
organization: "Strategic Data Solutions Lab, Hitachi America Ltd."
tags: ["agentic-ai", "contract-analysis", "information-extraction", "nlp", "sla-monitoring", "data-centers"]
stack: ["LangGraph", "LangChain", "Transformers", "PEFT", "sentence-transformers", "Pydantic", "LegalBench"]
paper: "https://arxiv.org/abs/2605.05354"
patent: "patents/patent-06"
slides: "https://github.com/omanshuthapliyal/ICDCS2026--Omanshu-Thapliyal/blob/main/ICDCS-slides-Omanshu_Thapliyal.pdf"
video: "https://drive.google.com/file/d/1Qg1Z77z8ebm93LKlbUaJDfVGBNXSsFcu/view?usp=sharing"
resources:
  - label: "Hitachi Review article (Dec 2024): From Supply Chain to Operations, A Portfolio Approach to Capacity Expansion in Colocation Data Centers"
    url: "https://www.hitachihyoron.com/rev/contents/202412/tech_docs/08/index.html"
related: ["papers/pub17", "papers/pub18", "patents/patent-06", "patents/patent-09"]
image: "/images/projects/proj6-sla-architecture-thumb.png"
image_alt: "System architecture: SLA documents flow through ingestion and a ReAct agent framework into a structured rules database, which labels historical sensor data and drives a per-customer prediction model whose streamed outputs serve operations, finance and compliance teams"
hero_image: "/images/projects/proj6-sla-architecture.png"
hero_alt: "System architecture: SLA documents are sanitized, a ReAct agent framework extracts and evaluates rules into a structured rules database, the rules programmatically label historical sensor data to train a per-customer multi-headed transformer, and its windowed predictions on live sensor data stream to operations, finance and compliance teams, who can feed custom rule changes back"
image_caption: "System architecture: contracts become a structured rules database that labels historical sensor data, trains a per-customer prediction model, and streams windowed predictions on live data to operations, finance and compliance teams, with their rule changes fed back. From [A Multi-Head Attention Approach for SLA Compliance Monitoring in Data Centers](/papers/a-multi-head-attention-approach-for-sla-compliance-monitoring-in-data-centers/), IEEE ICDCS 2026."
---

## Problem

Colocation contracts promise each tenant specific limits on power, temperature
and humidity, with penalty credits when those limits are broken. The terms that
matter, such as a measurement window, an exclusion or a deadline for claiming
credits, are scattered across long contracts and worded differently by every
vendor. Monitoring is usually reactive: a breach is noticed only after it has
already cost money.

## Approach

AI agents read each SLA contract and turn it into structured, machine-checkable
rules. Every rule carries the exact contract text it came from, and a
verification step checks that quote against the source before the rule is used.

Those rules then drive monitoring. They label historical sensor data
automatically, so no manual annotation is needed, and they train a model for
each customer in which every attention head tracks one SLA rule. Its
predictions reach three audiences: credit exposure for finance, risk scores and
suggested actions for operations, and an evidence trail for compliance.

## Outcome

{{< figure src="/images/projects/proj6-sla-demo.gif" alt="Screen recording of the platform: headline extraction metrics, the contract-to-rule pipeline, and a provenance trace from a contract clause to a detected breach" caption="Proof of concept: the working platform, from extraction metrics to the processing pipeline to a full provenance trace, ending in a detected breach and the remedy clause it triggers." >}}

- **Breaches predicted about 30 minutes ahead.** Operators get time to act
  before a violation costs money, instead of finding out afterwards.
- **Over 22,000 contract rules, each traceable to its source.** Every rule
  points back to the exact contract text it came from, so any alert can be
  audited.
- **A working end-to-end platform.** It runs from a raw contract all the way to
  a breach alert and the remedy clause it triggers.
- **Strong results on legal benchmarks.** It scores up to 100% on LegalBench
  contract-review tasks such as governing law and termination for convenience,
  and lifts ContractNLI accuracy from 65% to 78%.
- **Published, patented and heading to market.** Papers at IEEE ICDCS 2026 and
  an ICML 2026 workshop, a patent application filed, and the solution is now
  going through commercialization.
