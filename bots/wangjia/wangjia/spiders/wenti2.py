# -*- coding: utf-8 -*-

import scrapy
from utils.webpage import get_content
from wangjia.items import ProvinceItem, WentiItem

####################################################################
#                                                                  #
# USAGE: nohup scrapy crawl wenti2 --loglevel=INFO --logfile=log & #
#                                                                  #
####################################################################

class Wenti2Spider(scrapy.Spider):
    name = 'wenti2'
    allowed_domains = ['wdzj.com']
    start_urls = ['http://www.wdzj.com/daohang.html']
    pipeline = ['UniqueItemPersistencePipeline']

    def get_event_category_by_classname(self, classname):
        if classname == 'kc3': return '提现困难'
        if classname == 'kc4': return '停业'
        if classname == 'kc5': return '跑路'

        return None

    def parse(self, response):
        item_list = []
        content = response.xpath('//div[@id="issuePlatList"]/div[starts-with(@class, "rnav")]')
        for sel_ct in content:
            province_name = get_content(sel_ct.xpath('div[@class="til"]/div/p[not(@class="til_num")]/text()').extract())
            province_id = ProvinceItem.get_id_by_name(province_name)

            plat_list = sel_ct.xpath('ul[@class="til_cn"]/li')
            for sel_pt in plat_list:
                item = WentiItem()
                item['name'] = get_content(sel_pt.xpath('a/text()').extract())
                purl = get_content(sel_pt.xpath('a/@purl').extract()).split('/')
                while not purl[-1]: purl.pop()
                item['pin'] = purl.pop()
                item['province_id'] = province_id
                item['event_category'] = self.get_event_category_by_classname(get_content(sel_pt.xpath('i/@class').extract()))

                item_list.append(item)

        return item_list
