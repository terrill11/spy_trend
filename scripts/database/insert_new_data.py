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
vix_list = ['^VIX']

# ECONOMICS
series_ids_pct = ['DGS10', 'DGS30', 'USD1MTD156N', 'USD6MTD156N', 'USD12MD156N', 
                    'DFF', 'T10YIE', 'MORTGAGE15US', 'MORTGAGE30US', 'UNRATE']
series_ids_regs = ['M1', 'M2', 'CPIAUCSL']

# FOREX
forex_ticker_list = investing.get_ticker_list('forex')

# FUTURES
futures_ticker_list = investing.get_ticker_list('futures')


#---------- UPDATE TABLE FUNCTIONS -------------#
def print_results(ticker):
    print(f'{ticker} done updating')
    time.sleep(10)

def insert_data_equities():
    for ticker in equities_list:
        if '^' in ticker:
            sql_ticker = ticker.replace('^','I_')
        else:
            sql_ticker = ticker

        df = yahoo.get_all_data(ticker)

        for index, row in df.iterrows():
            query = update_table_queries.insert_data_equities(sql_ticker)
            data = (index.date(), row['High'], row['Low'], row['Open'], row['Adj Close'], row['Volume'])
            equities_db.insert_data(query, data)
        equities_db.conn.commit()

        print_results(ticker)

    for ticker in bonds_list:
        sql_ticker = ticker.replace('^', 'B_')
        df = yahoo.get_all_data(ticker)

        for index, row in df.iterrows():
            row *= 10
            query = insert_data_equities_bonds(sql_ticker)
            data = (index.date(), row['High'], row['Low'], row['Open'], row['Adj Close'])
            equities_db.insert_data(query, data)
        equities_db.conn.commit()

        print_results(ticker)

    for ticker in vix_list:
        sql_ticker = ticker.replace('^', 'I_')
        df = yahoo.get_all_data(ticker)

        for index, row in df.iterrows():
            query = insert_data_equities_vix(sql_ticker)
            data = (index.date(), row['High'], row['Low'], row['Open'], row['Adj Close'])
            equities_db.insert_data(query, data)
        equities_db.conn.commit()
        
        print_results(ticker)

def insert_data_economics():
    start_date = '1900-01-01'
    end_date = datetime.now().date() - timedelta(days = 1)

    for series_id in series_ids_pct:
        data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
        data /= 100

        for index, value in data.iteritems():
            if pd.isna(value):
                value = None
            query = update_table_queries.insert_data_economics_rates(series_id)
            data = (index, value)
            economics_db.insert_data(query, data)
        economics_db.conn.commit()

        print_results(series_id)

    for series_id in series_ids_regs:
        data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)

        for index, value in data.iteritems():
            if pd.isna(value):
                value = None
            query = update_table_queries.insert_data_economics_regs(series_id)
            data = (index, value)
            economics_db.insert_data(query, data)
        economics_db.conn.commit()
        
        print_results(series_id)

def insert_data_forex():
    # 2 parter (1990-01-01 - 2004-12-31)
    # start_date = '1990-01-01'
    # end_date = '2004-12-31'
    start_date = '2005-01-01'
    end_date = str(datetime.now().date() - timedelta(days = 1))

    for ticker in forex_ticker_list:
        sql_ticker = ticker.replace('-','_')

        smlID = forex_ticker_list[ticker]['smlID']
        curr_id = forex_ticker_list[ticker]['curr_id']
        df = investing.get_forex_data(ticker, start_date, end_date, smlID, curr_id)
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

        smlID = 2067751
        curr_id = 942611

        df = investing.get_forex_data(ticker, start_date, end_date, smlID, curr_id)
        df.index = pd.to_datetime(df.index)

        for index, row in df.iterrows():
            query = update_table_queries.insert_data_forex(sql_ticker)
            data = (index.date(), row['Close'], row['Open'], row['High'], row['Low'])
            forex_db.insert_data(query, data)
        forex_db.conn.commit()

        print_results(ticker)
    get_dxy_historical_data()

def insert_data_futures():
    # 2 parter (1990-01-01 - 2004-12-31)
    # start_date = '1990-01-01'
    # end_date = '2004-12-31'
    start_date = '2005-01-01'
    end_date = str(datetime.now().date() - timedelta(days = 1))

    for ticker in futures_ticker_list:
        sql_ticker = ticker.replace('+', '_')

        smlID = futures_ticker_list[ticker]['smlID']
        curr_id = futures_ticker_list[ticker]['curr_id']
        df = investing.get_futures_df(ticker+'Futures+', start_date, end_date, smlID, curr_id)
        df.index = pd.to_datetime(df.index)

        for index, row in df.iterrows():
            query = update_table_queries.insert_data_futures(sql_ticker)
            data = (index.date(), row['Close'], row['Open'], row['High'], row['Low'], row['Volume'])
            futures_db.insert_data(query, data)
        futures_db.conn.commit()

        print_results(ticker)

def insert_data_dix():
    df = pd.read_csv('https://squeezemetrics.com/monitor/static/DIX.csv')

    for index, value in df.iterrows():
        query = update_table_queries.insert_data_dix()
        data = (value[0], value[1], value[2], value[3])
        equities_db.insert_data(query, data)
    equities_db.conn.commit()

    print_results('DIX')


print('Running updates now.')
# insert_data_equities()
# insert_data_economics()
# insert_data_forex()
# insert_data_futures()
# insert_data_dix()


equities_db.conn.close()
economics_db.conn.close()
forex_db.conn.close()
futures_db.conn.close()