#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

from datetime import datetime
from datetime import timedelta
import pandas_datareader.data as web
import pyodbc
import requests
import time


# server connection setup
with open('/Users/terrill/Documents/work/stuff/spy_trend/sql_server_info_equities.txt', 'r') as f:
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