# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_trunk, get_content
from utils.exporter import read_cache
from wangjia.items import XinwenItem

###################################################################################
#                                                                                 #
# USAGE: nohup scrapy crawl xinwen -a cache=cache --loglevel=INFO --logfile=log & #
#                                                                                 #
###################################################################################

class XinwenSpider(scrapy.Spider):
    name = 'xinwen'
    allowed_domains = ['wdzj.com']
    start_urls = []
    image_url_prefix = 'http://www.wdzj.com/'
    pipeline = ['UniqueItemPersistencePipeline']
    #NOTE: (zacky, 2016.JUN.7th) SHOULD KEEP CONSISTENT WITH 'wangjia_news_list.py'.
    tab = ['', 'hangye', 'zhengce', 'pingtai', 'shuju', 'licai', 'guowai', 'guandian', 'yanjiu', 'jiedai',   \
           'jinrong', 'gundong', 'xiaodai', 'danbao', 'diandang', 'hydongtai', 'zhifu', 'zhongchou',         \
           'huobi', 'baogao', 'xiehui']
    #NOTE: (zacky, 2016.JUN.7th) JUST MARK UP BLACK TAB HERE.
    black_tab = ['fangtan', 'zhuanlan', 'video']

    def __init__(self,  cache='cache', *args, **kwargs):
        self.cache = cache+'.ch'
        super(XinwenSpider, self).__init__(*args, **kwargs)

    def get_thread_category_from_url(self, url):
        pos, thread, category = url.find('.html'), '', 0
        if pos != -1 and not any([bt in url for bt in self.black_tab]):
            tab, thread = url[:pos].split('/')[-2:]
            if tab in self.tab: category = self.tab.index(tab)

        return thread, category

    def modify_image_url(self, url):
        if not url.startswith('http'):
            return self.image_url_prefix + url

        return url

    def start_requests(self):
        if self.cache:
            self.logger.info('Loading New URLs From File %s.' % self.cache)
            self.start_urls = read_cache('cache', self.cache)

        #super(XinwenSpider, self).start_requests()
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        tc = self.get_thread_category_from_url(response.url)
        if not tc[0] or not tc[1]:
            self.logger.warning('Invalid Wangjia News Item From <%s>.' % response.url)
            return None

        symbol = (tc[0], self.tab[tc[1]], response.url)
        if response.xpath('//div[@id="messagetext" and @class="alert_info"]'):
            self.logger.warning('No.%s Wangjia News %s Item From <%s> Maybe Limited.' % symbol)
            return None

        self.logger.info('Parsing No.%s Wangjia News %s Item From <%s>.' % symbol)

        item = XinwenItem()
        item['thread'] = int(symbol[0])
        item['category_id'] = tc[1]
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
