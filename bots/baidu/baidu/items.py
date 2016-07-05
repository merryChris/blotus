# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models import baidu


class YiyuanCaijingItem(BaseItem):
    django_model = baidu.ApistoreYiyuanFinance
    update_fields_list = ['link', 'all_list', 'pub_date', 'title', 'channel_name', 'image_urls', 'desc',     \
                          'source']
    unique_key = ('link',)
