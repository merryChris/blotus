# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models import weidai

class ToubiaoItem(BaseItem):
    django_model = weidai.Tender
    update_fields_list = ['pin', 'location', 'title', 'interest_rate', 'time_limit', 'launch_date',          \
                          'volume', 'transfer_amount', 'progress', 'status']
    unique_key = 'pin'

    @classmethod
    def get_existed_object_by_uk(cls, pin=None):
        if not pin: return None

        return cls.django_model.objects.get(pin=pin)

class BiaodiItem(BaseItem):
    django_model = weidai.Bid
    update_fields_list = ['title', 'feature', 'volume', 'annual_profit', 'time_limit', 'interest_time',      \
                          'mode_of_payment', 'launch_time', 'progress', 'source_strore',                     \
                          'has_security_guarantee', 'user', 'gender', 'marital_status', 'hometown',          \
                          'payoffed', 'pending', 'overdue', 'vehicle_brand', 'vehicle_number',               \
                          'vehicle_kilometers', 'vehicle_price', 'mortgage_value', 'verification_time',      \
                          'verification_explanation']

    related_field = 'bid'


class BiaorenItem(BaseItem):
    django_model = weidai.Bidder
    update_fields_list = ['pin', 'user', 'amount', 'timestamp', 'source']
    unique_key = ('pin', 'user', 'timestamp')

    @classmethod
    def get_existed_object_by_uk(cls, pin=None, user=None, timestamp=None):
        if not pin or not user or not timestamp: return None

        return cls.django_model.objects.get(pin=pin, user=user, timestamp=timestamp)
