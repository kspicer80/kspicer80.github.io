---
title: "Building a Dash App to Visualize the 5, 13, 8 EMA Investment Strategy"
date: 2024-12-14 00:10:57
draft: true
toc: false
tags:
  - python
  - data parsing
  - data extraction
  - json
  - data analysis
  - yfinance
  - FED
  - FRED
  - python for economics
  - render.com
  - dash
  - plotly
  - stock analysis
---

So, continuing to goof-around a little bit with applying my Python knowledge to analysis of the stock markets, I decided to build a [Dash app](https://dash.plotly.com) with Plotly that would allow one to see real-time price action while also implementing the well-known ["5-13-8 EMA"](https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/moving-average-trading-strategies/using-the-5-8-13-ema-crossover-for-short-term-trades) [trading strategy](https://www.investopedia.com/articles/active-trading/010116/perfect-moving-averages-day-trading.asp).

It's still a work-in-progress to be sure ... and it's probably totally unnecessary---such indicators are quickly and easily used on platforms like [Trading View](https://www.tradingview.com) and [Ninja Trader](https://ninjatrader.com), but I wondered if I could do myself, from scratch.

