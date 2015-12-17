import scrapy, json
from utils.webpage import get_content
from p2peye.items import FeatureItem

#####################################################################
#                                                                   #
# USAGE: nohup scrapy crawl daohang --loglevel=INFO --logfile=log & #
#                                                                   #
#####################################################################

class DaohangSpider(scrapy.Spider):
    name = 'daohang'
    allowed_domains = ['p2peye.com']
    start_urls = ['http://www.p2peye.com/dh.php']
    pipeline = ['UniqueItemPersistencePipeline']

    def parse(self, response):
        item_list = []
        plats = response.xpath('//div[@class="c_module2 clear"]/div[@class="main"]/div[@class="warp"]/div[@class="c_modreg"]/ul/li')
        for plat in plats:
            daohang = FeatureItem()
            url = get_content(plat.xpath('a/@href').extract())
            purl = url.split('/')
            while not purl[-1]: purl.pop()
            daohang['pin'] = purl.pop().split('.')[0]
            if daohang['pin'] in ['www', 'statistics']: continue
            daohang['name'] = get_content(plat.xpath('a/text()').extract())
            daohang['link'] = url

            item_list.append(daohang)

        return item_list
