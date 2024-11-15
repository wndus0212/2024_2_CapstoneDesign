import pandas as pd
import yfinance as yf
import FinanceDataReader as fdr
from tqdm import tqdm  # 진행 상황 표시를 위한 라이브러리
from concurrent.futures import ThreadPoolExecutor

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

sp500_stocks = fdr.StockListing("S&P500").head(50)
nyse_stocks = fdr.StockListing("NYSE").head(50)
nasdaq_stocks = fdr.StockListing("NASDAQ").head(50)
stocks = pd.concat([sp500_stocks, nyse_stocks, nasdaq_stocks], ignore_index=True)
    

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
df_sorted = df.sort_values(by="market_caps", ascending=False).head(50)
print(df_sorted)
