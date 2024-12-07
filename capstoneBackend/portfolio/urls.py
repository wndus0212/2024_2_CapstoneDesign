# stockapp/urls.py
from django.urls import path, include
from . import views
from .views import PortfolioList

urlpatterns = [
    path('portfolios/', PortfolioList.as_view(), name='portfolio_list'),
]
