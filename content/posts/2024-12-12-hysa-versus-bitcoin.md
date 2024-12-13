---
title: "Economic Analyses: High-Yield Savings Accounts (HYSA) and Bitcoin ... Given Posible Reduction in the Interest Rate by the FED"
date: 2024-12-11 00:10:57
draft: false
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
---

Okay, so recently I've been moving into using my Python knowledge to look at and analyze financial data. We know that the FED is next scheduled to meet on December 17-18 of this year. Many are predicting that we will see a [decrease](https://www.cnbc.com/2024/12/07/the-fed-is-on-course-to-cut-interest-rates-in-december-but-what-happens-next-is-anyones-guess.html#:~:text=Economy-,The%20Fed%20is%20on%20course%20to%20cut%20interest%20rates%20in,happens%20next%20is%20anyone's%20guess&text=The%20not%2Dtoo%2Dhot%2C,needed%20to%20cut%20interest%20rates.) in interest rates.

So, if you have your money in a High-Yield Savings Account (HYSA)---which you obviously should---would it make more sense to move it elsewhere ... say, into Crypto? Thus, I set the task of answering this question and wanting to see if I could do it with all my new programming skills. Well---off we go, let's write some code!

What you'll need ahead of time is an API Key from [FRED](https://fred.stlouisfed.org)---you can get this simply by creating a (free) account---, which will allow us to grab the current FED interest rate. Other than that, we should be good to go!

```python

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import requests
import json

# Function to load configuration from a JSON file
def load_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

# Load configuration
config = load_config('config/config.json')

# Extract the FRED API key from the configuration
fred_api_key = config['fred_API_KEY']

# Function to fetch the current Federal Reserve interest rate
def fetch_fed_interest_rate(api_key):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id=FEDFUNDS&api_key={api_key}&file_type=json"
    response = requests.get(url)
    data = response.json()
    if 'observations' not in data:
        print("Error: 'observations' key not found in the response data")
        print(data)
        return None
    latest_observation = data['observations'][-1]
    return float(latest_observation['value']) / 100  # Convert to decimal

# Fetch the current Federal Reserve interest rate
current_fed_rate = fetch_fed_interest_rate(fred_api_key)
if current_fed_rate is None:
    raise ValueError("Failed to fetch the current Federal Reserve interest rate")

# Define potential reductions in the interest rate
rate_reductions = [0.25, 0.5, 0.75, 1.0]  # Reductions in percentage points

# Define the investment period (e.g., 1 year)
investment_period_days = 365

# Define the amount of money to invest
initial_investment = 9017.58  # $10,000

# Define the end date as today and the start date as one year ago
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=investment_period_days)).strftime('%Y-%m-%d')

# Fetch historical Bitcoin price data
btc_data = yf.download('BTC-USD', start=start_date, end=end_date)

# Calculate the returns from Bitcoin
btc_start_price = btc_data['Close'].iloc[0]
btc_end_price = btc_data['Close'].iloc[-1]
btc_return = (btc_end_price - btc_start_price) / btc_start_price

# Calculate the returns from the HYSA for different interest rate scenarios
hysa_returns = [current_fed_rate - reduction for reduction in rate_reductions]

# Calculate the final amounts for Bitcoin and HYSA
final_amount_btc = initial_investment * (1 + btc_return)
final_amount_hysa = initial_investment * (1 + current_fed_rate)
final_amounts_hysa_reductions = [initial_investment * (1 + hysa_return) for hysa_return in hysa_returns]

# Print the results
print(f"Initial Investment: ${initial_investment}")
print(f"Bitcoin Return: {btc_return * 100:.2f}%")
print(f"Final Amount if Invested in Bitcoin: ${final_amount_btc:.2f}")
print(f"Final Amount if Kept in HYSA: ${final_amount_hysa:.2f}")
for reduction, final_amount_hysa_reduction in zip(rate_reductions, final_amounts_hysa_reductions):
    print(f"HYSA Return with {reduction}% reduction: ${final_amount_hysa_reduction:.2f}")

# Plot the results
# Plot 1: Comparison with different interest rate reductions
labels_reductions = ['Bitcoin'] + [f'HYSA -{reduction}%' for reduction in rate_reductions]
final_amounts_reductions = [final_amount_btc] + final_amounts_hysa_reductions

plt.figure(figsize=(12, 8))
plt.bar(labels_reductions, final_amounts_reductions, color=['orange'] + ['blue'] * len(rate_reductions))
plt.xlabel('Investment Option')
plt.ylabel('Final Amount ($)')
plt.title('Comparison of Investment in Bitcoin vs. HYSA with Different Interest Rate Reductions')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Plot 2: Comparison without interest rate reductions
labels = ['Bitcoin', 'HYSA']
final_amounts = [final_amount_btc, final_amount_hysa]

plt.figure(figsize=(12, 8))
plt.bar(labels, final_amounts, color=['orange', 'blue'])
plt.xlabel('Investment Option')
plt.ylabel('Final Amount ($)')
plt.title('Comparison of Investment in Bitcoin vs. HYSA')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
```

So, this code produces the following plot:

![bitcoin_vs_hysa](/images/imgforblogposts/post_37/general_bitcoin_vs_hysa.png)

The output to the console is as follows:

![bitcoin_vs_hysa_console_output](/images/imgforblogposts/post_37/console_output_hysa_v_bitcoin.png)

Now, as everyone likes to note, crypto can be extremely volatile, so let's see if we can incorporate that into our calculations, using the ["Sharpe Ratio"](https://www.investing.com/academy/analysis/sharpe-ratio-definition/?utm_source=google&utm_medium=cpc&utm_campaign=21962679734&utm_content=723521203853&utm_term=dsa-1651811503903_&GL_Ad_ID=723521203853&GL_Campaign_ID=21962679734&ISP=1&gad_source=1&gbraid=0AAAAABIq5T6BdsHmRDmyaLYRD3_CimZ5F&gclid=CjwKCAiAjeW6BhBAEiwAdKltMtlJokJsEFbWAPpqUNC80912n2VY3zUTfRCi7N-bHtwiZXlAYY5teRoChbgQAvD_BwE), which is often used to measure volatility. If we add this we get the following console output:

![bitcoin_vs_hysa_including_sharpe](/images/imgforblogposts/post_37/outputs_with_sharpe_ratio.png)

Finally, we could have a look at things based on different reductions by the FED of the interest rate:

![different_FED_interest_rate_reductions](/images/imgforblogposts/post_37/bitcoin_vs_different_fed_rate_reductions.png)

Obviously, there is much to consider here:

1. Volatility: Bitcoin is clearly quite volatile---as the Sharpe ratio is high. 
2. Risk: If we have a high risk tolerance, then Bitcoin is fine; if we are more conservative, then HYSAs are probably the way to go.
3. If we want to go long-term and are okay with the short-term volatility, then we move our monies to Bitcoin; if we want more stable and predictable outcomes, then we keep everything in our HYSA.

Anyways---we'll watch the markets, obviously, and much more to come, as promised, as always.

P.S. For those that want a bit more data---how about a plot of the value of a dollar over time compared to some popular cryptocurrencies?

![value_of_a_dollar](/images/imgforblogposts/post_37/value_of_a_dollar_over_time.png)