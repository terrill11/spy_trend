#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import sys
sys.path.append('/Users/terrill/OneDrive/Documents/work/projects/spy/scripts/')

import pyodbc
from database.Database import Database
from database.QueriesCreateTable import QueriesCreateTable


# database connection setup
equities_db = Database('equities')
economics_db = Database('economics')
forex_db = Database('forex')
futures_db = Database('futures')

# queries
create_table_queries = QueriesCreateTable()

# EQUITIES
equity_tickers = ['SPY', 'QQQ', 'IWM', 'VTI', 'USO', 'GLD', 'SLV', 'DBO', 'UUP',                    # etfs
                    'TLT', 'IEF', 'SHY', 'BND',                                                     # bond etfs
                    'XLRE', 'XLK', 'XLV', 'XLF', 'XLY', 'XLI', 'XLP', 'XLU', 'XLE', 'XLB', 'XLC',   # SPDR industry funds
                    'VNQ', 'VGT', 'VHT', 'VFH', 'VCR', 'VIS', 'VDC', 'VPU', 'VDE', 'VAW', 'VOX']    # vanguard industry funds
index_tickers = ['I_RUT', 'I_DJI', 'I_IXIC', 'I_GSPC']
bond_tickers = ['B_TYX', 'B_TNX']
vix_tickers = ['I_VIX', 'I_VVIX', 'I_VXN']
new_equity_tickers = []

# ECONOMICS
economics_pct_tickers = ['DGS10', 'DGS30', 'USD1MTD156N', 'USD6MTD156N', 'USD12MD156N', 
                            'DFF', 'T10YIE', 'MORTGAGE15US', 'MORTGAGE30US', 'UNRATE']
economics_no_tickers = ['M1', 'M2', 'BOGMBBMW', 'CPIAUCSL', 'WIMFSL', 'DTWEXBGS', 'GOLDAMGBD228NLBM']
new_economics_tickers = []

# FOREX
forex_tickers = ['USD_JPY', 'USD_EUR', 'USD_CHF', 'USD_PLN', 'USD_CNY', 'USD_HUF', 'USD_RUB', 'USD_CAD',
                'USD_RON', 'USD_INR', 'USD_GBP', 'USD_AUD', 'USD_HKD', 'USD_SEK', 'USD_SGD',
                'XAU_USD', 'XAG_USD',
                'DXY']
new_forex_tickers = []

# FUTURES
futures_list = ['Crude_Oil_WTI', 'Brent_Oil', 'Natural_Gas']

# EQUITIES
def create_tables_equities_all():
    for ticker in equity_tickers:
        query = create_table_queries.create_table_equities(ticker)
        equities_db.create_table(ticker, query)
        
    for ticker in index_tickers:
        query = create_table_queries.create_table_equities(ticker)
        equities_db.create_table(ticker, query)

    for ticker in bond_tickers:
        query = create_table_queries.create_table_equities(ticker)
        equities_db.create_table(ticker, query)

    for ticker in vix_tickers:
        query = create_table_queries.create_table_equities(ticker)
        equities_db.create_table(ticker, query)

# ECONOMICS
def create_tables_economics_all():
    # for ticker in economics_pct_tickers:
    #     query = create_table_queries.create_table_economics_rate(ticker)
    #     economics_db.create_table(ticker, query)

    for ticker in new_economics_tickers:#economics_no_tickers:
        query = create_table_queries.create_table_economics_value(ticker)
        economics_db.create_table(ticker, query)

# FOREX
def create_tables_forex_all():
    for ticker in forex_tickers:
        query = create_table_queries.create_table_forex(ticker)
        forex_db.create_table(ticker, query)

# FUTURES
def create_tables_futures_all():
    for ticker in futures_list:
        query = create_table_queries.create_table_futures(ticker)
        futures_db.create_table(ticker, query)


# create_tables_equities_all()
# create_tables_economics_all()
# create_tables_forex_all()
# create_tables_futures_all()


equities_db.conn.close()
economics_db.conn.close()
forex_db.conn.close()
futures_db.conn.close()