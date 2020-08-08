#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import sys
sys.path.append('/Users/terrill/OneDrive/Documents/work/projects/spy/scripts/')

from forex.forex_scraper import Forex
from database.database_conn import Database
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import json
import requests
import pandas as pd
import pyodbc
import time

# server connection setup
forex_db = Database('forex')

# data scrape setup
forex = Forex()

ticker_list = forex.get_ticker_list()

# change this to approximate the last time table was updated
days_to_look_back = 60
start_date = str(datetime.now().date() - timedelta(days = days_to_look_back))
end_date = str(datetime.now().date() - timedelta(days = 1))

print('Running insert now.')
for ticker in ticker_list:
    print(f'Working on {ticker}')
    sql_ticker = ticker.replace('-','_')

    latest_entry = forex_db.get_latest_entry(sql_ticker)

    smlID = ticker_list[ticker]['smlID']
    curr_id = ticker_list[ticker]['curr_id']

    df = forex.get_data(ticker, start_date, end_date, smlID, curr_id)
    df = df.loc[df.index > latest_entry]
    df.index = pd.to_datetime(df.index)

    for index, row in df.iterrows():
        query = f'''INSERT {forex_db.database_name}.dbo.{sql_ticker} (Date, ClosePrice, OpenPrice, HighPrice, LowPrice)
                    VALUES (?,?,?,?,?)'''
        forex_db.cursor.execute(query, (index.date(), row['Close'], row['Open'], row['High'], row['Low']))
    forex_db.conn.commit()

    print(f'{ticker} saved')
    time.sleep(10)

def update_dxy_historical_data(start_date, end_date):
    ticker = 'US+Dollar+Index'
    sql_ticker = 'DXY'

    latest_entry = forex_db.get_latest_entry(sql_ticker)

    smlID = 2067751
    curr_id = 942611

    df = forex.get_data(ticker, start_date, end_date, smlID, curr_id)
    df = df.loc[df.index > latest_entry]
    df.index = pd.to_datetime(df.index)

    for index, row in df.iterrows():
        query = f'''INSERT {forex_db.database_name}.dbo.{sql_ticker} (Date, ClosePrice, OpenPrice, HighPrice, LowPrice)
                    VALUES (?,?,?,?,?)'''
        forex_db.cursor.execute(query, (index.date(), row['Close'], row['Open'], row['High'], row['Low']))
    forex_db.conn.commit()

    print('DXY saved')

update_dxy_historical_data(start_date, end_date)


forex_db.conn.close()