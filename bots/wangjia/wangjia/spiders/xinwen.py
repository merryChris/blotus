# -*- coding: utf-8 -*-

import scrapy
from utils.webpage import get_trunk, get_content
from wangjia.items import XinwenItem

#################################################################################################
#                                                                                               #
# USAGE: nohup scrapy crawl xinwen -a category=0 -a cache=cache --loglevel=INFO --logfile=log & #
#                                                                                               #
#################################################################################################

class XinwenSpider(scrapy.Spider):
    name = 'xinwen'
    allowed_domains = ['wdzj.com']
    start_urls = []
    image_url_prefix = 'http://www.wdzj.com'
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, category=0, cache=None, *args, **kwargs):
        self.category = int(category)
        self.cache = cache
        self.tab = ['', 'hangye', 'zhengce', 'pingtai', 'shuju', 'licai', 'guowai', 'guandian', 'yanjiu']
        super(XinwenSpider, self).__init__(*args, **kwargs)

    def get_urls_from_cache_file(self, filePath=None):
        if not filePath: return []

        f = open(filePath, 'r')
        l = map(get_trunk, f.readlines())
        f.close()

        return l

    def get_thread_from_url(self, url):
        pos = url.find('.html')
        if pos != -1: return url[:pos].split('/')[-1]

        return None

    def get_category_tab(self):
        return self.tab[self.category]

    def modify_image_url(self, url):
        if not url.startswith('http'):
            return self.image_url_prefix + url

        return url

    def start_requests(self):
        if self.cache:
            self.logger.info('Loading New URLs From File %s.' % self.cache)
            self.start_urls = self.get_urls_from_cache_file(self.cache)

        #super(XinwenSpider, self).start_requests()
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        symbol = (self.get_thread_from_url(response.url), self.get_category_tab(), response.url)
        if not symbol[0]:
            self.logger.warning('Invalid Wangjia News Item From <%s>.' % symbol[2])
            return None

        if response.xpath('//div[@id="messagetext" and @class="alert_info"]'):
            self.logger.warning('No.%s Wangjia News %s Item From <%s> Maybe Limited.' % symbol)
            return None

        self.logger.info('Parsing No.%s Wangjia News %s Item From <%s>.' % symbol)

        item = XinwenItem()
        item['thread'] = symbol[0]
        item['category_id'] = self.category
        item['source'] = symbol[2]

        article = response.xpath('//div[@class="con_news"]')
        item['title'] = get_content(article.xpath('h1/text()').extract())

        subtitle = article.xpath('ul/li[@class="n_time"]/text()').extract()[0].encode('utf8').split('：')
        item['created'] = get_content(subtitle[1].split())
        item['author'] = get_content(subtitle[-1].split())
        item['summary'] = get_content(article.xpath('ul/li[@class="a_abstract"]/span/text()').extract())

        body = article.xpath('ul/li[@class="news_con_p"]')
        item['content'] = ''.join([get_trunk(c) for c in body.xpath('.//text()').extract()])
        item['raw_content'] = get_content(body.extract())
        item['image_url'] = '#'.join([self.modify_image_url(get_trunk(c)) for c in body.xpath('.//img/@src').extract()]) or None

        return item
