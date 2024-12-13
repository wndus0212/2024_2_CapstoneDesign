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


exchange_data = yf.Ticker("USDKRW=X").history(period='max')


# 필요한 열만 추출 (예: 'Close')
exchange_data = exchange_data[['Close']]
exchange_data.reset_index(inplace=True)  # 날짜를 열로 변환
exchange_data['Date'] =pd.to_datetime(exchange_data['Date']).dt.date
# CSV 파일로 저장
exchange_data.to_csv("exchange_rate.csv", index=False)
print(type(exchange_data['Date'].iloc[-1]))
print(f"환율 데이터가 '{"exchange_rate.csv"}' 파일로 저장되었습니다.")