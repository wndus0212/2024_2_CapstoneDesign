from zipline.api import order, record, symbol
import zipline
import pandas as pd
import numpy as np
import time


# 전략 초기화

def initialize(context):
    context.asset = symbol(stock)
    context.short_window = 20  # 단기 이동평균 (5,10,20가능)
    context.long_window = 120  # 장기 이동평균 (120,180,240가능)


# 기간마다 실행됨
def handle_data(context, data):
    # 가격 데이터 가져오기
    price = data.current(context.asset, 'price')

    # 이동평균 계산
    short_mavg = data.history(context.asset, 'price', bar_count=context.short_window, frequency="1d").mean()
    long_mavg = data.history(context.asset, 'price', bar_count=context.long_window, frequency="1d").mean()

    # 매수/매도 로직
    if short_mavg > long_mavg:  # 단기 이동평균이 장기 이동평균을 초과하면 매수
        if not context.portfolio.positions[context.asset].amount:
            order(context.asset, 100)  # 100주 매수
    elif short_mavg < long_mavg:  # 반대로 매도
        if context.portfolio.positions[context.asset].amount:
            order(context.asset, -100)  # 100주 매도

    record(AAPL=price, short_mavg=short_mavg, long_mavg=long_mavg)


from zipline import run_algorithm
from datetime import datetime

start_date=datetime(2023,1,1)
end_date=datetime(2024,1,1)
stock=input('주식 입력:')
capital_base=int(input('초기 자산 입력:'))


result = run_algorithm(
    start=start_date,
    end=end_date,
    initialize=initialize,
    handle_data=handle_data,
    capital_base=capital_base,
    data_frequency='daily',
    bundle='bundled_data' #아직 데이터 가공이 구현x
)

import matplotlib.pyplot as plt

result.portfolio_value.plot()
plt.show()