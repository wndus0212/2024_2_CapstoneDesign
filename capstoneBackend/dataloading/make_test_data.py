import os
import django
import sys
# Django 프로젝트 루트를 설정합니다.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(PROJECT_ROOT)

# Django 설정 로드
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "capstoneBackend.settings")
django.setup()

from stockapp.models import Portfolios, Portfolio_Stocks

def create_test_data():
    # 포트폴리오 생성
    portfolio = Portfolios.objects.create(
        user_id=1235,  # 적절한 user_id 입력
        name="Test Portfolio",
    )

    # 포트폴리오에 할당 데이터 추가
    Portfolio_Stocks.objects.create(portfolio_id=portfolio.portfolio_id, stock_symbol="AAPL", allocation=0.6)
    Portfolio_Stocks.objects.create(portfolio_id=portfolio.portfolio_id, stock_symbol="TSLA", allocation=0.4)

    print(f"Created Portfolio ID: {portfolio.portfolio_id}")

if __name__ == "__main__":
    create_test_data()

