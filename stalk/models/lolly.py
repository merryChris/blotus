from django.db import models

class Lolly(models.Model):
    class Meta:
        abstract = True

    def update_attr(self, uf, item):
        for k in uf:
            setattr(self, k, item.get(k))
