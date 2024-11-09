# stockapp/utils.py

import requests
from django.core.cache import cache
import yfinance as yf

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

# 주식 시가총액 순위 데이터 요청
def get_stock_capitalization_rank(access_token):
    url = f"https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/ranking/market-cap"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "content-type": "application/json",
        "appKey": client_id,
        "appSecret": client_key,
        "tr_id": "FHPST01740000",
        "custtype": "P"
    }
    params = {
        "FID_INPUT_PRICE_2": "",             # 전체 조회
        "FID_COND_MRKT_DIV_CODE": "J",       # 코스피 시장 선택
        "FID_COND_SCR_DIV_CODE": "20174",    # 고유 조건 분류 코드
        "FID_DIV_CLS_CODE": "0",             # 전체 주식
        "FID_INPUT_ISCD": "0000",            # 전체 종목
        "FID_TRGT_CLS_CODE": "0",            # 전체 대상
        "FID_TRGT_EXLS_CLS_CODE": "0",       # 전체 제외 없음
        "FID_INPUT_PRICE_1": "",             # 전체 가격
        "FID_VOL_CNT": ""                    # 전체 거래량
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_stock_detail_info_kor(access_token, Id):
    url = f"https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/search-info"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "content-type": "application/json",
        "appKey": client_id,
        "appSecret": client_key,
        "tr_id": "CTPF1604R",
        "custtype": "P"
    }
    params = {
        "PDNO":Id,
        "PRDT_TYPE_CD":"300"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_stock_history(Id, start, end, period, interval):
    name = f"{Id}.KS"
    ticker = yf.Ticker(name)
    try:
        if period==0:
            df = ticker.history(start=start, end=end, interval=interval, auto_adjust=False)  # 최근 5일 데이터 가져오기
            if df.empty:
                print(f"No data found for stock {name}")
                return None
            
            print(df)
            return df
        else:
            df = ticker.history(period=period, interval=interval, auto_adjust=False)  # 최근 5일 데이터 가져오기
            if df.empty:
                print(f"No data found for stock {name}")
                return None
            
            print(df)
            return df

        
    except Exception as e:
        print(f"Error fetching data for {name}: {e}")
        return None

def get_stock_history_purchase_amount(Id, start, end, period, interval):
    name = f"{Id}.KS"
    ticker = yf.Ticker(name)
    try:
        if period==0:
            df = ticker.history(start=start, end=end, interval=interval, auto_adjust=False)  # 최근 5일 데이터 가져오기
            if df.empty:
                print(f"No data found for stock {name}")
                return None
            
            print(df)
            return df
        else:
            df = ticker.history(period=period, interval=interval, auto_adjust=False)  # 최근 5일 데이터 가져오기
            if df.empty:
                print(f"No data found for stock {name}")
                return None
            
            print(df)
            return df

        
    except Exception as e:
        print(f"Error fetching data for {name}: {e}")
        return None