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
openai.api_key="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"


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
    return JsonResponse({"output": float(data)})

def portfolio_initial(request, portfolio_id):
    Portfolio = Portfolios.objects.filter(portfolio_id=portfolio_id)
    if Portfolio is None:
        return JsonResponse({"error": "No data found for the specified stock"}, status=404)
    
    # 데이터프레임을 JSON 형식으로 변환
    data_json = Portfolio.to_dict(orient="records")  # 행별로 JSON 객체를 생성
    
    return JsonResponse({"output": data_json})

class InvestmentRecommendationView(APIView):
    def post(self, request):
        # POST로 전달된 투자 조건 가져오기
        strategy = request.data.get("strategy")
        duration = request.data.get("duration")
        amount = request.data.get("amount")
        goal = request.data.get("goal")
        risk_tolerance = request.data.get("risk_tolerance")
        name = request.data.get("name")

        stock_json_kospi = json.loads(get_stock_list("KOSPI", "market_caps").content)
        stock_json_usa = json.loads(get_stock_list_global("NASDAQ", "market_caps").content)
        sector_diff = get_sector_diff().to_json()
        # OpenAI API 호출 및 투자 추천 받기
        recommendation = self.get_investment_recommendation(
            strategy, duration, amount, goal, risk_tolerance, stock_json_kospi,stock_json_usa,sector_diff
        )
        data, description=self.save_to_csv(response=recommendation)
        if data.empty:  # 데이터가 비어 있는 경우
            return JsonResponse({"error": "No data found for the sectors"}, status=404)
        
        # 정상 응답 반환
        data_json = data.to_dict(orient="records")
        return JsonResponse({
        "output": data_json,
        "description": description  # description도 포함
    }, safe=False)

    def put(self, request):
        try:
            # 요청 데이터에서 종목 정보 가져오기
            portfolio_name = request.data.get('name')
            portfolio_stocks = request.data.get('portfolio_data').get('output')
            user_id = request.user.id   
            new_portfolio = Portfolios(
                name=portfolio_name,
                user_id=user_id
            )
            new_portfolio.save()
            
            for stock in portfolio_stocks:
                print(stock['티커'])
                new_stock = PortfolioStocks(
                    portfolio_id=new_portfolio.portfolio_id,
                    stock_symbol=stock['티커'],
                    allocation=stock['개수'],
                )
                new_stock.save()
            return Response({
                'portfolio_id': new_portfolio.portfolio_id,
                'name':portfolio_name
            }, status=status.HTTP_201_CREATED)
   
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get_investment_recommendation(self, strategy, duration, amount, goal, risk_tolerance, stock_data,stock_data_global,sector_diff):
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
        - 리스크 감수 범위: {risk_tolerance}%

        아래는 현재 시장 상황에 따라 참고 가능한 종목 리스트입니다:
        국내:
        {stock_summary}
        해외:
        {stock_summary_global}
        
        현재 섹터별 변화량입니다:
        {sector_diff}

        위 조건과 국내, 해외 종목 리스트, 섹터 추세를 참고하여 포트폴리오를 종목명, 티커, 섹터, 배분 비율(%), 개수, 배분 금액(KRW)으로 구성된 표 형태로 추천해 주세요.
        목록에 포함된 실제 주식 가격을 사용해 주세요.
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
    
    def save_to_csv(self,response):
        print(response)
        """
        API 응답을 CSV 파일로 저장하는 함수.
        """
        # 표 데이터를 리스트로 변환
        lines = response.splitlines()
        table_data = []
        header = []
        description = []
        # 데이터 처리
        
        for line in lines:
            if line.startswith("|") and "---" not in line:  # 표의 데이터 줄만 추출
                # "|"로 구분된 데이터를 리스트로 변환 후 양쪽 공백 제거
                columns = [col.strip() for col in line.split("|") if col.strip()]
                if not header:
                    header = columns  # 첫 번째 줄을 헤더로 설정
                else:
                    table_data.append(columns)
            elif line.strip() and not line.startswith("|"):
                description.append(line.strip())

        # 데이터프레임 생성
        df = pd.DataFrame(table_data, columns=header)

        # 설명 부분을 문자열로 합침
        description_text = "\n".join(description)
        # 데이터프레임 생성
        df = pd.DataFrame(table_data, columns=header)

        # CSV로 저장
        return df,description_text

    

def backtest(request, portfolio_id, period):
    portfolio = Portfolios.objects.filter(portfolio_id=portfolio_id).first()
    name = portfolio.name
    
    stock_quantities=getStockList(portfolio_id)
    allocation = calculate_allocation(stock_quantities)
    today = datetime.today()

    portfolio_folder = os.path.join(history_list, str(portfolio_id))
    if not os.path.exists(portfolio_folder):
        os.makedirs(portfolio_folder)\
        
    for symbol, allocation_ratio in allocation.items():  # allocation을 symbol, 비율로 순회
        print(f"Fetching data for: {symbol}")
        
        # 주식 데이터 가져오기
        data = get_stock_history_date(symbol, start=None, end=None, period=period, interval='1d')
        if data is not None and not data.empty:
            file_path = os.path.join(portfolio_folder, f"{symbol}.csv")
            data.to_csv(file_path, index=False)
            print(f"Data for {symbol} saved to {file_path}")
        else:
            print(f"No data found for {symbol}")

    results, mdd=run_backtest(
        csv_folder=portfolio_folder,
        initial_cash=100000000,
        allocation=allocation,
        portfolio_name=name
    )
    if isinstance(results, list):
        # 리스트를 DataFrame으로 변환
        results_df = pd.DataFrame(results)

        # DataFrame을 JSON으로 변환
        
    else:
        print("Unexpected results format")
    data_json = results_df.to_dict(orient="records")
    return JsonResponse({"output": data_json})

def portfolioHistory(request, portfolio_id):   
    stock_list = getStockList(portfolio_id)

    portfolio = Portfolios.objects.filter(portfolio_id=portfolio_id).first()

    if not portfolio:
        raise ValueError("해당 포트폴리오를 찾을 수 없습니다.")

    # start_at 날짜 가져오기
    start_date = portfolio.created_at  # start_at은 Django 모델의 필드라고 가정

    if not stock_list:
        raise ValueError("포트폴리오에 종목이 없습니다.")

    # 모든 종목의 가격 데이터 수집
    portfolio_data = []
    for stock_info in stock_list:
        stock_symbol = stock_info.get("symbols")
        allocation = stock_info.get("allocation", 1.0)  # 기본 할당량은 1.0

        if not stock_symbol:
            continue  # 종목 심볼이 없는 경우 스킵

        # 종목의 가격 히스토리 가져오기
        stock_history = get_stock_history_date(Id=stock_symbol, period='5y')
        if stock_history is not None:
            stock_df = pd.DataFrame(stock_history)
            if stock_history.iloc[-1]['Date']<datetime.today().strftime('%Y-%m-%d'):
                next_date = datetime.today().strftime('%Y-%m-%d')

                # 마지막 행 데이터를 기반으로 새 데이터 생성
                last_row = stock_df.iloc[-1].copy()  # 마지막 행 복사
                last_row['Date'] = next_date  # 날짜를 업데이트

                # 추가된 행을 데이터프레임에 삽입
                stock_df = pd.concat([stock_history, pd.DataFrame([last_row])], ignore_index=True)
            stock_df['stock_id'] = stock_symbol  # 종목 ID 추가
            stock_df['allocation'] = allocation  # 할당량 추가
            stock_df['adjusted_close'] = stock_df['Close'] * allocation  # 할당량 적용된 종가 계산
            portfolio_data.append(stock_df)
        

    # 데이터프레임 병합
    if not portfolio_data:
        raise ValueError("종목 히스토리를 가져오지 못했습니다.")

    combined_df = pd.concat(portfolio_data, ignore_index=True)

    # 시작 날짜 이후의 데이터 필터링
    combined_df['Date'] = pd.to_datetime(combined_df['Date'])
    combined_df = combined_df[combined_df['Date'] >= pd.to_datetime(start_date)]
    # 날짜별 포트폴리오 가치 계산 (adjusted_close 합계)
    portfolio_price_trend = (
        combined_df.groupby('Date')['adjusted_close']
        .sum()
        .reset_index()
        .rename(columns={'adjusted_close': 'portfolio_value'})
    )
    data_json = portfolio_price_trend.to_dict(orient="records")
    return JsonResponse({"output": data_json})

def montecarlo(request, portfolio_id):
    portfolio = Portfolios.objects.filter(portfolio_id=portfolio_id).first()
    name = portfolio.name
    
    stock_quantities=getStockList(portfolio_id)
    allocation = calculate_allocation(stock_quantities)
    print(allocation)
    today = datetime.today()
    duration_days = 365
    overall_start_date = (datetime.today() - timedelta(days=5*365))
    portfolio_folder = os.path.join(history_list, str(portfolio_id))
    if not os.path.exists(portfolio_folder):
        os.makedirs(portfolio_folder)\
    
    for symbol, allocation_ratio in allocation.items():  # allocation을 symbol, 비율로 순회
        print(f"Fetching data for: {symbol}")
        
        # 주식 데이터 가져오기
        data = get_stock_history_date(symbol, start=None, end=None, period="5y", interval='1d')

        if data is not None and not data.empty:
            file_path = os.path.join(portfolio_folder, f"{symbol}.csv")
            data.to_csv(file_path, index=False)
            print(f"Data for {symbol} saved to {file_path}")
        else:
            print(f"No data found for {symbol}")

    results_df = run_multiple_backtests(
        csv_folder=portfolio_folder,
        initial_cash=1000000,
        allocation=allocation,
        portfolio_name=name,
        start_date=overall_start_date,
        end_date=today,
        duration_days=duration_days,
        iterations=100
    )
    print(results_df)
    data_json = results_df.to_dict(orient="records")
    return JsonResponse({"output": data_json})