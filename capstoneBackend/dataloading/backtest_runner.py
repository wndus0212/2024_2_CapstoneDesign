import pandas as pd
import backtrader as bt
import numpy as np
import os
import sys
import django
import time
# Django 프로젝트 루트를 PYTHONPATH에 추가
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(PROJECT_ROOT)

# Django 설정 로드
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "capstoneBackend.settings")
django.setup()

# 필요한 모델 임포트
from stockapp.models import Portfolio_Stocks, Backtests
from dataloading.data_loader import load_data_from_db
from dataloading.strategies import FixedAllocationStrategy
from dataloading.data_extraction import calculate_mdd, calculate_sharpe_ratio, load_risk_free_rate


def get_portfolio_allocation(portfolio_id):
    """
    포트폴리오 ID를 기반으로 할당 데이터를 가져옵니다.
    """
    allocations = Portfolio_Stocks.objects.filter(portfolio_id=portfolio_id)
    if not allocations.exists():
        raise ValueError(f"No allocation data found for portfolio ID {portfolio_id}")

    return {item.stock_symbol: item.allocation for item in allocations}


def run_backtest(portfolio_id, start_date, end_date, initial_cash=1000000):
    """
    포트폴리오 ID를 기반으로 백테스트를 실행하며, 최종 Sharpe 비율을 계산합니다.
    """
    # 포트폴리오 할당 데이터 가져오기
    allocation = get_portfolio_allocation(portfolio_id)

    # Backtrader 설정
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(initial_cash)

    # 데이터 로드
    load_data_from_db(cerebro, allocation, start_date=start_date, end_date=end_date)

    # 전략 추가
    cerebro.addstrategy(FixedAllocationStrategy, allocation=allocation)

    # 분석기 추가
    class PortfolioValueTracker(bt.Analyzer):
        def __init__(self):
            self.values = []

        def next(self):
            self.values.append(self.strategy.broker.getvalue())

    cerebro.addanalyzer(PortfolioValueTracker, _name="portfolio_tracker")
    risk_free_rate_series = load_risk_free_rate(start_date, end_date)

    # risk_free_rate_series의 인덱스를 datetime으로 변환
    if not isinstance(risk_free_rate_series.index, pd.DatetimeIndex):
        risk_free_rate_series.index = pd.to_datetime(risk_free_rate_series.index)

    # 백테스트 실행
    strategies = cerebro.run()

    # 결과 처리
    portfolio_tracker = strategies[0].analyzers.portfolio_tracker
    portfolio_values = np.array(portfolio_tracker.values)
    daily_returns = np.diff(portfolio_values) / portfolio_values[:-1]

    # 무위험 수익률과 길이 조정
    date_range = pd.date_range(start=start_date, end=end_date)[:len(daily_returns)]
    risk_free_rates = risk_free_rate_series.reindex(date_range, method="pad").fillna(0).values

    # 1차원 배열로 변환
    if len(risk_free_rates.shape) > 1:
        risk_free_rates = risk_free_rates.flatten()

    # Sharpe 비율 계산
    sharpe_ratio = calculate_sharpe_ratio(daily_returns, risk_free_rates)

    # 최대 낙폭(MDD) 및 총 수익률
    total_return = (portfolio_values[-1] - initial_cash) / initial_cash
    mdd = calculate_mdd(portfolio_values)

    # 결과 데이터베이스 저장
    try:
        backtest_entry = Backtests.objects.create(
            portfolio_id=portfolio_id,
            start_date=start_date,
            end_date=end_date,
            total_return=total_return,
            max_drawdown=mdd,
            sharpe_ratio=sharpe_ratio,
            rebalance_values=str(portfolio_values),
            initial_amount=initial_cash,
        )
    except Exception as e:
        print(f"Error saving backtest: {e}")

    return {
        "portfolio_id": portfolio_id,
        "total_return": total_return,
        "max_drawdown": mdd,
        "sharpe_ratio": sharpe_ratio,
    }


def run_multiple_backtests(portfolio_id, start_date, end_date, duration_days,
                           initial_cash=1000000, iterations=100):
    """
    여러 번의 백테스트를 실행하며, 데이터베이스에서 포트폴리오 및 히스토리 데이터를 로드.

    Args:
        portfolio_id: 실행할 포트폴리오의 ID.
        start_date: 전체 데이터의 시작 날짜 (YYYY-MM-DD).
        end_date: 전체 데이터의 종료 날짜 (YYYY-MM-DD).
        duration_days: 각 백테스트의 기간 (일 단위).
        initial_cash: 초기 투자 금액 (기본값 1000000).
        iterations: 백테스트 반복 횟수 (기본값 100).

    Returns:
        dict: 총 실행 결과, 각 실행의 최종 포트폴리오 가치, Sharpe Ratio, MDD 리스트를 포함.
    """

    # 실행 시간 측정
    start_time = time.time()

    # 포트폴리오 데이터 로드
    allocation = get_portfolio_allocation(portfolio_id)

    # 결과 저장
    portfolio_values = []
    sharpe_ratios = []
    mdds = []

    for i in range(iterations):
        # 고정된 기간으로 무작위 시작일과 종료일 생성
        random_start_date, random_end_date = generate_fixed_date_range(start_date, end_date, duration_days)

        print(f"백테스트 {i + 1}/{iterations}: {random_start_date} ~ {random_end_date}")
        try:
            # Backtrader 설정
            cerebro = bt.Cerebro()
            cerebro.broker.set_cash(initial_cash)

            # 데이터 로드
            load_data_from_db(cerebro, allocation, start_date=random_start_date, end_date=random_end_date)

            # 전략 추가
            cerebro.addstrategy(FixedAllocationStrategy, allocation=allocation)

            # 분석기 추가
            class PortfolioValueTracker(bt.Analyzer):
                def __init__(self):
                    self.values = []

                def next(self):
                    self.values.append(self.strategy.broker.getvalue())

            cerebro.addanalyzer(PortfolioValueTracker, _name="portfolio_tracker")
            risk_free_rate_series = load_risk_free_rate(start_date, end_date)
            # 백테스트 실행
            strategies = cerebro.run()
            portfolio_tracker = strategies[0].analyzers.portfolio_tracker
            portfolio_values_list = portfolio_tracker.values

            # 결과 계산
            total_return = (portfolio_values_list[-1] - initial_cash) / initial_cash
            mdd = calculate_mdd(portfolio_values_list)
            daily_returns = np.diff(portfolio_values_list) / portfolio_values_list[:-1]
            dates = pd.date_range(start=random_start_date, end=random_end_date)[:len(daily_returns)]
            risk_free_rates = risk_free_rate_series.reindex(dates, method='pad').values
            sharpe_ratio = calculate_sharpe_ratio(daily_returns, risk_free_rates)

            # 결과 저장
            portfolio_values.append(portfolio_values_list[-1])
            sharpe_ratios.append(sharpe_ratio)
            mdds.append(mdd)

        except Exception as e:
            print(f"백테스트 {i + 1} 실패: {e}")

    # 실행 시간 측정 종료
    elapsed_time = time.time() - start_time
    print(f"전체 백테스트 실행 시간: {elapsed_time:.2f}초")

    # 결과 반환
    return {
        "final_portfolio_values": portfolio_values,
        "sharpe_ratios": sharpe_ratios,
        "mdds": mdds,
    }


def generate_fixed_date_range(start_date, end_date, duration_days):
    """
    고정된 기간을 기반으로 무작위 시작일과 종료일 생성.

    Args:
        start_date (str): 전체 데이터의 시작 날짜.
        end_date (str): 전체 데이터의 종료 날짜.
        duration_days (int): 고정된 기간 (일 단위).

    Returns:
        tuple: 무작위 시작일 및 종료일 (YYYY-MM-DD 형식).
    """
    import random
    from datetime import datetime, timedelta

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # 시작일은 종료일에서 고정 기간만큼의 여유를 둬야 함
    random_start = start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days - duration_days)
    )
    random_end = random_start + timedelta(days=duration_days)

    return random_start.strftime("%Y-%m-%d"), random_end.strftime("%Y-%m-%d")
