import yfinance as yf
import pandas as pd

# Wikipedia에서 S&P 500 종목 티커 목록을 가져오기
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
tables = pd.read_html(url)

# 첫 번째 테이블이 S&P 500 종목 목록입니다.
sp500_df = tables[0]

# 티커 목록 추출
tickers = sp500_df['Symbol'].tolist()

# 각 종목의 시가총액 가져오기
def get_market_cap(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return info.get('marketCap', None)

# 시가총액 데이터 가져오기
market_caps = {}
for ticker in tickers:
    market_cap = get_market_cap(ticker)
    if market_cap:
        market_caps[ticker] = market_cap

# 시가총액 순으로 정렬
sorted_market_caps = sorted(market_caps.items(), key=lambda x: x[1], reverse=True)

# 상위 10개 종목 출력
top_10_market_caps = sorted_market_caps[:10]
for rank, (ticker, cap) in enumerate(top_10_market_caps, 1):
    print(f"{rank}. {ticker}: {cap}")
