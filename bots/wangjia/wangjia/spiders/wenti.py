import scrapy
from utils.webpage import log_empty_fields, get_content
from wangjia.items import ProvinceItem, WentiItem

###################################################################
#                                                                 #
# USAGE: nohup scrapy crawl wenti --loglevel=INFO --logfile=log & #
#                                                                 #
###############################################################a#

class WentiSpider(scrapy.Spider):
    name = 'wenti'
    allowed_domains = ['wdzj.com']
    start_urls = ['http://shuju.wdzj.com/problem-1.html']
    pipeline = ['UniqueItemPersistencePipeline']

    def parse(self, response):
        self.logger.info('Parsing Wangjia Problem Platform From <%s>.' % response.url)

        platform_list = []
        platforms = response.xpath('//div[@class="wtpt"]/table/tbody/tr')
        for rt in platforms:
        #for idx, rt in enumerate(platforms[1:]):
            content = rt.xpath('td')

            item = WentiItem()
            item['name'] = get_content(content[1].xpath('.//text()').extract())
            item['problem_time'] = get_content(content[2].xpath('text()').extract(), exclude=('-'))
            item['launch_time'] = get_content(content[3].xpath('text()').extract(), exclude=('-'))
            item['registered_capital'] = get_content(content[4].xpath('text()').extract(), exclude=('-'))
            #if idx == 179: item['province_id'] = 22
            #else:
            province_name = get_content(content[5].xpath('text()').extract())
            item['province_id'] = ProvinceItem.get_id_by_name(province_name)
            #print item.get_uk(), province_name, item['province_id']
            item['accounted_revenue'] = get_content(content[6].xpath('text()').extract(), exclude=('-'))
            item['involved_passenger'] = get_content(content[7].xpath('text()').extract(), exclude=('-'))
            item['event_category'] = get_content(content[8].xpath('text()').extract(), exclude=('-'))

            log_empty_fields(item, self.logger)
            if item.get_uk(): platform_list.append(item)

        return platform_list
