#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import sys
sys.path.append('/Users/terrill/OneDrive/Documents/work/projects/spy/scripts/')

import pyodbc
from database.sql_server_conn import connect_to_database

# server connection setup
conn, cursor = connect_to_database('futures')

futures_list = ['CL_F', 'GC_F', 'SI_F', 'ZF_F', 'ZN_F']

for ticker in futures_list:
    query = f'''CREATE TABLE Futures.dbo.{ticker} (
                            Date DATE,
                            HighPrice DECIMAL(16,6),
                            LowPrice DECIMAL(16,6),
                            OpenPrice DECIMAL(16,6),
                            ClosePrice DECIMAL(16,6),
                            Volume BIGINT
                        )'''

    cursor.execute(query)
    conn.commit()
    print(f'{ticker} table added.')