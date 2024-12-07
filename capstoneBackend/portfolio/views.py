from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Portfolios
from .serializers import PortfolioSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound

class PortfolioList(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능
    
    def get(self, request):
        # 인증되지 않은 사용자는 처리하지 않음
        if request.user.is_authenticated:
            user_id = request.user.id
            portfolios = Portfolios.objects.filter(user_id=user_id)
            serializer = PortfolioSerializer(portfolios, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )

class PortfolioStockList(APIView):
    def get(self, request):
        portfolios = Portfolios.objects.all()
        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


