import yfinance as yf
import pandas as pd
import FinanceDataReader as fdr
from concurrent.futures import ThreadPoolExecutor
import os
from pykrx import stock
from pprint import pprint

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'stockapp\data\stock_list', 'sp500_with_industries.csv')

# 예시 데이터 생성
data=yf.Ticker('MSFT').history()

# 3일 이동평균선 계산 (rolling 함수 사용)
data['MA_3'] = data['Close'].rolling(window=3).mean()

# 5일 이동평균선 계산
data['MA_5'] = data['Close'].rolling(window=5).mean()

# 출력
print(data)
