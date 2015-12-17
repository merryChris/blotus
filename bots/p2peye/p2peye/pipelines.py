# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy_djangoitem import ValidationError

class UniqueItemPersistencePipeline(object):

    def process_item(self, item, spider):
        if item.unique_key and not item.get_uk():
            return None

        klass = item.__class__
        try:
            # If item doesn't exist, create it.
            item.instance.validate_unique()
            item.save()
        except ValidationError as e:
            # If item exists, update it.
            uk_params = item.get_uk_params()
            spider.logger.info('Duplicate Item From ' + str(uk_params) + '.')
            obj = klass.get_existed_object_by_uk(uk_params)
            update_fields = item.get_update_fields(obj)
            if update_fields:
                obj.update_attr(update_fields, item)
                obj.save()

        return item
