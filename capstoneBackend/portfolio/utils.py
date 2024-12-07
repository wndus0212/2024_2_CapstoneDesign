import yfinance as yf
from .models import *
from django.core.cache import cache
from django.http import JsonResponse
import yfinance as yf
import FinanceDataReader as fdr
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os
from datetime import datetime, timedelta

def get_portfolio_sum(portfolio_id):
    stocks = PortfolioStocks.objects.filter(portfolio_id=portfolio_id)
    total_sum=0
    symbols = [stock.stock_symbol for stock in stocks]
    allocations = [stock.allocation for stock in stocks]
    
    # yfinance를 사용해 한 번에 여러 종목의 데이터를 가져옵니다
    tickers = yf.Tickers(" ".join(symbols))
    
    # 각 종목에 대한 가격 정보를 가져오고 합산합니다
    for i, stock in enumerate(stocks):
        ticker = tickers.tickers[stock.stock_symbol]
        price = ticker.history(period="1d")['Close'].iloc[-1]  # 최신 종가를 가져옵니다
        total_sum += price * allocations[i]
    
    return total_sum