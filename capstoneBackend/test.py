
import requests
from django.core.cache import cache
from django.http import JsonResponse
import yfinance as yf
import FinanceDataReader as fdr
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

sectors=['technology',
         'financial-services',
         'consumer-cyclical',
         'healthcare',
         'communication-services',
         'industrials',
         'consumer-defensive',
         'energy',
         'real-estate',
         'basic-materials',
         'utilities']

market_caps=[]

for sector in sectors:
    market_caps.append(yf.Sector(sector).overview['market_weight'])

print(market_caps)