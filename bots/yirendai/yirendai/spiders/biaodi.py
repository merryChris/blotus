# -*- coding: utf-8 -*-
import scrapy
from utils.webpage import get_content
from yirendai.items import ToubiaoItem, BiaodiItem

############################################################################################
#                                                                                          #
# USAGE: nohup scrapy crawl biaodi -a from_id=1 -a to_id=2 --loglevel=INFO --logfile=log & #
#                                                                                          #
############################################################################################

class BiaodiSpider(scrapy.Spider):
	name = 'biaodi'
	allowed_domains = ['www.yirendai.com']
	start_formated_url = 'https://www.yirendai.com/loan/view/{pin}?page=1&tabflag=0'
	pipeline = ['RelatedItemPersistencePipeline']
	bid_detail_form = '{num}人完成投标{percentage}%'

	def __init__(self, from_id=1, to_id=1, *args, **kwargs):
		self.shortlist = xrange(int(from_id), int(to_id)+1)
		self.mapping = {}
		super(BiaodiSpider, self).__init__(*args, **kwargs)

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
		self.logger.info('Parsing ID.%d Yinrendai Bid List Info From <%s>' % symbol)
		self.object = ToubiaoItem.get_object_by_pk(symbol[0])

		item = BiaodiItem()
		finance = response.xpath('//div[@class="finance_box clearfix"]')
		if finance:
			left = finance.xpath('div[@class="elite_left l"]')

			left_info = left.xpath('table/tr[@class="num"]/td')
			item['interest_rate'] = get_content(left_info[0].xpath('strong/text()').extract())
			item['term'] = get_content(left_info[1].xpath('strong/text()').extract())
			item['volume'] = get_content(left_info[2].xpath('strong/text()').extract())

			# We use this string format to get the bid detail information easily.
			bid_detail_info = left.xpath('div/p[@class="progressTxt l"]')
			item['bid_detail'] = self.bid_detail_form.format(num=get_content(bid_detail_info.xpath('span/text()').extract()),
				percentage=get_content(bid_detail_info.xpath('//span[@id="percent"]/text()').extract()))

			item['remain_amount'] = get_content(finance.xpath('div[@class="elite_right l"]/p/span/text()').extract())

		detail = response.xpath('//li[@class="oneInfo"]')
		if detail:
			personal_info = detail[0].xpath('table//td[not(@class="dd")]')
			if personal_info:
				item['nikename'] = get_content(personal_info[0].xpath('text()').extract())
				item['gender'] = get_content(personal_info[1].xpath('text()').extract())
				item['phone_number'] = get_content(personal_info[2].xpath('text()').extract())
				item['education'] = get_content(personal_info[3].xpath('text()').extract())
				item['marital_status'] = get_content(personal_info[4].xpath('text()').extract())
				item['house'] = get_content(personal_info[5].xpath('text()').extract())
				item['address'] = get_content(personal_info[6].xpath('text()').extract())

			job_status = detail[1].xpath('table//td[not(@class="dd")]')
			if job_status:
				item['job_type'] = get_content(job_status[0].xpath('text()').extract())
				item['job_city'] = get_content(job_status[1].xpath('text()').extract())
				item['job_year'] = get_content(job_status[2].xpath('text()').extract())
				item['annual_income'] = get_content(job_status[3].xpath('text()').extract())
				item['credit_limit'] = get_content(job_status[4].xpath('text()').extract())

			bid_info = detail[2].xpath('table//td[not(@class="dd")]')
			if bid_info:
				item['loan_volume'] = get_content(bid_info[0].xpath('text()').extract())
				item['loan_term'] = get_content(bid_info[1].xpath('text()').extract())
				item['loan_interest_rate'] = get_content(bid_info[2].xpath('text()').extract())
				item['loan_purpose'] = get_content(bid_info[3].xpath('text()').extract())
				item['payment_method'] = get_content(bid_info[4].xpath('text()').extract())
				item['tender_deadline'] = get_content(bid_info[5].xpath('text()').extract())

		return item
