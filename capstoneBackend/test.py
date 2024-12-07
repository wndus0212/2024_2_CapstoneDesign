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

print(yf.Ticker('MSTF').info)