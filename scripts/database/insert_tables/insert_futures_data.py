#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import sys
sys.path.append('/Users/terrill/OneDrive/Documents/work/projects/spy/scripts/')

from database.sql_server_conn import connect_to_database
from datetime import datetime
from datetime import timedelta
import pandas_datareader.data as web
import pyodbc
import requests
import time


# server connection setup
conn, cursor = connect_to_database('futures')

def get_data_from_yahoo(ticker):
    start = datetime(1990,1,1)
    end = (datetime.now() - timedelta(days = 1))
    df = web.DataReader(ticker, 'yahoo', start, end)
    return df

futures_list = ['CL=F', 'GC=F', 'SI=F', 'ZF=F', 'ZN=F']

print('Running insert now.')
for ticker in futures_list:
    df = get_data_from_yahoo(ticker)

    if '=' in ticker:
        ticker = ticker.replace('=','_')

    for index, row in df.iterrows():
        query = f'''INSERT Futures.dbo.{ticker} (Date, HighPrice, LowPrice, OpenPrice, ClosePrice, Volume)
                        VALUES (?,?,?,?,?,?)'''
        cursor.execute(query, (index.date(), row['High'], row['Low'], row['Open'], row['Adj Close'], row['Volume']))
    conn.commit()

    print(f'{ticker} done saving')
    time.sleep(10)