# -*- coding: utf-8 -*-

# Scrapy settings for exporterHelper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

from bots import setup_django_env
setup_django_env()

BOT_NAME = 'exporterHelper'

SPIDER_MODULES = ['exporterHelper.spiders']
NEWSPIDER_MODULE = 'exporterHelper.spiders'

DOWNLOAD_HANDLERS = {'s3': None}

ITEM_PIPELINES = {'exporterHelper.pipelines.CacheFileExporterPersistencePipeline': 1,
                  'exporterHelper.pipelines.TokenFileExporterPersistencePipeline': 1}

DOWNLOAD_DELAY = 2
DOWNLOAD_TIMEOUT = 100

COOKIES_DEBUG = True
