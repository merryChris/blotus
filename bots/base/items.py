from scrapy_djangoitem import DjangoItem
from stalk.models import province

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

class ProvinceItem(BaseItem):
    django_model = province.Province

    @classmethod
    def get_id_by_name(cls, name):
        if not name: return 0

        obj = cls.django_model.objects.get(name=name)
        return obj.pk
