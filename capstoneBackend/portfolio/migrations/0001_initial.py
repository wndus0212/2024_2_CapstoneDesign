# Generated by Django 5.1.3 on 2024-12-07 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolios',
            fields=[
                ('portfolio_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.TextField()),
                ('name', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Portfolios',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PortfolioStocks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portfolio_id', models.TextField(default='0')),
                ('stock_symbol', models.TextField()),
                ('allocation', models.FloatField()),
            ],
            options={
                'db_table': 'Portfolio_Stocks',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Backtests',
            fields=[
                ('backtest_id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.TextField()),
                ('end_date', models.TextField()),
                ('total_return', models.FloatField(blank=True, null=True)),
                ('annualized_return', models.FloatField(blank=True, null=True)),
                ('max_drawdown', models.FloatField(blank=True, null=True)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='portfolio.portfolios')),
            ],
            options={
                'db_table': 'Backtests',
                'managed': True,
            },
        ),
    ]
