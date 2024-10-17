
import requests
import csv
import io
from datetime import datetime
import pandas as pd

# Replace with your FRED API key
FRED_API_KEY = 'c1d61afe873caa4129d952e24f6ea33a'
FRED_BASE_URL = 'https://api.stlouisfed.org/fred/series/observations'

def get_m2_data(start_date='2020-01-01', end_date='2023-07-01'):
    # Build the API request URL
    params = {
        'series_id': 'M2SL',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'observation_start': start_date,
        'observation_end': end_date
    }
    response = requests.get(FRED_BASE_URL, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract the data
        dates = [obs['date'] for obs in data['observations']]
        values = [float(obs['value']) for obs in data['observations']]
        
        # Create a DataFrame
        df = pd.DataFrame({
            'date': pd.to_datetime(dates),
            'M2': values
        })
        df.set_index('date', inplace=True)
        
        # Resample the data to a daily frequency and interpolate
        df_daily = df.resample('D').interpolate(method='linear')

        df_daily.to_csv("data/m2_to_btc/m2_data.csv")

    else:
        print(f"Failed to fetch data from FRED API. Status code: {response.status_code}")

    

    return df_daily

def get_historical_btc_price(interval='1d', filename='data/m2_to_btc/btc_price_binance.csv'):
    url = 'https://api.binance.com/api/v3/klines'
    interval = '1d'
    filename = 'data/m2_to_btc/btc_price_binance.csv'
    
    params = {
        'symbol': 'BTCUSDT',
        'interval': interval,
        'limit': 1000
    }
    response = requests.get(url, params=params)
    data = response.json()
    header = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 
                'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']

    df = pd.DataFrame(data, columns=header)
    
    # Convert timestamps to readable dates in YYYY-MM-DD format
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms').dt.strftime('%Y-%m-%d')
    df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms').dt.strftime('%Y-%m-%d')
    
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

    
if __name__ == "__main__":
    get_m2_data()
    get_historical_btc_price()
