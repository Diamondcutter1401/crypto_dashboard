import pandas as pd
import matplotlib.pyplot as plt

def plot_funding_rate_and_btc_price_from_csv(csv_file):
    # Read the merged data from the CSV file
    merged_df = pd.read_csv(csv_file)

    # Convert DateTime to datetime format if it's not already
    merged_df['DateTime'] = pd.to_datetime(merged_df['DateTime'], format='%Y-%m-%d-%H')

    # Plot BTC Price on the primary y-axis
    fig, ax1 = plt.subplots(figsize=(14, 7))
    ax1.set_xlabel('DateTime')
    ax1.set_ylabel('Price', color='tab:blue')
    ax1.plot(merged_df['DateTime'], merged_df['Price'], color='tab:blue', label='Price')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Create a secondary y-axis for the Funding Rate
    ax2 = ax1.twinx()
    ax2.set_ylabel('Funding Rate', color='tab:orange')
    ax2.plot(merged_df['DateTime'], merged_df['Funding Rate'], color='tab:orange', label='Funding Rate')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Title and legends
    plt.title('Funding Rate and BTC Price Over Time')
    fig.tight_layout()  # Adjust layout to make room for the labels
    plt.show()

if __name__ == "__main__":
    # Specify the path to your merged CSV file
    csv_file = 'data/funding/merged_funding_rate_BTCUSDT_price.csv'
    
    # Plot the data from the CSV file
    plot_funding_rate_and_btc_price_from_csv(csv_file)
