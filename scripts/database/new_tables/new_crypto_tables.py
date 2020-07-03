#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import pyodbc
import pandas

with open('/Users/terrill/Documents/work/stuff/spy_trend/server_info.txt', 'r') as f:
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

crypto_tickers = ['BTC-USD', 'ETC-USD', 'LTC-USD']

for ticker in crypto_tickers:
    cursor.execute(f'''CREATE TABLE finance.dbo.{ticker} (
                            Date DATE,
                            Price DECIMAL,
                            Open DECIMAL,
                            High DECIMAL,
                            Low DECIMAL,
                            Volume INT
                        )''').fetchall()

conn.close()