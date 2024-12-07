# stockapp/urls.py
from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('portfolios/', PortfolioList.as_view(), name='portfolio_list'),
    path('portfolios/stock_list/<str:portfolio_id>/', PortfolioStockList.as_view(), name='PortfolioStockList'),
]
