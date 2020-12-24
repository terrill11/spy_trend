#!/Users/terrill/Documents/work/python_virtual_environments/venv_spy/bin/python

import pandas as pd
import pyodbc
import settings

class Database():
    def __init__(self, database_name):
        sql_server = settings.server_creds(database_name)

        server_name = sql_server['Server']
        server_port = sql_server['Port']
        database_name = sql_server['Database']
        username = sql_server['UID']
        password = sql_server['PWD']

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

    def query_to_df(self, query):
        return pd.read_sql(query, self.conn)