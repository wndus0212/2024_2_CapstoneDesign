# stockapp/utils.py

import requests
from django.core.cache import cache
from django.http import JsonResponse
import yfinance as yf
import FinanceDataReader as fdr
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# API 키와 Secret 키 입력
client_id = "PSekA1zSBGgE4mJCmCgT06UTivilW4ZmLCim"
client_key = "PfTX7zfZ26lV2OtzRGXYcB1g5/zSiq6FSwtfunbFqkLiM+Y4ljrd6NOiAurW2IvC4q5Xbmtx3FPOnUEfnn91lZ/+o9FL20G90440ALEZ2ozKUfw/RbREh8OXwg0G8LvCfm22OaIzVJBJeMi8kZNBhs+tw4CipqsuV+v6EWgi1Lv6gyDyUEE="

# 토큰 발급
def get_access_token():
    # 캐시에서 토큰을 확인
    access_token = cache.get('access_token')
    if access_token:
        return access_token  # 캐시에서 토큰을 찾았으면 바로 반환

    # 토큰 발급 API 호출
    url = "https://openapi.koreainvestment.com:9443/oauth2/tokenP"
    headers = {
        "content-type": "application/json"
    }
    payload = {
        "grant_type": "client_credentials",
        "appkey": client_id,
        "appsecret": client_key
    }
    response = requests.post(url, headers=headers, json=payload)
    
    # 토큰을 발급받았으면 캐시에 저장 (24시간 동안 유효)
    access_token = response.json().get("access_token")
    if access_token:
        cache.set('access_token', access_token, timeout=86400)  # 86400초 = 24시간
    return access_token

# 주식 일봉 데이터 요청
def get_stock_daily_candles(access_token, symbol, timeframe='D'):
    url = f"https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/inquire-daily-price"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "content-type": "application/json",
        "appKey": client_id,
        "appSecret": client_key,
        "tr_id": "FHKST01010400"  # 일봉 조회 API TR_ID
    }
    params = {
        "FID_COND_MRKT_DIV_CODE": "J",  # 코스피(J) / 코스닥(K) 선택
        "FID_INPUT_ISCD": symbol,       # 종목 코드 입력
        "FID_PERIOD_DIV_CODE": timeframe, # 'D'는 일봉, 'W'는 주봉, 'M'은 월봉
        "FID_ORG_ADJ_PRC": "0"          # 수정 주가 적용 여부 (0: 미적용, 1: 적용)
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_stock_data(symbol):
    try:
        stock_data = yf.Ticker(symbol)
        stock_info = stock_data.info
        price = stock_info.get('currentPrice', None)
        market_cap = stock_info.get('marketCap', None)
        vol = stock_info.get('volume', None)
        return price, market_cap, vol
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None, None, None
    
# 주식 리스트 데이터 요청
import json
import FinanceDataReader as fdr
import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from django.http import JsonResponse

def get_stock_data(symbol):
    try:
        stock_data = yf.Ticker(symbol)
        stock_info = stock_data.info
        price = stock_info.get('currentPrice', None)
        market_cap = stock_info.get('marketCap', None)
        vol = stock_info.get('volume', None)
        return price, market_cap, vol
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None, None, None

def get_stock_list(market, sort):
    try:
        # KRX 종목 리스트 가져오기
        stocks = fdr.StockListing(market).head(50)

        # 심볼에 '.KS' 또는 '.KQ' 추가
        symbols = [
            f"{code}.{'KS' if Market == 'KOSPI' else 'KQ'}"
            for code, Market in zip(stocks['Code'], stocks['Market'])
        ]
        names = stocks['Name'].tolist()

        # 병렬로 데이터 가져오기
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(get_stock_data, symbols))

        # 결과 처리
        prices, market_caps, volume = zip(*results)
        prices = [price if price is not None else 0 for price in prices]
        market_caps = [market_cap if market_cap is not None else 0 for market_cap in market_caps]
        volume = [vol if vol is not None else 0 for vol in volume]

        # 데이터프레임 생성
        data = {
            'symbols': symbols,
            'names': names,
            'prices': prices,
            'market_caps': market_caps,
            'volume': volume
        }

        # 데이터프레임 생성 후 정렬
        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by=sort, ascending=False).head(50)

        # 결과를 JSON 형태로 변환
        stocks_json = df_sorted.to_json(orient='records', force_ascii=False)

        # JsonResponse로 반환
        return JsonResponse(json.loads(stocks_json), safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_stock_list_global(market, sort):
    try:
        # 글로벌 시장의 종목 리스트를 가져오기
        if market == 'GLB':
            sp500_stocks = fdr.StockListing("S&P500").head(50)
            nyse_stocks = fdr.StockListing("NYSE").head(50)
            nasdaq_stocks = fdr.StockListing("NASDAQ").head(50)
            stocks = pd.concat([sp500_stocks, nyse_stocks, nasdaq_stocks], ignore_index=True)
        elif market == 'SP500':
            stocks = fdr.StockListing("S&P500").head(50)
        else:
            stocks = fdr.StockListing(market).head(50)

        # 심볼과 이름을 가져옴
        symbols = stocks['Symbol'].tolist()
        names = stocks['Name'].tolist()

        # 병렬로 데이터 가져오기
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(get_stock_data, symbols))

        # 결과 처리
        prices, market_caps, volume = zip(*results)
        prices = [price if price is not None else 0 for price in prices]
        market_caps = [market_cap if market_cap is not None else 0 for market_cap in market_caps]
        volume = [vol if vol is not None else 0 for vol in volume]

        # 데이터프레임 생성
        data = {
            'symbols': symbols,
            'names': names,
            'prices': prices,
            'market_caps': market_caps,
            'volume': volume
        }

        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by=sort, ascending=False).head(50)

        # 결과를 JSON 형태로 변환
        stocks_json = df_sorted.to_json(orient='records', force_ascii=False)

        # JsonResponse로 반환
        return JsonResponse(json.loads(stocks_json), safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_stock_history(Id, start, end, period, interval):
    name = f"{Id}.KS"
    ticker = yf.Ticker(name)
    try:
        if period==0:
            df = ticker.history(start=start, end=end, interval=interval, auto_adjust=False)  
            if df.empty:
                print(f"No data found for stock {name}")
                return None
            
            return df
        else:
            df = ticker.history(period=period, interval=interval, auto_adjust=False)  
            if df.empty:
                print(f"No data found for stock {name}")
                return None
            
            return df

        
    except Exception as e:
        print(f"Error fetching data for {name}: {e}")
        return None
