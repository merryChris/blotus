# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models import p2peye

class FeatureItem(BaseItem):
    django_model = p2peye.PlatformFeature
    update_fields_list = ['name', 'link', 'feature']
    unique_key = 'pin'

    @classmethod
    def get_existed_object_by_uk(cls, pin=None):
        if not pin: return None

        return cls.django_model.objects.get(pin=pin)
