# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_content
from yirendai.items import ToubiaoItem

###################################################################################################
#                                                                                                 #
# USAGE: nohup scrapy crawl toubiao -a start_page=1 -a end_page=2 --loglevel=INFO --logfile=log & #
#                                                                                                 #
###################################################################################################

class ToubiaoSpider(scrapy.Spider):
	name = 'toubiao'
	allowed_domains = ['www.yirendai.com']
	start_formated_url = 'http://www.yirendai.com/loan/list/{page_id}'
	status_list = {'bidForm': '投标中', 'bidFormbidForm_full':'已满标'}
	pipeline = ['UniqueItemPersistencePipeline']

	def __init__(self, start_page=1, end_page=1, *args, **kwargs):
		self.shortlist = xrange(int(start_page), int(end_page)+1)
		super(ToubiaoSpider, self).__init__(*args, **kwargs)

	def get_pin_from_url(self, url):
		return url.split('?')[0].split('/')[-1]

	def start_requests(self):
		for i in self.shortlist:
			url = self.start_formated_url.format(page_id=i)
			yield self.make_requests_from_url(url)

	def parse(self, response):
		self.logger.info('Parsing Yinrendai Tender List Info From <%s>.' % response.url)

		item_list = []
		tender_list = response.xpath('//li[@class="clearfix"]')
		for tender in tender_list:
			item = ToubiaoItem()
			item['loan_type'] = get_content(tender.xpath('div/@class').extract()).split('_')[-1]

			left = tender.xpath('div/div[@class="leftpart"]')
			if left:
				item['loan_url'] = get_content(left.xpath('./h3/a/@href').extract())
				item['pin'] = self.get_pin_from_url(get_content(left.xpath('h3/a/@href').extract()))
				item['loan_description'] = get_content(left.xpath('h3/a/text()').extract())
				item['warrant_icon'] = get_content(left.xpath('h3/a/span/@class').extract())

				item['progress'] = get_content(left.xpath('div[@class="l bidDetail"]/p/text()').extract())
				item['volume'] = get_content(left.xpath('div[@class="l bid_total"]/h4/span/text()').extract())
				item['interest_rate'] = get_content(left.xpath('div[@class="l bid_rate"]/h4/span/text()').extract())
				item['term'] = get_content(left.xpath('div[@class="l bidInfor"]/h4/span/text()').extract())

			right = tender.xpath('div/div[@class="rightpart"]')
			if right:
				item['status'] = self.status_list.get(get_content(right.xpath('div/@class').extract()))

			item_list.append(item)

		return item_list
