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
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
etf_file_path = os.path.join(BASE_DIR, 'data', 'Top_100_ETF.csv')
sp500_file_path=os.path.join(BASE_DIR, 'data', 'sp500.csv')
kosdaq = os.path.join(BASE_DIR, 'data\stock_list', 'kosdaq_150_with_industries.csv')
kospi = os.path.join(BASE_DIR, 'data\stock_list', 'kospi_200_with_industries.csv')
sp500 = os.path.join(BASE_DIR, 'data\stock_list', 'sp500_with_industries.csv')
search_term_file_path = os.path.join(BASE_DIR, 'data', 'search_term.csv')
sectors_list = os.path.join(BASE_DIR, 'data', 'sectors_with_korean_names.csv')
# API 키와 Secret 키 입력
client_id = "PSekA1zSBGgE4mJCmCgT06UTivilW4ZmLCim"
client_key = "PfTX7zfZ26lV2OtzRGXYcB1g5/zSiq6FSwtfunbFqkLiM+Y4ljrd6NOiAurW2IvC4q5Xbmtx3FPOnUEfnn91lZ/+o9FL20G90440ALEZ2ozKUfw/RbREh8OXwg0G8LvCfm22OaIzVJBJeMi8kZNBhs+tw4CipqsuV+v6EWgi1Lv6gyDyUEE="
koreabank_key='E5WOQZL3DAUIKF1YS69Q'

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

def get_market_cap(symbol):
    """
    특정 심볼의 시가총액 가져오기
    """
    try:
        stock_data = yf.Ticker(symbol)
        stock_info = stock_data.info
        return stock_info.get('marketCap', None)
    except Exception as e:
        print(f"Error fetching market cap for {symbol}: {e}")
        return None

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



def get_stock_detail_info(Id):
    ticker = yf.Ticker(Id)
    try:
        ticker_info=ticker.info
        print(ticker)
        return ticker_info
    
    except Exception as e:
        print(f"Error fetching data for {Id}: {e}")
        return None

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


def get_index(option, indexname, start, end, period, interval):
    if option == 'sector':
        sectors = [
            {'ticker': 'XLY', 'name': 'Consumer Discretionary'},
            {'ticker': 'XLC', 'name': 'Communication Services'},
            {'ticker': 'XLF', 'name': 'Financials'},
            {'ticker': 'XLI', 'name': 'Industrials'},
            {'ticker': 'XLE', 'name': 'Energy'},
            {'ticker': 'XLB', 'name': 'Materials'},
            {'ticker': 'XLV', 'name': 'Health Care'},
            {'ticker': 'XLP', 'name': 'Consumer Staples'},
            {'ticker': 'XLK', 'name': 'Technology'},
            {'ticker': 'XLRE', 'name': 'Real Estate'},
            {'ticker': 'XLU', 'name': 'Utilities'}
        ]  
        
        sector_data = []
        # 각 섹터별 데이터 가져오기
        for sector in sectors:
            try:
                ticker = sector['ticker']  # 티커만 사용
                if indexname=='KOSPI':
                    period='5d'
                    interval='1d'
                df = get_stock_history(ticker, start, end, period, interval)  # 수정된 부분
                if df is not None and not df.empty:  # 데이터가 존재하고 비어있지 않은지 확인
                    sector_info = yf.Ticker(ticker).info
                    stock_history_json = df.reset_index().to_dict(orient='records')
                    name = sector_info.get('name', None)
                    
                    sector_data.append({
                        'Sector': sector['name'],  # 섹터 이름 사용
                        'Stock History': stock_history_json
                    })
                else:
                    print(f"No data found for {sector['name']}")
            except Exception as e:
                print(f"Error fetching data for {sector['name']}: {e}")

        # 데이터프레임으로 변환
        if sector_data:
            df = pd.DataFrame(sector_data)
            return df
    
        else:
            return None  # 데이터를 못 구한 경우 None 반환
    else:
        df = get_stock_history(indexname, start, end, period, interval)
        
        if df is not None and not df.empty:
            return df
        else:
            print(f"No data found for {indexname}")
            return None  # 데이터가 없으면 None 반환

def get_stock_diff(symbol):
    try:
        stock_data = yf.Ticker(symbol)
        stock_info = stock_data.info
        price = stock_info.get('currentPrice', None)
        name=stock_info.get('name', None)
        # 과거 주가 데이터 가져오기
        history = stock_data.history(period='ytd')  # 1년 데이터
        if stock_info['quoteType']=='Stock':
            price=stock_info['currentPrice']
        else:
            price=history['Close'].iloc[-1] if len(history)>1 else None

        d_close = history['Close'].iloc[-2] if len(history) > 1 else None
        m_close = history['Close'].shift(20).iloc[-1] if len(history) > 20 else None
        y_close = history['Close'].iloc[0] if len(history) > 0 else None

        # 시가총액 변화량 계산
        d_change = price - d_close  if d_close else 0
        m_change = price - m_close if m_close else 0
        y_change = price - y_close if y_close else 0

        # 퍼센트로 변화량 계산
        d_change_percent = (d_change / (d_close)) * 100 if d_change else 0
        m_change_percent = (m_change / (m_close)) * 100 if m_change else 0
        y_change_percent = (y_change / (y_close )) * 100 if y_change else 0

        data = {
            'Symbol': [symbol],
            'Name': [name],
            'Current Price': [price],
            '1 Day Change': [d_change],
            '1 Day Change per': [d_change_percent],
            '1 Month Change': [m_change],
            '1 Month Change per': [m_change_percent],
            '1 Year Change': [y_change],
            '1 Year Change per': [y_change_percent]
        }

        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None, None, None
    
def get_sector_diff(request):
    sectors = pd.read_csv(sectors_list)  # 섹터 목록 CSV 파일 읽기
    sector_changes = []

    for _, sector in sectors.iterrows():  # 각 섹터에 대해 반복
        symbol = sector['ticker']
        name_ko = sector['name_ko']
        name = sector['name']

        # get_stock_diff 함수 호출하여 변화량 데이터를 가져오기
        stock_diff_df = get_stock_diff(symbol)

        if stock_diff_df is not None:  # 데이터가 있는 경우
            # 이름과 한글 이름을 데이터프레임에 추가
            stock_diff_df['name'] = name
            stock_diff_df['name_ko'] = name_ko
            
            sector_changes.append(stock_diff_df)

    # 모든 섹터에 대해 가져온 데이터프레임을 하나로 결합
    if sector_changes:
        combined_df = pd.concat(sector_changes, ignore_index=True)
        
        # 하루 변화량 기준으로 정렬
        combined_df = combined_df.sort_values(by='1 Day Change per', ascending=False)

        return combined_df
    else:
        return None

def get_sector_stock_list(sector):
    # KOSPI 데이터 읽기
    kospi_list = pd.read_csv(kospi, dtype={'Symbol': str})
    kospi_list['Symbol'] +='.KS'
    kospi_sector_stocks = kospi_list[kospi_list['Sector'] == sector].head(5)
    kospi_sector_stocks['Market'] = 'KOSPI'  # KOSPI 시장 추가

    # KOSDAQ 데이터 읽기
    kosdaq_list = pd.read_csv(kosdaq, dtype={'Symbol': str})
    kosdaq_list['Symbol'] +='.KQ'
    kosdaq_sector_stocks = kosdaq_list[kosdaq_list['Sector'] == sector].head(5)
    kosdaq_sector_stocks['Market'] = 'KOSDAQ'  # KOSDAQ 시장 추가

    # S&P500 데이터 읽기
    sp500_list = pd.read_csv(sp500, dtype={'Symbol': str})
    sp500_sector_stocks = sp500_list[sp500_list['Sector'] == sector].head(5)
    sp500_sector_stocks['Market'] = 'S&P500'  # S&P500 시장 추가

    # 세 데이터프레임 합치기
    combined_df = pd.concat([kospi_sector_stocks, kosdaq_sector_stocks, sp500_sector_stocks], ignore_index=True)

    stock_data = []
    for _, stock in combined_df.iterrows():
        ticker = yf.Ticker(stock['Symbol'])
        try:
            # 시가총액 추출
            market_cap = ticker.info.get('marketCap', 0)

            stock_data.append({
                'Name': stock['Name'],
                'Symbol': stock['Symbol'],
                'Market': stock['Market'],
                'MarketCap': market_cap,
            })
        except Exception as e:
            print(f"Error fetching data for {stock['Symbol']}: {e}")
    
    # 데이터프레임 생성
    final_df = pd.DataFrame(stock_data)

    return final_df


def get_financial_statement(Id, Option):
    stock = yf.Ticker(Id)
    
    if Option=='income_stmt':
        financial_state=stock.income_stmt
    elif Option=='balance_sheet':
        financial_state=stock.balance_sheet
    else:
        financial_state=stock.cashflow

    if financial_state is not None:
        financial_state = financial_state.T  # 전치하여 년도를 행으로 변환
    
    return financial_state[:-1]

def get_moving_average(stock_id, start, end, period, interval):
    df = get_stock_history(stock_id, start, end, period, interval)
    df['MA_3'] = df['Close'].rolling(window=3).mean()
    df['MA_5'] = df['Close'].rolling(window=5).mean()
    ma_df = df[['MA_3', 'MA_5']].dropna()
    return ma_df

def get_bollinger_band(stock_id, start, end, period, interval):
    data = yf.Ticker(stock_id)
    df =get_stock_history(stock_id, start, end, period, interval)

    # 'Close' 값으로 볼린저 밴드 계산
    window = 20  # 이동평균 기간
    df['Moving Average'] = df['Close'].rolling(window=window).mean()
    df['Std Dev'] = df['Close'].rolling(window=window).std()
    df['Upper Band'] = df['Moving Average'] + (df['Std Dev'] * 2)
    df['Lower Band'] = df['Moving Average'] - (df['Std Dev'] * 2)
    df = df.dropna()
    return df

def get_search_term():
    stocks = pd.read_csv(search_term_file_path)
    return stocks

def get_kor_bond(name, start, end):
    koreabank_key='E5WOQZL3DAUIKF1YS69Q'
    url = 'https://ecos.bok.or.kr/api/StatisticSearch/' + koreabank_key \
            + '/json/kr/1/100/817Y002/D/'+start+'/'+end+'/010210000'
    response = requests.get(url)
    result = response.json()
    list_total_count=(int)(result['StatisticSearch']['list_total_count'])
    list_count=(int)(list_total_count/100) + 1


    rows=[]
    for i in range(0,list_count):
        starttmp = str(i * 100 + 1)
        endtmp = str((i + 1) * 100)
        
        url = 'https://ecos.bok.or.kr/api/StatisticSearch/' + koreabank_key + '/json/kr/' \
                + starttmp + '/' + endtmp + '/817Y002/D/20060101/20230315/010210000'
        response = requests.get(url)
        result = response.json()
        rows = rows + result['StatisticSearch']['row']
        
    df10y=pd.DataFrame(rows)

    df10y=df10y[['ITEM_NAME1','TIME','DATA_VALUE']]
    df10y['date']=pd.to_datetime((df10y['TIME'].str[:4] + '-' + df10y['TIME'].str[4:6] + '-' + df10y['TIME'].str[6:8]))
    df10y=df10y.astype({'DATA_VALUE':'float'})
    df10y=df10y.drop_duplicates()
    print(df10y)

def get_us_bond(name, periond):
    df = get_stock_history(name, period=periond )
    return df

def get_currency():
    usd_krw = yf.Ticker("USDKRW=X")
    usd_krw_data = usd_krw.history(period="1d")
    return usd_krw_data
