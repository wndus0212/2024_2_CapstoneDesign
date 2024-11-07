# stockapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.stock_data, name='stock_data'),
    path('rank/', views.stock_rank, name='stock_rank'),
    path('itemchartprice/', views.stock_itemchartprice, name='stock_itemchartprice'),
]
