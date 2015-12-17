# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from stalk.models import p2peye

class BaseItem(DjangoItem):
    django_model = None
    update_fields_list = []
    unique_key = None

    def get_uk(self):
        # Return 'None' or valid 'str' or valid 'tuple'.
        if not self.unique_key: return None

        if isinstance(self.unique_key, str): return self.get(self.unique_key, None)
        values = [self.get(x) for x in self.unique_key if self.get(x)]

        if len(values) != len(self.unique_key): return None
        return tuple(values)

    def get_uk_params(self):
        if not self.unique_key or not self.get_uk(): return None

        if isinstance(self.unique_key, str): return {self.unique_key: self.get_uk()}
        return dict(zip(self.unique_key, self.get_uk()))

    def get_update_fields(self, obj):
        uf = []
        for key in self.update_fields_list:
            if not getattr(obj, key) and self.get(key):
                uf.append(key)

        return uf

    @classmethod
    def get_object_by_pk(cls, pk):
        try:
            obj = cls.django_model.objects.get(pk=pk)
        except cls.django_model.DoesNotExist:
            return None

        return obj

class FeatureItem(BaseItem):
    django_model = p2peye.PlatformFeature
    update_fields_list = ['name', 'link', 'feature']
    unique_key = 'pin'

    @classmethod
    def get_existed_object_by_uk(cls, kwargs):
        if not kwargs.get('pin'):
            return None

        return cls.django_model.objects.get(pin=kwargs.get('pin'))
