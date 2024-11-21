import yfinance as yf
import pandas as pd
import FinanceDataReader as fdr
from concurrent.futures import ThreadPoolExecutor
import os
from pykrx import stock
from pprint import pprint

def get_financial_statement(Id, Option):
    stock = yf.Ticker(Id)
    
    if Option=='incom_stmt':
        financial_state=stock.income_stmt
        required_columns = ['Total Revenue','Cost Of Revenue', 'Gross Profit','Operating Income','Net Income']
        filtered_data = financial_state[required_columns]
    elif Option=='balance_sheet':
        financial_state=stock.balance_sheet
        required_columns = ['Current Assets ', 'Total Non Current Assets ', 'Current Liabilities ', 'Total Non Current Liabilities Net Minority Interest']
        filtered_data = financial_state[required_columns]
    else:
        financial_state=stock.cashflow
        required_columns = ['Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow', 'Cash And Cash Equivalents']
        filtered_data = financial_state[required_columns]
    if financial_state is not None:
        financial_state = financial_state.T  # 전치하여 년도를 행으로 변환
    
    return filtered_data


print(yf.Ticker("MSFT").income_stmt.columns)