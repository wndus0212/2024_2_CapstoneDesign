import pandas as pd
import os
import shutil

import pandas as pd
import os
import shutil
import backtrader as bt


def load_data_from_csv(cerebro, path, allocation, start_date=None, end_date=None, temp_dir="temp_filtered_data"):
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
            ticker = filename.split(".")[0]
            data_path = os.path.join(path, filename)

            # CSV 데이터 읽기
            df = pd.read_csv(data_path)
            df['date'] = pd.to_datetime(df['date'])  # 날짜 변환

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

    print(f"데이터 로드가 완료되었습니다. 임시 디렉토리: {temp_dir}")


def cleanup_temp_files(temp_dir):
    """
    필터링된 데이터를 저장한 임시 디렉토리를 삭제합니다.

    temp_dir: 삭제할 임시 디렉토리 경로
    """
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print(f"임시 데이터 디렉토리 '{temp_dir}'가 삭제되었습니다.")