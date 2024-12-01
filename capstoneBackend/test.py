import yfinance as yf
import pandas as pd
import FinanceDataReader as fdr
from concurrent.futures import ThreadPoolExecutor
import os
from pykrx import stock
from pprint import pprint
import requests


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'stockapp\data\stock_list', 'sp500_with_industries.csv')
kosdaq = os.path.join(BASE_DIR, 'stockapp\data\stock_list', 'kosdaq_150_with_industries.csv')
kospi = os.path.join(BASE_DIR, 'stockapp\data\stock_list', 'kospi_200_with_industries.csv')
sp500 = os.path.join(BASE_DIR, 'stockapp\data\stock_list', 'sp500_with_industries.csv')
nasdaq = os.path.join(BASE_DIR, 'stockapp\data\stock_list', 'nasdaq100_with_industries.csv')

import yfinance as yf
import pandas as pd

us_bond_5=yf.Ticker('^FVX')
ytm_5=us_bond_5.history(period="max").Close
print(ytm_5)

us_bond_30=yf.Ticker('^TYX')
ytm_30=us_bond_30.history(period="max").Close
print(ytm_30)