#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import pyodbc
import pandas

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

forex_tickers = ['USD_JPY', 'USD_EUR', 'USD_CHF', 'USD_PLN', 'USD_CNY', 'USD_HUF', 'USD_RUB', 'USD_CAD',
                'USD_RON', 'USD_INR', 'USD_GBP', 'USD_AUD', 'USD_HKD', 'USD_SEK', 'USD_SGD', 'XAU_USD']

for ticker in forex_tickers:
    query = f'''CREATE TABLE Forex.dbo.{ticker} (
                            Date DATE,
                            ClosePrice DECIMAL(14,4),
                            OpenPrice DECIMAL(14,4),
                            HighPrice DECIMAL(14,4),
                            LowPrice DECIMAL(14,4))'''
    cursor.execute(query)
    conn.commit()
    print(f'{ticker} table added.')

conn.close()