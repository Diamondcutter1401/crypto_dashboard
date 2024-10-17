import pandas as pd
import os 

# Get the historical data for a specific coin
symbol_list = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","FTMUSDT","SUIUSDT","INJUSDT","ATOMUSDT","TONUSDT",
          "AVAXUSDT","SEIUSDT","NEARUSDT","ARBUSDT","OPUDST","STRKUSDT","AAVEUSDT","ALTUSDT","ETHFIUSDT",
          "PENDLEUSDT","FETUSDT","TAOUSDT","TIAUSDT","DOGEUSDT","SHIBAUSDT","PEPEUSDT","PIXELUSDT",
          "AXSUSDT","IMXUSDT","LDOUSDT","SSVUSDT","UNIUSDT","LINKUSDT","ENAUSDT","WUSDT","CPOOLUSDT" ,
          "WLDUSDT","PHBUSDT","ARKMUSDT","BANANAUSDT","DYMUSDT","DOGEUSDT","SHIBUSDT","PEPEUSDT","MAVUSDT"]

for symbol in symbol_list:
    try:
        volume_df = pd.read_csv(f"data/price/{symbol}_price.csv",index_col=0)
        volume_df['DateTime'] = volume_df['DateTime'].str.slice(0, 10)
        try:
            open_interest_df = pd.read_csv(f"data/open_interest/{symbol}_open_interest_binance.csv",index_col=0)

            merged_df = pd.merge(volume_df, open_interest_df, left_on='DateTime', right_on='Date', how='right')
            merged_df = merged_df.drop_duplicates()
            def select_every_third_row(group):
                return group.iloc[1::3]  # Select rows at index 1, 3, 5 within each group

            # Apply the function to each group based on 'DateTime'
            merged_df = merged_df.groupby('DateTime').apply(select_every_third_row).reset_index(drop=True)
            merged_df.to_csv(f'data/momentum/{symbol}_momentum.csv', index=False)

            print(f'saved {symbol}_open_momentum.csv')
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
data_directory = "data/momentum"

# Initialize an empty DataFrame to store the results
result_df = pd.DataFrame()

# Loop through each file in the directory
for filename in os.listdir(data_directory):
    if filename.endswith(".csv"):  # Assuming the files are CSVs
        file_path = os.path.join(data_directory, filename)

        # Read the coin data
        df = pd.read_csv(file_path)

        # Sort by 'DateTime' to ensure we're getting the latest date
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df = df.sort_values(by='DateTime')

        # Get the latest date (t) and the previous date (t-1)
        latest_row = df.iloc[-1]  # Last row (t)
        previous_row = df.iloc[-2]  # Second last row (t-1)

        # Calculate percentage changes
        price_change = ((latest_row['Price'] - previous_row['Price']) / previous_row['Price']) * 100
        volume_change = ((latest_row['Volume'] - previous_row['Volume']) / previous_row['Volume']) * 100
        oi_change = ((latest_row['Open Interest'] - previous_row['Open Interest']) / previous_row['Open Interest']) * 100
        oi_value_change = ((latest_row['Open Interest Value'] - previous_row['Open Interest Value']) / previous_row['Open Interest Value']) * 100

        # Create a DataFrame row with the data from the latest date and the percentage changes
        result_row = pd.DataFrame({
            'Coin': [filename.replace('.csv', '')],  # Extract the coin name from the file name
            'DateTime': [latest_row['DateTime']],
            'Price': [latest_row['Price']],
            'Volume': [latest_row['Volume']],
            'Open Interest': [latest_row['Open Interest']],
            'Open Interest Value': [latest_row['Open Interest Value']],
            'Price Change (%)': [price_change],
            'Volume Change (%)': [volume_change],
            'OI Change (%)': [oi_change],
            'OI Value Change (%)': [oi_value_change]
        })

        # Concatenate the result_row to result_df
        result_df = pd.concat([result_df, result_row], ignore_index=True)

# Optionally, save the result to a CSV file
result_df.to_excel('data/momentum/1.Momentum_summary.xlsx', index=False)