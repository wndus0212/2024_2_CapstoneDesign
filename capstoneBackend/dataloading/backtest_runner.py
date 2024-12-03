import pandas as pd
import backtrader as bt
import re
from data_loader import load_data_from_db
from strategies import FixedAllocationStrategy
import csv
import time
from data_extraction import calculate_mdd

from data_loader import load_data_from_db

def run_backtest(initial_cash=1000000, allocation=None, start_date=None, end_date=None,
                 portfolio_name="Default Portfolio"):
    """
    단일 백테스트 실행 함수. 데이터베이스를 사용.
    """
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(initial_cash)

    # 데이터베이스에서 데이터 로드
    load_data_from_db(cerebro, allocation, start_date=start_date, end_date=end_date)

    # 전략 추가
    cerebro.addstrategy(FixedAllocationStrategy, allocation=allocation, portfolio_name=portfolio_name)

    # 백테스트 실행
    print(f"초기 투자 금액: {cerebro.broker.get_cash():,.0f}원")
    strategies = cerebro.run()
    print(f"최종 투자 금액: {cerebro.broker.get_value():,.0f}원")

    # 리밸런싱 로그 반환
    strategy = strategies[0]
    return strategy.rebalance_log


def run_multiple_backtests(csv_folder, initial_cash, allocation, portfolio_name,
                           start_date, end_date, duration_days, iterations=100, temp_dir="temp_filtered_data"):
    """
    여러 번의 백테스트 실행 함수.

    csv_folder: CSV 파일 경로
    initial_cash: 초기 투자 금액
    allocation: 투자 비율 딕셔너리
    portfolio_name: 포트폴리오 이름
    start_date: 전체 데이터의 시작 날짜 (YYYY-MM-DD)
    end_date: 전체 데이터의 종료 날짜 (YYYY-MM-DD)
    duration_days: 각 백테스트의 기간 (일 단위)
    iterations: 백테스트 반복 횟수
    temp_dir: 임시 디렉토리 경로
    """
    # 실행 시간 측정 시작
    start_time = time.time()
    results = []  # 모든 백테스트 결과 저장

    for i in range(iterations):
        # 고정된 기간으로 무작위 시작일과 종료일 생성
        random_start_date, random_end_date = generate_fixed_date_range(start_date, end_date, duration_days)

        print(f"백테스트 {i + 1}/{iterations}: {random_start_date} ~ {random_end_date}")
        try:
            # 백테스트 실행
            rebalance_results = run_backtest(
                csv_folder,
                initial_cash=initial_cash,
                allocation=allocation,
                start_date=random_start_date,
                end_date=random_end_date,
                portfolio_name=f"{portfolio_name}_{i + 1}",
                temp_dir=temp_dir
            )

            # 결과 요약
            final_cash = calculate_final_cash(rebalance_results)
            total_withdrawn = calculate_total_withdrawn(rebalance_results)

            results.append({
                "iteration": i + 1,
                "start_date": random_start_date,
                "end_date": random_end_date,
                "final_cash": final_cash,
                "total_withdrawn": total_withdrawn,
            })

        except Exception as e:
            print(f"백테스트 {i + 1} 실패: {e}")

    # 실행 시간 측정 종료
    end_time = time.time()
    elapsed_time = end_time - start_time

    # 결과 저장
    results_df = pd.DataFrame(results)
    results_df.to_csv("backtest_results_fixed_duration.csv", index=False)
    print("백테스트 결과가 'backtest_results_fixed_duration.csv'에 저장되었습니다.")

    # 실행 시간 출력
    print(f"전체 백테스트 실행 시간: {elapsed_time:.2f}초")

    return results_df

def generate_fixed_date_range(start_date, end_date, duration_days):
    """
    고정된 기간을 기반으로 무작위 시작일과 종료일 생성.

    start_date: 전체 데이터의 시작 날짜
    end_date: 전체 데이터의 종료 날짜
    duration_days: 고정된 기간 (일 단위)
    """
    import random
    import datetime

    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    # 시작일은 종료일에서 고정 기간만큼의 여유를 둬야 함
    random_start = start_date + datetime.timedelta(
        days=random.randint(0, (end_date - start_date).days - duration_days)
    )
    random_end = random_start + datetime.timedelta(days=duration_days)

    return random_start.strftime("%Y-%m-%d"), random_end.strftime("%Y-%m-%d")


def save_rebalance_log_to_csv(rebalance_log, output_file):
    """
    리밸런싱 로그를 CSV 파일로 저장합니다.

    rebalance_log: 리밸런싱 로그 리스트
    output_file: 저장할 CSV 파일 경로
    """
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["portfolio_name", "date", "ticker", "position"])  # 헤더 작성

        for entry in rebalance_log:
            portfolio_name = entry['portfolio_name']
            date = entry['date']
            for ticker, position in entry['positions'].items():
                writer.writerow([portfolio_name, date, ticker, position])


def calculate_final_cash(rebalance_results):
    """
    리밸런싱 결과에서 최종 자산 금액을 계산합니다.
    """
    if rebalance_results:
        return rebalance_results[-1].get("final_cash", 0)
    return 0


def calculate_total_withdrawn(rebalance_results):
    """
    리밸런싱 결과에서 총 인출 금액을 계산합니다.
    """
    if rebalance_results:
        return sum(entry.get("withdrawn_cash", 0) for entry in rebalance_results)
    return 0
