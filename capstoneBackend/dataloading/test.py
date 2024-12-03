import os
import sys
import django
import yfinance as yf

# Django 프로젝트 루트 경로 추가
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_ROOT)

# Django 설정 모듈 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "capstoneBackend.settings")

# Django 환경 초기화
django.setup()

# Django 모델 임포트
from stockapp.models import StockHistory

def get_and_save_financial_data(stock_id):
    """
    yfinance에서 데이터를 가져와 데이터베이스에 저장
    """
    stock = yf.Ticker(stock_id)
    stock_history = stock.history(interval='1d', period='max', auto_adjust=False)

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
    print(f"Data for {stock_id} saved successfully!")

if __name__ == "__main__":
    # 저장할 주식 티커 리스트
    stock_ids = ['AAPL', 'TSLA', 'JPM', 'AMZN', 'MSFT', '005930.KS', '105560.KS', '196170.KQ', '247540.KQ']

    for stock_id in stock_ids:
        get_and_save_financial_data(stock_id)

