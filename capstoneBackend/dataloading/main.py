import os
import sys
import django

# Django 프로젝트 루트를 PYTHONPATH에 추가
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(PROJECT_ROOT)

# Django 설정 로드
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "capstoneBackend.settings")
django.setup()

# 백테스트 함수 임포트
from dataloading.backtest_runner import run_backtest, run_multiple_backtests

# 테스트 실행 (필요에 따라 파라미터 수정)
if __name__ == "__main__":
    result = run_backtest(
        portfolio_id=2,  # 포트폴리오 ID
        start_date="2023-01-01",
        end_date="2023-12-31",
        initial_cash=1000000
    )
    print(f"Backtest Result: {result}")

csv_folder_path = r"C:\Users\shs\Desktop\code\historys"
custom_allocation = {"AAPL": 0.2, "MSFT": 0.3, "JPM": 0.2, "TSLA":0.3}
portfolio_name = "Fixed Duration Portfolio"
overall_start_date = "2020-01-01"
overall_end_date = "2022-12-31"
duration_days = 365
"""
# 여러 백테스트 실행
results_df = run_multiple_backtests(
    csv_folder=csv_folder_path,
    initial_cash=1000000,
    allocation=custom_allocation,
    portfolio_name=portfolio_name,
    start_date=overall_start_date,
    end_date=overall_end_date,
    duration_days=duration_days,
    iterations=100
)
"""