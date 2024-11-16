import zipline
from zipline.api import order_target_percent, record, symbol, set_benchmark, schedule_function
from zipline import run_algorithm
import pandas as pd
from datetime import datetime
from zipline.utils.events import date_rules, time_rules


# CSV 파일에서 데이터 늘리기
def load_data_from_csv(csv_file):
    df = pd.read_csv(csv_file)

    # 종목 리스트와 가격 데이터 추출
    df['symbol'] = df['symbol'].str.upper()  # 종목 코드 대문자로 변환
    df.set_index('symbol', inplace=True)  # symbol을 인덱스로 설정

    # 날짜 인덱스를 가상으로 추가하기 위해 날짜 범위를 생성 (예: 2022-01-01 ~ 2024-01-01)
    date_range = pd.date_range(start='2022-01-01', end='2024-01-01', freq='B')  # 영업일 단위

    # DataFrame을 만들어서 ohlcv 데이터를 추가
    made_data = pd.DataFrame(index=date_range)

    for symbol in df.index:
        price = df.loc[symbol, 'price']
        volume = df.loc[symbol, 'volume']

        # ohlcv 데이터를 생성
        made_data[symbol] = pd.DataFrame({
            'open': price,
            'high': price*1.05,
            'low': price*0.95,
            'close': price,
            'volume': volume
        }, index=date_range)

    return made_data


# 전략 설정
def initialize(context):
    tickers_input = input("종목과 비율을 쉼표로 구분하여 입력하세요 (예: 종목1:40, 종목2:30, 종목3:20, 종목4:10): ")

    # 문자열 가공 (gpt 인풋에 따라 바뀔수도 있음)
    tickers_and_weights = tickers_input.split(",")

    # 종목과 비율을 변환
    context.assets = []
    context.target_weights = {}

    for ticker_weight in tickers_and_weights:
        ticker, weight = ticker_weight.split(":")
        ticker = ticker.strip()
        weight = float(weight.strip()) / 100

        context.assets.append(symbol(ticker))
        context.target_weights[symbol(ticker)] = weight

    # 주기적인 리밸런싱 이벤트 설정 (동적 X)
    schedule_function(rebalance, date_rules.month_start(), time_rules.market_open())


# 리밸런싱 함수
def rebalance(context, data):
    for asset in context.assets:
        target_weight = context.target_weights[asset]
        order_target_percent(asset, target_weight)  # 목표 비율에 맞춰 포지션 조정


# 거래 및 기록
def handle_data(context, data):
    # 기록할 변수들
    record(**{ticker: context.portfolio.positions[symbol(ticker)].amount for ticker in context.target_weights.keys()})

csv_file = ''  # CSV 파일 경로 (이 파일은 날짜, 종가 등 데이터를 포함해야 함!!!!!)

made_data = load_data_from_csv(csv_file)

start_date = pd.Timestamp('2022-01-01')
end_date = pd.Timestamp('2024-01-01')

# 백테스트 실행
result = run_algorithm(start=start_date,
                       end=end_date,
                       initialize=initialize,
                       handle_data=handle_data,
                       capital_base=100000,  # 초기 자본금
                       data_frequency='daily',
                       bundle='custom_bundle',  # 커스텀 데이터 번들 (삭제시 강제로 야후파이낸스에서 불러오는듯?)
                       bundle_data=made_data)  # CSV 데이터를 직접 번들로 사용하는 방법

# 백테스트 결과 확인
import matplotlib.pyplot as plt

result.portfolio_value.plot()
plt.show()

