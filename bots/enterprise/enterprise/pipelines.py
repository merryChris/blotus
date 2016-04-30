# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from bots.base.pipelines import BaseUniqueItemPersistencePipeline
from bots.base.pipelines import BaseCacheExporterPersistencePipeline

class UniqueItemPersistencePipeline(BaseUniqueItemPersistencePipeline):
    pass

class TokenFileExporterPersistencePipeline(BaseCacheExporterPersistencePipeline):

    def get_type(self):
        return 'token'

    def get_filesuffix(self):
        return 'tk'

    def get_filename(self, spider):
        return getattr(spider, 'plat_id', 'test')+'.'+self.get_filesuffix()

    def log_successful_info(self, item, spider):
        symbol = (item['record'], getattr(spider, 'plat_id', 'test'))
        spider.logger.info('Successfully Receive Token <%s> From No.%s Plat.' % symbol)

    def log_failure_info(self, spider):
        spider.logger.info('Fail To Receive Token From No.%s Plat.' % getattr(spider, 'plat_id', 'test'))
