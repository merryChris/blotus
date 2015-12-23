# -*- coding: utf-8 -*-

# Scrapy settings for imageHelper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

from bots import setup_django_env
setup_django_env()

BOT_NAME = 'imageHelper'

SPIDER_MODULES = ['imageHelper.spiders']
NEWSPIDER_MODULE = 'imageHelper.spiders'

DOWNLOAD_HANDLERS = {'s3': None}

ITEM_PIPELINES = {'imageHelper.pipelines.ImagePersistencePipeline': 1}

IMAGES_STORE = 'img'

DOWNLOAD_DELAY = 6
DOWNLOAD_TIMEOUT = 100
