# stockapp/views.py
from django.http import JsonResponse
from .utils import *

def stock_data(request):
    symbol = "005930"  # 삼성전자 종목 코드
    access_token = get_access_token()  # 토큰 발급
    daily_data = get_stock_daily_candles(access_token, symbol)  # 주식 데이터 가져오기

    # 주식 데이터를 JsonResponse로 반환
    return JsonResponse(daily_data)

def stock_list(request, market, sort):
    if market=='KOR_ETF':
        list = get_etf_list(sort=sort)  # 주식 데이터 가져오기
        return list
    else:
        list = get_stock_list(market=market, sort=sort)  # 주식 데이터 가져오기
        return list
    
def stock_list_global(request, market, sort):
    if market=='GLB_ETF':
        list = get_etf_list_global(sort=sort)  # 주식 데이터 가져오기
        return list
    else:
        list = get_stock_list_global(market=market, sort=sort)  # 주식 데이터 가져오기
        return list

def stock_detail(request, stock_id):
    print(f"Requested stock_id: {stock_id}")
    access_token = get_access_token()  # 토큰 발급
    data = get_stock_detail_info(access_token, id)  # 주식 데이터 가져오기
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

def stock_index(request, Id):
    data = get_stock_index(Id=Id)  # 주식 데이터 가져오기
    if data is None:
        return JsonResponse({"error": "No data found for the specified stock"}, status=404)
    
    # 데이터프레임을 JSON 형식으로 변환
    data_json = data.to_dict(orient="records")  # 행별로 JSON 객체를 생성
    
    return JsonResponse({"output": data_json})

def sector_weight(request):
    try:
        # 섹터 데이터 가져오기
        data = get_sector_weight()
        if data is None or data.empty:  # 데이터가 비어 있는 경우
            return JsonResponse({"error": "No data found for the sectors"}, status=404)
        
        # 정상 응답 반환
        return JsonResponse({"output": data}, safe=False)
    except Exception as e:
        print(f"Error in sector_weight: {e}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)
    
def financial_state(request, Id, Option):
    try:
        # 재무 데이터 가져오기
        data = get_financial_statement(Id, Option)
        
        # 데이터가 없거나 비어있으면 에러 반환
        if data is None or data.empty:  
            return JsonResponse({"error": "No data found for the financial statement"}, status=404)
        
        # NaN 값을 처리하거나 제거할 필요가 있을 경우 (예시: NaN을 0으로 대체)
        data = data.fillna(0)  # NaN을 0으로 대체 (원하는 방법으로 처리 가능)
        
        # DataFrame을 JSON으로 변환
        result = data.to_dict(orient="records")  # 각 행을 딕셔너리 형태로 변환
        
        return JsonResponse({"output": result}, safe=False)  # JSON으로 반환
    except Exception as e:
        print(f"Error in financial_state: {e}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)
    
def search_term(request):
    try:
        data=get_search_term()
        if data is None or data.empty:  
            return JsonResponse({"error": "No data found for the financial statement"}, status=404)
        
        # NaN 값을 처리하거나 제거할 필요가 있을 경우 (예시: NaN을 0으로 대체)
        data = data.fillna(0)  # NaN을 0으로 대체 (원하는 방법으로 처리 가능)
        
        # DataFrame을 JSON으로 변환
        result = data.to_dict(orient="records")  # 각 행을 딕셔너리 형태로 변환
        
        return JsonResponse({"output": result}, safe=False)  # JSON으로 반환
    except Exception as e:
        print(f"Error in financial_state: {e}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)