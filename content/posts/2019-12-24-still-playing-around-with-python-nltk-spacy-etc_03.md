---
title: "Still Playing Around with Python, NLTK, spaCy, etc."
date: 2021-12-25T08:19:43-06:00
draft: false
toc: false
images:
tags:
  - digital humanities
---

Ugh, so clearly my discipline in posting is nonexistent. It's fine—I'm still just dipping my toes in the water here—and not only that, I'm interested in trying to document my learning curve here, such as it is ... here's a WordCloud for Bram Stoker's _Dracula_:

![Fig. 1: Word Cloud for Bram Stoker's _Dracula_](/images/imgforblogposts/post_3/figure_1_stoker_word_cloud.png)

This past July I got an opportunity to do a NEH Summer Seminar over at the University of Iowa ("[Religion, Secularism, and the Novel](https://religion-secularism-novel.sites.uiowa.edu/)"), where the group read a number of canonical novels (_Crusoe_, _Silas Marner_, _Dracula_, _On the Road_, and _Home_). I enjoyed the seminar and loved all the so-called traditional humanities stuff: deep discussion, attentiveness to rhetoric and form, and all the other things that we literary scholars do so well. I did also fidget around with some of the newer DH methods (at the time it was really just basic computational stuff: counting tokens, plotting frequency dispersions, making silly little Word Clouds, etc.) on those very same texts we were looking at (excluding Robinson's _Home_).

Here's a ["lexical dispersion plot"](https://www.nltk.org/book_1ed/ch01.html) for the word "time" in Stoker's _Dracula_:

![Time](/images/imgforblogposts/post_3/figure_2_time_in_stoker.png)

Here's a dispersion plot for some of the major characters in _Dracula_:

![Character Dispersion Plots](/images/imgforblogposts/post_3/figure_3_character_dispersion_plots.png)

Here are some common nouns in _Dracula_:

![Common Nouns](/images/imgforblogposts/post_3/figure_4_common_word_counts.png)

Another Dispersion Plot

I didn't really find anything too profound—although it did for some reason surprise me just slightly that a word like "time" occurred as frequently as it did in _Dracula_ (simple counts found it 373 times [full exploratory notebook for this is available [here](https://github.com/kspicer80/nehsummerseminar2019playground/blob/master/nehexploratorynotebook.ipynb)—the dispersion plots too at this moment in time aren't actually plotting in Jupyter Notebooks {the [issue](https://github.com/googlecolab/colabtools/issues/397), it seems, is [known](https://stackoverflow.com/questions/54264548/nltk-lexical-dispersion-plot-does-not-show-on-google-colab) as of 24 December 2019}]).

I also spent a little bit of time messing around with [spaCy](https://spacy.io/)—tinkering around with the "Part of Speech" (POS) tagger and other things on the four texts. Here are some counts of different parts of speech in the four novels:

![Different Counts of Parts Speech](/images/imgforblogposts/post_3/figure_5_kinds_of_words_kerouac.png)

Dean, in _On the Road_, always trying to live in the eternal now, makes total sense the verb "to be" would show up all around him.

![Dean Verbs](/images/imgforblogposts/post_3/figure_6_kerouac_gender.png)

The code to generate the above figure is available [here](https://gist.github.com/kspicer80/f78d0cfccc43a9e07b05efca6b652b96))

One of the day's questions about _On the Road_ at the NEH Seminar had to do with what exactly it is like to read a book like _On the Road_ after the #MeToo movement. Some quick counting of the verbs used to describe Marylou, for instance, comes up as follows:

```python
 ('be', 34),
 ('have', 10),
 ('want', 10),
 ('know', 9),
 ('go', 9),
 ('say', 8),
 ('sleep', 7),
 ('see', 6),
 ('get', 5),
 ('sit', 5),
 ('make', 5),
 ('take', 5),
 ('tell', 4),
 ('find', 4),
 ('jump', 3),
 ('run', 3),
 ('do', 3),
 ('drive', 3),
 ('wait', 3),
 ('lean', 3)
```
Looking at Sal:

```python
 ('be', 25),
 ('go', 18),
 ('say', 14),
 ('get', 10),
 ('tell', 8),
 ('think', 8),
 ('have', 7),
 ('want', 5),
 ('know', 4),
 ('come', 4),
 ('dig', 4),
 ('do', 3),
 ('call', 3),
 ('let', 3),
 ('make', 3),
 ('see', 3),
 ('ask', 2),
 ('arrive', 2),
 ('remember', 2),
 ('find', 2)
```
And now at Dean:

```python
 ('be', 198),
 ('say', 105),
 ('go', 44),
 ('have', 41),
 ('take', 29),
 ('come', 28),
 ('see', 27),
 ('know', 26),
 ('tell', 25),
 ('get', 25),
 ('yell', 21),
 ('do', 17),
 ('drive', 17),
 ('want', 14),
 ('cry', 14),
 ('sit', 13),
 ('look', 12),
 ('talk', 11),
 ('sleep', 11),
 ('stand', 11)
```
As I say, I'm still just dipping my toes in ... more to come I'm sure.

P.S. Code used to generate things here can be found in [this repo](https://github.com/kspicer80/nehsummerseminar2019playground).
