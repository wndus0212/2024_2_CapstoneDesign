# portfolio/serializers.py
from rest_framework import serializers
from .models import Portfolios
from .models import PortfolioStocks

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolios
        fields = '__all__'  # 모든 필드를 반환합니다.

class PortfolioStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioStocks
        fields = '__all__'  # 모든 필드를 반환합니다.
