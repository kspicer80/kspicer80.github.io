---
title: "Inaugural Post and ... Re-posting an Old Post (1 of 4) from an Older WordPress site"
date: 2021-12-24T08:19:43-06:00
draft: false
toc: false
tags:
  - beverly cleary, bevery cleary ramona, dependency parsing, dh, digital humanities, old wordpress posts, displacy, python, python nltk, spacy, visualization
---

Okay, so here goes for an inaugural post—hoping to essentially combine my graduate work (in Continental Philosophy and Derridean deconstruction—where the _X without X_ [updated 12.24.2021: the old website this initial post came from was at xwithoutxdrs.wordpress.com] locution is so at home in the work of Blanchot, Derrida, et. al.)—with all of the new toys I am learning to play with from the Digital Humanities.

So after a week-long [research institute](http://dhsouthbend.org/dhri/) put together by some fantastic people at the College of St. Mary's and Notre Dame earlier in the summer, I got my hands dirty with a whole host of tools of the trade within the Digital Humanities.  As one can see from the [curriculum](http://dhsouthbend.org/dhri/curriculum/), the week was rather intense and both I and [my colleague](https://annaioanes.wordpress.com/) came back exhausted, to be sure, but also full of all kinds of new knowledge and (best of all) a sense of how much knowledge we still need to try to acquire.

Playing around with [spaCy](https://spacy.io/)-displaCy and a sentence from Beverly Cleary's _Ramona Forever_ (image shows a "dependency parsing" for the novel's first sentence—my youngest child is reading all of these books at the moment):

![]("/images/imgforblogposts/post_1/ramona_sentence.svg")

<p align = "center">
<img src = "/images/imgforblogposts/post_1/ramona_sentence.svg">
</p>

Feel free to go and compare the nicer (less black-and-white version) provided by Google's Cloud Natural Language API [here](https://cloud.google.com/natural-language/). 

More to come ... (I'm also hoping to use this whole site as a kind of sandbox in which to play around with many of these new toys, not to mention just Wordpress itself ... [I need a bunch more time playing around with this new "block" editor thing here too[updated as of 12.24.2021: I need more time to fiddle around with Markdown, HTML, and a bunch of other stuff]]—nobody'll read these things anyways, so here seems as good a place as any, lol ...)

The simple code to generate the displaCy figure is here:

```python
import spacy
nlp = spacy.load("en_core_web_lg")
from pathlib import Path

sentence = "Guess what? Ramona Quimby asked one Friday evening when her Aunt Beatrice dropped by to show off her new ski clothes and to stay for supper."

doc = nlp(sentence)
dep_image = spacy.displacy.render(doc, style="dep", minify=True)
output_path = Path("ramona_sentence.svg")
output_path.open("w", encoding="utf-8").write(dep_image)
```
