# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_url_param, get_content
from weidai.items import ToubiaoItem, BiaodiItem

############################################################################################
#                                                                                          #
# USAGE: nohup scrapy crawl biaodi -a from_id=1 -a to_id=1 --loglevel=INFO --logfile=log & #
#                                                                                          #
############################################################################################

class BiaodiSpider(scrapy.Spider):
    name = 'biaodi'
    allowed_domains = ["www.weidai.com.cn"]
    start_formated_url = 'https://www.weidai.com.cn/bid/showBorrowDetail?bid={bid}'
    feature_map = {'newIcon': '新手',
                   'shouIcon': '手机',
                   'iconA': '定向',
                   'iconB': '奖',
                   'iconC': '定时',
                   'iconD': '债权',
                   'iconF': '信用'}
    pipeline = ['RelatedItemPersistencePipeline']

    def __init__(self, from_id=1, to_id=1, *args, **kwargs):
        to_id = max(int(from_id), int(to_id))
        self.shortlist = xrange(int(from_id), int(to_id)+1)
        self.mapping = {}
        super(BiaodiSpider, self).__init__(*args, **kwargs)

    def get_feature_type(self):
        feature = self.valid_type.get(self.bid_type)
        if self.bid_type == 'other':
            feature = feature[self.credit]

        return feature

    def start_requests(self):
        for i in self.shortlist:
            obj = ToubiaoItem.get_object_by_pk(i)
            self.mapping[obj.pin] = obj.id
            url = self.start_formated_url.format(bid=obj.pin)
            yield self.make_requests_from_url(url)

    def parse(self, response):
        #NOTE: (zacky, 2015.APR.27th) PIPELINE FUNCTIONS RELATED WILL BE PROCESSED, SO WE KEEP THE OBJECT STATE HERE.
        symbol = (self.mapping.get(get_url_param(response.url, 'bid')), response.url)
        self.logger.info('Parsing ID.%d Weidai Bid Info From <%s>.' % symbol)
        self.object = ToubiaoItem.get_object_by_pk(symbol[0])

        item = BiaodiItem()

        overview = response.xpath('//div[contains(@class, "infoDetails")]')
        if overview:
            title = overview.xpath('div[starts-with(@class, "title")]')
            item['title'] = get_content(title.xpath('h1/text()').extract())
            fl = []
            for icon in title.xpath('div[@class="icon"]/i'):
                feature = self.feature_map.get(get_content(icon.xpath('@class').extract()))
                if feature: fl.append(feature)
            item['feature'] = '\001'.join(fl)
            if title.xpath('//div[@class="aqzsBg"]'): item['has_security_guarantee'] = 1

            info = overview.xpath('ul[starts-with(@class, "infoUl")]')
            if info:
                item['volume'] = get_content(info.xpath('li[@class="total"]/p//text()').extract(), num=2)
                item['annual_profit'] = get_content(info.xpath('li[@class="profit"]/p//text()').extract(), num=4)
                item['time_limit'] = get_content(info.xpath('li[@class="date"]/p//text()').extract(), num=2)

            date_info = overview.xpath('//ul[starts-with(@class, "dateUl")]/li')
            if date_info:
                item['interest_time'] = get_content(date_info[0].xpath('text()').extract())
                item['mode_of_payment'] = get_content(date_info[1].xpath('text()').extract())
                item['launch_time'] = get_content(date_info[2].xpath('text()').extract())

            rate_info = overview.xpath('//ul[starts-with(@class, "rateUl")]/li')
            if rate_info:
                item['progress'] = get_content(rate_info[0].xpath('em/text()').extract())
                item['source_strore'] = get_content(rate_info[1].xpath('text()').extract())

        detail = response.xpath('//div[starts-with(@class, "detailsContent")]')
        #NOTE: (zacky, 2016.JAN.19th) SPECIALLY FOR CREDIT BIDS BASIC INFO.
        if response.xpath('//div[contains(@class, "xinyong")]'):
            content = detail.xpath('div[@class="detailsItem curr"]/div[@class="content"]')
            rows = content[0].xpath('.//tr')
            cols = rows[0].xpath('td[contains(@class, "Content")]')
            item['user'] = get_content(cols[0].xpath('text()').extract())
            item['gender'] = get_content(cols[2].xpath('text()').extract())
            item['marital_status'] = get_content(cols[1].xpath('text()').extract())

            cols = rows[1].xpath('td[@class="item1Content"]')
            item['hometown'] = get_content(rows[1].xpath('td[@class="item1Content"]/text()').extract())
            tmp = get_content(rows[1].xpath('td[@class="item2Content"]/text()').extract())

            cols = content[1].xpath('.//tr/td[contains(@class, "Content")]')
            item['payoffed'] = get_content(cols[0].xpath('text()').extract())
            item['pending'] = get_content(cols[1].xpath('text()').extract())
            item['overdue'] = get_content(cols[2].xpath('text()').extract())
        else:
            lefts  = detail.xpath('div[@class="leftTitle"]')
            rights = detail.xpath('div[@class="content"]')
            if len(lefts) > 0: item['user'] = get_content(lefts[0].xpath('span/text()').extract())

            if len(rights) > 0:
                content = rights[0].xpath('ul[starts-with(@class, "infoUl")]')
                info = content[0].xpath('li')
                item['gender'] = get_content(info[0].xpath('text()').extract())
                item['marital_status'] = get_content(info[1].xpath('text()').extract())
                item['hometown'] = get_content(info[2].xpath('text()').extract())

                info = content[1].xpath('li')
                item['payoffed'] = get_content(info[0].xpath('text()').extract())
                item['pending'] = get_content(info[1].xpath('text()').extract())
                item['overdue'] = get_content(info[2].xpath('text()').extract())

            if len(rights) > 1:
                info = rights[1].xpath('ul[starts-with(@class, "infoUl")]/li')
                item['vehicle_brand'] = get_content(info[0].xpath('.//text()').extract(), skipFirst=True)
                item['vehicle_number'] = get_content(info[1].xpath('.//text()').extract(), skipFirst=True)
                item['vehicle_kilometers'] = get_content(info[2].xpath('.//text()').extract(), skipFirst=True)
                item['vehicle_price'] = get_content(info[3].xpath('.//text()').extract(), skipFirst=True)
                item['mortgage_value'] = get_content(info[4].xpath('.//text()').extract(), skipFirst=True)
                item['verification_time'] = get_content(info[5].xpath('.//text()').extract(), skipFirst=True)
                item['verification_explanation'] = get_content(info[6].xpath('.//text()').extract(), skipFirst=True)

        return item
