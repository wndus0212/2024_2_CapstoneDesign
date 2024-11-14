import pandas as pd
import yfinance as yf
import FinanceDataReader as fdr
from tqdm import tqdm  # 진행 상황 표시를 위한 라이브러리
import time

data = pd.read_csv(r'C:\CapstoneDesign\2024_2_CapstoneDesign\capstoneBackend\etf_data\ETF_Ticker.csv')
stocks=data['Ticker'].tolist()
symbols = []
names = []
prices = []
market_caps = []
volume = []

# 진행 상황 표시를 위한 tqdm 사용
for stock in tqdm(stocks, desc="Processing Symbols", unit="symbol"):
    try:
        # Yahoo Finance에서 해당 종목의 데이터 가져오기
        stock_data = yf.Ticker(stock)  # 종목 심볼 뒤에 '.VN'을 붙여서 Yahoo Finance에서 조회
        stock_info = stock_data.info
        
        if stock_info['quoteType'] == "ETF":
            symbols.append(stock)
            names.append(stock_info.get('longName', None))  # 'longName'이 정확한 키일 수 있습니다.
            prices.append(stock_info.get('previousClose', None))  # 주가
            market_caps.append(stock_info.get('totalAssets', None))  # 시가총액
            volume.append(stock_info.get('volume', None))  # 거래량
        else:
            print(stock + " is not ETF")
    except Exception as e:
        print(f"Error retrieving data for {stock}: {e}")
        # 오류 발생 시 해당 종목은 건너뛰고, 리스트에 추가하지 않음
    time.sleep(0.5)

# 데이터프레임 생성
data = {
    'Symbol': symbols,
    'Name': names,
    'Price': prices,
    'Market Cap': market_caps,
    'Volume': volume
}

df = pd.DataFrame(data)

# market cap을 기준으로 내림차순 정렬 (None은 마지막에 오도록 처리)
df['Market Cap'] = pd.to_numeric(df['Market Cap'], errors='coerce')  # 숫자로 변환, 변환 불가 시 NaN 처리
df_sorted = df.sort_values(by='Market Cap', ascending=False)

print(df_sorted.head(5))  # 상위 5개 출력
df.to_csv(r'C:\CapstoneDesign\2024_2_CapstoneDesign\capstoneBackend\etf_data\ETF_data.csv', index=False, encoding='utf-8')