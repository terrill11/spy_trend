#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import pandas as pd
import pyodbc

class Database():
    def __init__(self, database_name):
        with open(f'/Users/terrill/Documents/work/stuff/spy_trend/sql_server_info_{database_name}.txt', 'r') as f:
            line = f.readline().split(',')
        server_name = line[0]
        server_port = line[1]
        database_name = line[2]
        username = line[3]
        password = line[4]

        self.conn = pyodbc.connect('Driver={FreeTDS};'
                                f'Server={server_name};'
                                f'Port={server_port};'
                                f'Database={database_name};'
                                f'UID={username};'
                                f'PWD={password}')
        self.cursor = self.conn.cursor()
        self.database_name = database_name

    # returns latest entry of table in string date format
    def get_latest_entry(self, ticker):
        get_last_entry = f'''SELECT top 1 *
                            FROM {self.database_name}.dbo.{ticker} with(nolock)
                            order by date desc'''
        last_entry_df = pd.read_sql(get_last_entry, self.conn)
        latest_entry = str(last_entry_df['Date'].values[0])

        return latest_entry

    def create_table(self, ticker, query):
        self.cursor.execute(query)
        self.conn.commit()
        print(f'{ticker} table added.')

    def insert_data(self, query, data):
        self.cursor.execute(query, data)