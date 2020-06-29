#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

import bs4 as bs
import datetime as dt
import json
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import requests
import pandas_datareader.data as web
import pandas as pd
import pickle
import os

style.use('ggplot')


spy_site = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
file_path = '/Users/terrill/OneDrive/Documents/work/projects/spy'

def get_sp500_tickers(site):
    resp = requests.get(site)
    soup = bs.BeautifulSoup(resp.text, 'lxml')

    table = soup.find('table', {'class': 'wikitable sortable'})

    sectors = {}
    for ticker in table.findAll('tr')[1:]:
        symbol = ticker.findAll('td')[0].text.strip('\n')
        sector = ticker.findAll('td')[3].text.strip('\n')
        security = ticker.findAll('td')[1].text.strip('\n')

        # special cases with class A/B/C stocks
        if 'Class B' in security or 'Class C' in security:
            continue
        if symbol == 'BF.B':
            symbol = 'BF-A'
        if symbol == 'BRK.B':
            symbol = 'BRK-A'

        if sector in sectors:
            sectors[sector].append(symbol)
        else:
            sectors[sector] = []

    with open(file_path+'/final_dfs/sp500.json', 'w') as f:
        json.dump(sectors, f)

    return sectors

# print(get_sp500_tickers(spy_site))

def get_ticker_names(index):
    return [ticker for sector in list(index.values()) for ticker in sector]

# saves prices to csv locally
def get_data_from_yahoo(file, index):
    with open(file, 'r') as f:
        stock_list = json.load(f)

    tickers = get_ticker_names(stock_list)

    if not os.path.exists(f'{file_path}/{index}_dfs'):
        os.makedirs(f'{file_path}/{index}_dfs')

    start = dt.datetime(1990,1,1)
    end = dt.datetime(2020,5,1)

    for ticker in tickers:
        print(ticker)
        if not os.path.exists(f'{file_path}/{index}_dfs/{ticker}.csv'):
            # try:
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv(f'{file_path}/{index}_dfs/{ticker}.csv')
            # except:
            #     print('Could not get {}'.format(ticker))
        else:
            print('Already have {}!'.format(ticker))

spy500_list = file_path+'/final_dfs/sp500.json'
get_data_from_yahoo(spy500_list, 'sp500')

def compile_data(file, index):
    with open(file, 'r') as f:
        stock_list = json.load(f)

    tickers = get_ticker_names(stock_list)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        df = pd.read_csv(f'{file_path}/{index}_dfs/{ticker}.csv'.format(file_path, ticker))
        df.set_index('Date', inplace=True)
        df.rename(columns={'Adj Close': ticker, 'Volume': f'{ticker}_volume'}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)

    print(main_df.head())
    main_df.to_csv(f'{file_path}/final_dfs/{index}_joined_close.csv')

compile_data(spy500_list, 'sp500')


def visualize_corr_data():
    df = pd.read_csv(file_path+'/final_dfs/sp500_joined_close.csv')

    df_corr = df.corr()
    print(df_corr.head())

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1, 1)
    plt.tight_layout()
    plt.show()

# visualize_corr_data()
