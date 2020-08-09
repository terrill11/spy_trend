#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import json
import requests
import pandas as pd
import pyodbc
import time

class InvestingScraper():
    def __init__(self):
        self.urlheader = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"
            }

    def get_ticker_list(self, name):
        with open(f'/Users/terrill/OneDrive/Documents/work/projects/spy/scripts/{name}/ticker_ids.json') as f:
            ticker_list = json.load(f)
            
        return ticker_list

    def __get_data(self, ticker, start, end, smlID, curr_id):
        new_ticker = ticker.replace('-','/')

        start = datetime.strptime(str(start), '%Y-%m-%d').strftime('%m/%d/%Y')
        end = datetime.strptime(str(end), '%Y-%m-%d').strftime('%m/%d/%Y')

        url = 'https://www.investing.com/instruments/HistoricalDataAjax'
        payload = {'header': f'{new_ticker}+Historical+Data',
                    'st_date': start,
                    'end_date': end,
                    'sort_col': 'date',
                    'action': 'historical_data',
                    'smlID': smlID,
                    'sort_ord': 'DESC',
                    'interval_sec': 'Daily',
                    'curr_id': curr_id
                    }
        req = requests.post(url, headers=self.urlheader, data=payload)
        soup = BeautifulSoup(req.content, "lxml")

        table = soup.find('table', id="curr_table")
        split_rows = table.find_all("tr")
        data_rows = split_rows[:0:-1]

        return data_rows

    def get_forex_df(self, ticker, start, end, smlID, curr_id):
        data_rows = self.__get_data(ticker, start, end, smlID, curr_id)

        #columns = ['Date', 'Price', 'Open', 'High', 'Low', 'Change %']
        df = pd.DataFrame(columns = ['Close', 'Open', 'High', 'Low'])
        for row in data_rows:
            columns = list(row.stripped_strings)
            columns = [column.replace(',','') for column in columns]

            date = str(datetime.strptime(columns[0], '%b %d %Y').strftime('%Y-%m-%d'))
            close_price = float(columns[1])
            open_price = float(columns[2])
            high_price = float(columns[3])
            low_price = float(columns[4])

            df.loc[date] = [close_price, open_price, high_price, low_price]

        return df

    def get_futures_df(self, ticker, start, end, smlID, curr_id):
        data_rows = self.__get_data(ticker, start, end, smlID, curr_id)

        #columns = ['Date', 'Price', 'Open', 'High', 'Low', 'Volume', 'Change %']
        df = pd.DataFrame(columns = ['Close', 'Open', 'High', 'Low', 'Volume'])
        for row in data_rows:
            columns = list(row.stripped_strings)
            columns = [column.replace(',','') for column in columns]

            date = str(datetime.strptime(columns[0], '%b %d %Y').strftime('%Y-%m-%d'))
            close_price = float(columns[1])
            open_price = float(columns[2])
            high_price = float(columns[3])
            low_price = float(columns[4])
            if columns[5] == '-':
                volume = 0
            else:
                volume = float(columns[5][:-1]) * 1000

            df.loc[date] = [close_price, open_price, high_price, low_price, volume]

        return df