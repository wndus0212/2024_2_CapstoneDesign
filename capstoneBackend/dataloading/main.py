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
        portfolio_id=6,  # 포트폴리오 ID
        start_date="2016-01-01",
        end_date="2021-01-01",
        initial_cash=1000000
    )
    print(f"Backtest Result: {result}")

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
from dataloading.backtest_runner import run_multiple_backtests

if __name__ == "__main__":
    # 입력 파라미터 설정
    portfolio_id = 6  # 실행할 포트폴리오의 ID
    start_date = "2010-01-01"  # 백테스트 시작 날짜
    end_date = "2022-12-31"  # 백테스트 종료 날짜
    duration_days = 365*5  # 각 백테스트 기간 (일 단위)
    initial_cash = 1000000  # 초기 투자 금액
    iterations = 100  # 백테스트 반복 횟수

    # 백테스트 실행
    results = run_multiple_backtests(
        portfolio_id=portfolio_id,
        start_date=start_date,
        end_date=end_date,
        duration_days=duration_days,
        initial_cash=initial_cash,
        iterations=iterations
    )

    # 결과 출력
    print("백테스트 결과:")
    print(f"최종 포트폴리오 가치: {results['final_portfolio_values']}")
    print(f"Sharpe Ratio: {results['sharpe_ratios']}")
    print(f"MDD: {results['mdds']}")

    import pandas as pd
    df = pd.DataFrame({
        "Final Portfolio Value": results["final_portfolio_values"],
        "Sharpe Ratio": results["sharpe_ratios"],
        "MDD": results["mdds"],
    })
    df.to_csv("backtest_results.csv", index=False)
    print("결과가 'backtest_results.csv'에 저장되었습니다.")
