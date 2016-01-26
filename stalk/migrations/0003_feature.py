# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stalk', '0002_auto_20160120_0905'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('navigation', models.OneToOneField(primary_key=True, db_column=b'id', serialize=False, to='stalk.Navigation')),
                ('name', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(max_length=20, null=True)),
                ('company_tag', models.CharField(max_length=20, null=True)),
                ('illustration', models.TextField(null=True)),
                ('recommendation', models.CharField(max_length=10, null=True)),
                ('withdraw_num', models.CharField(max_length=10, null=True)),
                ('withdraw_day', models.CharField(max_length=10, null=True)),
                ('guard_num', models.CharField(max_length=10, null=True)),
                ('guard_day', models.CharField(max_length=10, null=True)),
                ('service_num', models.CharField(max_length=10, null=True)),
                ('service_status', models.CharField(max_length=10, null=True)),
                ('experience_num', models.CharField(max_length=10, null=True)),
                ('experience_status', models.CharField(max_length=10, null=True)),
                ('impression', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'wangjia_feature',
            },
        ),
    ]
