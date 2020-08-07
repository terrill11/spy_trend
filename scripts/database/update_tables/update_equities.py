#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import sys
sys.path.append('/Users/terrill/OneDrive/Documents/work/projects/spy/scripts/')

from equities.yahoo_scraper import Yahoo
from database.sql_server_conn import connect_to_database
from datetime import datetime
from datetime import timedelta
import pandas as pd
import pandas_datareader.data as web
import requests
import time


conn, cursor = connect_to_database('equities')


yahoo = Yahoo()
# change this to approximate the last time table was updated
days_to_look_back = 60


equities_list = ['SPY', 'QQQ',  'IWM', 'TLT', 'IEF', 'USO',
                'XLRE', 'XLK', 'XLV', 'XLF', 'XLY', 'XLI', 'XLP', 'XLU', 'XLE', 'XLB', 'XLC',
                'VNQ', 'VGT', 'VHT', 'VFH', 'VCR', 'VIS', 'VDC', 'VPU', 'VDE', 'VAW', 'VOX',
                '^RUT', '^DJI', '^IXIC', '^GSPC']       # indexes
# no volumn columns
bonds_list = ['^TYX', '^TNX']     # bonds/treasuries, need to x10 all data
vix_list = ['^VIX']


print('Running insert now.')
for ticker in equities_list[1:]:
    if '^' in ticker:
        sql_ticker = ticker.replace('^','I_')
    else:
        sql_ticker = ticker

    get_last_entry = f'''SELECT top 1 *
                        FROM equities.dbo.{sql_ticker} with(nolock)
                        order by date desc'''
    last_entry_df = pd.read_sql(get_last_entry, conn)
    latest_entry = str(last_entry_df['Date'].values[0])

    data_to_insert = yahoo.get_last_x_days_data(ticker, latest_entry, days_to_look_back)

    for index, row in data_to_insert.iterrows():
        query = f'''INSERT Equities.dbo.{sql_ticker} (Date, HighPrice, LowPrice, OpenPrice, ClosePrice, Volume)
                        VALUES (?,?,?,?,?,?)'''
        cursor.execute(query, (index.date(), row['High'], row['Low'], row['Open'], row['Adj Close'], row['Volume']))
    conn.commit()
    
    print(f'{ticker} done saving')
    time.sleep(10)
print('Equities List finished updating')

for ticker in bonds_list:
    sql_ticker = ticker.replace('^', 'B_')

    get_last_entry = f'''SELECT top 1 *
                        FROM equities.dbo.{sql_ticker} with(nolock)
                        order by date desc'''
    last_entry_df = pd.read_sql(get_last_entry, conn)
    latest_entry = str(last_entry_df['Date'].values[0])

    data_to_insert = yahoo.get_last_x_days_data(ticker, latest_entry, days_to_look_back)

    for index, row in data_to_insert.iterrows():
        row *= 10
        query = f'''INSERT Equities.dbo.{sql_ticker} (Date, HighPrice, LowPrice, OpenPrice, ClosePrice)
                        VALUES (?,?,?,?,?)'''
        cursor.execute(query, (index.date(), row['High'], row['Low'], row['Open'], row['Adj Close']))
    conn.commit()

    print(f'{ticker} done saving')
    time.sleep(10)
print('Bond List finished updating')

for ticker in vix_list:
    sql_ticker = ticker.replace('^', 'I_')

    get_last_entry = f'''SELECT top 1 *
                        FROM equities.dbo.{sql_ticker} with(nolock)
                        order by date desc'''
    last_entry_df = pd.read_sql(get_last_entry, conn)
    latest_entry = str(last_entry_df['Date'].values[0])    

    data_to_insert = yahoo.get_last_x_days_data(ticker, latest_entry, days_to_look_back)

    for index, row in data_to_insert.iterrows():
        query = f'''INSERT Equities.dbo.{sql_ticker} (Date, HighPrice, LowPrice, OpenPrice, ClosePrice)
                        VALUES (?,?,?,?,?)'''
        cursor.execute(query, (index.date(), row['High'], row['Low'], row['Open'], row['Adj Close']))
    conn.commit()
    
    print(f'{ticker} done saving')
    time.sleep(10)
print('VIX List finished updating')


conn.close()