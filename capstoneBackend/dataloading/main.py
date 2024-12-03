from backtest_runner import run_backtest, run_multiple_backtests

# 단일 백테스트 실행
run_backtest(
    initial_cash=1000000,
    allocation={"AAPL": 0.5, "MSFT": 0.3, "JPM": 0.2},
    start_date="2020-01-01",
    end_date="2022-12-31",
    portfolio_name="Tech & Finance Portfolio"
)

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