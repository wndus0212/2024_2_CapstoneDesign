import yfinance as yf
import pandas as pd

stock=yf.Ticker('AAPL')
print(stock.cashflow)