import requests
import pandas as pd
from datetime import datetime

def get_historical_fear_and_greed_index(limit=700):
    """
    Fetches historical Fear and Greed Index data from the Alternative.me API.

    :param limit: The number of historical data points to fetch. The maximum is 100.
    """
    url = f'https://api.alternative.me/fng/?limit={limit}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data["data"]
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def save_to_csv(fng_data, filename='data/fear_greed/fear_greed_index.csv'):
    """
    Saves the Fear and Greed Index data to a CSV file.
    """
    if fng_data:
        # Convert the timestamp to a readable date format and create a DataFrame
        for entry in fng_data:
            entry['timestamp'] = datetime.fromtimestamp(int(entry['timestamp'])).strftime('%Y-%m-%d')
        
        df = pd.DataFrame(fng_data)
        df = df.iloc[::-1] 
        # Save the DataFrame to a CSV file
        df.to_csv(filename, index=False)

        print(f"Historical Fear and Greed Index data saved to {filename}")
    else:
        print("No data to save.")

if __name__ == "__main__":
    # Fetch the historical Fear and Greed Index data (set limit for how many days of data)
    fng_data = get_historical_fear_and_greed_index(limit=700)  # Fetch data for the past 365 days
    
    if fng_data:
        # Save the data to a CSV file
        save_to_csv(fng_data)
    else:
        print("Could not retrieve historical Fear and Greed Index data.")
