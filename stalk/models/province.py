from django.db import models
from lolly import Lolly

class Province(Lolly):
    name = models.CharField(unique=True, max_length=20)

    class Meta:
        app_label = 'stalk'
        db_table = 'province'
