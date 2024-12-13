# stockapp/urls.py
from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('portfolios/', PortfolioList.as_view(), name='portfolio_list'),
    path('portfolio_sum/<int:portfolio_id>/', view=portfolio_sum, name='portfolio_sum'),
    path('portfolio_initial/<int:portfolio_id>/', view=portfolio_sum, name='portfolio_sum'),
    path('portfolios/stock_list/<int:portfolio_id>/', PortfolioStockList.as_view(), name='PortfolioStockList'),
    path('ai_portfolio/', InvestmentRecommendationView.as_view(), name='investment-recommendation'),
    path('backtest/<int:portfolio_id>/<str:period>/', view=backtest, name='backtest'),
    path('montecarlo/<int:portfolio_id>/', view=montecarlo, name='montecarlo'),
    path('history/<int:portfolio_id>/', view=portfolioHistory, name='portfolioHistory'),
    
]
