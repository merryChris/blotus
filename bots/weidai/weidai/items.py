# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models import weidai

class ToubiaoItem(BaseItem):
    django_model = weidai.Tender
    update_fields_list = ['pin', 'feature', 'location', 'title', 'interest_rate', 'time_limit', 'volume', 'progress']
    merge_fields_list  = ['feature']
    unique_key = 'pin'

    @classmethod
    def get_existed_object_by_uk(cls, pin=None):
        if not pin: return None

        return cls.django_model.objects.get(pin=pin)

class BiaodiItem(BaseItem):
    django_model = weidai.Bid

class BiaorenItem(BaseItem):
    django_model = weidai.Bidder
