---
title: "Total *non sequitur*: Tracking the Price of Silver"
date: 2024-08-18 00:01:00
draft: false
toc: false
tags:
  - python
  - matplotlib
  - plotly
  - data analysis
  - data extraction
  - yfinance
  - stocks
  - silver prices
  - matplotlib
  - stock analysis
  - market analysis
  - data visualization
  - data analysis
  - graph plotting
---

### Silver Price Tracker

So, my father has some vintage Silver pieces from 1973 and 1974 produced by the Franklin Mint with all kinds of different national banks on each one.  We've been trying to figure out how to unload them---either to collectors or to folks that will simply melt them down for the silver alone.  I figured I'd do a little coding.

The first is a plot over the last couple of months of Silver prices:

![silver_price_last_couple_of_months](/images/imgforblogposts/post_35/last_couple_of_months_plot.png)

For those interested, yahoo finance has data going back plus twenty years---the data looks like this:

![all_historical_data](images/imgforblogposts/post_35/all_yfinance_data.png)

Here is a plot of some models' predictions for future Silver prices:

![silver_price_prediction_models](/images/imgforblogposts/post_35/all_models_silver_prices.png)

For those interested, here are some pics of the silver ingots themselves ...

I've got the Certificate of Authentication:

![authenticity](/images/imgforblogposts/post_35/IMG_0016.jpeg)

and then a picture of the ingots themselves:

![ingots](/images/imgforblogposts/post_35/IMG_0017.jpeg)

I'll try to update the plots pretty frequently. And if anyone is interested in making an offering on this just let me know at [kspicer@stfrancis.edu](mailto:kspicer@stfrancis.edu).

*Nota bene*: Code to produce this is available in this repo [here](https://github.com/kspicer80/silver_price_tracking).

P.S. Some more models, [ETS](https://www.statsmodels.org/dev/examples/notebooks/generated/ets.html#), [SARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average), and [LSTM](https://en.wikipedia.org/wiki/Long_short-term_memory) ...

Here is one week out:

![1_week_predictions](/images/imgforblogposts/post_35/lstm_and_other_model_predictions_1w.png)

And two weeks out:

![2_week_predictions](/images/imgforblogposts/post_35/lstm_and_other_model_predictions_1w.png)

And three to six months out:

![3_and_6_months_predictions](/images/imgforblogposts/post_35/lstm_and_other_model_predictions_3m_6m.png)

Testing a candlestick plot with plotly:

<iframe src="static//images/imgforblogposts/post_35/candlestick_plot_11_14_24.html" width=100% height="600px"></iframe>
