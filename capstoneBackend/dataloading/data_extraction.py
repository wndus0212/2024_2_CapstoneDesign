import numpy as np
import pandas as pd

def load_risk_free_rate(start_date, end_date):
    """
    미국 국채 수익률 데이터를 읽고 백테스트 기간에 맞게 필터링합니다.
    """
    csv_path = "DGS10.csv"  # 실제 파일 경로
    df = pd.read_csv(csv_path, parse_dates=["DATE"])

    # 열 이름 변경
    df = df.rename(columns={"DATE": "date", "DGS10": "rate"})

    # 문제 값 처리: '.'을 NaN으로 변환
    df["rate"] = df["rate"].replace('.', None)
    df["rate"] = pd.to_numeric(df["rate"], errors="coerce")  # 숫자로 변환

    # NaN 값 대체: Forward Fill
    df["rate"].fillna(method="ffill", inplace=True)

    # 백분율을 소수로 변환
    df["rate"] = df["rate"] / 100

    # 날짜 필터링
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    print(f"Filtered data: {len(df)} rows")

    return df.set_index("date")["rate"]


def calculate_mdd(portfolio_values):
    """
    포트폴리오 가치 리스트에서 MDD를 계산합니다.
    """
    running_max = np.maximum.accumulate(portfolio_values)
    drawdown = (portfolio_values - running_max) / running_max
    mdd = drawdown.min()
    return mdd

def calculate_sharpe_ratio(portfolio_returns, risk_free_rates):
    """
    일별 수익률에 기반한 Sharpe Ratio 계산.
    Args:
        portfolio_returns: NumPy 배열, 포트폴리오의 일별 수익률.
        risk_free_rates: NumPy 배열, 일별 무위험 수익률.
    Returns:
        float: Sharpe Ratio.
    """
    # 초과 수익률 계산
    excess_returns = portfolio_returns - risk_free_rates

    # 평균 및 표준 편차 계산
    mean_excess_return = np.mean(excess_returns)
    std_dev_excess_return = np.std(excess_returns)

    if std_dev_excess_return == 0:
        return 0  # 변동성이 없는 경우

    return mean_excess_return / std_dev_excess_return
