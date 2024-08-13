# Step 1: Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Step 2: Fetch historical data for Silver (symbol: 'SI=F')
silver_data = yf.download('SI=F', start='2018-01-01', end='2024-08-25')

# Step 3: Process the data
# Display the first few rows of the data
print(silver_data.head())

# Step 4: Visualize the data
plt.figure(figsize=(14, 7))
plt.plot(silver_data['Close'], label='Silver Price')
plt.title('Silver Price Over the Last Five Years')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)

# Save the plot to the specified directory
plt.savefig('/Users/spicy.kev/Documents/github/kspicer80.github.io/static/images/imgforblogposts/post_35/')

# Show the plot
plt.show()
