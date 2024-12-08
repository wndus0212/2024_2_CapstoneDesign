import sqlite3
import pandas as pd
import backtrader as bt
import os
def load_data_from_db(cerebro, allocation, start_date=None, end_date=None):
    """
    데이터베이스에서 데이터를 로드하여 Backtrader로 변환.
    """
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '../database.sqlite3'))

    for ticker in allocation.keys():
        query = """
            SELECT date, open AS Open, high AS High, low AS Low, close AS Close, volume AS Volume
            FROM stockapp_stockhistory
            WHERE ticker = ?
        """
        params = [ticker]
        if start_date and end_date:
            query += " AND date BETWEEN ? AND ?"
            params.extend([start_date, end_date])
        elif start_date:
            query += " AND date >= ?"
            params.append(start_date)
        elif end_date:
            query += " AND date <= ?"
            params.append(end_date)

        # 데이터 읽기
        df = pd.read_sql_query(query, conn, params=params)

        if df.empty:
            print(f"{ticker}에 대한 데이터가 없습니다.")
            continue

        # Backtrader 데이터로 변환
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        data = bt.feeds.PandasData(dataname=df)
        cerebro.adddata(data, name=ticker)

    conn.close()
    print("데이터베이스에서 데이터 로드 완료.")