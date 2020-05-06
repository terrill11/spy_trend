#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv/bin/python

import datetime as dt
import requests
import pandas_datareader.data as web

file_path = '/Users/terrill/OneDrive/Documents/work/projects/spy'

# saves prices to csv locally
def get_data_from_yahoo(ticker):
    # with open(file, 'r') as f:
    #     stock_list = json.load(f)

    # tickers = get_ticker_names(stock_list)

    # if not os.path.exists(f'{file_path}/{index}_dfs'):
    #     os.makedirs(f'{file_path}/{index}_dfs')

    start = dt.datetime(1990,1,1)
    end = dt.datetime(2020,5,1)

    # for ticker in tickers:
    #     print(ticker)
    #     if not os.path.exists(f'{file_path}/{index}_dfs/{ticker}.csv'):
    #         # try:
    #         df = web.DataReader(ticker, 'yahoo', start, end)
    #         df.to_csv(f'{file_path}/{index}_dfs/{ticker}.csv')
    #         # except:
    #         #     print('Could not get {}'.format(ticker))
    #     else:
    #         print('Already have {}!'.format(ticker))

    df = web.DataReader(ticker, 'yahoo', start, end)
    df.to_csv(f'{file_path}/final_dfs/sector etfs - vanguard/{ticker}.csv')


# if __name__=='__main__':
#     get_data_from_yahoo(file, index)

etf_list = ['spy', 'qqq', 'tlt', '^vix', 'iwm', 'ief', 'cl=f', 'uso', 'gc=f', 'vnq']
spdr_etfs = ['xlre', 'xlk', 'xlv', 'xlf', 'xly', 'xli', 'xlp', 'xlu', 'xle', 'xlb', 'xlc']
vanguard_etfs = ['vnq', 'vgt', 'vht', 'vfh', 'vcr', 'vis', 'vdc', 'vpu', 'vde', 'vaw', 'vox']

for i in vanguard_etfs:
    get_data_from_yahoo(i)