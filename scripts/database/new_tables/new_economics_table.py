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

economics_pct_tickers = ['DGS10', 'DGS30', 'USD1MTD156N', 'USD6MTD156N', 'USD12MD156N', 
                            'DFF', 'T10YIE', 'MORTGAGE15US', 'MORTGAGE30US', 'UNRATE']
economics_bil_tickers = ['M1', 'M2']
cpi = 'CPIAUCSL'

# rates
for ticker in economics_pct_tickers[:1]:
    query = f'''CREATE TABLE finance.dbo.{ticker} (
                            Date DATE,
                            Rate DECIMAL(5,4))'''
    cursor.execute(query)
    conn.commit()
    print(f'{ticker} table added.')

# # M1 & M2
# for ticker in economics_bil_tickers:
#     cursor.execute(f'''CREATE TABLE finance.dbo.{ticker} (
#                             Date DATE,
#                             Dollars DECIMAL
#                         )''').fetchall()

# # CPI
# cursor.execute(f'''CREATE TABLE finance.dbo.{cpi} (
#                         Date DATE,
#                         Index DECIMAL
#                     )''').fetchall()

conn.close()


