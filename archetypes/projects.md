---
title: "Your Project Title Goes Here"

# used for ordering (descending)
date: "{{ .Date }}"

# --- new, all optional, backward compatible ---
# one-line description shown on the card
summary: ""

# "Ongoing", "2023-present", "Completed 2024", etc. Shown as a small
# label on the card.
status: ""

# tag chips shown on the card, e.g. ["robotics", "verification"]
tags: []

# set true to render this as the large spotlight card at the top of
# the grid (use for the 1-2 things you want visitors to see first)
featured: false

# page-resource filename (e.g. "cover.jpg", placed next to this file
# in the same folder) or an absolute path like "/images/foo.png".
# Leave blank to get a placeholder cover instead.
cover: ""

links:
    website: 'https://example.com/'
    code: 'https://github.com/'
---

Write the full project writeup here — this renders on the project's
own page. Code blocks, images/figures, and LaTeX (via the site's
existing MathJax setup) all work here same as in blog posts.
