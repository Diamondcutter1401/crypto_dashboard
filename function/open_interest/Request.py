import requests
import pandas as pd
from datetime import datetime

def fetch_open_interest(symbol, period='1d', limit=500):
    url = 'https://fapi.binance.com/futures/data/openInterestHist'
    params = {
        'symbol': symbol,
        'period': period,  # '1d' for daily open interest data
        'limit': limit     # Maximum limit is 500
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Process the data and convert timestamps to readable format
        open_interest_data = []
        for entry in data:
            open_time = datetime.fromtimestamp(entry['timestamp'] / 1000).strftime('%Y-%m-%d')
            open_interest_info = {
                'Date': open_time,
                'Open Interest': entry['sumOpenInterest'],
                'Open Interest Value': entry['sumOpenInterestValue']
            }
            open_interest_data.append(open_interest_info)
        
        return pd.DataFrame(open_interest_data)
    else:
        print(f"Failed to fetch data. HTTP Status code: {response.status_code}")
        return pd.DataFrame()

def save_open_interest_to_csv(df, symbol):
    filename = f'data/open_interest/{symbol}_open_interest_binance.csv'
    df.to_csv(filename, index=False)
    print(f"Open interest data saved to {filename}")

SYMBOL = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","FTMUSDT","SUIUSDT","INJUSDT","ATOMUSDT","TONUSDT",
          "AVAXUSDT","SEIUSDT","NEARUSDT","ARBUSDT","OPUDST","STRKUSDT","AAVEUSDT","ALTUSDT","ETHFIUSDT",
          "PENDLEUSDT","FETUSDT","TAOUSDT","TIAUSDT","DOGEUSDT","SHIBAUSDT","PEPEUSDT","PIXELUSDT",
          "AXSUSDT","IMXUSDT","LDOUSDT","SSVUSDT","UNIUSDT","LINKUSDT","ENAUSDT","WUSDT","CPOOLUSDT" ,
          "WLDUSDT","PHBUSDT","ARKMUSDT","BANANAUSDT","DYMUSDT","DOGEUSDT","SHIBUSDT","PEPEUSDT","MAVUSDT"]

if __name__ == "__main__":
    # Fetch the open interest data
    for symbol in SYMBOL:
        open_interest_df = fetch_open_interest(symbol)
        if not open_interest_df.empty:
            # Save the data to a CSV file
            save_open_interest_to_csv(open_interest_df,symbol)
        else:
            print(f"No open interest data was fetched for {symbol}.")
