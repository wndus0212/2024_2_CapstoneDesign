# stockapp/urls.py
from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('portfolios/', PortfolioList.as_view(), name='portfolio_list'),
    path('portfolios/stock_list/<int:portfolio_id>/', PortfolioStockList.as_view(), name='PortfolioStockList'),
    path('ai_portfolio/', InvestmentRecommendationView.as_view(), name='investment-recommendation'),
    path('backtest/<int:portfolio_id>/', view=backtest, name='backtest'),
]
