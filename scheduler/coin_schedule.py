import schedule
import time
import os
from datetime import datetime

# List of Python scripts to run
scripts_to_run = [
    "function/m2_to_btc/Request.py",
    "function/category/request.py",
    "function/funding/Request.py",
    "function/fear_greed_index/Request.py",
    "function/open_interest/Request.py",
    "function/altcoin/momentum.py",
    "function/funding/Chart_display.py",
    "function/fear_greed_index/Chart_display.py",
    "function/open_interest/Open_interest_to_price_chart.py",
    "function/open_interest/oi_value_to_price_chart.py"
    ]

def run_scripts():
    """
    Function to run each script in the list.
    """
    for script in scripts_to_run:
        try:
            print(f"Running {script} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            os.system(f"cd /Users/tungle/Desktop/Data/Crypto\ dashboard ; /usr/bin/env /Users/tungle/opt/anaconda3/bin/python {script}")  # Executes the Python script
        except Exception as e:
            print(f"Failed to run {script}: {e}")

# Schedule the scripts to run every day at 9 AM
schedule.every().day.at("09:00").do(run_scripts)
run_scripts()
print("Scheduler is running...")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(4320)  # Check every minute
