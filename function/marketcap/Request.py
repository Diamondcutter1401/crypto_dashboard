import requests
import csv
import datetime

# Define the API URL
url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
params = {
    'vs_currency': 'usd',
    'days': '365',  # 1 year
}

# Send request to CoinGecko API
response = requests.get(url, params=params)
data = response.json()

# Extract market cap data
market_caps = data['market_caps']

# Define the file path for saving the CSV
file_path = 'btc_market_cap_past_year.csv'

# Write the data to a CSV file
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Date', 'Market Cap (USD)'])
    
    # Write market cap data
    for item in market_caps:
        timestamp = datetime.datetime.fromtimestamp(item[0] / 1000)  # convert to human-readable time
        market_cap = item[1]
        writer.writerow([timestamp, market_cap])

print(f'Market cap data saved to {file_path}')
