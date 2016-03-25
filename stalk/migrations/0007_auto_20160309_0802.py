# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-09 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stalk', '0006_auto_20160309_1335'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_id', models.CharField(max_length=10, unique=True)),
                ('user_id', models.CharField(max_length=50, null=True)),
                ('user_nickname', models.CharField(max_length=50, null=True)),
                ('age', models.IntegerField()),
                ('education', models.CharField(max_length=50, null=True)),
                ('marriage', models.CharField(max_length=50, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('length_of_service', models.CharField(max_length=50, null=True)),
                ('income_scale', models.CharField(max_length=50, null=True)),
                ('credit_level', models.CharField(max_length=50, null=True)),
                ('loan_application_num', models.IntegerField()),
                ('success_application_num', models.IntegerField()),
                ('payoff_num', models.IntegerField()),
                ('credit_line', models.FloatField()),
                ('total_loan_amount', models.FloatField()),
                ('total_left_to_pay', models.FloatField()),
                ('overdue_amount', models.FloatField()),
                ('overdue_times', models.IntegerField()),
                ('critical_overdue_times', models.IntegerField()),
            ],
            options={
                'db_table': 'renrendai_borrower',
            },
        ),
        migrations.CreateModel(
            name='InvestRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_id', models.CharField(max_length=10, null=True)),
                ('user_id', models.CharField(max_length=10, null=True)),
                ('amount', models.FloatField()),
                ('lend_time', models.DateTimeField(default=b'')),
            ],
            options={
                'db_table': 'renrendai_investrecord',
            },
        ),
        migrations.CreateModel(
            name='LoanInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_id', models.CharField(max_length=10, unique=True)),
                ('title', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(max_length=15, null=True)),
            ],
            options={
                'db_table': 'renrendai_loaninfo',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_id', models.CharField(max_length=10, unique=True)),
                ('product_name', models.CharField(max_length=50, null=True)),
                ('amount', models.FloatField()),
                ('income_ratio', models.FloatField()),
                ('pay_period', models.IntegerField()),
                ('guarantee_method', models.CharField(max_length=50, null=True)),
                ('pre_pay_ratio', models.FloatField()),
                ('pay_method', models.CharField(max_length=50, null=True)),
                ('loan_detail', models.TextField()),
            ],
            options={
                'db_table': 'renrendai_product',
            },
        ),
        migrations.AlterUniqueTogether(
            name='investrecord',
            unique_together=set([('loan_id', 'user_id', 'lend_time')]),
        ),
    ]