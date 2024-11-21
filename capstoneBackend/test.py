import yfinance as yf
import pandas as pd
import FinanceDataReader as fdr
from concurrent.futures import ThreadPoolExecutor
import os
from pykrx import stock
from pprint import pprint


tickers = ['1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', '1010', 
           '1011', '1012', '1013', '1014', '1015', '1016', '1017', '1018', '1019', '1020', 
           '1021', '1024', '1025', '1026', '1027', '1028', '1034', '1035', '1150', '1151', 
           '1152', '1153', '1154', '1155', '1156', '1157', '1158', '1159', '1160', '1167', 
           '1182', '1224', '1227', '1232', '1244', '1894']

for ticker in tickers:
    print(ticker, stock.get_index_ticker_name(ticker))  # Print the name of the index
    try:
        price_change = stock.get_index_price_change("20240101", "20240228", ticker)  # Get price change data
        print(price_change.head(2))
    except Exception as e:  # Catch exceptions
        print(f"Error with ticker {ticker}: {e}")

data = stock.get_index_ohlcv_by_date("20240101", "20240228", "1028")  # KOSPI 200
print(data)
