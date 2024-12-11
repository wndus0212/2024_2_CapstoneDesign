import os
import sys
import django
import yfinance as yf
import pandas as pd
from datetime import datetime
import FinanceDataReader as fdr

# Django 프로젝트 루트 경로 추가
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_ROOT)

# Django 설정 모듈 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "capstoneBackend.settings")

# Django 환경 초기화
django.setup()

# Django 모델 임포트
from stockapp.models import StockHistory


def get_top_stocks_from_market(market, limit=50):
    """
    FinanceDataReader를 사용해 특정 시장에서 상위 N개의 종목을 가져옴
    market: 'KOSPI' 또는 'KOSDAQ'
    limit: 가져올 종목 수
    """
    try:
        stocks = fdr.StockListing(market).head(limit)
        return stocks[['Code', 'Name']]  # 종목 코드와 이름 반환
    except Exception as e:
        print(f"Error fetching stock list from {market}: {e}")
        return pd.DataFrame()


def save_stock_to_database(ticker, market_type):
    """
    주어진 티커와 시장 유형(KS: KOSPI, KQ: KOSDAQ)으로 데이터를 yfinance에서 가져와 데이터베이스에 저장
    ticker: 주식 코드
    market_type: 'KS' (KOSPI) 또는 'KQ' (KOSDAQ)
    """
    try:
        # 티커에 .KS 또는 .KQ 추가
        full_ticker = f"{ticker}.{market_type}"

        # yfinance에서 데이터 가져오기
        stock = yf.Ticker(full_ticker)
        history = stock.history(period="max")  # 가능한 모든 데이터 가져오기

        if history.empty:
            print(f"No data found for {full_ticker}")
            return

        # 필요한 열만 사용
        history = history[['Open', 'High', 'Low', 'Close', 'Volume']]
        history.reset_index(inplace=True)
        history['Date'] = history['Date'].dt.date

        # 전진 채우기로 누락된 값을 직전 값으로 채움
        history.ffill(inplace=True)

        # 데이터베이스에 저장
        for _, row in history.iterrows():
            StockHistory.objects.get_or_create(
                ticker=full_ticker,
                date=row['Date'],
                defaults={
                    'open': row['Open'],
                    'high': row['High'],
                    'low': row['Low'],
                    'close': row['Close'],
                    'volume': row['Volume'],
                }
            )

        print(f"Data for {full_ticker} has been saved to the database without duplication.")

    except Exception as e:
        print(f"Error saving data for {ticker}: {e}")


if __name__ == "__main__":
    # KOSPI와 KOSDAQ 시장에서 상위 50개 종목 가져오기
    print("Fetching top 50 stocks from KOSPI and KOSDAQ...")
    kospi_stocks = get_top_stocks_from_market("KOSPI", limit=50)
    kosdaq_stocks = get_top_stocks_from_market("KOSDAQ", limit=50)

    # 데이터베이스에 저장
    print("Saving stocks to the database...")
    for _, row in kospi_stocks.iterrows():
        save_stock_to_database(row['Code'], market_type="KS")  # KOSPI 종목

    for _, row in kosdaq_stocks.iterrows():
        save_stock_to_database(row['Code'], market_type="KQ")  # KOSDAQ 종목

    print("All stock data has been saved to the database.")

