import FinanceDataReader as fdr
import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# KRX 종목 리스트 가져오기
stocks = fdr.StockListing("KRX").head(50)
symbols = [
    f"{code}.{'KS' if Market == 'KOSPI' else 'KQ'}"
    for code, Market in zip(stocks['Code'], stocks['Market'])
]
names = stocks['Name'].tolist()

# 주식 데이터 가져오기 함수
def get_stock_data(symbol):
    try:
        stock_data = yf.Ticker(symbol)
        stock_info = stock_data.info
        price = stock_info.get('currentPrice', None)
        market_cap = float(stock_info.get('marketCap', 0)) if stock_info.get('marketCap') else None
        volume = stock_info.get('volume', None)
        return price, market_cap, volume
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None, None, None

# 병렬로 데이터 가져오기
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(get_stock_data, symbols))

# 결과 처리
prices, market_caps, volume = zip(*results)
data = {
    'symbols': symbols,
    'names': names,
    'prices': prices,
    'market_caps': market_caps,
    'volume': volume
}
df = pd.DataFrame(data)
df_sorted = df.sort_values(by='market_caps', ascending=False).head(50)

print(df_sorted)
