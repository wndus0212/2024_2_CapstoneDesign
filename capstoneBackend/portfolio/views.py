from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import PortfolioSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
import yfinance as yf
from .utils import *

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
    def get(self, request, portfolio_id):
        try:
            # 특정 portfolio_id에 해당하는 PortfolioStock 가져오기
            stocks = PortfolioStocks.objects.filter(portfolio_id=portfolio_id)
            stock_data = []
            for stock in stocks:
                # 종목 가격을 가져옵니다
                ticker = yf.Ticker(stock.stock_symbol)
                
                # 가격을 가져올 때, 오류가 발생할 경우 0으로 설정
                try:
                    price = ticker.history(period="1d")['Close'].iloc[-1]
                except Exception as e:
                    price = 0  # 가격을 가져오지 못할 경우 기본값 0 사용

                # 종목 데이터 생성
                stock_data.append({
                    'name': ticker.info['longName'],
                    'symbol': stock.stock_symbol,
                    'allocation': stock.allocation,
                    'price': price * stock.allocation
                })
            return Response(stock_data, status=status.HTTP_200_OK)
        except PortfolioStocks.DoesNotExist:
            return Response({'error': 'Portfolio not found'}, status=status.HTTP_404_NOT_FOUND)


def portfolio_sum(request, portfolio_id):
    data=get_portfolio_sum(portfolio_id)
    if data is None:
        return JsonResponse({"error": "No data found for the specified stock"}, status=404)
    
    # 데이터프레임을 JSON 형식으로 변환
    data_json = data.to_dict(orient="records")  # 행별로 JSON 객체를 생성
    
    return JsonResponse({"output": data_json})