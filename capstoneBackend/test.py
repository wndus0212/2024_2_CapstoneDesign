import yfinance as yf
import pandas as pd
import FinanceDataReader as fdr
from concurrent.futures import ThreadPoolExecutor
import os
from pykrx import stock
from pprint import pprint
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'stockapp\data\stock_list', 'sp500_with_industries.csv')

koreabank_key='E5WOQZL3DAUIKF1YS69Q'
url = 'https://ecos.bok.or.kr/api/StatisticSearch/' + koreabank_key \
        + '/json/kr/1/100/817Y002/D/20070101/20230315/010210000'
response = requests.get(url)
result = response.json()
list_total_count=(int)(result['StatisticSearch']['list_total_count'])
list_count=(int)(list_total_count/100) + 1


rows=[]
for i in range(0,list_count):
    start = str(i * 100 + 1)
    end = str((i + 1) * 100)
    
    url = 'https://ecos.bok.or.kr/api/StatisticSearch/' + koreabank_key + '/json/kr/' \
            + start + '/' + end + '/817Y002/D/20070101/20230315/010210000'
    response = requests.get(url)
    result = response.json()
    rows = rows + result['StatisticSearch']['row']
    
df10y=pd.DataFrame(rows)

df10y=df10y[['ITEM_NAME1','TIME','DATA_VALUE']]
df10y['date']=pd.to_datetime((df10y['TIME'].str[:4] + '-' + df10y['TIME'].str[4:6] + '-' + df10y['TIME'].str[6:8]))
df10y=df10y.astype({'DATA_VALUE':'float'})
df10y=df10y.drop_duplicates()
print(df10y)