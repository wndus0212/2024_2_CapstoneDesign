# stockapp/models.py
from django.db import models

class Stock(models.Model):
    symbol = models.CharField(max_length=10)     # 종목 코드
    date = models.DateField()                    # 거래 날짜
    opening_price = models.FloatField()          # 시가
    highest_price = models.FloatField()          # 고가
    lowest_price = models.FloatField()           # 저가
    closing_price = models.FloatField()          # 종가
    volume = models.BigIntegerField()            # 거래량

    def __str__(self):
        return f"{self.symbol} - {self.date}"
