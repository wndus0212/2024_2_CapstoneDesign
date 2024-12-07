from django.db import models

# Create your models here.
class Backtests(models.Model):
    backtest_id = models.AutoField(primary_key=True, blank=True)
    portfolio = models.ForeignKey('Portfolios', models.DO_NOTHING)
    start_date = models.TextField()
    end_date = models.TextField()
    total_return = models.FloatField(blank=True, null=True)
    annualized_return = models.FloatField(blank=True, null=True)
    max_drawdown = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Backtests'


class PortfolioStocks(models.Model):
    portfolio_id = models.TextField(default='0')
    stock_symbol = models.TextField()
    allocation = models.FloatField()

    class Meta:
        managed = True
        db_table = 'Portfolio_Stocks'


class Portfolios(models.Model):
    portfolio_id = models.AutoField(primary_key=True, blank=True)
    user_id = models.TextField()
    name = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'Portfolios'