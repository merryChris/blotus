from django.db import models
from lolly import Lolly


class YiyuanFinance(Lolly):
    link = models.URLField(unique=True, null=True)
    all_list = models.TextField(null=True)
    pub_date = models.CharField(max_length=50, null=True)
    title = models.TextField(null=True)
    channel_name = models.TextField(null=True)
    image_urls = models.TextField(null=True)
    desc = models.TextField(null=True)
    source = models.CharField(max_length=50, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'baidu_apistore_yiyuan_finance'
