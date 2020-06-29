#!/Users/terrill/Documents/work/python_virtual_environments/web_scraping/bin/python

import requests
from bs4 import BeautifulSoup
import os
import numpy as np
import pandas as pd
import json
import time

# BTC scrape https://www.investing.com/crypto/bitcoin/btc-usd-historical-data
# ETH scrape https://www.investing.com/crypto/ethereum/eth-usd-historical-data

urlheader = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

with open('currency_ids.json') as f:
  ticker_list = json.load(f)

start_date = '01/01/2005'
end_date = '06/19/2020'

for ticker in ticker_list:
  print(f'Working on {ticker}')

  newticker = ticker.replace('-','/')

  url = 'https://www.investing.com/instruments/HistoricalDataAjax'
  payload = {'header': f'{newticker}+Historical+Data',
              'st_date': start_date,
              'end_date': end_date,
              'sort_col': 'date',
              'action': 'historical_data',
              'smlID': ticker_list[ticker]['smlID'],
              'sort_ord': 'DESC',
              'interval_sec': 'Daily',
              'curr_id': ticker_list[ticker]['curr_id']}
  req = requests.post(url, headers=urlheader, data=payload)
  soup = BeautifulSoup(req.content, "lxml")

  table = soup.find('table', id="curr_table")
  split_rows = table.find_all("tr")

  header_list = split_rows[0:1]
  split_rows_rev = split_rows[:0:-1]

  with open(f'results/{ticker}.csv', 'w') as output_file:
    for row in header_list:
        columns = list(row.stripped_strings)
        columns = [column.replace(',','') for column in columns]
        output_file.write(f'{columns[0]}, {columns[2]}, {columns[3]}, {columns[4]}, Close\n')

    for row in split_rows_rev:
        columns = list(row.stripped_strings)
        columns = [column.replace(',','') for column in columns]
        output_file.write(f'{columns[0]}, {columns[2]}, {columns[3]}, {columns[4]}, {columns[1]}\n')

  time.sleep(10)

  print(f'{ticker} saved')

# for some reason headers are saved with white space and cannot be removed above so we'll do it here
for f in ticker_list:
  df = pd.read_csv(f'/Users/terrill/OneDrive/Documents/work/projects/spy/final_dfs/forex/{f}.csv')
  df.columns = [i.strip(' ') for i in df.columns]
  df.set_index('Date', inplace=True)
  df.to_csv(f'/Users/terrill/OneDrive/Documents/work/projects/spy/final_dfs/forex/{f}.csv')

print('Cleaning done!')