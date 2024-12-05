import numpy as np

def calculate_mdd(portfolio_values):
    """
    포트폴리오 가치 리스트에서 MDD를 계산합니다.
    """
    running_max = np.maximum.accumulate(portfolio_values)
    drawdown = (portfolio_values - running_max) / running_max
    mdd = drawdown.min()
    return mdd

def calculate_sharpe_ratio(portfolio_returns, risk_free_rate=0.0):
    """
    포트폴리오 수익률로부터 Sharpe Ratio를 계산합니다.

    Args:
        portfolio_returns: 포트폴리오의 일일 수익률 리스트 또는 NumPy 배열.
        risk_free_rate: 무위험 수익률 (기본값 0.0).

    Returns:
        Sharpe Ratio (float). 변동성이 없는 경우 0을 반환.
    """
    # 초과 수익률 계산
    excess_returns = portfolio_returns - risk_free_rate

    # 초과 수익률의 평균
    mean_excess_return = np.mean(excess_returns)

    # 초과 수익률의 표준 편차
    std_dev_excess_return = np.std(excess_returns)

    # 표준 편차가 0인 경우 (변동성이 없는 경우)
    if std_dev_excess_return == 0:
        return 0  # Sharpe Ratio를 0으로 처리

    # Sharpe Ratio 계산
    sharpe_ratio = mean_excess_return / std_dev_excess_return
    return sharpe_ratio
