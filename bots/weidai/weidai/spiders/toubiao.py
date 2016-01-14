# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_url_param, get_content
from weidai.items import ToubiaoItem

########################################################################################################################################
#                                                                                                                                      #
# USAGE: nohup scrapy crawl toubiao -a bid_type=other -a credit=-1 -a start_page_id=1 -a end_page_id=2 --loglevel=INFO --logfile=log & #
#                                                                                                                                      #
########################################################################################################################################

class ToubiaoSpider(scrapy.Spider):
    name = "toubiao"
    allowed_domains = ["www.weidai.com.cn"]
    start_formated_url = 'https://www.weidai.com.cn/bid/tenderList?searchFlag=search&typeCondition={bid_type}&page={page_id}&credit={credit}'
    valid_type = {'newBorrow': '新手标',
                  'timing': '定时标',
                  'directional': '定向标',
                  'debt': '债权转让',
                  'other': ['','','信用标','直投']}
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, bid_type='other', credit=-1, start_page_id=1, end_page_id=1, *args, **kwargs):
        self.bid_type = bid_type
        self.credit = int(credit)
        if self.credit != 2: self.credit = -1
        self.shortlist = xrange(int(start_page_id), int(end_page_id)+1)
        super(ToubiaoSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        if not self.valid_type.has_key(self.bid_type): return

        for i in self.shortlist:
            url = self.start_formated_url.format(bid_type=self.bid_type, page_id=i, credit=self.credit)
            yield self.make_requests_from_url(url)

    def parse(self, response):
        self.logger.info('Parsing Weidai Tender List Info From <%s>.' % response.url)

        item_list = []
        tender_list = response.xpath('//ul[@class="storeTitle storeObject"]')
        for item in tender_list:
            tender = ToubiaoItem()
            tender['pin'] = get_url_param(get_content(item.xpath('li[@class="fl no1"]/a/@href').extract()), 'bid')
            tender['location'] = get_content(item.xpath('li[@class="fl no1"]/p/text()').extract())
            tender['title'] = get_content(item.xpath('li[@class="fl no1"]/a/@title').extract())
            tender['interest_rate'] = get_content(item.xpath('li[@class="fl no3"]/text()').extract())
            tender['time_limit'] = get_content(item.xpath('li[@class="fl no4"]/text()').extract())
            if self.bid_type == 'debt':
                tender['launch_date'] = get_content(item.xpath('li[@class="fl no5"]/text()').extract())
                tender['transfer_amount'] = get_content(item.xpath('li[@class="fl no6"]/text()').extract())
            else:
                tender['volume'] = get_content(item.xpath('li[@class="fl no5"]/text()').extract())
                tender['progress'] = get_content(item.xpath('li[@class="fl no6"]/span/text()').extract())
            tender['status'] = get_content(item.xpath('li[@class="fl no7"]//text()').extract())

            item_list.append(tender)

        return item_list
