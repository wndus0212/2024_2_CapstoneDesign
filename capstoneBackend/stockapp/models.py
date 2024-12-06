# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Backtests(models.Model):
    backtest_id = models.AutoField(primary_key=True, blank=True)
    portfolio = models.ForeignKey('Portfolios', models.DO_NOTHING)
    start_date = models.TextField()
    end_date = models.TextField()
    total_return = models.FloatField(blank=True, null=True)
    annualized_return = models.FloatField(blank=True, null=True)
    max_drawdown = models.FloatField(blank=True, null=True)
    sharpe_ratio = models.FloatField(blank=True, null=True)
    rebalance_values = models.TextField(blank=True, null=True)
    initial_amount = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Backtests'


class Portfolio_Stocks(models.Model):
    portfolio = models.ForeignKey('Portfolios', models.DO_NOTHING)
    stock_symbol = models.TextField()
    allocation = models.FloatField()

    class Meta:
        managed = False
        db_table = 'Portfolio_Stocks'


class Portfolios(models.Model):
    portfolio_id = models.AutoField(primary_key=True, blank=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    name = models.TextField()
    created_at = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Portfolios'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True, blank=True)
    google_id = models.TextField(unique=True)
    email = models.TextField(unique=True)
    name = models.TextField(blank=True, null=True)
    profile_picture = models.TextField(blank=True, null=True)
    created_at = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Users'

class StockHistory(models.Model):
    ticker = models.CharField(max_length=20)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.IntegerField()

    class Meta:
        unique_together = ('ticker', 'date')
        ordering = ['date']
