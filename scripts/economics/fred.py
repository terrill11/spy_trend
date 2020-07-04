#!/Users/terrill/OneDrive/Documents/work/projects/spy/venv_spy/bin/python

from datetime import datetime as dt
import numpy as np
import pandas as pd
import requests
import urllib.request as url_request
import xml.etree.ElementTree as ET
import os


class Fred():
    root_url = 'https://api.stlouisfed.org/fred'
    nan_char = '.'

    def __init__(self, api_key=None, api_key_path=None):
        '''
        Initialize the class with the API key. Add the API key directly as a parameter or store it in a file first.
        Otherwise go to http://research.stlouisfed.org/fred2/ and sign up for an account to get a free API key.
        '''
        if api_key is not None:
            self.api_key = api_key
        elif api_key_path is not None:
            with open(api_key_path, 'r') as f:
                self.api_key = f.readline()
        else:
            return 'Missing API key. Sign up for a free account at http://research.stlouisfed.org/fred2/'

    def __fetch_data(self, url):
        '''
        Helper function that helps fetch data from the url
        '''
        url += f'&api_key={self.api_key}'

        try:
            response = url_request.urlopen(url)
            root = ET.fromstring(response.read())
        except HTTPError as e:
            root = ET.fromstring(e.read())
            raise ValueError(root.get('message'))
        return root

    def __parse_date_string(self, date_str, format='%Y-%m-%d'):
        '''
        Parses the FRED data's date string int datetime format
        '''

        pass

    def get_series_info(self, series_id):
        '''
        Retrives infomation about the series such as title, frequency, observation start/end dates, units, etc.
        '''
        url += f'{self.root_url}/series?series_id={series_id}'
        root = self.__fetch_data(url)

        if root is None or not len(root):
            raise ValueError('No info exists for series id: ' + series_id)
        info = pd.Series(root.getchildren()[0].attrib)
        return info

    def get_series(self, series_id, observation_start=None, observation_end=None, **kwargs):
        '''
        Retrives data of the series_id.

        date format in 'YYYY-mm-dd'

        All additional parameters: https://api.stlouisfed.org/docs/fred/series_observations.html

        Returns a Pandas Series where each index is the observation date and value is the value
        '''
            
        url = f'{self.root_url}/series/observations?series_id={series_id}'

        if observation_start is not None:
            url += f'&observation_start={observation_start}'
        if observation_end is not None:
            url += f'&observation_end={observation_end}'
        if kwargs.keys():
            url += f'&{url_parse.urlencode(kwargs)}'

        root = self.__fetch_data(url)
        if root is None:
            raise ValueError(f'No data exists for {series_id}')

        data = {}
        for child in root.getchildren():
            val = child.get('value')

            if val == self.nan_char:
                val = np.nan
            else:
                val = float(val)

            data[child.get('date')] = val

        return pd.Series(data)