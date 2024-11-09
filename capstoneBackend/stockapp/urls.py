# stockapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.stock_data, name='stock_data'),
    path('rank/', views.stock_rank, name='stock_rank'),
    path('detail/<str:stock_id>/', views.stock_detail, name='stock_detail'),
    path('history/<str:stock_id>/', views.stock_history, name='stock_history'),
]
