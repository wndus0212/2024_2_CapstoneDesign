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

def get_sector_stock_list(sector):
    # KOSPI 데이터 읽기
    kospi_list = pd.read_csv(kospi, dtype={'Symbol': str})
    kospi_list['Symbol'] +='.KS'
    kospi_sector_stocks = kospi_list[kospi_list['Sector'] == sector].head(5)
    kospi_sector_stocks['Market'] = 'KOSPI'  # KOSPI 시장 추가

    # KOSDAQ 데이터 읽기
    kosdaq_list = pd.read_csv(kosdaq, dtype={'Symbol': str})
    kosdaq_list['Symbol'] +='.KQ'
    kosdaq_sector_stocks = kosdaq_list[kosdaq_list['Sector'] == sector].head(5)
    kosdaq_sector_stocks['Market'] = 'KOSDAQ'  # KOSDAQ 시장 추가

    # S&P500 데이터 읽기
    sp500_list = pd.read_csv(sp500, dtype={'Symbol': str})
    sp500_sector_stocks = sp500_list[sp500_list['Sector'] == sector].head(5)
    sp500_sector_stocks['Market'] = 'S&P500'  # S&P500 시장 추가

    # 세 데이터프레임 합치기
    combined_df = pd.concat([kospi_sector_stocks, kosdaq_sector_stocks, sp500_sector_stocks], ignore_index=True)

    stock_data = []
    for _, stock in combined_df.iterrows():
        ticker = yf.Ticker(stock['Symbol'])
        try:
            # 시가총액 추출
            market_cap = ticker.info.get('marketCap', 0)

            stock_data.append({
                'Name': stock['Name'],
                'Symbol': stock['Symbol'],
                'Market': stock['Market'],
                'MarketCap': market_cap,
            })
        except Exception as e:
            print(f"Error fetching data for {stock['Symbol']}: {e}")
    
    # 데이터프레임 생성
    final_df = pd.DataFrame(stock_data)

    return final_df

# 예시 사용: 'Technology' 섹터의 주식 목록을 가져오기
sector_stocks = get_sector_stock_list('Technology')

# 결과 확인
print(sector_stocks)