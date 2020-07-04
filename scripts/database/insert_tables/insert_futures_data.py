#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

from datetime import datetime
from datetime import timedelta
import pandas_datareader.data as web
import pyodbc
import requests
import time


# server connection setup
with open('/Users/terrill/Documents/work/stuff/spy_trend/sql_server_info_futures.txt', 'r') as f:
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


futures_list = ['cl=f', 'gc=f', 'zn=f', 'zf=f']
