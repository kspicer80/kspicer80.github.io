---
title: "Topic Modeling the United States Supreme Court"
date: 2022-06-01 00:01:00 [change this!]
draft: true
toc: false
images:
tags:
  - digital humanities
  - machine learning
  - supervised machine learning
  - matplotlib
  - data visualization
  - work stuff
  - python
  - python for digital humanities
  - pandas
  - topic modeling
  - PCA
  - principal component analysis
  - Top2Vec
  - united states supreme court opinions
  - sklearn
  - ussc
---

# General Background

(All code from this section is available in this repository [here](https://github.com/kspicer80/roe_v_wade_topic_modeling).)

Friday of last week, June 24th, 2022, was a profoundly dark day for a great many of us in the United States. Feeling somewhat helpless as the Supreme Court published the [final draft](https://www.supremecourt.gov/opinions/21pdf/19-1392_6j37.pdf) of _Dobbs v. Jackson Women's Health Organization_, I couldn't help but fall back on old patterns. Not really knowing what else to do—I had a student with whom I had recently read the leaked original draft posted by [Politico](https://www.politico.com/news/2022/05/02/read-justice-alito-initial-abortion-opinion-overturn-roe-v-wade-pdf-00029504)—I couldn't help but say to her when the opinion came down that I didn't know what else to do other than to get to reading. There's something about the academic position—"Well, let's get started reading ..."—that felt so weak to me at the moment in the face of all the implications and consequences of this huge decision, but, honestly, I wasn't quite sure what else to do other than to go to the default thing that the academic does: read ... and think. Last Friday was a very dark day for sure; as I heard one commentator say (who exactly escapes me at the moment), it isn't every day that you can wake up and can see that your daughter literally has fewer rights on that day than her own mother or grandmother had over all the decades since 1973. "A dark day" doesn't even really capture things.

I read the draft decision multiple times—twice, in fact—; I read the full version of the consenting and dissenting opinions, again, twice. I figured this might be as good an opportunity as any to try out some of the things I've learned recently working with the whole [topic modeling](https://en.wikipedia.org/wiki/Topic_model) area of NLP and machine learning in general.

## Roe v. Wade (410 US 113) Topic Modeling Over Time

_Humanities Data Analysis: Case Studies with Python_ by Folgert Karsdorp, Mike Kestemont, and Allen Riddell (a fantastically awesome text, by the way, I should say!) has an entire chapter that would seem perfectly fine for my purposes here. Chapter 9, "A Topic Model of United States Supreme Court Opinions, 1900-2000," has a ton of the data that we would want to be looking at here with regards to thinking about the _Dobbs_ decision. Karsdorp, et. al. has a [dataset with a .jsonl file](https://www.humanitiesdataanalysis.org/topic-models/notebook.html) with a ton of Supreme Court opinions separated by author name, case_id, the type of opinion, and the year the opinion was submitted. We start with the standard moves: importing the necessary libraries and getting the .jsonl file read into a dataframe:

``` python
import os
import gzip
import pandas as pd
import numpy as np

with gzip.open('../datasets/supreme-court-opinions-by-author.jsonl.gz', 'rt') as fh:
    df = pd.read_json(fh, lines=True).set_index(['us_reports_citation', 'authors'])
```

We're interested in looking at the _Roe_ case, which is denoted as "410 US 113," Harry Blackmun wrote the main opinion:

```python
print(df.loc['410 US 113'].loc['blackmun', 'text'][:250])
```
    
    OPINION BY: BLACKMUN
    OPINION
    MR. JUSTICE BLACKMUN delivered the opinion of the Court.
    This Texas federal appeal and its Georgia companion, Doe v. Bolton, post, p. 179, present constitutional challenges to state criminal abortion legislation. The Tex
    

We can also just quickly looking at the distribution of opinions over time in the dataset if we like:

```python
df['year'].hist(bins=50)
```

![distribution of opinions](/images/imgforblogposts/post_16/number_of_opinions_distribution_histogram.png)

We can also get some simple information (how many opinions are there in the dataframe, etc.):

```python
df['year'].describe()

    count    34677.000000
    mean      1928.824552
    std         48.821262
    min       1794.000000
    25%       1890.000000
    50%       1927.000000
    75%       1974.000000
    max       2008.000000
    Name: year, dtype: float64
```

The next thing we need to do is convert all of the text of each case's opinion into a numerical representation that the computer can understand:

``` python
import sklearn.feature_extraction.text as text

vec= text.CountVectorizer(lowercase=True, min_df=100, stop_words='english')
dtm = vec.fit_transform(df['text'])

print(f'Shape of document-term matrix: {dtm.shape}. '
     f'Number of tokens: {dtm.sum()}')
```

This results in a ```(34677, 13231)``` matrix with a total number of tokens of ```36,139,890```—quite a few tokens there, to be sure. We then utilize the [Latent Dirichlet Allocation model](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) to transform the document-term matrix and find all the different "topics" contained within all our texts:

``` python
import sklearn.decomposition as decomposition
model = decomposition.LatentDirichletAllocation(n_components=100, learning_method='online', random_state=1)

document_topic_distributions = model.fit_transform(dtm)
vocabulary = vec.get_feature_names()
assert model.components_.shape == (100, len(vocabulary))
assert document_topic_distributions.shape == (dtm.shape[0], 100)
```

We can then have a look at the topic distributions that describe the case and Blackmun's opinion. The result shows us that "Topic 14" is the highest:

``` python
blackmun_opinion = document_topic_distributions.loc['410 US 113'].loc['blackmun']
blackmun_opinion.sort_values(ascending=False).head(10)

Topic 14    0.261380
Topic 63    0.103755
Topic 6     0.079996
Topic 49    0.079675
Topic 17    0.049497
Topic 35    0.038979
Topic 42    0.037718
Topic 93    0.034306
Topic 78    0.033144
Topic 41    0.032153
Name: blackmun, dtype: float64
```

We can next look at the most frequently occuring words per this particular topic and it would seem to give us what we would expect:

``` python
topic_word_distributions.loc['Topic 14'].sort_values(ascending=False).head(18)

child        7148.398106
children     5668.526880
medical      5167.666624
health       3431.308011
women        3194.024162
treatment    2919.207243
care         2912.593764
hospital     2839.550152
family       2722.583008
age          2686.429177
parents      2646.981270
mental       2515.309043
abortion     2473.571781
social       2115.088729
statute      2025.966412
life         1893.954525
woman        1820.462268
physician    1813.155061
Name: Topic 14, dtype: float64
```

Karsdorp, et. al. next utilize the "Spaeth Issue Areas" (documentation for this is available through [Washington University in St. Louis's](http://scdb.wustl.edu/documentation.php?var=issueArea) SCDB ["Supreme Court Database"]) that categorizes decisions based on a number of "broad areas":

> Values:  
    1 Criminal Procedure  
    2 Civil Rights  
    3 First Amendment  
    4 Due Process  
    5 Privacy  
    6 Attorneys  
    7 Unions  
    8 Economic Activity  
    9 Judicial Power  
    10 Federalism  
    11 Interstate Relations  
    12 Federal Taxation  
    13 Miscellaneous  
    14 Private Action

(# 14 was added since the 2016 version utilized in Karsdorp, et. al., so I have added it here.)First we put this into a dictionary; next we read in a dataframe the ```scdb_2021_case_based.csv``` file (also pulled from Wash U's [website](http://scdb.wustl.edu/data.php)) and then join this dataframe to our previous one containing all the opinions, being sure to join it together using the "issueArea" column from the SCDB file with the "case_id" column of the original opinions dataframe; lastly we utilize the pandas ```Categorical``` [function](https://pandas.pydata.org/docs/reference/api/pandas.Categorical.html) to convert our wanted column to the ```Categorical``` datatype. We can then see how many of the opinions in our original dataframe fall under each of the different Spaeth areas within Topic 14:

 ``` python
 issueArea
Criminal Procedure       33288.010972
Civil Rights            172757.834085
First Amendment          34239.879011
Due Process              33358.340810
Privacy                  93654.682271
Attorneys                 3454.198377
Unions                    3553.985849
Economic Activity        18875.924499
Judicial Power           23458.627270
Federalism               16451.143912
Interstate Relations        78.270460
Federal Taxation          2052.147267
Miscellaneous              526.598339
Private Action              20.014372
Name: Topic 14, dtype: float64
```






## Top2Vec Topic Modeling Plots

## PCA (Principal Component Analysis) of Recent Justices (Gorsuch, Kavanaugh, Barrett)