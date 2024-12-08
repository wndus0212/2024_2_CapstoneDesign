import os
import django
import sys
# Django 설정
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "capstoneBackend.settings")
django.setup()

from stockapp.models import Portfolios, Portfolio_Stocks, Backtests

def delete_test_portfolio(portfolio_name):
    test_portfolio = Portfolios.objects.filter(name=portfolio_name)
    if test_portfolio.exists():
        portfolio_id = test_portfolio.first().portfolio_id

        # 종속 데이터 삭제
        Backtests.objects.filter(portfolio_id_id=portfolio_id).delete()  # 수정된 부분
        Portfolio_Stocks.objects.filter(portfolio_id=portfolio_id).delete()

        # 포트폴리오 삭제
        test_portfolio.delete()

        print(f"Deleted portfolio: {portfolio_name} and all related data.")
    else:
        print(f"No portfolio found with the name: {portfolio_name}")

if __name__ == "__main__":
    delete_test_portfolio("Test Portfolio")

