import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


btc_df = pd.read_csv('data/m2_to_btc/btc_price_binance.csv')

fear_greed_df = pd.read_csv('data/fear_greed/fear_greed_index.csv')

# btc_df.rename(columns={'Close':'BTC Price','Open Time':'Date'}, inplace=True)

merged_df = pd.merge(fear_greed_df,btc_df,left_on='timestamp',right_on='Open Time',how='left')

merged_df.to_csv('data/fear_greed/merged_fear_greed_to_btc.csv', index=False)

# Plot BTC Price on the primary y-axis
fig, ax1 = plt.subplots(figsize=(14, 7))
ax1.set_xlabel('DateTime')
ax1.set_ylabel('Price', color='tab:blue')
ax1.plot(merged_df['Open Time'], merged_df['Close'], color='tab:blue', label='Price')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Create a secondary y-axis for the Open Interest
ax2 = ax1.twinx()
ax2.set_ylabel('Fear Greed Index', color='tab:orange')
ax2.plot(merged_df['Open Time'], merged_df['value'], color='tab:orange', label='Fear Greed Index')
ax2.tick_params(axis='y', labelcolor='tab:orange')

# Format the x-axis to show fewer date ticks
ax1.xaxis.set_major_locator(ticker.MaxNLocator(10))  # Limit the number of ticks to 10
# Title and legends

plt.title('Fear Greed Index and BTC Price Over Time')
fig.tight_layout()  # Adjust layout to make room for the labels
plt.show()