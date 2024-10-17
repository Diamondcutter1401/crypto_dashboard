import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

def chart_display():
    coin = input("Please enter coin pair: ")

    df = pd.read_csv(f"data/momentum/{coin}_momentum.csv")

    # Plot BTC Price on the primary y-axis
    fig, ax1 = plt.subplots(figsize=(14, 7))
    ax1.set_xlabel('DateTime')
    ax1.set_ylabel('Price (USD)', color='tab:blue')
    ax1.plot(df['DateTime'], df['Price'], color='tab:blue', label='Price')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Create a secondary y-axis for the Open Interest
    ax2 = ax1.twinx()
    ax2.set_ylabel('Open Interest', color='tab:orange')
    ax2.plot(df['DateTime'], df['Open Interest'], color='tab:orange', label='Open Interest')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Format the x-axis to show fewer date ticks
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(10))  # Limit the number of ticks to 10
    # Title and legends

    plt.title(f'Open Interest and {coin} Price Over Time')
    fig.tight_layout()  # Adjust layout to make room for the labels
    plt.show()

    response = input("Wanna see other charts ?")
    if response == "y" or response == " y":
        chart_display()
    else :
        pass

chart_display()