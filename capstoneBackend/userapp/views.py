from django.shortcuts import render
# stockapp/views.py
from django.http import JsonResponse
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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta

# Create your views here.

@csrf_exempt
def save_user(request):
    if request.method == "POST":
        try:
            # 요청 데이터 로드
            data = json.loads(request.body)
            credential = data.get("credential")
            if not credential:
                return JsonResponse({"error": "Credential is missing"}, status=400)

            # ID 토큰 검증
            try:
                idinfo = id_token.verify_oauth2_token(
                    credential,
                    requests.Request(),
                    "700784575917-c4vrf3c2gf7auollkkonsgrao3sr6191.apps.googleusercontent.com",
                )
            except ValueError as e:
                return JsonResponse({"error": "Invalid token", "details": str(e)}, status=400)

            # 사용자 정보 추출
            google_id = idinfo.get("sub")
            email = idinfo.get("email")
            name = idinfo.get("name", "")
            profile_picture = idinfo.get("picture", "")

            # 사용자 데이터베이스 업데이트 또는 생성
            user, created = Users.objects.update_or_create(
                google_id=google_id,
                defaults={
                    "email": email,
                    "username": name,
                    "profile_picture": profile_picture,
                    "created_at": datetime.now(),
                },
            )

            # JWT 토큰 생성 (1시간 만료)
            expiration_time = datetime.now(timezone.utc) + timedelta(days=7)
            token = jwt.encode(
                {
                    "user_id": user.id,
                    "exp": expiration_time,
                    "jti": str(uuid.uuid4()),
                    "token_type": "access",
                },
                settings.SECRET_KEY,
                algorithm="HS256"
            )
            # 토큰을 응답으로 반환
            return JsonResponse({"token": token}, status=200)
        
        except Exception as e:
            # 예기치 않은 오류 처리
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@api_view(['POST'])
def verify_token(request):
    token = request.headers.get('Authorization', '')[7:]  # 'Bearer ' 제거 (길이 7을 기준으로)
    print(token)
    try:
        # Access Token 검증
        decoded = AccessToken(token)
        id = decoded.payload.get('user_id')  # user_id를 payload에서 추출

        # user_id로 사용자를 조회
        user = Users.objects.get(id=id)  # 'id' 대신 'user_id' 사용

        return Response({'valid': True, 'decoded': decoded.payload, 'user': user.username}, status=status.HTTP_200_OK)
    except TokenError as e:
        # 토큰이 유효하지 않거나 만료된 경우
        return Response({'valid': False, 'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    except Users.DoesNotExist:
        # 사용자 조회 실패
        return Response({'valid': False, 'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)