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
data = yf.Ticker('MSFT').history(period="1y")

# DataFrame 생성
df = pd.DataFrame(data)

# 20일 이동평균선 (Middle Band)
df['Middle Band'] = df['Close'].rolling(window=20).mean()

# 20일 표준편차
df['STD'] = df['Close'].rolling(window=20).std()

# 상단선 (Upper Band)
df['Upper Band'] = df['Middle Band'] + (df['STD'] * 2)

# 하단선 (Lower Band)
df['Lower Band'] = df['Middle Band'] - (df['STD'] * 2)

# 결과 출력
df_reset = df.reset_index()
print(df_reset[['Date', 'Middle Band', 'Upper Band', 'Lower Band']].dropna())