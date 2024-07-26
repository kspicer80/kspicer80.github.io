# generate_plot.py
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Fetch historical data for Silver (symbol: 'SI=F')
silver_data = yf.download('SI=F', start='2018-01-01', end=pd.Timestamp.today().strftime('%Y-%m-%d'))

# Process the data
print(silver_data.head())

# Visualize the data
plt.figure(figsize=(14, 7))
plt.plot(silver_data['Close'], label='Silver Price')
plt.title('Silver Price Over the Last Five Years')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.savefig('static/imgforblogposts/post35/silver_price_plot.png')
