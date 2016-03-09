# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_content
from yirendai.items import ToubiaoItem, BiaorenItem

#############################################################################################
#                                                                                           #
# USAGE: nohup scrapy crawl biaoren -a from_id=1 -a to_id=2 --loglevel=INFO --logfile=log & #
#                                                                                           #
#############################################################################################

class BiaorenSpider(scrapy.Spider):
	name = 'biaoren'
	allowed_domains = ['www.yirendai.com']
	start_formated_url = 'https://www.yirendai.com/loan/view/{pin}?page=1&tabflag=1'
	pipeline = ['UniqueItemPersistencePipeline']

	def __init__(self, from_id=1, to_id=1, *args, **kwargs):
		self.shortlist = xrange(int(from_id), int(to_id)+1)
		self.mapping = {}
		super(BiaorenSpider, self).__init__(*args, **kwargs)

	def get_pin_from_url(self, url):
		return url.split('?')[0].split('/')[-1]

	def start_requests(self):
		for i in self.shortlist:
			obj = ToubiaoItem.get_object_by_pk(i)
			self.mapping[obj.pin] = obj.id
			url = self.start_formated_url.format(pin=obj.pin)
			yield self.make_requests_from_url(url)

	def parse(self, response):
		symbol = (self.mapping.get(self.get_pin_from_url(response.url)), response.url)
		self.logger.info('Parsing ID.%d Yinrendai Bidder List Info From <%s>' % symbol)
		self.object = ToubiaoItem.get_object_by_pk(symbol[0])

		item_list=[]
		record = response.xpath('//table[@class="bidRecord"]//tr')

		for row in record:
			item = BiaorenItem()
			detail = row.xpath('.//td')
			if not detail:	continue

			item['pin'] = self.object.pin
			item['bid_nikename'] = get_content(detail[0].xpath('text()').extract())
			item['bid_amount'] = get_content(detail[1].xpath('text()').extract())
			item['bid_time'] = get_content(detail[2].xpath('text()').extract())

			item_list.append(item)

		return item_list
