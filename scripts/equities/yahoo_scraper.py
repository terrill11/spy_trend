#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

from datetime import datetime
from datetime import timedelta
import pandas_datareader.data as web
import requests

class Yahoo():
    def __init__(self):
        self.source = 'yahoo'

    def get_all_data(self, ticker):
        start = datetime(1990,1,1)
        end = (datetime.now() - timedelta(days = 1))
        df = web.DataReader(ticker, self.source, start, end)
        return df

    def get_data_from_range(self, ticker, start, end):
        start = datetime.strptime(start, '%Y-%m-%d').date()
        end = datetime.strptime(end, '%Y-%m-%d').date()
        df = web.DataReader(ticker, self.source, start, end)
        return df

    def get_last_x_days_data(self, ticker, latest_entry, days_to_look_back):
        start = datetime.now() - timedelta(days = days_to_look_back)
        end = (datetime.now() - timedelta(days = 1))
        df = web.DataReader(ticker, self.source, start, end)
        df = df.loc[df.index > latest_entry]
        return df