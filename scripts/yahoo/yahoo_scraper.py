#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import datetime as dt
import requests
import pandas_datareader.data as web

file_path = '/Users/terrill/OneDrive/Documents/work/projects/spy'
forex_file_path = '/Users/terrill/OneDrive/Documents/work/finance/forex'

# saves prices to csv locally
def get_data_from_yahoo(ticker):
    start = dt.datetime(1990,1,1)
    end = dt.datetime(2020,6,16)

    df = web.DataReader(ticker, 'yahoo', start, end)
    #df.to_csv(f'{file_path}/final_dfs/sector etfs - vanguard/{ticker}.csv')
    #df.to_csv(f'{file_path}/final_dfs/futures/{ticker}.csv')
    df.to_csv(f'{file_path}/final_dfs/forex/{ticker}.csv')


# if __name__=='__main__':
#     get_data_from_yahoo(file, index)

etf_list = ['spy', 'qqq', 'tlt', '^vix', 'iwm', 'ief', 'uso',  'vnq']
futures_list = ['cl=f', 'gc=f', 'zn=f', 'zf=f']
spdr_etfs = ['xlre', 'xlk', 'xlv', 'xlf', 'xly', 'xli', 'xlp', 'xlu', 'xle', 'xlb', 'xlc']
vanguard_etfs = ['vnq', 'vgt', 'vht', 'vfh', 'vcr', 'vis', 'vdc', 'vpu', 'vde', 'vaw', 'vox']
forex = ['JPY=X', 'EUR=X', 'CHF=X', 'PLN=X', 'CNY=X', 'HUF=X', 'RUB=X', 'CAD=X', 
        'RON=X', 'INR=X', 'GBP=X', 'AUD=X', 'HKD=X', 'SEK=X', 'SGD=X', 'BTC-USD']

for i in forex:
    get_data_from_yahoo(i)
    print(f'{i} done saving')