---
title: "More _The Turn of the Screw_ Data Analysis"
date: 2022-05-27 11:49:00
draft: false
toc: false
images:
tags:
  - digital humanities
  - henry james
  - turn of the screw
  - matplotlib
  - nltk
  - NLTK 
  - data visualization
  - word frequency counts
  - work stuff
  - python
  - python for digital humanities
---
  
I know I mentioned in [an earlier post](https://kspicer80.github.io/posts/2022-04-20-tei-encoding-with-henry-james/)—a couple of different posts actually ([here](https://kspicer80.github.io/posts/2022-05-15-more-tots-hmtl-testing_introductory_post/) and [here]() too)—that I've been doing a bunch of work with Henry James's canonical _The Turn of the Screw_. I thought I would post a little bit more here of what I've been up to as of late with this. A student of mine was fascinated by the use of the words "prodigious" and "portentous" in the Governess's narrative in _Turn_. She said she noticed it frequently. It makes sense that these words would be in the Governess's narrative, given her penchant for playing the detective (or the psychoanalyst), always trying to read the signs pointing to forbidden knowledge. But how often does she use these words? Let's write some code, make some graphs, and figure it out.

First things first, let's have a look-see at the [NLTK library](https://www.nltk.org/) for some basic word counts/[lexical dispersion plots](https://www.nltk.org/api/nltk.draw.dispersion.html#module-nltk.draw.dispersion). 

A simple use of the [```nltk.text.concordance```](https://www.nltk.org/howto/concordance.html)  function can give us a nice print out of a specific range of tokens within the text that has the word in question.

``` python
import nltk
from nltk.tokenize import word_tokenize
from nltk.draw.dispersion import dispersion_plot
import matplotlib.pyplot as plt

with open(r'nltk_playground\tots.txt', encoding='utf-8') as f:
    data = f.read()

tokens = word_tokenize(data)
tots_text = nltk.Text(tokens)
    
prodigious_concordance = tots_text.concordance('prodigious', width=200)
```

For "prodigious" we get the following output:

![Concordance output for "prodigious"](/images/imgforblogposts/post_13/concordance_for_prodigious.png)

An equally simple call of the ```dispersion_plot``` NLTK function gives us an image of where the word appears in the text as a whole:

``` python
plt.figure(figsize=(12, 9))
targets = ['prodigious']
dispersion_plot(tokens, targets, ignore_case=True, title='Lexical Dispersion Plot for "Prodigious"')
```

![Lexical Dispersion Plot for "Prodigious"](/images/imgforblogposts/post_13/lexical_dispersion_plot_for_prodigious.png)

Of course, we can plot them both on the same figure if we like:

![Lexical Dispersion Plot for "Prodigious" and "Portentous"](/images/imgforblogposts/post_13/lexical_dispersion_plot_for_prodigious_and_portentous.png)

We could also [lemmatize](https://en.wikipedia.org/wiki/Lemmatisation) the text [beforehand](https://www.nltk.org/_modules/nltk/stem/wordnet.html) and see if we get any more words hitting our target list (here we'll just provide a list of lemmas to search for, find, and then plot):

``` python 
targets=['prodigious', 'prodigiously', 'prodigiousness', 'portentous', 'portentously']
dispersion_plot(tokens, targets, ignore_case=True, title='Lexical Dispersion Plot of Lemmas for "Prodigious" and "Portentous"')
``` 

![Lemma Lexical Dispersion Plot](/images/imgforblogposts/post_13/lemma_lexical_dispersion_plot.png)

After a bunch of conversations with my student about these words, I thought it might be curious to see how the frequency of these words compare over a larger selection of James's corpus. Easy enough—I grabbed all the texts I could from [Project Gutenberg by James](https://www.gutenberg.org/ebooks/author/113).

Again, some very simple [Python code](https://github.com/kspicer80/henry_james/blob/main/prodigious_and_portentous_counts.py) can give us counts of these words and lemmas across multiple works by James:

![Counts across James's Corpus](/images/imgforblogposts/post_13/prodigious_and_portentous_counts_across_james_corpus.png)

We can see that the frequency of some of these words go over the course of time; we also see that the counts for _Turn_ are also pretty high, especially for "prodigious." More to come on this, for sure, as I would like to write a post dealing with the motif of repetition in the story. 

(All the code for this post is available in this [repo](https://github.com/kspicer80/henry_james).)












