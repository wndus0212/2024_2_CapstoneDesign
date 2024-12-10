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
from stockapp.utils import *
import openai
from django.views import View
from stockapp.utils import get_stock_list,get_stock_list_global
from dotenv import load_dotenv
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
history_list = os.path.join(BASE_DIR, 'data/history')
load_dotenv()
key= os.getenv('OPENAI_API_KEY')

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
                    'names': ticker.info['longName'],
                    'symbols': stock.stock_symbol,
                    'allocation': stock.allocation,
                    'prices': price * stock.allocation,
                })
            return Response(stock_data, status=status.HTTP_200_OK)
        except PortfolioStocks.DoesNotExist:
            return Response({'error': 'Portfolio not found'}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, portfolio_id):
        try:
            # 요청 데이터에서 종목 정보 가져오기
            stock_symbol = request.data.get('symbols')
            allocation = request.data.get('allocation')

            # stock_symbol과 allocation이 제공되지 않으면 오류 처리
            if not stock_symbol or allocation is None:
                return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

            # allocation이 0일 경우 해당 종목을 삭제
            if allocation == 0:
                # 해당 종목이 있는지 확인
                stock = PortfolioStocks.objects.filter(portfolio_id=portfolio_id, stock_symbol=stock_symbol).first()
                if stock:
                    stock.delete()  # 종목 삭제
                    return Response({'message': f'Stock {stock_symbol} removed from portfolio.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': f'Stock {stock_symbol} not removed from portfolio.없음'}, status=status.HTTP_200_OK)
                

            # 이미 존재하는 종목인지 확인
            existing_stock = PortfolioStocks.objects.filter(portfolio_id=portfolio_id, stock_symbol=stock_symbol).first()
            
            if existing_stock:
                # 종목이 이미 존재하면 allocation만 업데이트
                existing_stock.allocation = allocation
                existing_stock.save()
                return Response({
                    'portfolio_id': portfolio_id,
                    'symbols': stock_symbol,
                    'allocation': allocation,
                }, status=status.HTTP_200_OK)
            else:
                # 종목이 존재하지 않으면 새로 추가
                new_stock = PortfolioStocks(
                    portfolio_id=portfolio_id,
                    stock_symbol=stock_symbol,
                    allocation=allocation,
                )
                new_stock.save()
                return Response({
                    'portfolio_id': portfolio_id,
                    'symbols': stock_symbol,
                    'allocation': allocation,
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def portfolio_sum(request, portfolio_id):
    data=get_portfolio_sum(portfolio_id)
    if data is None:
        return JsonResponse({"error": "No data found for the specified stock"}, status=404)
    
    # 데이터프레임을 JSON 형식으로 변환
    data_json = data.to_dict(orient="records")  # 행별로 JSON 객체를 생성
    
    return JsonResponse({"output": data_json})


class InvestmentRecommendationView(APIView):
    def post(self, request):
        # POST로 전달된 투자 조건 가져오기
        strategy = request.data.get("strategy")
        duration = request.data.get("duration")
        amount = request.data.get("amount")
        goal = request.data.get("goal")
        market = request.data.get("market")
        risk_tolerance = request.data.get("risk_tolerance")
        name = request.data.get("name")

        stock_json_kospi = json.loads(get_stock_list("KOSPI", "market_caps").content)
        stock_json_usa = json.loads(get_stock_list_global("NASDAQ", "market_caps").content)

        # OpenAI API 호출 및 투자 추천 받기
        recommendation = self.get_investment_recommendation(
            strategy, duration, amount, goal, market, risk_tolerance, stock_json_kospi,stock_json_usa
        )
        print(key)
        # 결과 반환
        return JsonResponse({"recommendation": recommendation})

    def get_investment_recommendation(self, strategy, duration, amount, goal, market, risk_tolerance, stock_data,stock_data_global):
        print("global",stock_data_global[0]['names'])
        stock_summary = "\n".join([f"- {row['names']} ({row['symbols']}): {row['market_caps']}" for row in stock_data])
        stock_summary_global = "\n".join([f"- {row['names']} ({row['symbols']}): {row['market_caps']}" for row in stock_data_global])
        print(openai.api_key)
        prompt = f"""
        주식 투자 추천 요청:
        - 투자 전략: {strategy}
        - 기간: {duration} 년
        - 투자 금액: {amount} KRW
        - 목표 수익률: {goal}%
        - 시장: {market}
        - 리스크 감수 범위: {risk_tolerance}%

        아래는 현재 시장 상황에 따라 참고 가능한 종목 리스트입니다:
        {stock_summary}
        {stock_summary_global}
        위 조건과 국내, 해외 종목 리스트를 참고하여 포트폴리오를 종목명, 티커, 섹터, 배분 비율(%), 배분 금액(KRW)으로 구성된 표 형태로 추천해 주세요.
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",  
            messages=[
                {"role": "system", "content": "전문 주식 투자 추천 시스템입니다. 사용자가 요청한 조건에 맞는 포트폴리오와 설명을 제공합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        result = response['choices'][0]['message']['content']
        return result
    

def backtest(request, portfolio_id):
    portfolio = Portfolios.objects.filter(portfolio_id=portfolio_id).first()
    name = portfolio.name
    
    stock_quantities=getStockList(portfolio_id)
    allocation = calculate_allocation(stock_quantities)
    print(allocation)
    today = datetime.today()

    portfolio_folder = os.path.join(history_list, str(portfolio_id))
    if not os.path.exists(portfolio_folder):
        os.makedirs(portfolio_folder)\
        
    for symbol, allocation_ratio in allocation.items():  # allocation을 symbol, 비율로 순회
        print(f"Fetching data for: {symbol}")
        
        # 주식 데이터 가져오기
        data = get_stock_history_date(symbol, start=None, end=None, period='5y', interval='1d')

        if data is not None and not data.empty:
            file_path = os.path.join(portfolio_folder, f"{symbol}.csv")
            data.to_csv(file_path, index=False)
            print(f"Data for {symbol} saved to {file_path}")
        else:
            print(f"No data found for {symbol}")

    results=run_backtest(
        csv_folder=portfolio_folder,
        initial_cash=100000000,
        allocation=allocation,
        portfolio_name=name
    )
    if isinstance(results, list):
        # 리스트를 DataFrame으로 변환
        results_df = pd.DataFrame(results)

        # DataFrame을 JSON으로 변환
        data_json = results_df.to_dict(orient="records")
    else:
        print("Unexpected results format")
    
    return JsonResponse({"output": data_json})
