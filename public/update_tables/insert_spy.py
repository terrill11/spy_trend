#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import pyodbc
import pandas

with open('/Users/terrill/OneDrive/Documents/work/projects/spy/database_scripts/server_info.txt', 'r') as f:
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
latest_entry = cursor.execute('''SELECT TOP 1 regular_date
                                FROM finance.dbo.test with(nolock)
                                ORDER BY regular_date DESC''').fetchall()

print(latest_entry)

conn.close()