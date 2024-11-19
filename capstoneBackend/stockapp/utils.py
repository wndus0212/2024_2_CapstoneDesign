# stockapp/utils.py

import requests
from django.core.cache import cache
from django.http import JsonResponse
import yfinance as yf
import FinanceDataReader as fdr
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
etf_file_path = os.path.join(BASE_DIR, 'data', 'Top_100_ETF_list.csv')
search_term_file_path = os.path.join(BASE_DIR, 'data', 'search_term.csv')
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

def get_etf_data(symbol):
    try:
        stock_data = yf.Ticker(symbol)
        stock_info = stock_data.info
        price = stock_info.get('previousClose', None)
        market_cap = stock_info.get('totalAssets', None)
        vol = stock_info.get('volume', None)
        return price, market_cap, vol
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None, None, None

def get_stock_list(market, sort):
    try:
        # KRX 종목 리스트 가져오기
        stocks = fdr.StockListing(market).head(100)

        # 심볼에 '.KS' 또는 '.KQ' 추가
        symbols = [
            f"{code}.{'KS' if Market == 'KOSPI' else 'KQ'}"
            for code, Market in zip(stocks['Code'], stocks['Market'])
        ]
        names = stocks['Name'].tolist()
        prices = stocks['Close'].tolist()
        market_caps = stocks['Marcap'].tolist()
        volume = stocks['Volume'].tolist()


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
        if market == 'SP500':
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

def get_etf_list(sort):
    try:
        # KRX 종목 리스트 가져오기
        stocks = fdr.StockListing('ETF/KR').head(50)

        # 심볼에 '.KS' 또는 '.KQ' 추가
        symbols = stocks['Symbol']+'.KS'
        names = stocks['Name'].tolist()
        prices = stocks['Price'].tolist()
        market_caps = stocks['MarCap'].tolist()
        volume = stocks['Volume'].tolist()

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
    
def get_etf_list_global(sort):
    try:
        # KRX 종목 리스트 가져오기
        stocks = pd.read_csv(etf_file_path)
        symbols = stocks['symbols']
        names = stocks['names'].tolist()
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(get_etf_data, symbols))

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



def get_stock_detail_info(access_token, Id):
    if Id.endswith(".KS") or Id.endswith(".KQ"):
        id=Id[:6]
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
            "PDNO":id,
            "PRDT_TYPE_CD":"300"
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    else:
        stock=yf.Ticker(Id)
        # 결과를 JSON 형태로 변환
        stocks_json = stock.to_json(orient='records', force_ascii=False)

        # JsonResponse로 반환
        return JsonResponse(json.loads(stocks_json), safe=False)

def get_stock_history(Id, start=None, end=None, period=0, interval='1d'):
    ticker = yf.Ticker(Id)
    try:
        if period == 0:
            # 특정 기간의 데이터를 가져오기
            df = ticker.history(start=start, end=end, interval=interval, auto_adjust=False)
        else:
            # 최근 기간 데이터를 가져오기
            df = ticker.history(period=period, interval=interval, auto_adjust=False)
        
        if df.empty:
            print(f"No data found for stock {Id}")
            return None
        
        # 필요한 컬럼만 선택
        selected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if all(col in df.columns for col in selected_columns):
            return df[selected_columns]
        else:
            print(f"Some required columns are missing in the data for stock {Id}.")
            return None
        
    except Exception as e:
        print(f"Error fetching data for {Id}: {e}")
        return None

def get_stock_index(Id):
    try:
        if Id=='SP500':
            df=fdr.DataReader('S&P500','2024-06')
        else:
            df = fdr.DataReader(Id,'2024')
        if df.empty:
            print(f"No data found for stock {Id}")
            return None
        
        return df
        
    except Exception as e:
        print(f"Error fetching data for {Id}: {e}")
        return None

def get_sector_weight():
    sectors = ['technology', 'financial-services', 'consumer-cyclical', 'healthcare', 
               'communication-services', 'industrials', 'consumer-defensive', 
               'energy', 'real-estate', 'basic-materials', 'utilities']
    
    market_weight = []

    for sector in sectors:
        # 섹터 데이터 가져오기
        try:
            sector_data = yf.Sector(sector).overview
            if sector_data is not None:
                weight = sector_data.get('market_weight', 0)  # 값이 없으면 0으로 처리
                market_weight.append(weight)
            else:
                print(f"No data for sector: {sector}")  # 디버깅 출력
                market_weight.append(0)  # 기본값 0 추가
        except Exception as e:
            print(f"Error fetching data for sector {sector}: {e}")
            market_weight.append(0)  # 오류 발생 시 기본값 0 추가

    # 데이터프레임 생성
    df = pd.DataFrame({
        'sector': sectors,
        'market_weight': market_weight
    })

    return df.to_dict(orient='records')

def get_financial_statement(Id, Option):
    stock = yf.Ticker(Id)
    
    if Option=='1':
        financial_state=stock.income_stmt
    elif Option=='2':
        financial_state=stock.balance_sheet
    else:
        financial_state=stock.cashflow
    
    if financial_state is not None:
        financial_state = financial_state.T  # 전치하여 년도를 행으로 변환
    
    return financial_state

def get_search_term():
    stocks = pd.read_csv(search_term_file_path)
    return stocks