import yfinance as yf
import pandas as pd
import FinanceDataReader as fdr
from concurrent.futures import ThreadPoolExecutor
import os
from pykrx import stock
from pprint import pprint

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sp500_file_path = os.path.join(BASE_DIR, 'stockapp\data', 'sp500_sector.csv')


sectors = [
    {'ticker': 'XLY', 'name': 'Consumer Discretionary'},
    {'ticker': 'XLC', 'name': 'Communication Services'},
    {'ticker': 'XLF', 'name': 'Financials'},
    {'ticker': 'XLI', 'name': 'Industrials'},
    {'ticker': 'XLE', 'name': 'Energy'},
    {'ticker': 'XLB', 'name': 'Materials'},
    {'ticker': 'XLV', 'name': 'Health Care'},
    {'ticker': 'XLP', 'name': 'Consumer Staples'},
    {'ticker': 'XLK', 'name': 'Technology'},
    {'ticker': 'XLRE', 'name': 'Real Estate'},
    {'ticker': 'XLU', 'name': 'Utilities'}
]

for sector in sectors:
    print(yf.Ticker(sector['ticker']).info)