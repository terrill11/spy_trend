#!/Users/terrill/Documents/work/python_virtual_environments/web_scraping/bin/python

import requests
from bs4 import BeautifulSoup
import os
import numpy as np

# BTC scrape https://www.investing.com/crypto/bitcoin/btc-usd-historical-data
# ETH scrape https://www.investing.com/crypto/ethereum/eth-usd-historical-data

urlheader = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

# ticker_list = ['USD/JPY', 'USD/EUR', 'USD/CHF', 'USD/PLN', 'USD/CNY', 'USD/HUF', 'USD/RUB', 'USD/CAD',
#                 'USD/RON', 'USD/INR', 'USD/GBP', 'USD/AUD', 'USD/HKD', 'USD/SEK', 'USD/SGD', 'XAU/USD']

# for ticker in ticker_list:
#     print(f'Working on {ticker}')

ticker = 'USD/HUF'

newticker = ticker.replace('/','-')

url = 'https://www.investing.com/instruments/HistoricalDataAjax'
payload = {'header': f'{ticker}+Historical+Data',
            'st_date': '06/01/2020',
            'end_date': '06/19/2020',
            'sort_col': 'date',
            'action': 'historical_data',
            'smlID': '106684',
            'sort_ord': 'DESC',
            'interval_sec': 'Daily',
            'curr_id': '91'}
req = requests.post(url, headers=urlheader, data=payload)
soup = BeautifulSoup(req.content, "lxml")

table = soup.find('table', id="curr_table")
split_rows = table.find_all("tr")

output_filename = f'/Users/terrill/OneDrive/Documents/work/projects/spy/apis/investing.com/results/{newticker}.csv'
os.makedirs(os.path.dirname(output_filename), exist_ok=True)
output_file = open(output_filename, 'w')
header_list = split_rows[0:1]
split_rows_rev = split_rows[:0:-1]


for row in header_list:
    columns = list(row.stripped_strings)
    columns = [column.replace(',','') for column in columns]
    output_file.write(f'{columns[0]}, {columns[2]}, {columns[3]}, {columns[4]}, Close\n')

for row in split_rows_rev:
    columns = list(row.stripped_strings)
    columns = [column.replace(',','') for column in columns]
    output_file.write(f'{columns[0]}, {columns[2]}, {columns[3]}, {columns[4]}, {columns[1]}\n')

output_file.close()

print(f'{ticker} saved')