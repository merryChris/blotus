# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models.renrendai import Product,InvestRecord,LoanInfo,Borrower

class LoanInfoItem(BaseItem):
    django_model = LoanInfo
    update_fields_list = ['loan_id','title','status']
    unique_key = ('loan_id',)

class BorrowerItem(BaseItem):
    django_model = Borrower
    update_fields_list = ['loan_id', 'user_id', 'user_nickname', 'age','education', 'marriage', 'city',      \
                          'length_of_service', 'income_scale', 'credit_level', 'loan_application_num',       \
                          'success_application_num', 'payoff_num', 'credit_line', 'total_loan_amount',       \
                          'total_left_to_pay', 'overdue_amount', 'overdue_times', 'critical_overdue_times']
    unique_key = ('loan_id',)

class ProductItem(BaseItem):
    django_model = Product
    update_fields_list = ['loan_id', 'product_name', 'amount', 'income_ratio', 'pay_period',                 \
                          'guarantee_method', 'pre_pay_ratio', 'pay_method', 'loan_detail']
    unique_key = ('loan_id',)

class InvestRecordItem(BaseItem):
    django_model = InvestRecord
    update_fields_list = ['loan_id', 'user_id', 'amount', 'lend_time']
    unique_key = ('loan_id', 'user_id', 'lend_time')
