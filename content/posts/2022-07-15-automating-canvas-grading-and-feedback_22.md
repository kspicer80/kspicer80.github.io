---
title: "Visualizing Online Class Discussion Boards (_redux_)"
date: 2022-07-20 00:01:00
draft: true
toc: false
images:
tags:
  - digital humanities
  - canvas instructure
  - discussion boards
  - online learning
  - lms
  - plotly
  - networkx
  - data visualization
  - custom functions
  - online discussion boards
  - work stuff
  - python
  - python for digital humanities
  - pandas
  - gephi
---

In a very [early post](https://kspicer80.github.io/posts/2019-12-31-visualizing-online-class-discussion-boards_04/) on this blog, I went through some of my incredibly kludgy attempts to visualize the discussion boards in my ENGL200: Introduction to Literature: Weird Fiction course that I have been teaching every semester since Fall of 2019. I have improved things quite a bit and made the worfklow a whole lot easier. I figured I could, once again, take everyone through the steps to see if it might be at all helpful for others with similar use-cases. I know that, originally, I had really just wanted to produce some simple ["network graphs"](https://en.wikipedia.org/wiki/Network_theory) that would keep track of the stories and authors that students were referencing in their posts each and every week. In that original post I was hard-coding each time a particular student made reference to a story/author, but I figured it would be nice to see if I couldn't automate this a little bit. 
