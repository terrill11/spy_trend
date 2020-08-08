#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import sys
sys.path.append('/Users/terrill/OneDrive/Documents/work/projects/spy/scripts/')

from economics.fred import Fred
from database.database_conn import Database
from datetime import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import pyodbc
import time


# server connection setup
economics_db = Database('economics')

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
    latest_entry = economics_db.get_latest_entry(series_id)

    data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
    data /= 100
    data = data[data.index > latest_entry]

    for index, value in data.iteritems():
        if pd.isna(value):
            value = None
        query = f'''INSERT {economics_db.database_name}.dbo.{series_id} (Date, Rate)
                            VALUES (?,?)'''
        economics_db.cursor.execute(query, (index, value))
    economics_db.conn.commit()

    print(f'{series_id} table updated.')
    time.sleep(10)

for series_id in series_ids_regs:
    latest_entry = economics_db.get_latest_entry(series_id)

    data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
    data = data[data.index > latest_entry]

    for index, value in data.iteritems():
        if pd.isna(value):
            value = None
        query = f'''INSERT {economics_db.database_name}.dbo.{series_id} (Date, Value)
                            VALUES (?,?)'''
        economics_db.cursor.execute(query, (index, value))
    economics_db.conn.commit()
    
    print(f'{series_id} table updated.')
    time.sleep(10)

economics_db.conn.close()