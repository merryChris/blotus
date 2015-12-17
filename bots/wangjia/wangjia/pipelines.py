# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy_djangoitem import ValidationError
from functools import wraps

def check_spider_pipeline(process_item_method):

    @wraps(process_item_method)
    def wrapper(self, item, spider):

        msg = '%%s %s pipline step.' % (self.__class__.__name__,)
        if self.__class__.__name__ in spider.pipeline:
            spider.logger.debug(msg % 'Executing')
            return process_item_method(self, item, spider)
        else:
            spider.logger.debug(msg % 'Skipping')
            return item

    return wrapper

class UniqueItemPersistencePipeline(object):

    @check_spider_pipeline
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

class RelatedItemPersistencePipeline(object):

    @check_spider_pipeline
    def process_item(self, item, spider):
        klass = item.__class__
        try:
            # If spider.object has existed related item, update it.
            obj = getattr(spider.object, item.related_field)
            update_fields = item.get_update_fields(obj)
            if update_fields:
                obj.update_attr(update_fields, item)
                obj.save()
        except klass.django_model.DoesNotExist as e:
            # If spider.object has no related item, create it.
            setattr(spider.object, item.related_field, item.instance)
            item.save()
            spider.object.save()

        return item
