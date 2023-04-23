---
title: "Digital Rhetoric and Predictive Machine Learning Models on Twitter Data"
date: 2023-04-25 00:01:00
draft: true
toc: false
tags:
  - linear regression
  - pandas
  - machine learning
  - seaborn
  - scikit-learn
  - matplotlib
  - data visualization
  - python
  - jupyter
  - jupyter notebooks
  - codecademy
  - data visualization
  - twitter
  - digital rhetoric
  - dual-credit endorsement
  - grad-level courses
---

In my ENGE 515: Digital Rhetoric graduate-level course currently running (full list of courses is available through the [USF REAL program](https://www.stfrancis.edu/real/courses/), housed within the [College of Education](https://www.stfrancis.edu/education/)), we have been getting our feet wet in this field of rhetoric focused on the realm/world of "the digital" (I do notice too now—somehow it had slipped my mind—that I [wrote a little bit already](https://kspicer80.github.io/posts/2022-05-23-grad-level-digital-rhetoric-course_14/) about how this course went last summer). This past week (Week 6), we had a read of some somewhat contemporary work in this field, namely:

1. Crystal VanKooten's "Methodologies and Methods for Research in Digital Rhetoric" (available [here](https://www.enculturation.net/methodologies-and-methods-for-research-in-digital-rhetoric));
2. Sarah Riddick's "Deliberative Drifting: A Rhetorical Field Method for Audience Studies on Social Media”Download Deliberative Drifting: A Rhetorical Field Method for Audience Studies on Social Media" available in *Computers an Composition* 54 (2019): 1-27;
3. John Gallagher's "A Framework for Internet Case Study Methodology in Writing Studies," also available in *Computers and Composition* 54 (2019): 1-14.

I found the discussion of these texts on the boards to be incredibly thought-provoking (a big shout-out to [Leslie Allenspach](https://www.dupage88.net/site/page/15113) and many others for getting us onto this track). One of the things that bubbled to the surface most was what it might mean to talk about users' "engagement" on a social media platform like Twitter. The topic frequently centered around scholars' use of said platform as a kind of "object of research" all on its own—and many participants were somewhat surprised (I think) to learn that scholars and academics have produced work "mining" data from this platform in the same way that those within the private sector (companies, ad agencies, etc.) have been doing for years and years now.

Of course, I got to thinking about all of this from my own somewhat peculiar position of being an academic who also knows how to code (thankfully—or "hopefully"—that number continues to grow and grow each and every day) ... and, so, needless, to say, I was curious to think about what kinds of "data points" one might utilize in order to think through this admittedly somewhat amorphous concept of "user engagement." Furthermore, I started to wonder a bit too about whether or not there were somewhat more "expansive" parsings of this term than the one that we might get if we solely looked at the simple binary mechanism of the "Like" button. Moreover, I got meditating whether or not it would behoove us who work solely within the humanities (or who engage with the study of rhetoric, but, perhaps, not necessarily with that adjective, "digital," before the noun) to try to think about this issue of "engagement" in a more expansive way. What do I mean, exactly? Well, I wonder if "engagement"—at least when we're talking about the infamous 'Like' button—is often, quite unfruitfully, thought solely in a binary way: either a post is liked or it's not. But do we not need a metric for engagement that allows for some kind of degree? It's hard to say "how engaged" one might be if the button options are largely binary ... :) And how soon before we shift away from the like button simply because it might not (for many) be sophisticated enough to give us much data as a 'data point.' No doubt Riddick is correct to say that this button can give us a "data point"—that's undoubtedly true, but I often wonder how useful the like button is ... I have done some very simple machine learning on Twitter datasets in the past (see [here](https://kspicer80.github.io/posts/2022-03-26-twitter-viral-tweet-classification-project_08/) for an example of trying to classify a "Viral Tweet" and [here](https://kspicer80.github.io/posts/2022-02-15-twitter-sentiment-analysis_07/) for some sentiment analysis applied to Twitter data) and got thinking about how often a "feature" of this kind of dataset is utilized in order to train the models. Certainly the length gives us a non-binary structure and, no doubt, that's partly why we so often utilize it in the [feature engineering](https://towardsdatascience.com/what-is-feature-engineering-importance-tools-and-techniques-for-machine-learning-2080b0269f10) part of our workflows.

As I was responding to the posts over this past weekend, I was wondering how others have operationalized something like this "engagement" factor and then utilize it in models. I came across a dataset through the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)—which is a wonderful resource for those interested in training and testing out machine learning models—that had a ton of [labeled and wrangled data](https://archive.ics.uci.edu/ml/datasets/Buzz+in+social+media+#) that discussed ["Buzz"](http://grabmemedia.com/buzz-and-hype/) on Twitter. I also came across another [published paper](https://dl.acm.org/doi/fullHtml/10.1145/3184558.3191591) by Clemens Deusser, et. al.—after running the linear regression model I'll showcase below—that was after a similar quarry. Table 1 of Deusser, et. al. has a wonderful list of "Features" utilized, which included everything from the "contentlength" of the message string, to the number of comments, likes, replies, shares, reply ratios, and so much more. The dataset from Kawala, et. al. on the UCI site had a list of 77 different attributes collected in their dataset, with all kinds of things being measured (all descriptions below come from the datasets "Twitter.names" file, which contains all the information about the columns in the dataset). Here is just a small sample: 

1. "Average Discussions Length (ADL) (columns [63,69]): This feature directly measures the average length of a discussion belonging to the instance's topic."
2. "Author Interaction (AT) (columns [49,55]): This feature measures the average number of authors interacting on the instance's topic within a discussion."
3. "Number of Created Discussions (NCD) (columns [0,6]): This feature measures the number of discussions created at time step t and involving the instance's topic."
4. "Author Increase (AI) (columns [7,13]): This features [*sic*] the number of new authors interacting on the instance's topic at time t (i.e. its popularity)
5. "Attention Level (measured with number of authors) (AS(NA)) (columns [14,20]): This feature is a measure of the attention payed [*sic*] to a [*sic*] the instance's topic on a social media.
6. "Attention Level (measured with number of contributions) (AS(NAC)) (columns [35,41]): This feature is a measure of the attention payed [*sic*] to a the instance's topic on a social media."

In the very rightmost column, there is a "Predicted attribute," defined as follows: "Mean Number of active discussion (NAD). This attribute is a positive integer that describe the popularity of the instance's topic," which is the degree of "buzz" for a particular topic.

Could we do a little bit of work to see which of these attributes might be most strongly related to this "buzz" number? Let's write a little code and see.






This plot suggests quite a [strong positive correlation](https://static-assets.codecademy.com/Courses/data-literacy/stats/ex9-corr/index.html) between these two variables.


![regression_line_plot] 





