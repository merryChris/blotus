# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models import yirendai

class ToubiaoItem(BaseItem):
    django_model = yirendai.YrdTender
    update_fields_list = ['pin', 'loan_type', 'loan_url', 'bid_description', 'warrant_icon', 'progress',     \
                          'volume', 'interest_rate', 'term', 'status']
    unique_key = 'pin'

    @classmethod
    def get_existed_object_by_uk(cls, pin=None):
        if not pin: return None

        return cls.django_model.objects.get(pin=pin)


class BiaodiItem(BaseItem):
    django_model = yirendai.YrdBid
    update_fields_list = ['interest_rate', 'term', 'volume', 'bid_detail', 'remain_amount', 'nikename',      \
                          'gender', 'phone_number', 'education', 'marital_status', 'house', 'address',       \
                          'job_type', 'job_city', 'job_year', 'annual_income', 'credit_limit',               \
                          'loan_volume', 'loan_term', 'loan_interest_rate', 'loan_purpose',                  \
                          'payment_method', 'tender_deadline']
    related_field = 'yrdbid'


class BiaorenItem(BaseItem):
    django_model = yirendai.YrdBidder
    update_fields_list = ['pin', 'bid_nikename', 'bid_amount', 'bid_time']
    unique_key = ('pin', 'bid_nikename', 'bid_time')

    @classmethod
    def get_existed_object_by_uk(cls, pin=None, bid_nikename=None, bid_time=None):
        if not pin or not bid_nikename or not bid_time: return None

        return cls.django_model.objects.get(pin=pin, bid_nikename=bid_nikename, bid_time=bid_time)
