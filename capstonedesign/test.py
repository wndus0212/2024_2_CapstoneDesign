import pandas as pd
import yfinance as yf
import FinanceDataReader as fdr

stocks = fdr.StockListing("NASDAQ")['Symbol'].tolist()

symbols = []
names = []
prices = []
market_caps = []
volume = []

# 각 종목의 주가와 시가총액 가져오기
for stock in stocks:
    try:
        # Yahoo Finance에서 해당 종목의 데이터 가져오기
        stock_data = yf.Ticker(stock)  # 종목 심볼 뒤에 '.VN'을 붙여서 Yahoo Finance에서 조회
        stock_info = stock_data.info
        
        if stock_info['quoteType'] == "ETF":
            print(stock + " is ETF")
            # 주가와 시가총액을 가져와서 리스트에 추가
            names.append(stock_info.get('longName', None))  # 'longName'이 정확한 키일 수 있습니다.
            symbols.append(stock_info.get('symbol', None))  # 'symbol' 대신 'Symbols'가 정확할 수 있습니다.
            prices.append(stock_info.get('currentPrice', None))  # 주가
            market_caps.append(stock_info.get('marketCap', None))  # 시가총액
            volume.append(stock_info.get('volume', None))  # 거래량
        else:
            print(stock + " is not ETF")
    except Exception as e:
        print(f"Error retrieving data for {stock}: {e}")
        # 오류 발생 시 해당 종목은 건너뛰고, 리스트에 추가하지 않음

# 데이터프레임 생성
data = {
    'Symbol': symbols,
    'Name': names,
    'Price': prices,
    'Market Cap': market_caps,
    'Volume': volume
}

df = pd.DataFrame(data)
print(df)
