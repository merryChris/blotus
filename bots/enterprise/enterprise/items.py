# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem, ExporterItem
from stalk.models import enterprise

class JiekuanItem(BaseItem):
    django_model = enterprise.Loan
    update_fields_list = ['plat_id', 'plat_name', 'title', 'amount', 'process', 'interest_rate',             \
                          'borrow_period', 'borrow_unit', 'reward', 'type', 'repay_type', 'username',        \
                          'user_id', 'user_avatar_url', 'province', 'city', 'borrow_detail', 'url',          \
                          'success_time', 'publish_time', 'invest_count']
    unique_key = ('bid_id',)

class ToubiaoItem(BaseItem):
    django_model = enterprise.Invest
    update_fields_list = ['bid_id', 'plat_id', 'plat_name', 'user_id', 'username', 'amount', 'valid_amount', \
                          'add_date', 'status', 'type', 'url']
    unique_key = ('invest_id',)

class YuqiItem(BaseItem):
    django_model = enterprise.Overdue
    update_fields_list = ['plat_id', 'plat_name', 'user_id', 'username', 'idcard', 'overdue_count',          \
                          'overdue_total', 'overdue_principal', 'payment_total', 'payment_count',            \
                          'payment_period', 'repay_amount', 'wait_amount']
    unique_key = ('plat_id', 'user_id')
