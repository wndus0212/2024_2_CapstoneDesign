import os
import sys
import django
import yfinance as yf
from datetime import datetime, timedelta

# Django 프로젝트 루트 경로 추가
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_ROOT)

# Django 설정 모듈 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "capstoneBackend.settings")

# Django 환경 초기화
django.setup()

# Django 모델 임포트
from stockapp.models import StockHistory


def get_last_update_date(ticker):
    """
    데이터베이스에서 주어진 티커의 마지막 업데이트 날짜를 가져옴
    """
    latest_record = StockHistory.objects.filter(ticker=ticker).order_by('-date').first()
    return latest_record.date if latest_record else None


def get_and_save_financial_data(stock_id):
    """
    yfinance에서 데이터를 가져와 데이터베이스에 저장
    stock_id: 주식 또는 채권의 티커
    """
    # 데이터 가져오기 시작 날짜 결정
    last_update_date = get_last_update_date(stock_id)
    start_date = (last_update_date + timedelta(days=1)) if last_update_date else None

    stock = yf.Ticker(stock_id)
    stock_history = stock.history(interval='1d', start=start_date, auto_adjust=False)

    if stock_history.empty:
        print(f"No new data for {stock_id}")
        return

    # 필요한 열만 선택
    stock_history = stock_history[['Open', 'High', 'Low', 'Close', 'Volume']]
    stock_history.reset_index(inplace=True)
    stock_history['Date'] = stock_history['Date'].dt.date

    for _, row in stock_history.iterrows():
        # 데이터베이스에 저장
        StockHistory.objects.update_or_create(
            ticker=stock_id,
            date=row['Date'],
            defaults={
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                'volume': row['Volume'],
            }
        )

    print(f"Data for {stock_id} has been updated in the database.")


if __name__ == "__main__":
    # 주식 및 채권 티커
    tickers = ["AAPL", "GOOGL", "MSFT", "^TNX"]  # 기존 주식 + 채권

    # 데이터 가져오기
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        get_and_save_financial_data(ticker)
        print(f"Data for {ticker} has been saved to the database.")
