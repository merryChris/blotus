import scrapy
from scrapy import log
from utils.webpage import get_content
from exporterHelper.items import URLItem

############################################################################
#                                                                          #
# USAGE: nohup scrapy crawl wangjia_rating --loglevel=INFO --logfile=log & #
#                                                                          #
############################################################################

class WangjiaRatingJsonSpider(scrapy.Spider):
    name = 'wangjia_rating'
    allowed_domains = ['wdzj.com']
    url_prefix = 'http://www.wdzj.com'
    start_urls = ['http://www.wdzj.com/pingji.html']

    def parse(self, response):
        self.log('Parsing Wangjia Rating Item URLs From <%s>.' % response.url, level=log.INFO)

        item_list = []
        elements = response.xpath('//table[@id="rateTable_body"]/tbody/tr')
        for ele in elements:
            item = URLItem()
            item['url'] = self.url_prefix + get_content(ele.xpath('td/a[@class="pname"]/@href').extract())

            item_list.append(item)

        return item_list
