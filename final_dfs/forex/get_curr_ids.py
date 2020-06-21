#!/Users/terrill/Documents/work/python_virtual_environments/web_scraping/bin/python

import requests
from bs4 import BeautifulSoup
import os
import numpy as np
import json

urlheader = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

ticker_list = ['USD-JPY', 'USD-EUR', 'USD-CHF', 'USD-PLN', 'USD-CNY', 'USD-HUF', 'USD-RUB', 'USD-CAD',
                'USD-RON', 'USD-INR', 'USD-GBP', 'USD-AUD', 'USD-HKD', 'USD-SEK', 'USD-SGD', 'XAU-USD']

ticker_ids = {}

for ticker in ticker_list:
  newticker = ticker.lower()

  url = f'https://www.investing.com/currencies/{newticker}-historical-data'
  req = requests.get(url, headers=urlheader)
  soup = BeautifulSoup(req.content, "lxml")

  curr_id = soup.select_one('div[data-pair-id]')['data-pair-id']

  all_scripts = soup.find_all("script")
  site_data = str(all_scripts[33])
  start = site_data.find('window.siteData.smlID')
  end = site_data.find(';', start)
  smlID = site_data[start:end].split('=')[1].strip(' ')

  ticker_ids[ticker] = {'curr_id': curr_id, 'smlID': smlID}


with open('currency_ids.json', 'w') as f:
  json.dump(ticker_ids, f)
  print('Currency IDs successfully saved')

# print(ticker_ids)




#data-pair-id
#window.siteData.smlID