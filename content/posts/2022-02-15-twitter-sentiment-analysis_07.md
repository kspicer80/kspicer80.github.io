---
title: "Sentiment Analysis of Peer Institutions' Main Twitter Accounts"
date: 2022-02-09T06:14:31-06:00
draft: true
toc: false
images:
tags:
  - sentiment analysis
  - TextBlob
  - digital humanities
---

Well, February has come around and that's the time at my school where we get all kinds of nice financial data about how wages and compensation by faculty rank compare between a number of "peer institutions" (the usual ones linked with USF are [Benedictine](https://www.ben.edu), [Dominican](https://dom.edu), [Lewis](https://www.lewisu.edu), and [Saint Xavier](https://www.sxu.edu)) I wondered a bit if one might do a little bit of data visualization not of financial information, but of, say, Twitter accounts. Thinking it might be fun to dabble a little bit in some very basic sentiment analysis, I was curious to see what the main Twitter accounts for these five Chicagoland "peer institution" universities might look like—thus, I wrangled some data to see what there was to see. Would one be correct to assume that Twitter accounts for these universities would slide largely in the "positive" sentiment direction?

Well, let's start with my [current institution](https://twitter.com/uofstfrancis):

![](/images/imgforblogposts/post_7/usf_sentiment_results_pie_chart.png)

Running all of the university's tweets through the [TextBlob](https://textblob.readthedocs.io/en/dev/quickstart.html) python library, it shows the USF Twitter account to be pretty positive. Results for the rest of the schools is pretty similar:

![](/images/imgforblogposts/post_7/ben_u_sentiment_results_pie_chart.png)
