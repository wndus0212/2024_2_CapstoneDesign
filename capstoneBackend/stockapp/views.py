# stockapp/views.py
from django.http import JsonResponse
from .utils import *

def stock_data(request):
    symbol = "005930"  # 삼성전자 종목 코드
    access_token = get_access_token()  # 토큰 발급
    daily_data = get_stock_daily_candles(access_token, symbol)  # 주식 데이터 가져오기

    # 주식 데이터를 JsonResponse로 반환
    return JsonResponse(daily_data)

def stock_list(request, market):
    list = get_stock_list(market=market)  # 주식 데이터 가져오기
    # 주식 데이터를 JsonResponse로 반환 (safe=False 추가)
    return list

def stock_detail(request, stock_id):
    print(f"Requested stock_id: {stock_id}")
    access_token = get_access_token()  # 토큰 발급
    data = get_stock_detail_info_kor(access_token, stock_id)  # 주식 데이터 가져오기
    return JsonResponse(data)

def stock_history(request, stock_id):
    start = request.GET.get('start')
    end = request.GET.get('end')
    period = request.GET.get('period')
    interval = request.GET.get('interval')
    
    data = get_stock_history(Id=stock_id, start=start, end=end, period=period, interval=interval)  # 주식 데이터 가져오기
    if data is None:
        return JsonResponse({"error": "No data found for the specified stock"}, status=404)
    
    # 데이터프레임을 JSON 형식으로 변환
    data_json = data.to_dict(orient="records")  # 행별로 JSON 객체를 생성
    
    return JsonResponse({"output": data_json})
