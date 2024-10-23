import requests
import csv
import datetime


def get_marketcap(symbol_coingecko,symbol_global):
    # Define the API URL
    url = f'https://api.coingecko.com/api/v3/coins/{symbol_coingecko}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': '365',  # 1 year
    }

    # Send request to CoinGecko API
    response = requests.get(url, params=params)
    print(response.status_code)
    print(response.text)
    data = response.json()

    # Extract market cap data
    market_caps = data['market_caps']

    # Define the file path for saving the CSV
    file_path = f'data/marketcap/{symbol_global}_marketcap.csv'

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

SYMBOL = {"BTCUSDT":"bitcoin","ETHUSDT":"ethereum","BNBUSDT":"binancecoin","SOLUSDT":"solana",
          "FTMUSDT":"fantom","SUIUSDT":"sui","INJUSDT":"injective-protocol","ATOMUSDT":"cosmos","TONUSDT":"the-open-network",
          "AVAXUSDT":"avalanche-2","SEIUSDT":"sei-network","NEARUSDT":"near","ARBUSDT":"arbitrum","OPUDST":"optimism",
          "STRKUSDT":"starknet","AAVEUSDT":"aave","ALTUSDT":"altlayer","ETHFIUSDT":"ether-fi",
          "PENDLEUSDT":"pendle","FETUSDT":"fetch-ai","TAOUSDT":"bittensor","TIAUSDT":"celestia","DOGEUSDT":"dogecoin",
          "SHIBAUSDT":"shiba-inu","PEPEUSDT":"pepe","PIXELUSDT":"pixels",
          "AXSUSDT":"axie-infinity","IMXUSDT":"immutable-x","LDOUSDT":"lido-dao","SSVUSDT":"ssv-network",
          "UNIUSDT":"uniswap","LINKUSDT":"chainlink","ENAUSDT":"ethena","WUSDT":"wormhole","CPOOLUSDT":"clearpool" ,
          "WLDUSDT":"worldcoin-wld","PHBUSDT":"phoenix-global","ARKMUSDT":"arkham","BANANAUSDT":"banana-gun",
          "DYMUSDT":"dymension","DOGEUSDT":"dogecoin","SHIBUSDT":"shiba-inu","MAVUSDT":"maverick-protocol"}

for symbol in SYMBOL:
    marketcap = get_marketcap(SYMBOL[symbol],symbol)
    if marketcap is None :
        print (f'No marketcap data was fetch for {symbol}')
    else:
        print (f'data was saved to data/marketcap/{symbol}_marketcap.csv')