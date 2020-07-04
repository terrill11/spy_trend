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
conn, cursor = connect_to_database('equities')

# data scraping
def get_data_from_yahoo(ticker):
    start = datetime(1990,1,1)
    end = (datetime.now() - timedelta(days = 1))
    df = web.DataReader(ticker, 'yahoo', start, end)
    return df

equities_list = ['SPY', 'QQQ',  'IWM', 'TLT', 'IEF', 'USO',
                'XLRE', 'XLK', 'XLV', 'XLF', 'XLY', 'XLI', 'XLP', 'XLU', 'XLE', 'XLB', 'XLC',
                'VNQ', 'VGT', 'VHT', 'VFH', 'VCR', 'VIS', 'VDC', 'VPU', 'VDE', 'VAW', 'VOX',
                '^RUT', '^DJI', '^IXIC', '^GSPC']       # indexes

# no volumn columns
bonds_list = ['^TYX', '^TNX']     # bonds/treasuries, need to x10 all data
vix_list = ['^VIX']


print('Running insert now.')
for ticker in equities_list[-4:]:
    df = get_data_from_yahoo(ticker)

    if '^' in ticker:
        ticker = ticker.replace('^','I_')

    for index, row in df.iterrows():
        query = f'''INSERT Equities.dbo.{ticker} (Date, HighPrice, LowPrice, OpenPrice, ClosePrice, Volume)
                        VALUES (?,?,?,?,?,?)'''
        cursor.execute(query, (index.date(), row['High'], row['Low'], row['Open'], row['Adj Close'], row['Volume']))
    conn.commit()
    print(f'{ticker} done saving')
    time.sleep(10)
    # spy might need volume column to be bigint next time

for ticker in bonds_list:
    df = get_data_from_yahoo(ticker)

    new_ticker = ticker.replace('^', 'B_')

    for index, row in df.iterrows():
        row *= 10
        query = f'''INSERT Equities.dbo.{new_ticker} (Date, HighPrice, LowPrice, OpenPrice, ClosePrice)
                        VALUES (?,?,?,?,?)'''
        cursor.execute(query, (index.date(), row['High'], row['Low'], row['Open'], row['Adj Close']))
    conn.commit()

    print(f'{ticker} done saving')
    time.sleep(10)

for ticker in vix_list:
    df = get_data_from_yahoo(ticker)

    new_ticker = ticker.replace('^', 'I_')

    for index, row in df.iterrows():
        query = f'''INSERT Equities.dbo.{new_ticker} (Date, HighPrice, LowPrice, OpenPrice, ClosePrice)
                        VALUES (?,?,?,?,?)'''
        cursor.execute(query, (index.date(), row['High'], row['Low'], row['Open'], row['Adj Close']))
    conn.commit()
    
    print(f'{ticker} done saving')
    time.sleep(10)


conn.close()