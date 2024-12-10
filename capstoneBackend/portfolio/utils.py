import yfinance as yf
from .models import *
from django.core.cache import cache
from django.http import JsonResponse
import yfinance as yf
import FinanceDataReader as fdr
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os
from datetime import datetime, timedelta
import pandas as pd
import backtrader as bt
import re
import csv
import time
import shutil
import numpy as np

def get_stock_history_date(Id, start=None, end=None, period=0, interval='1d'):
    ticker = yf.Ticker(Id)
    try:
        if period == 0:
            # 특정 기간의 데이터를 가져오기
            df = ticker.history(start=start, end=end, interval=interval, auto_adjust=False)
        else:
            # 최근 기간 데이터를 가져오기
            df = ticker.history(period=period, interval=interval, auto_adjust=False)
        
        if df.empty:
            print(f"No data found for stock {Id}")
            return None
        
        # 필요한 컬럼만 선택
        df = df.reset_index()
        df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
        selected_columns = ['Date','Open', 'High', 'Low', 'Close', 'Volume']
        if all(col in df.columns for col in selected_columns):
            return df[selected_columns]
        else:
            print(f"Some required columns are missing in the data for stock {Id}.")
            return None
        
    except Exception as e:
        print(f"Error fetching data for {Id}: {e}")
        return None


def getStockList(portfolio_id):
    # 특정 portfolio_id에 해당하는 PortfolioStock 가져오기
    stocks = PortfolioStocks.objects.filter(portfolio_id=portfolio_id)
    stock_data = []
    for stock in stocks:
        # 종목 가격을 가져옵니다
        ticker = yf.Ticker(stock.stock_symbol)
        
        # 가격을 가져올 때, 오류가 발생할 경우 0으로 설정
        try:
            price = ticker.history(period="1d")['Close'].iloc[-1]
        except Exception as e:
            price = 0  # 가격을 가져오지 못할 경우 기본값 0 사용

        # 종목 데이터 생성
        stock_data.append({
            'symbols': stock.stock_symbol,
            'allocation': stock.allocation,
        })
    return stock_data
    
def get_portfolio_sum(portfolio_id):
    stocks = PortfolioStocks.objects.filter(portfolio_id=portfolio_id)
    total_sum=0
    symbols = [stock.stock_symbol for stock in stocks]
    allocations = [stock.allocation for stock in stocks]
    
    # yfinance를 사용해 한 번에 여러 종목의 데이터를 가져옵니다
    tickers = yf.Tickers(" ".join(symbols))
    
    # 각 종목에 대한 가격 정보를 가져오고 합산합니다
    for i, stock in enumerate(stocks):
        ticker = tickers.tickers[stock.stock_symbol]
        price = ticker.history(period="1d")['Close'].iloc[-1]  # 최신 종가를 가져옵니다
        total_sum += price * allocations[i]
    
    return total_sum

def run_backtest(csv_folder, initial_cash=1000000, allocation=None, start_date=None, end_date=None,
                 portfolio_name="Default Portfolio", temp_dir="temp_filtered_data"):
    """
    단일 백테스트 실행 함수.

    csv_folder: CSV 파일 경로
    initial_cash: 초기 투자 금액
    allocation: 투자 비율 딕셔너리 (예: {"AAPL": 0.4, "MSFT": 0.3})
    start_date: 데이터 시작 날짜
    end_date: 데이터 종료 날짜
    portfolio_name: 포트폴리오 이름
    temp_dir: 임시 디렉토리 경로
    """
    # Cerebro 인스턴스 생성
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(initial_cash)

    # CSV 데이터 로드
    load_data_from_csv(cerebro, csv_folder, allocation, temp_dir=temp_dir)

    # 전략 추가
    cerebro.addstrategy(FixedAllocationStrategy, allocation=allocation, portfolio_name=portfolio_name)

    # 백테스트 실행
    print(f"초기 투자 금액: {cerebro.broker.get_cash():,.0f}원")
    strategies = cerebro.run()  # 실행된 전략 객체 리스트 반환
    print("strategies",strategies)
    print(f"최종 투자 금액: {cerebro.broker.get_value():,.0f}원")

    # 첫 번째 전략 인스턴스의 리밸런싱 로그 가져오기
    strategy = strategies[0]
    rebalance_log = strategy.rebalance_log
    portfolio_values = strategy.portfolio_values

    mdd = calculate_mdd(portfolio_values)
    print(f"최종 최대 손실폭 (MDD): {mdd * 100:.2f}%")

    # 임시 파일 정리
    cleanup_temp_files(temp_dir)

    # 리밸런싱 로그 저장
    sanitized_name = re.sub(r'[^\w\s-]', '', portfolio_name).replace(' ', '_')  # 안전한 파일명 생성
    output_file = f"rebalance_log_{sanitized_name}.csv"
    save_rebalance_log_to_csv(rebalance_log, output_file)

    print(f"리밸런싱 로그가 '{output_file}'에 저장되었습니다.")
    return rebalance_log

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

def calculate_mdd(portfolio_values):
    """
    포트폴리오 가치 리스트에서 MDD를 계산합니다.
    """
    running_max = np.maximum.accumulate(portfolio_values)
    drawdown = (portfolio_values - running_max) / running_max
    mdd = drawdown.min()
    return mdd

def load_data_from_csv(cerebro, path, allocation, temp_dir="temp_filtered_data"):
    """
    CSV 데이터를 로드하고 Backtrader 데이터 피드로 변환하여 Cerebro에 추가합니다.

    cerebro: Backtrader Cerebro 인스턴스
    path: CSV 파일이 있는 디렉토리 경로
    allocation: 각 종목의 투자 비율 딕셔너리
    start_date: 데이터 시작 날짜 (포맷: 'YYYY-MM-DD')
    end_date: 데이터 종료 날짜 (포맷: 'YYYY-MM-DD')
    temp_dir: 필터링된 데이터를 저장할 임시 디렉토리
    """
    # 임시 디렉토리 생성
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            ticker = filename[:-4]
            data_path = os.path.join(path, filename)

            # CSV 데이터 읽기
            df = pd.read_csv(data_path)
            
            # 데이터가 비어있는지 확인
            if df.empty:
                print(f"{ticker} 데이터가 비어있습니다.")
                continue

            # 임시 디렉토리에 필터링 없이 데이터 저장
            filtered_csv_path = os.path.join(temp_dir, f"filtered_{ticker}.csv")
            df.to_csv(filtered_csv_path, index=False)

            # CSV 데이터 로더
            data = bt.feeds.GenericCSVData(
                dataname=filtered_csv_path,
                dtformat='%Y-%m-%d',  # 날짜 형식 지정
                timeframe=bt.TimeFrame.Days,  # 일 단위 데이터
                compression=1,
                headers=True,  # 첫 번째 행을 헤더로 사용
                openinterest=-1  # 'openinterest' 열 없을 경우 -1로 설정
            )

            # Cerebro에 데이터 추가
            cerebro.adddata(data, name=ticker)

    print(f"데이터 로드가 완료되었습니다. 임시 디렉토리: {temp_dir}")

def cleanup_temp_files(temp_dir):
    """
    필터링된 데이터를 저장한 임시 디렉토리를 삭제합니다.

    temp_dir: 삭제할 임시 디렉토리 경로
    """
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print(f"임시 데이터 디렉토리 '{temp_dir}'가 삭제되었습니다.")

class FixedAllocationStrategy(bt.Strategy):
    params = (
        ('rebalance_months', 1),  # 리밸런싱 간격 (개월 수)
        ('portfolio_name', 'Default Portfolio')  # 포트폴리오 이름
    )

    def __init__(self, allocation):
        """
        allocation: 각 종목의 초기 투자 비율 딕셔너리, 예: {"AAPL": 0.4, "MSFT": 0.3, "JPM": 0.3}
        """
        self.allocation = allocation
        self.last_rebalance = None  # 마지막 리밸런싱 날짜 저장
        self.rebalance_log = []  # 리밸런싱 결과 저장 리스트
        self.portfolio_values = []

    def next(self):
        # 현재 날짜 및 포트폴리오 가치 기록
        current_date = self.datas[0].datetime.date(0)
        current_value = self.broker.get_value()
        self.portfolio_values.append(current_value)

        # 첫 번째 리밸런싱 실행 시점 설정
        if not self.last_rebalance:
            self.last_rebalance = current_date

        # 리밸런싱: 현재 날짜와 마지막 리밸런싱 날짜 비교
        months_since_rebalance = (current_date.year - self.last_rebalance.year) * 12 + (
                    current_date.month - self.last_rebalance.month)
        if months_since_rebalance >= self.params.rebalance_months:
            self.rebalance_portfolio()
            self.last_rebalance = current_date

    def rebalance_portfolio(self):
        """
        목표 비중에 맞춰 포트폴리오를 리밸런싱합니다.
        """
        total_value = self.broker.get_value()
        positions = {}  # 현재 포지션 정보 저장

        for data in self.datas:
            ticker = data._name
            if ticker not in self.allocation:
                print(ticker)
                print("allocation:",self.allocation)
                continue  # allocation에 포함되지 않은 종목은 건너뜀

            target_value = total_value * self.allocation.get(ticker, 0)
            print("target value",target_value)
            current_position = self.getposition(data).size
            current_price = data.close[0]
            print("current_price",current_price)
            target_position = target_value // current_price

            if current_position < target_position:
                self.buy(data=data, size=target_position - current_position)
            elif current_position > target_position:
                self.sell(data=data, size=current_position - target_position)

            # 포지션 정보 저장 (allocation에 포함된 종목만 기록)
            positions[ticker] = target_position

        # 리밸런싱 로그 저장
        self.rebalance_log.append({
            'portfolio_name': self.params.portfolio_name,
            'date': self.last_rebalance,
            'portfolio_value': total_value,
            'positions': positions,
        })

        print(f"리밸런싱 완료: {self.last_rebalance}")
        print(f"포트폴리오 이름: {self.params.portfolio_name}")
        print(f"포지션: {positions}")

def calculate_allocation(stock_quantities):
    """
    주식과 개수 배열을 입력받아 할당 비율을 계산합니다.

    stock_quantities: [("AAPL", 50), ("MSFT", 30), ("JPM", 20)]
    return: {"AAPL": 0.5, "MSFT": 0.3, "JPM": 0.2}
    """
    total_quantity = sum(stock['allocation'] for stock in stock_quantities)  # allocation 값을 합산
    allocation = {stock['symbols']: stock['allocation'] / total_quantity for stock in stock_quantities}  # 비율 계산
    return allocation