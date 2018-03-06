# ZEN Address Tracker

This tool was designed for the ZEN miner who wants to keep track of incoming transactions for tax purposes.

Feel free to use this in your own projects! I just developed this as a little hobby project. May or may not be maintained.

If you find this tool to be useful, please consider buying me a beer (or help me not drown in my student loan payments) by donating here:


ZEN: znacPknwMcgmNfgoq1h1BMXRH6vxgHqsCBj

LTC: LXwXzt1yTGeQRVsQFKxgb5Ln5s7N5JuiKW

# Requirements
Developed using Python 3.6.2. Use pip to install missing modules.

1. Module: requests
2. Module: tzlocal

# Usage
Example: python zen_tracker.py "zen address"

1. Finds all transactions using the Insight API on explorer.zensystem.io.
2. Reads all receive transactions.
3. Reads all spent transactions.
4. Reads coin data by date using the Bittrex API.
5. Sorts all the data.
6. Writes out a CSV file using the ZEN address as the name.

# CSV Format
Current CSV data in order:
1. Date
2. Value
3. Fee
4. After Fee
5. BTC-ZEN
6. USDT-BTC ($)
7. USDT-ZEN ($)
8. Received ($)
9. Sent ($)
10. Fees ($)
11. After Fee ($)
