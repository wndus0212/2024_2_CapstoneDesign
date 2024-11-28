import yfinance as yf
import pandas as pd
import FinanceDataReader as fdr
from concurrent.futures import ThreadPoolExecutor
import os
from pykrx import stock
from pprint import pprint

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'stockapp\data\stock_list', 'sp500_with_industries.csv')

df=pd.read_csv(file_path,dtype=str)

grouped = df.groupby(['Sector', 'Industry'])

# 그룹별 데이터 확인 (예시로 첫 번째 그룹 출력)
for (Sector, Industry), group in grouped:
    print(f"Sector: {Sector}, Industry: {Industry}")
    print(group.head(), "\n")