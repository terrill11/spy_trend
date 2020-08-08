#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import sys
sys.path.append('/Users/terrill/OneDrive/Documents/work/projects/spy/scripts/')

from equities.yahoo_scraper import Yahoo
from database.database_conn import Database
from datetime import datetime
from datetime import timedelta
import pandas as pd
import pandas_datareader.data as web
import requests
import time


# database connection setup
futures_db = Database('futures')

# data scrape setup
yahoo = Yahoo()

# change this to approximate the last time table was updated
days_to_look_back = 60

futures_list = ['CL=F', 'GC=F', 'SI=F', 'ZF=F', 'ZN=F']


print('Running insert now.')
for ticker in futures_list[1:]:
    sql_ticker = ticker.replace('=', '_')

    latest_entry = futures_db.get_latest_entry(sql_ticker)
    data_to_insert = yahoo.get_last_x_days_data(ticker, latest_entry, days_to_look_back)

    for index, row in data_to_insert.iterrows():
        query = f'''INSERT {futures_db.database_name}.dbo.{sql_ticker} (Date, HighPrice, LowPrice, OpenPrice, ClosePrice, Volume)
                        VALUES (?,?,?,?,?,?)'''
        futures_db.cursor.execute(query, (index.date(), row['High'], row['Low'], row['Open'], row['Adj Close'], row['Volume']))
    futures_db.conn.commit()

    print(f'{ticker} done saving')
    time.sleep(10)

print('Futures list finished updating')


futures_db.conn.close()