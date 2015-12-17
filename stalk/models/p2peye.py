from django.db import models
from lolly import Lolly


class PlatformFeature(Lolly):
    pin = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=50, null=True)
    link = models.URLField(null=True)
    feature = models.CharField(max_length=500, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'p2peye_platform_feature'

    def get_uk_code(self):
        return str(self.id)+'_'+self.pin
