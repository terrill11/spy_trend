#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import sys
sys.path.append('/Users/terrill/OneDrive/Documents/work/projects/spy/scripts/')

from database.sql_server_conn import connect_to_database
from datetime import datetime
from datetime import timedelta
import pandas_datareader.data as web
import pyodbc
import requests
import time


# server connection setup
conn, cursor = connect_to_database('futures')


futures_list = ['cl=f', 'gc=f', 'zn=f', 'zf=f']
