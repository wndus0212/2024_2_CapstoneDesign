import FinanceDataReader as fdr
import yfinance as yf
import pandas as pd

# 호치민 증권거래소 종목 데이터 가져오기
stocks = fdr.StockListing('KOSPI').head(5)



# 결과 확인
print(stocks)
