---
title: "Bitcoin vs. the DOW and NASDAQ"
date: 2025-01-06 00:10:57
draft: false
toc: false
tags:
  - python
  - data parsing
  - data extraction
  - json
  - data analysis
  - yfinance
  - financial analysis
  - financial suggestions
  - python for economics
  - stock analysis
  - stocks
  - stock analysis
  - cryptos
  - cryptocurrencies
  - bitcoin
  - Dow Jones Industrial Average
  - NASDAQ
  - BIT-USC
  - Bitcoin
  - ^DJI
  - ^IXI
---

So there's been a lot of talk lately about [Microstrategy's](https://finance.yahoo.com/quote/MSTR/) seemingly almost constant buys of Bitcoin almost every single day. There's also been quite a lot of chatter recently about some other hardware companies, ([Marvel Technologies](https://finance.yahoo.com/quote/MRVL/), [MARA](https://finance.yahoo.com/quote/MARA/), etc.) getting involved. We also have things like ["Coinbase"](https://finance.yahoo.com/quote/COIN/) that is frequently linked to Bitcoin as well. 

I thought I would do some coding to see how correlated these stock tickers are with Bitcoin. But before that I wrote some code to see how correlated the Dow Jones and NASDAQ were with BTC-USD. Do our "normal" markets just follow what Bitcoin's up to ...? Here's an exploratory [Jupyter Notebook](https://jupyter.org) with some analysis:

{{< jupyter src="/notebooks/01-06-2025_btc_vs_regular_exchanges.html" >}}

If we wanted a plot of all these exchanges vs. the top ten crypto---here we go:

![dow_nasdaq_vs_top_ten_crypto](/images/imgforblogposts/post_38/dow_nasdas_vs_top_ten_cryptos.png)

Repo containing this and other code related to the markets is available [here](https://github.com/kspicer80/stock_stuff/tree/main).



