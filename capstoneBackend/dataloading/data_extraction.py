import numpy as np

def calculate_mdd(portfolio_values):
    """
    포트폴리오 가치 리스트에서 MDD를 계산합니다.
    """
    running_max = np.maximum.accumulate(portfolio_values)
    drawdown = (portfolio_values - running_max) / running_max
    mdd = drawdown.min()
    return mdd
