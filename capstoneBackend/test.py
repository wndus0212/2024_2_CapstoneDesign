import yfinance as yf
import pandas as pd
import FinanceDataReader as fdr
from concurrent.futures import ThreadPoolExecutor
import os

stocks=fdr.StockListing('KRX')
print(stocks)