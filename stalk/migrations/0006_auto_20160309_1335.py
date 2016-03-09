# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stalk', '0005_auto_20160307_1403'),
    ]

    operations = [
        migrations.CreateModel(
            name='YrdBidder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pin', models.CharField(max_length=10)),
                ('bid_nikename', models.CharField(max_length=20, null=True)),
                ('bid_amount', models.CharField(max_length=20, null=True)),
                ('bid_time', models.CharField(max_length=20, null=True)),
            ],
            options={
                'db_table': 'yirendai_bidder',
            },
        ),
        migrations.CreateModel(
            name='YrdTender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pin', models.CharField(unique=True, max_length=10)),
                ('loan_type', models.CharField(max_length=20, null=True)),
                ('loan_url', models.CharField(max_length=50, null=True)),
                ('loan_description', models.CharField(max_length=50, null=True)),
                ('warrant_icon', models.CharField(max_length=20, null=True)),
                ('progress', models.CharField(max_length=50, null=True)),
                ('volume', models.CharField(max_length=20, null=True)),
                ('interest_rate', models.CharField(max_length=20, null=True)),
                ('term', models.CharField(max_length=20, null=True)),
                ('status', models.CharField(max_length=20, null=True)),
            ],
            options={
                'db_table': 'yirendai_tender',
            },
        ),
        migrations.CreateModel(
            name='YrdBid',
            fields=[
                ('tender', models.OneToOneField(primary_key=True, db_column=b'id', serialize=False, to='stalk.YrdTender')),
                ('interest_rate', models.CharField(max_length=20, null=True)),
                ('term', models.CharField(max_length=20, null=True)),
                ('volume', models.CharField(max_length=20, null=True)),
                ('bid_detail', models.CharField(max_length=50, null=True)),
                ('remain_amount', models.CharField(max_length=20, null=True)),
                ('nikename', models.CharField(max_length=50, null=True)),
                ('gender', models.CharField(max_length=10, null=True)),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('education', models.CharField(max_length=20, null=True)),
                ('marital_status', models.CharField(max_length=20, null=True)),
                ('house', models.CharField(max_length=50, null=True)),
                ('address', models.CharField(max_length=50, null=True)),
                ('job_type', models.CharField(max_length=20, null=True)),
                ('job_city', models.CharField(max_length=20, null=True)),
                ('job_year', models.CharField(max_length=20, null=True)),
                ('annual_income', models.CharField(max_length=20, null=True)),
                ('credit_limit', models.CharField(max_length=20, null=True)),
                ('loan_volume', models.CharField(max_length=20, null=True)),
                ('loan_term', models.CharField(max_length=20, null=True)),
                ('loan_interest_rate', models.CharField(max_length=20, null=True)),
                ('loan_purpose', models.CharField(max_length=50, null=True)),
                ('payment_method', models.CharField(max_length=20, null=True)),
                ('tender_deadline', models.CharField(max_length=20, null=True)),
            ],
            options={
                'db_table': 'yirendai_bid',
            },
        ),
        migrations.AlterUniqueTogether(
            name='yrdbidder',
            unique_together=set([('pin', 'bid_nikename', 'bid_time')]),
        ),
    ]
