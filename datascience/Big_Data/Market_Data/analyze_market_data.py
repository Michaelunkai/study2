import pandas as pd
import matplotlib.pyplot as plt

# Load Data
df = pd.read_csv('AAPL_daily.csv', index_col=0, parse_dates=True)

# Plot Closing Price
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['4. close'], label='Closing Price')
plt.title('AAPL Closing Price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
