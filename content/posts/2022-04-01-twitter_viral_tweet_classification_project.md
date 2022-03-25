---
title: "Viral Tweet Classification Project"
date: 
draft: true
toc: false
images:
tags:
  - machine learning
  - digital humanities
  - Python for the digital humanities
  - Python
  - k-nearest neighbors
  - Codecademy
  - Twitter
  - viral tweets
  - sklearn
  - matplotlib
  - pandas
---

I had a bit of fun recently working on a machine learning classification project using some Twitter data (said project coming through [Codecademy](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)). The goal was to see if we could write some code to properly detect whether or not a tweet was viral (using the [K-Nearest Neighbors](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) algorithm). I also played around with a [logistic regression](https://en.wikipedia.org/wiki/Logistic_regression) model as well. All the code for the following is available in this [repo](https://github.com/kspicer80/twitter_classification_codecademy_project). I then took all this dabbling and turned the algorithms on some different datasets of a much more "literary" kind. (Another post is still to come on seeing how well the algorithms might be able to distinguish between Willa Cather and one of her key predecessors, Sarah Orne Jewett.)

So, first things first, we're importing the necessary libraries for this task:

``` python
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
pd.options.display.width = 0
```

After reading in all the Twitter data from a .json file, we needed to think a little bit about how exactly we might want to define a "viral tweet"? Base it solely on the number of retweets, on the number of likes, on the number of favorites? The parameters for the original task suggested we might start with the median number of retweets for each tweet (I also had a look at the ```favorite_count``` as well to see what the minimum, maximum, median, and mean numbers looked like):

``` python
retweet_counts = viral_tweets['retweet_count']
median_retweet_count = viral_tweets['retweet_count'].median()
mean_retweet_count = viral_tweets['retweet_count'].mean()

print(viral_tweets.agg(
    {
        "retweet_count": ["min", "max", "median", 'mean'],
        "favorite_count": ["min", "max", "median", "mean"],
    }
))
```
Graphing these values we get the following:

![](/images/imgforblogposts/post_8/Figure_1.png)



![](/images/imgforblogposts/post_6/excel_worksheet_clutter.png)
