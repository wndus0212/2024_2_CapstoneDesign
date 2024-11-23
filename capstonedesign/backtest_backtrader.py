import pandas as pd
import backtrader as bt
import os
import shutil
import re
import csv


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

    def next(self):
        for data in self.datas:
            if data._name not in self.allocation:
                continue
                # 초기 투자 금액 저장
        self.starting_cash = self.broker.get_cash()

    def next(self):
        # 리밸런싱을 위한 현재 날짜
        current_date = self.datas[0].datetime.date(0)

        # 첫 번째 리밸런싱 실행 시점 설정
        if not self.last_rebalance:
            self.last_rebalance = current_date

        # 리밸런싱: 현재 날짜와 마지막 리밸런싱 날짜 비교
        months_since_rebalance = (current_date.year - self.last_rebalance.year) * 12 + (current_date.month - self.last_rebalance.month)
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
                continue  # allocation에 포함되지 않은 종목은 건너뜀

            target_value = total_value * self.allocation.get(ticker, 0)
            current_position = self.getposition(data).size
            current_price = data.close[0]
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
            'positions': positions
        })

        print(f"리밸런싱 완료: {self.last_rebalance}")
        print(f"포트폴리오 이름: {self.params.portfolio_name}")
        print(f"포지션: {positions}")


def load_data_from_csv(cerebro, path, allocation, start_date=None, end_date=None, temp_dir="temp_filtered_data"):
    """
    cerebro: Backtrader Cerebro 인스턴스
    path: CSV 파일 경로
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
            ticker = filename.split(".")[0]
            data_path = os.path.join(path, filename)

            # CSV 데이터 읽기
            df = pd.read_csv(data_path)
            df['date'] = pd.to_datetime(df['date'])

            # 기간 필터링
            if start_date:
                df = df[df['date'] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df['date'] <= pd.to_datetime(end_date)]

            # 필터링 후 데이터가 없는 경우 건너뜀
            if df.empty:
                print(f"기간 필터링 후 {ticker} 데이터가 없습니다.")
                continue

            # 필터링된 데이터를 임시 디렉토리에 저장
            filtered_csv_path = os.path.join(temp_dir, f"filtered_{ticker}.csv")
            df.to_csv(filtered_csv_path, index=False)

            # CSV 데이터 로더
            data = bt.feeds.GenericCSVData(
                dataname=filtered_csv_path,
                dtformat='%Y-%m-%d',
                timeframe=bt.TimeFrame.Days,
                compression=1,
                headers=True,
                openinterest=-1
            )

            # Cerebro에 데이터 추가
            cerebro.adddata(data, name=ticker)


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


def cleanup_temp_files(temp_dir):
    """
    필터링된 데이터를 저장한 임시 디렉토리를 삭제합니다.
    """
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print(f"임시 데이터 디렉토리 '{temp_dir}'가 삭제되었습니다.")


def run_backtest(csv_folder, initial_cash=1000000, allocation=None, start_date=None, end_date=None,
                 portfolio_name="Default Portfolio", temp_dir="temp_filtered_data"):
    """
    백테스트 실행 함수.

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

    # CSV 데이터 로드 (기간 필터 추가)
    load_data_from_csv(cerebro, csv_folder, allocation, start_date=start_date, end_date=end_date, temp_dir=temp_dir)

    # 전략 추가
    cerebro.addstrategy(FixedAllocationStrategy, allocation=allocation, portfolio_name=portfolio_name)

    # 백테스트 실행
    print(f"초기 투자 금액: {cerebro.broker.get_cash():,.0f}원")
    strategies = cerebro.run()  # 실행된 전략 객체 리스트 반환
    print(f"최종 투자 금액: {cerebro.broker.get_value():,.0f}원")

    # 첫 번째 전략 인스턴스의 리밸런싱 로그 가져오기
    strategy = strategies[0]
    rebalance_log = strategy.rebalance_log

    # 결과 차트 표시
    cerebro.plot()

    # 임시 디렉토리 삭제
    cleanup_temp_files(temp_dir)

    # 리밸런싱 로그 저장
    sanitized_name = re.sub(r'[^\w\s-]', '', portfolio_name).replace(' ', '_')  # 안전한 파일명 생성
    output_file = f"rebalance_log_{sanitized_name}.csv"
    save_rebalance_log_to_csv(rebalance_log, output_file)

    print(f"리밸런싱 로그가 '{output_file}'에 저장되었습니다.")
    return rebalance_log


# 실행 코드
csv_folder_path = r"C:\Users\shs\Desktop\code\historys"
custom_allocation = {"AAPL": 0.5, "MSFT": 0.3, "JPM": 0.2}
portfolio_name = "Tech & Finance Portfolio"
start_date = "2020-01-01"
end_date = "2022-12-31"

# 백테스트 실행
rebalance_results = run_backtest(
    csv_folder_path,
    initial_cash=1000000,
    allocation=custom_allocation,
    start_date=start_date,
    end_date=end_date,
    portfolio_name=portfolio_name
)
