# Generated by Django 5.1.3 on 2024-12-07 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('google_id', models.TextField(unique=True)),
                ('email', models.TextField(unique=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('profile_picture', models.TextField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Users',
                'managed': True,
            },
        ),
    ]
