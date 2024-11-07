# stockapp/views.py
from django.http import JsonResponse
from .utils import *

def stock_data(request):
    symbol = "005930"  # 삼성전자 종목 코드
    access_token = get_access_token()  # 토큰 발급
    daily_data = get_stock_daily_candles(access_token, symbol)  # 주식 데이터 가져오기

    # 주식 데이터를 JsonResponse로 반환
    return JsonResponse(daily_data)

def stock_rank(request):
    access_token = get_access_token()  # 토큰 발급
    rank_data = get_stock_capitalization_rank(access_token)  # 주식 데이터 가져오기

    # 주식 데이터를 JsonResponse로 반환
    return JsonResponse(rank_data)

def stock_itemchartprice(request):
    access_token = get_access_token()  # 토큰 발급
    itemchartprice_data = get_stock_capitalization_rank(access_token)  # 주식 데이터 가져오기

    # 주식 데이터를 JsonResponse로 반환
    return JsonResponse(itemchartprice_data)
