#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

from fred import Fred
from datetime import datetime as dt
from datetime import timedelta
import numpy as np
import pandas as pd
import pyodbc
import time

# server connection setup
with open('/Users/terrill/Documents/work/stuff/spy_trend/sql_server_info_economics.txt', 'r') as f:
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

# api setup
api_key_path = '/Users/terrill/Documents/work/stuff/spy_trend/fred_api_key.txt'
fred = Fred(api_key_path=api_key_path)

print('Running insert now.')
start_date = '1900-01-01'
end_date = dt.now().date() - timedelta(days = 1)

series_ids_pct = ['DGS10', 'DGS30', 'USD1MTD156N', 'USD6MTD156N', 'USD12MD156N', 
                    'DFF', 'T10YIE', 'MORTGAGE15US', 'MORTGAGE30US', 'UNRATE']

series_ids_regs = ['M1', 'M2', 'CPIAUCSL']

for series_id in series_ids_pct:
    data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
    data /= 100

    for index, value in data.iteritems():
        if pd.isna(value):
            value = None
        query = f'''INSERT Economics.dbo.{series_id} (Date, Rate)
                            VALUES (?,?)'''
        cursor.execute(query, (index, value))
    conn.commit()

    print(f'{series_id} table updated.')
    time.sleep(10)

for series_id in series_ids_regs:
    data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)

    for index, value in data.iteritems():
        if pd.isna(value):
            value = None
        query = f'''INSERT Economics.dbo.{series_id} (Date, Value)
                            VALUES (?,?)'''
        cursor.execute(query, (index, value))
    conn.commit()
    print(f'{series_id} table updated.')
    time.sleep(10)

conn.close()