import requests
import pandas as pd

API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'
symbol = 'AAPL'
function = 'TIME_SERIES_DAILY'
url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={API_KEY}'

response = requests.get(url)
data = response.json()

# Convert to DataFrame
df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
df = df.astype(float)
df.index = pd.to_datetime(df.index)

# Save to CSV
df.to_ ('AAPL_daily. ')
