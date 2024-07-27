import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime

end_date = datetime.today().strftime('%Y-%m-%d')
silver_data = yf.download('SI=F', start='2018-01-01', end=end_date)

plt.figure(figsize=(14, 7))
plt.plot(silver_data['Close'], label='Silver Price')
plt.title('Silver Price Over the Last Five Years')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.savefig('static/images/imgforblogposts/post_35/silver_price_plot.png')
plt.show()