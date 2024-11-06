# stockapp/views.py
from django.http import JsonResponse
from .utils import get_access_token, get_stock_daily_candles  # 위에서 작성한 함수들

def stock_data(request):
    symbol = "005930"  # 삼성전자 종목 코드
    access_token = get_access_token()  # 토큰 발급
    daily_data = get_stock_daily_candles(access_token, symbol)  # 주식 데이터 가져오기

    # 주식 데이터를 JsonResponse로 반환
    return JsonResponse(daily_data)
