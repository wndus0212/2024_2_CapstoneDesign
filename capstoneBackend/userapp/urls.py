# stockapp/urls.py
from django.urls import path
from . import views
from .views import save_user

urlpatterns = [
    path('api/users', views.save_user, name='save_user'),
    path('api/token/verify/', views.verify_token, name='verify_token')
]
