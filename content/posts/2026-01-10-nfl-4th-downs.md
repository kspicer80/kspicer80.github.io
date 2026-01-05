---
title: ""
date: 2026-01-10 00:05:00
draft: true
toc: false
tags:
  - python
  - data parsing
  - data extraction
  - data analysis
  - NFL
  - python for sports
  - polars
  - matplotlib
  - data visualization
  - csv
  - nflreadpy
---

### Introductory Setup

This past Thanksgiving I headed over to Sioux City, IA to visit my folks, brother, and sister-in-law. Thursday found my father and I watching the Chiefs game against the Cowboys (Dallas carried the day [31-28](https://www.nfl.com/games/chiefs-at-cowboys-2025-reg-13?tab=stats)).   At some point, my dad turned to me and said something to the effect of you, "Doesn't it seem like teams nowadays are going for it on fourth down far more than they used to?" "Oooh, I suppose so, though that's a fantastically empirical question we could figure out." "Sounds like a question for [ChatGPT](https://chatgpt.com)," he comically quipped. As per usual, I told him that don't sound like any fun and said I'd much rather code it up myself. So, here, below, is the workflow to investigate (github repo with everything is available [here](https://github.com/kspicer80/nfl_fourth_downs)). I've split said repo into either different steps, which we'll have a look at below.

#### Step 1: Gathering the Data

As always, we start by gathering the data we need.  