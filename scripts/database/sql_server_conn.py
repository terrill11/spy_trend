#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import pyodbc

def connect_to_database(database_name):
    with open(f'/Users/terrill/Documents/work/stuff/spy_trend/sql_server_info_{database_name}.txt', 'r') as f:
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

    return conn, cursor