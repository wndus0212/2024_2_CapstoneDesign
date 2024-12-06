# stockapp/urls.py
from django.urls import path
from . import views
from .views import save_user

urlpatterns = [
    path('data/', views.stock_data, name='stock_data'),
    path('list/<str:market>/<str:sort>/', views.stock_list, name='stock_list'),
    path('list_global/<str:market>/<str:sort>/', views.stock_list_global, name='stock_list_global'),
    path('detail_info/<str:stock_id>/', views.stock_detail, name='stock_detail'),
    path('history/<str:stock_id>/', views.stock_history, name='stock_history'),
    path('chart/moving_average/<str:stock_id>/', views.moving_avarage, name='moving_avarage'),
    path('chart/bollinger_band/<str:stock_id>/', views.bollinger_band, name='bollinger_band'),

    path('index/<str:option>/<str:indexname>/', views.index, name='index'),
    path('stock_diff/<str:stock_id>/', views.stock_diff, name='stock_diff'),
    path('sector_diff/', views.sector_diff, name='sector_diff'),
    path('sector_stock_list/<str:sector>/', views.sector_stock_list, name='sector_stock_list'),
    path('financial_state/<str:Option>/<str:Id>/',views.financial_state, name='financial_state'),
    path('search_term/', views.search_term, name='search_term'),

    path('create_test_data/', views.create_test_data, name='create_test_data'),
    path('api/users', views.save_user, name='save_user'),
    path('api/token/verify/', views.verify_token, name='verify_token')
]
