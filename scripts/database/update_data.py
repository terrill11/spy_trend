#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import sys
sys.path.append('/Users/terrill/OneDrive/Documents/work/projects/spy/scripts/')

from database.Database import Database
from database.QueriesUpdateTable import QueriesUpdateTable
from equities.YahooScraper import Yahoo
from economics.Fred import Fred
from forex.InvestingScraper import InvestingScraper

from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import json
import pandas as pd
import pandas_datareader.data as web
import pyodbc
import requests
import time


# database connection setup
equities_db = Database('equities')
economics_db = Database('economics')
forex_db = Database('forex')
futures_db = Database('futures')

# queries
update_table_queries = QueriesUpdateTable()

# other packages
yahoo = Yahoo()
fred = Fred(api_key_path='/Users/terrill/Documents/work/stuff/spy_trend/fred_api_key.txt')
investing = InvestingScraper()


# change this to approximate the last time table was updated
days_to_look_back = 30
start_date = datetime.now().date() - timedelta(days = days_to_look_back)
end_date = datetime.now().date() - timedelta(days = 1)


#---------- TICKER LISTS -------------#
# EQUITIES
equities_list = ['SPY', 'QQQ', 'IWM', 'VTI',                                                    # index etfs
                'GLD', 'SLV', 'USO', 'DBO', 'UUP',                                              # futures etfs
                'TLT', 'IEF', 'SHY', 'BND',                                                     # bond etfs
                'XLRE', 'XLK', 'XLV', 'XLF', 'XLY', 'XLI', 'XLP', 'XLU', 'XLE', 'XLB', 'XLC',   # SPDR industry funds
                'VNQ', 'VGT', 'VHT', 'VFH', 'VCR', 'VIS', 'VDC', 'VPU', 'VDE', 'VAW', 'VOX',    # vanguard industry funds
                '^RUT', '^DJI', '^IXIC', '^GSPC']                                               # indexes
# no volumn columns
bonds_list = ['^TYX', '^TNX']     # bonds/treasuries, need to x10 all data
vix_list = ['^VIX', '^VVIX', '^VXN']

# ECONOMICS
series_ids_pct = ['DGS10', 'DGS30', 'USD1MTD156N', 'USD6MTD156N', 'USD12MD156N', 
                    'DFF', 'T10YIE', 'MORTGAGE15US', 'MORTGAGE30US', 'UNRATE']
series_ids_regs = ['M1', 'M2', 'BOGMBBMW', 'CPIAUCSL', 'WIMFSL', 'DTWEXBGS', 'GOLDAMGBD228NLBM']

# FOREX
forex_ticker_list = investing.get_ticker_list('forex')

# FUTURES
futures_ticker_list = investing.get_ticker_list('futures')


#---------- UPDATE TABLE FUNCTIONS -------------#
def print_results(ticker):
    print(f'{ticker} done updating')
    time.sleep(10)

def update_tables_equities():
    for ticker in equities_list:
        if '^' in ticker:
            sql_ticker = ticker.replace('^','I_')
        else:
            sql_ticker = ticker

        latest_entry = equities_db.get_latest_entry(sql_ticker)
        data_to_insert = yahoo.get_last_x_days_data(ticker, latest_entry, days_to_look_back)

        for index, row in data_to_insert.iterrows():
            query = update_table_queries.insert_data_equities(sql_ticker)
            data = (index.date(), row['High'], row['Low'], row['Open'], row['Adj Close'], row['Volume'])
            equities_db.insert_data(query, data)
        equities_db.conn.commit()

        print_results(ticker)

    for ticker in bonds_list:
        sql_ticker = ticker.replace('^', 'B_')

        latest_entry = equities_db.get_latest_entry(sql_ticker)
        data_to_insert = yahoo.get_last_x_days_data(ticker, latest_entry, days_to_look_back)

        for index, row in data_to_insert.iterrows():
            row *= 10
            query = update_table_queries.insert_data_equities_bonds(sql_ticker)
            data = (index.date(), row['High'], row['Low'], row['Open'], row['Adj Close'])
            equities_db.insert_data(query, data)
        equities_db.conn.commit()

        print_results(ticker)

    for ticker in vix_list:
        sql_ticker = ticker.replace('^', 'I_')

        latest_entry = equities_db.get_latest_entry(sql_ticker)
        data_to_insert = yahoo.get_last_x_days_data(ticker, latest_entry, days_to_look_back)

        for index, row in data_to_insert.iterrows():
            query = update_table_queries.insert_data_equities_vix(sql_ticker)
            data = (index.date(), row['High'], row['Low'], row['Open'], row['Adj Close'])
            equities_db.insert_data(query, data)
        equities_db.conn.commit()
        
        print_results(ticker)

def update_tables_economics():
    for series_id in series_ids_pct:
        latest_entry = economics_db.get_latest_entry(series_id)

        data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
        data /= 100
        data = data[data.index > latest_entry]

        for index, value in data.iteritems():
            if pd.isna(value):
                value = None
            query = update_table_queries.insert_data_economics_rates(series_id)
            data = (index, value)
            economics_db.insert_data(query, data)
        economics_db.conn.commit()

        print_results(series_id)

    for series_id in series_ids_regs:
        latest_entry = economics_db.get_latest_entry(series_id)

        data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
        data = data[data.index > latest_entry]

        for index, value in data.iteritems():
            if pd.isna(value):
                value = None
            query = update_table_queries.insert_data_economics_regs(series_id)
            data = (index, value)
            economics_db.insert_data(query, data)
        economics_db.conn.commit()
        
        print_results(series_id)

def update_tables_forex():
    for ticker in forex_ticker_list:
        sql_ticker = ticker.replace('-','_')

        latest_entry = forex_db.get_latest_entry(sql_ticker)

        smlID = forex_ticker_list[ticker]['smlID']
        curr_id = forex_ticker_list[ticker]['curr_id']
        df = investing.get_forex_df(ticker, start_date, end_date, smlID, curr_id)
        df = df.loc[df.index > latest_entry]
        df.index = pd.to_datetime(df.index)

        for index, row in df.iterrows():
            query = update_table_queries.insert_data_forex(sql_ticker)
            data = (index.date(), row['Close'], row['Open'], row['High'], row['Low'])
            forex_db.insert_data(query, data)
        forex_db.conn.commit()

        print_results(ticker)

    # DXY
    def get_dxy_historical_data():
        ticker = 'US+Dollar+Index'
        sql_ticker = 'DXY'

        latest_entry = forex_db.get_latest_entry(sql_ticker)

        smlID = 2067751
        curr_id = 942611

        df = investing.get_forex_df(ticker, start_date, end_date, smlID, curr_id)
        df = df.loc[df.index > latest_entry]
        df.index = pd.to_datetime(df.index)

        for index, row in df.iterrows():
            query = update_table_queries.insert_data_forex(sql_ticker)
            data = (index.date(), row['Close'], row['Open'], row['High'], row['Low'])
            forex_db.insert_data(query, data)
        forex_db.conn.commit()

        print_results(ticker)
    get_dxy_historical_data()

def update_tables_futures():
    for ticker in futures_ticker_list:
        sql_ticker = ticker.replace('+', '_')

        latest_entry = futures_db.get_latest_entry(sql_ticker)

        smlID = futures_ticker_list[ticker]['smlID']
        curr_id = futures_ticker_list[ticker]['curr_id']
        df = investing.get_futures_df(ticker+'Futures+', start_date, end_date, smlID, curr_id)
        df = df.loc[df.index > latest_entry]
        df.index = pd.to_datetime(df.index)

        for index, row in df.iterrows():
            query = update_table_queries.insert_data_futures(sql_ticker)
            data = (index.date(), row['Close'], row['Open'], row['High'], row['Low'], row['Volume'])
            futures_db.insert_data(query, data)
        futures_db.conn.commit()

        print_results(ticker)

def update_tables_dix():
    latest_entry = equities_db.get_latest_entry('I_DIX')
    df = pd.read_csv('https://squeezemetrics.com/monitor/static/DIX.csv')
    df = df.loc[df['date'] > latest_entry]

    for index, value in df.iterrows():
        query = update_table_queries.insert_data_dix()
        data = (value[0], value[1], value[2], value[3])
        equities_db.insert_data(query, data)
    equities_db.conn.commit()

    print_results('DIX')


print('Running updates now.')
# update_tables_equities()
# update_tables_economics()
update_tables_forex()
# update_tables_futures()
# update_tables_dix()


equities_db.conn.close()
economics_db.conn.close()
forex_db.conn.close()
futures_db.conn.close()