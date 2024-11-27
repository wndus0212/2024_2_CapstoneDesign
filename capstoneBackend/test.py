import yfinance as yf
import pandas as pd
import FinanceDataReader as fdr
from concurrent.futures import ThreadPoolExecutor
import os
from pykrx import stock
from pprint import pprint

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'stockapp\data\stock_list', 'sp500.csv')

df=pd.read_csv(file_path)

industries = []

# 각 주식의 industry 정보를 가져오기
for symbol in df['Symbol']:  # 'symbols' 열에 티커가 들어 있다고 가정
    try:
        ticker = yf.Ticker(symbol)
        industry = ticker.info.get('industry', 'Unknown')  # 'industry' 키가 없을 때 기본값 'Unknown'
        industries.append(industry)
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        industries.append('Error')  # 실패한 경우 'Error' 추가

# 데이터프레임에 industry 열 추가
df['industry'] = industries

# 결과 출력 및 저장
print(df)
df.to_csv("sp500_with_industries.csv", index=False)  # 결과를 새 CSV 파일로 저장
if os.path.exists("sp500_with_industries.csv"):
    print(f"파일이 저장되었습니다")
else:
    print(f"파일이 없습니다")