---
title: "Visualizing Online Class Discussion Boards (_redux_)"
date: 2022-07-20 00:01:00 [CHANGE THIS!!!!!]
draft: true
toc: false
images:
tags:
  - discussion boards
  - online learning
  - lms
  - plotly
  - networkx
  - data visualization
  - custom functions
  - automating grading
  - automating student feedback
  - online discussion boards
  - json
  - xml
  - work stuff
  - python
  - python for digital humanities
  - pandas
  - gephi
---

In a very [early post](https://kspicer80.github.io/posts/2019-12-31-visualizing-online-class-discussion-boards_04/) on this blog, I went through some of my incredibly kludgy attempts to visualize the discussion boards in my ENGL200: Introduction to Literature: Weird Fiction course that I have been teaching every semester since Fall of 2019. I have improved things quite a bit and made the worfklow a whole lot easier. I figured I could, once again, take everyone through the steps to see if it might be at all helpful for others with similar use-cases. I know that, originally, I had really just wanted to produce some simple ["network graphs"](https://en.wikipedia.org/wiki/Network_theory) that would keep track of the stories and authors that students were referencing in their posts each and every week. In that original post I was hard-coding each time a particular student made reference to a story/author, but I figured it would be nice to see if I couldn't automate this a little bit. 

So the first thing we need to do is gather all of the data. Ideally, it would be nice to have some methods native to the Canvas Instructure LMS to download all of the Discussion Board posts from a particular Canvas course shell. At the moment of writing, there is still no way to do this simply using Canvas's tools, although, again, as seems quite usual and common for Canvas, [members of the community]((https://community.canvaslms.com/t5/Canvas-Question-Forum/Is-there-a-way-to-download-all-student-submissions-in-a-CANVAS/td-p/163333)) have suggested adding such a feature to the Instructure's offerings. Fortunately, there are some user-developed scripts that will allow one to grab all of the posts (best Canvas Usercript for this is available through [TamperMonkey](https://www.tampermonkey.net/) [here](https://breid.host.dartmouth.edu/userscripts/)). Once you run the script while in the "Discussion" arena of Canvas, you can get a ```.csv``` file that has all kinds of fantastic information and data in it. 








All of the plotly visualizations is available [here](https://github.com/kspicer80/solo_projects/tree/main/weird_fiction_visualizations) ...