#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import sys
sys.path.append('/Users/terrill/OneDrive/Documents/work/projects/spy/scripts/')

from economics.fred import Fred
from database.sql_server_conn import connect_to_database
from datetime import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import pyodbc
import time


# server connection setup
conn, cursor = connect_to_database('economics')

# api setup
api_key_path = '/Users/terrill/Documents/work/stuff/spy_trend/fred_api_key.txt'
fred = Fred(api_key_path=api_key_path)

# change this to approximate the last time table was updated
days_to_look_back = 60
start_date = datetime.now().date() - timedelta(days = days_to_look_back)
end_date = datetime.now().date() - timedelta(days = 1)

series_ids_pct = ['DGS10', 'DGS30', 'USD1MTD156N', 'USD6MTD156N', 'USD12MD156N', 
                    'DFF', 'T10YIE', 'MORTGAGE15US', 'MORTGAGE30US', 'UNRATE']
series_ids_regs = ['M1', 'M2', 'CPIAUCSL']


for series_id in series_ids_pct:
    get_last_entry = f'''SELECT top 1 *
                        FROM Economics.dbo.{series_id} with(nolock)
                        order by date desc'''
    last_entry_df = pd.read_sql(get_last_entry, conn)
    latest_entry = str(last_entry_df['Date'].values[0])

    data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
    data /= 100
    data = data[data.index > latest_entry]

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
    get_last_entry = f'''SELECT top 1 *
                        FROM Economics.dbo.{series_id} with(nolock)
                        order by date desc'''
    last_entry_df = pd.read_sql(get_last_entry, conn)
    latest_entry = str(last_entry_df['Date'].values[0])

    data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
    data = data[data.index > latest_entry]

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