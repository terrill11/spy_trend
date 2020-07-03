#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
from datetime import timedelta
import os
import numpy as np
import pandas as pd
import pyodbc
import json
import time

# server connection setup
with open('/Users/terrill/Documents/work/stuff/spy_trend/sql_server_info_forex.txt', 'r') as f:
    line = f.readline().split(',')

server_name = line[0]
server_port = line[1]
database_name = line[2]
username = line[3]
password = line[4]

conn = pyodbc.connect('Driver={FreeTDS};'
                      f'Server={server_name};'
                      f'Port={server_port};'
                      f'Database={database_name};'
                      f'UID={username};'
                      f'PWD={password}')
cursor = conn.cursor()


# data scraping
urlheader = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}
with open('/Users/terrill/OneDrive/Documents/work/projects/spy/scripts/database/forex/currency_ids.json') as f:
    ticker_list = json.load(f)


start_date = '01/01/2005'
end_date = (dt.now().date() - timedelta(days = 1)).strftime('%m/%d/%Y')

print('Running insert now.')
for ticker in ticker_list:
    print(f'Working on {ticker}')

    new_ticker = ticker.replace('-','/')
    table_ticker = ticker.replace('-','_')

    url = 'https://www.investing.com/instruments/HistoricalDataAjax'
    payload = {'header': f'{new_ticker}+Historical+Data',
                'st_date': start_date,
                'end_date': end_date,
                'sort_col': 'date',
                'action': 'historical_data',
                'smlID': ticker_list[ticker]['smlID'],
                'sort_ord': 'DESC',
                'interval_sec': 'Daily',
                'curr_id': ticker_list[ticker]['curr_id']
                }
    req = requests.post(url, headers=urlheader, data=payload)
    soup = BeautifulSoup(req.content, "lxml")

    table = soup.find('table', id="curr_table")
    split_rows = table.find_all("tr")

    data_rows = split_rows[:0:-1]

    #columns = ['Date', 'Price', 'Open', 'High', 'Low', 'Change %']
    for row in data_rows:
        columns = list(row.stripped_strings)
        columns = [column.replace(',','') for column in columns]

        date = str(dt.strptime(columns[0], '%b %d %Y').strftime('%Y-%m-%d'))
        close_price = float(columns[1])
        open_price = float(columns[2])
        high_price = float(columns[3])
        low_price = float(columns[4])

        query = f'''INSERT Forex.dbo.{table_ticker} (Date, ClosePrice, OpenPrice, HighPrice, LowPrice)
                    VALUES (?,?,?,?,?)'''
        cursor.execute(query, (date, close_price, open_price, high_price, low_price))
    conn.commit()

    print(f'{ticker} saved')
    time.sleep(10)

conn.close()