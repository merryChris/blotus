from django.db import models

class Lolly(models.Model):
    class Meta:
        abstract = True

    def update_attr(self, uf=[], mf=[], item=None):
        if not item: return

        for k in uf:
            setattr(self, k, item.get(k))
        for k in mf:
            ori = getattr(self, k).encode('utf8').split('\001')
            now = item.get(k).split('\001')
            setattr(self, k, '\001'.join(ori+now))
