#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import pyodbc
import pandas

with open('/Users/terrill/OneDrive/Documents/work/projects/spy/scripts/database/server_info.txt', 'r') as f:
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

forex_tickers = ['USD-JPY', 'USD-EUR', 'USD-CHF', 'USD-PLN', 'USD-CNY', 'USD-HUF', 'USD-RUB', 'USD-CAD',
                'USD-RON', 'USD-INR', 'USD-GBP', 'USD-AUD', 'USD-HKD', 'USD-SEK', 'USD-SGD', 'XAU-USD']

for ticker in forex_tickers:
    cursor.execute(f'''CREATE TABLE finance.dbo.{ticker} (
                            Date DATE,
                            Price DECIMAL,
                            Open DECIMAL,
                            High DECIMAL,
                            Low DECIMAL
                        )''').fetchall()

conn.close()