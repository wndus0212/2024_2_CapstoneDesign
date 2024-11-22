import yfinance as yf
import pandas as pd
import FinanceDataReader as fdr
from concurrent.futures import ThreadPoolExecutor
import os
from pykrx import stock
from pprint import pprint

import yfinance as yf
import pandas as pd

def get_sector_data():
    sectors = [
        '^SP500-25', '^SP500-30', '^SP500-35', '^SP500-45',
        '^SP500-15', '^SP500-60', '^SP500-50', '^SP500-55',
        '^SP500-40', '^GSPE'
    ]
    
    sector_data_list = []

    for sector in sectors:
        try:
            ticker = yf.Ticker(sector)
            # 현재 시가총액
            current_market_cap = ticker.info.get('marketCap', None)
            print(current_market_cap)
            # 하루, 한 달, 1년 간격으로 주가 데이터 가져오기
            daily_history = ticker.history(period="1d", interval="1d")
            monthly_history = ticker.history(period="1mo", interval="1d")
            yearly_history = ticker.history(period="1y", interval="1d")
            
            if not daily_history.empty and current_market_cap is not None:
                # 하루 변화량
                daily_change = current_market_cap * ((daily_history['Close'][-1] / daily_history['Close'][0]) - 1)
                
                # 한 달 변화량
                monthly_change = current_market_cap * ((monthly_history['Close'][-1] / monthly_history['Close'][0]) - 1)
                
                # 1년 변화량
                yearly_change = current_market_cap * ((yearly_history['Close'][-1] / yearly_history['Close'][0]) - 1)
                
                # 데이터 저장
                sector_data_list.append({
                    "Sector": sector,
                    "Current Market Cap": current_market_cap,
                    "1 Day Change": daily_change,
                    "1 Month Change": monthly_change,
                    "1 Year Change": yearly_change
                })
            else:
                # 데이터가 없을 경우 처리
                sector_data_list.append({
                    "Sector": sector,
                    "Current Market Cap": None,
                    "1 Day Change": None,
                    "1 Month Change": None,
                    "1 Year Change": None
                })
        except Exception as e:
            print(f"Error fetching data for {sector}: {e}")
            sector_data_list.append({
                "Sector": sector,
                "Current Market Cap": None,
                "1 Day Change": None,
                "1 Month Change": None,
                "1 Year Change": None
            })

    # 데이터프레임 생성
    df = pd.DataFrame(sector_data_list)
    return df

# 데이터 가져오기 및 출력
sector_df = get_sector_data()
print(sector_df)
