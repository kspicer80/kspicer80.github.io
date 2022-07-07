---
title: "Topic Modeling the United States Supreme Court Utilizing the Top2Vec Library"
date: 2022-07-01 00:01:00 [change this!]
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
  - principal component analysis
  - Top2Vec
  - united states supreme court opinions
  - sklearn
  - ussc
---

Here in this post I'd like to continue working on the same project used in the previous post ([here](https://kspicer80.github.io/posts/2022-07-06-topic-modeling-the-ussc/)) while trying out the [Top2Vec library](https://github.com/ddangelov/Top2Vec)). As is so often the case, I came across this library via Dr. William Mattingly's YoutTube channel, who devoted two different videos to using this library ([here](https://www.youtube.com/watch?v=bEaxKSQ4Av8) and [here](https://www.youtube.com/watch?v=rmWI3xu9SII)). So let's jump in and see what we can do with this library. 

This time around we're using a slightly different dataset that comes Kaggle—[it contains](https://www.kaggle.com/datasets/gqfiddler/scotus-opinions) all of the USSC opinions from 1970 on. So let's load up some libraries and get everything read in as usual. Top2Vec needs a list of strings to process and vectorize, so we'll convert the dataframe that contains the texts (the .csv file has a column named ```text``` that we'll use) of the opinions into a list:

``` python
import pandas as pd
from top2vec import Top2Vec

file = '/Users/spicy.kev/Documents/github/supreme_court_opinion_topic_modeling/data/opinions_since_1970.csv'

df = pd.read_csv(file)

docs = df.text.tolist()
```

Then it's just a simple call to get a model built: ```top2vec_model = Top2Vec(docs) ```. Given that there are around 10,000 unique values for the ```text``` column, the model took quite a while to get everything processed—of course, one can easily save the model for further work by calling ```top2vec_model.save``` and passing a filename. Once everything was processed, we can get the vectors for all of the documents in the .csv: ```vectors = top2vec_model._get_document_vectors(). Following the [Top2Vec documentation](https://github.com/ddangelov/Top2Vec/blob/master/README.md), we can use the [UMAP library](https://umap-learn.readthedocs.io/en/latest/) to get the data into a format (a 2-dimensional form) that will allow us to produce a scatterplot of all the topics. First we perform the reduction and then we set up some umap_args for the plot:

``` python
reduced2d = umap.UMAP(n_neighbors=15, n_components=2, metric='cosine', verbose=True).fit(vectors)

umap_args_for_plot = {
    "n_neighbors": 10,
    "n_components": 2,
    "metric": "cosine",
    "min_dist": 0.10,
    'spread': 1
}
```

