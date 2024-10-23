import requests
import pandas as pd
from datetime import datetime, timedelta
import time

def adjust_hour(hour):
    """Adjust the hour according to the specified rules."""
    if hour < 8:
        return '00'
    elif hour < 16:
        return '08'
    else:
        return '16'

def fetch_funding_rate(symbol, limit=10000):
    url = 'https://fapi.binance.com/fapi/v1/fundingRate'
    
    all_data = []
    fetch_limit = 1000
    
    while limit > 0:
        params = {
            'symbol': symbol,
            'limit': min(fetch_limit, limit),
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if not data:
                break
            
            for entry in data:
                funding_time = datetime.utcfromtimestamp(entry['fundingTime'] / 1000)
                adjusted_hour = adjust_hour(funding_time.hour)
                funding_time_str = funding_time.strftime(f'%Y-%m-%d-{adjusted_hour}')
                funding_info = {
                    'DateTime': funding_time_str,
                    'Funding Rate': entry['fundingRate']
                }
                all_data.append(funding_info)
                
            limit -= fetch_limit
        else:
            print(f"Failed to fetch data. HTTP Status code: {response.status_code}")
            break
    
    return pd.DataFrame(all_data)

def fetch_coin_price(symbol, max_retries=5):
    url = 'https://api.binance.com/api/v3/klines'
    
    params = {
        'symbol': symbol,
        'interval': '8h',
        'limit': 1000
    }

    btc_prices = []
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            for entry in data:
                price_time = datetime.fromtimestamp(entry[0] / 1000)
                adjusted_hour = adjust_hour(price_time.hour)
                price_time_str = price_time.strftime(f'%Y-%m-%d-{adjusted_hour}')
                btc_info = {
                    'DateTime': price_time_str,
                    'Price': float(entry[4]),
                    'Volume': float(entry[7])  # Closing price
                }
                btc_prices.append(btc_info)
            return pd.DataFrame(btc_prices)
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
                time.sleep(5)  # Wait before retrying
            else:
                print("Max retries exceeded. Exiting.")
                return pd.DataFrame()

def main():
    # Fetch Funding Rates up to the current date
    for symbol in SYMBOL:
        funding_df = fetch_funding_rate(symbol)
        funding_df.to_csv(f'data/funding/{symbol}_funding_rate.csv')

        if not funding_df.empty:
            
            # Fetch Prices        
            price_df = fetch_coin_price(symbol)
            price_df.to_csv(f'data/price/{symbol}_price.csv')
            
            if not price_df.empty:
                # Merge the DataFrames
                merged_df = pd.merge(funding_df, price_df, on='DateTime', how='left')
                
                # Save to CSV
                merged_df.to_csv(f'data/funding/merged_funding_rate_{symbol}_price.csv', index=False)
                print(f"Merged data saved to 'merged_funding_rate_{symbol}_price.csv'.")
            else:
                print(f"No {symbol} price data was fetched.")
        else:
            print(f"No {symbol} funding rate data was fetched.")

SYMBOL = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","FTMUSDT","SUIUSDT","INJUSDT","ATOMUSDT","TONUSDT",
          "AVAXUSDT","SEIUSDT","NEARUSDT","ARBUSDT","OPUDST","STRKUSDT","AAVEUSDT","ALTUSDT","ETHFIUSDT",
          "PENDLEUSDT","FETUSDT","TAOUSDT","TIAUSDT","DOGEUSDT","SHIBAUSDT","PEPEUSDT","PIXELUSDT",
          "AXSUSDT","IMXUSDT","LDOUSDT","SSVUSDT","UNIUSDT","LINKUSDT","ENAUSDT","WUSDT","CPOOLUSDT" ,
          "WLDUSDT","PHBUSDT","ARKMUSDT","BANANAUSDT","DYMUSDT","DOGEUSDT","SHIBUSDT","PEPEUSDT","MAVUSDT"]

if __name__ == "__main__":
    main()
