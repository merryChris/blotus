import scrapy
from utils.webpage import get_content
from exporterHelper.items import ExporterItem

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
    pipeline = ['CacheFileExporterPersistencePipeline']

    def parse(self, response):
        self.logger.info('Parsing Wangjia Rating Item URLs From <%s>.' % response.url)

        item = ExporterItem()
        elements = response.xpath('//table[@id="rateTable_body"]/tbody/tr')
        for ele in elements:
            item.set_record(self.url_prefix + get_content(ele.xpath('td/a[@class="pname"]/@href').extract()))

        return item
