#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

from fred import Fred
from datetime import datetime as dt
import time
import pyodbc
import pandas

# server connection setup
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

# api setup
api_key_path = '/Users/terrill/OneDrive/Documents/work/projects/spy/scripts/database/economics/api_key.txt'
fred = Fred(api_key_path=api_key_path)


start_date = '1900-01-01'
end_date = dt.now().date()

series_ids_pct = ['DGS10', 'DGS30', 'USD1MTD156N', 'USD6MTD156N', 'USD12MD156N', 
                    'DFF', 'T10YIE', 'MORTGAGE15US', 'MORTGAGE30US', 'UNRATE']

series_ids_bil = ['M1', 'M2']

series_ids_no = ['CPIAUCSL']

# note series index dates are in string (do i have to convert it to datetime object before i insert to database?)
# also note for NULL values, might have to fix later
for series_id in series_ids_pct[:1]:
    data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
    data /= 100

    for index, value in data.iteritems():
        query = f'''INSERT finance.dbo.{series_id} (Date, Rate)
                            VALUES (?,?)'''
        cursor.execute(query, (index, round(value, 4)))
    conn.commit()
    print(f'{series_id} table updated.')
    # time.sleep(10)

# for series_id in series_ids_bil:
#     data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
#     data *= 1000000000

#     for index, value in data.iteritems():
#         cursor.execute(f'''INSERT finance.dbo.{series_id} (date, decimal_numbers)
#                             VALUES ({index}, {value})''')
#     time.sleep(10)

# for series_id in series_ids_no:
#     data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)

#     for index, value in data.iteritems():
#         cursor.execute(f'''INSERT finance.dbo.{series_id} (date, decimal_numbers)
#                             VALUES ({index}, {value})''')

    time.sleep(10)