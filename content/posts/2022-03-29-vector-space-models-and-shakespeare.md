---
title: "Using Vector Space Models with Shakespeare's Plays"
date: 2022-03-29
draft: true
toc: false
images:
tags:
  - digital humanities
  - Python for the digital humanities
  - Python
  - document term matrix
  - sklearn
  - matplotlib
  - pandas
  - TEI Simple
  - Text Encoding Initiative
  - TEI
  - Shakespeare
  - Folger Digital Library
  - box plots
  - distance metrics
  - cosine distance
  - Manhattan distance
  - city block distance
  - euclidean distance
---

![Chandos Portrait of Shakespeare](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Shakespeare.jpg/187px-Shakespeare.jpg)

Much of the toe-dipping into this new DH field I've been doing as of late has centered around learning many of the kinds of projects carried out and then turning the methods within those projects onto mew artifacts. A while back I worked my way through Folgert Karsdorp, Mike Kestemont, and Allen Riddell's [_Humanities Data Analysis: Case Studies with Python_](https://press.princeton.edu/books/hardcover/9780691172361/humanities-data-analysis). I found a great deal of it thought-provoking and fascinating—especially the chapters devoted to modeling texts with vector spaces and the later chapter on stylometry, which focused on some texts by Hildegard of Bingen and Bernard of Clairvaux. With regards to the first vector space angle, a good deal of very old and dusty linear algebra from my undergraduate days has been rattling around in my head as of late—and it was quite fun to see if I could get any of the old gears turning again (some I definitely could, others will need a bit more grease to get things moving once more).

Chapter 3 of _Humanities Data Analysis_ focused on visually "mapping" a number of different genres of plays from classical French theater, utilizing some vector space math. I wondered what things would look like if we turned these methods on some of Shakespeare's works. All the plays Karsdorp, et. al. were working with were in .xml format—and after learning how much time the data analyst working on just getting data into a form and structure ("preprocessing" that is ready for analytic work in the first place, it seemed easy enough to simply grab the bard's texts from _The Folger Shakespeare_, especially since one can get them all in [TEI Simple](https://tei-c.org/tag/tei-simple/) [.xml format](https://shakespeare.folger.edu/download-the-folger-shakespeare-complete-set/)—which makes all the plays incredibly easy to parse since all the work of encoding has been done for one already.
