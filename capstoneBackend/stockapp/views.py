# stockapp/views.py
from django.http import JsonResponse
from .utils import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from django.conf import settings
import json
import jwt  
import uuid
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from datetime import datetime, timezone

google_api_id="411762794275-vpjchb1sc9dgpu2ar25tkbb60u82o52o.apps.googleusercontent.com"

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
    data = get_stock_detail_info(stock_id)  # 주식 데이터 가져오기
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

def index(request, option, indexname):
    try:
        # 섹터 데이터 가져오기
        start = request.GET.get('start')
        end = request.GET.get('end')
        period = request.GET.get('period')
        interval = request.GET.get('interval')
        data = get_index(option, indexname, start, end, period, interval)
        if data.empty:  # 데이터가 비어 있는 경우
            return JsonResponse({"error": "No data found for the sectors"}, status=404)
        
        # 정상 응답 반환
        data_json = data.to_dict(orient="records")
        return JsonResponse({"output": data_json}, safe=False)
    except Exception as e:
        print(f"Error in index: {e}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)
    

def stock_diff(request, stock_id):
    try:
        # 섹터 데이터 가져오기
        data = get_stock_diff(stock_id)
        if data.empty:  # 데이터가 비어 있는 경우
            return JsonResponse({"error": "No data found for the sectors"}, status=404)
        
        # 정상 응답 반환
        data_json = data.to_dict(orient="records")
        return JsonResponse({"output": data_json}, safe=False)
    except Exception as e:
        print(f"Error in diff: {e}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)
    
def sector_diff(request):
    try:
        # 섹터 데이터 가져오기
        data = get_sector_diff(request)
        if data.empty:  # 데이터가 비어 있는 경우
            return JsonResponse({"error": "No data found for the sectors"}, status=404)
        
        # 정상 응답 반환
        data_json = data.to_dict(orient="records")
        return JsonResponse({"output": data_json}, safe=False)
    except Exception as e:
        print(f"Error in diff: {e}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)

def sector_stock_list(request, sector):
    try:
        data=get_sector_stock_list(sector)
        if data.empty:  # 데이터가 비어 있는 경우
            return JsonResponse({"error": "No data found for the sectors"}, status=404)
        
        # 정상 응답 반환
        data_json = data.to_dict(orient="records")
        return JsonResponse({"output": data_json}, safe=False)
    except Exception as e:
        print(f"Error in diff: {e}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)

def moving_avarage(request, stock_id):
    try:
        start = request.GET.get('start')
        end = request.GET.get('end')
        period = request.GET.get('period')
        interval = request.GET.get('interval')
        data=get_moving_average(stock_id, start, end, period, interval)
        if data.empty:  # 데이터가 비어 있는 경우
            return JsonResponse({"error": "No data found for the sectors"}, status=404)
        
        # 정상 응답 반환
        data_json = data.to_dict(orient="records")
        return JsonResponse({"output": data_json}, safe=False)
    except Exception as e:
        print(f"Error in movingaverage: {e}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)

def bollinger_band(request, stock_id):
    try:
        start = request.GET.get('start')
        end = request.GET.get('end')
        period = request.GET.get('period')
        interval = request.GET.get('interval')
        data=get_bollinger_band(stock_id, start, end, period, interval)
        if data.empty:  # 데이터가 비어 있는 경우
            return JsonResponse({"error": "No data found for the sectors"}, status=404)
        
        # 정상 응답 반환
        data_json = data.to_dict(orient="records")
        return JsonResponse({"output": data_json}, safe=False)
    except Exception as e:
        print(f"Error in bollingerband: {e}")
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
    
def kor_bonds(name, start, end, request):
    try:
        data=get_kor_bond(name, start, end)
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

def us_bonds(name, period, request):
    try:
        data=get_us_bond(name, period)
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
    
def create_test_data(request):
    # 테스트 데이터 생성
    test_data = Users.objects.create(
        user_id=1234, 
        google_id = "test",
        email ="test",
        name = "test",)
    return JsonResponse({"message": "Test data created successfully!"})

@csrf_exempt
def save_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            credential = data.get("credential")
            if not credential:
                return JsonResponse({"error": "Credential is missing"}, status=400)

            # ID 토큰 검증
            idinfo = id_token.verify_oauth2_token(
                credential,
                requests.Request(),
                "700784575917-c4vrf3c2gf7auollkkonsgrao3sr6191.apps.googleusercontent.com",
            )
            # 사용자 정보 추출
            google_id = idinfo["sub"]
            email = idinfo["email"]
            name = idinfo.get("name", "")
            profile_picture = idinfo.get("picture", "")

            # 사용자 데이터베이스 업데이트 또는 생성
            user, created = Users.objects.update_or_create(
                google_id=google_id,
                defaults={
                    "email": email,
                    "name": name,
                    "profile_picture": profile_picture,
                    "created_at": datetime.now(),
                },
            )

            # JWT 토큰 생성
            token = jwt.encode(
                {"user_id": user.user_id, "exp": datetime.now(timezone.utc) + timedelta(hours=1),"jti": str(uuid.uuid4()), "token_type": "access", }, 
                settings.SECRET_KEY, 
                algorithm='HS256'
            )

            # 토큰을 응답으로 반환
            return JsonResponse({"token": token}, status=200)
        except ValueError as e:
            return JsonResponse({"error": "Invalid token", "details": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@api_view(['POST'])
def verify_token(request):
    token = request.headers.get('Authorization', '')  # 'Bearer ' 제거
    if not token:
        return Response({"detail": "Authorization token is missing"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Access Token 검증
        decoded = AccessToken(token)
        return Response({'valid': True, 'decoded': decoded.payload}, status=status.HTTP_200_OK)
    except TokenError as e:
        # 토큰이 유효하지 않거나 만료된 경우
        return Response({'valid': False, 'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)