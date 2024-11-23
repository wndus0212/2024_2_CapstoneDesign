import yfinance as yf
import pandas as pd
import FinanceDataReader as fdr
from concurrent.futures import ThreadPoolExecutor
import os
from pykrx import stock
from pprint import pprint

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sp500_file_path = os.path.join(BASE_DIR, 'stockapp\data', 'sp500_sector.csv')


def get_stock_history(Id, start=None, end=None, period=0, interval='1d'):
    ticker = yf.Ticker(Id)
    try:
        if period == 0:
            # 특정 기간의 데이터를 가져오기
            df = ticker.history(start=start, end=end, interval=interval, auto_adjust=False)
        else:
            # 최근 기간 데이터를 가져오기
            df = ticker.history(period=period, interval=interval, auto_adjust=False)
        
        if df.empty:
            print(f"No data found for stock {Id}")
            return None
        
        # 필요한 컬럼만 선택
        selected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if all(col in df.columns for col in selected_columns):
            return df[selected_columns]
        else:
            print(f"Some required columns are missing in the data for stock {Id}.")
            return None
        
    except Exception as e:
        print(f"Error fetching data for {Id}: {e}")
        return None



def get_index(option, indexname, start, end, period, interval):
    if option == 'sector':
        if indexname == 'SPDR':
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
        else:
            sectors = [
                {'ticker': 'KOSPI200SECTOR-0.KS', 'name': 'KOSPI 200 Communication Services'},
                {'ticker': 'KOSPI200SECTOR-1.KS', 'name': 'KOSPI 200 Constructions'},
                {'ticker': 'KOSPI200SECTOR-2.KS', 'name': 'KOSPI 200 Heavy Industries'},
                {'ticker': 'KOSPI200SECTOR-3.KS', 'name': 'KOSPI 200 Steels & Materials'},
                {'ticker': 'KOSPI200SECTOR-4.KS', 'name': 'KOSPI 200 Energy & Chemicals'},
                {'ticker': 'KOSPI200SECTOR-5.KS', 'name': 'KOSPI 200 IT'},
                {'ticker': 'KOSPI200SECTOR-6.KS', 'name': 'KOSPI 200 Financials'},
                {'ticker': 'KOSPI200SECTOR-7.KS', 'name': 'KOSPI 200 Consumer Staples'},
                {'ticker': 'KOSPI200SECTOR-8.KS', 'name': 'KOSPI 200 Consumer Discretionary'},
                {'ticker': 'KOSPI200SECTOR-9.KS', 'name': 'KOSPI 200 Industrials'},
                {'ticker': 'KOSPI200SECTOR-10.KS', 'name': 'KOSPI 200 Health Care'}
            ]

        sector_data = []
        # 각 섹터별 데이터 가져오기
        for sector in sectors:
            try:
                ticker = sector['ticker']  # 티커만 사용
                df = get_stock_history(ticker, start, end, period, interval)  # 수정된 부분
                if df is not None and not df.empty:  # 데이터가 존재하고 비어있지 않은지 확인
                    sector_info = yf.Ticker(ticker).info
                    name = sector_info.get('name', None)
                    
                    sector_data.append({
                        'Sector': sector['name'],  # 섹터 이름 사용
                        'Stock History': df
                    })
                else:
                    print(f"No data found for {sector['name']}")
            except Exception as e:
                print(f"Error fetching data for {sector['name']}: {e}")

        # 데이터프레임으로 변환
        if sector_data:
            df = pd.DataFrame(sector_data)
            return df
        else:
            return None  # 데이터를 못 구한 경우 None 반환
    else:
        indexname = '^' + indexname
        df = get_stock_history(indexname, start, end, period, interval)
        
        if df is not None and not df.empty:
            return df
        else:
            print(f"No data found for {indexname}")
            return None  # 데이터가 없으면 None 반환


# 테스트 호출
df = get_index('index', 'KS11', "", "2024-12-31", "1mo", "1d")

print(df)