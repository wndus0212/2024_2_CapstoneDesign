
import yfinance as yf
import FinanceDataReader as fdr

stocks = fdr.StockListing('KRX') # KRX: 2,663 종목(=코스피+코스닥+코넥스)
print(stocks)