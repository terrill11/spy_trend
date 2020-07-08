#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import sys
sys.path.append('/Users/terrill/OneDrive/Documents/work/projects/spy/scripts/')

import pandas as pd
from database.sql_server_conn import connect_to_database

conn, cursor = connect_to_database('equities')

df = pd.read_csv('https://squeezemetrics.com/monitor/static/DIX.csv')

# columns = date, price(spx), dix, gex
for index, value in df.iterrows():
    query = f'''INSERT Equities.dbo.I_DIX (Date, SPX, DIX, GEX)
                    VALUES (?,?,?,?)'''
    cursor.execute(query, (value[0], value[1], value[2], value[3]))

conn.commit()

conn.close()