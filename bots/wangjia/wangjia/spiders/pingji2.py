import scrapy
from utils.webpage import log_empty_fields, get_trunk, get_content
from wangjia.items import DaohangItem, PingjiItem

########################################################################################################
#                                                                                                      #
# USAGE: nohup scrapy crawl pingji2 -a timestamp=201506 -a cache=cache --loglevel=INFO --logfile=log & #
#                                                                                                      #
########################################################################################################

class Pingji2Spider(scrapy.Spider):
    name = 'pingji2'
    allowed_domains = ['wdzj.com']
    start_url_prefix = 'http://www.wdzj.com/dangan/'
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, timestamp='201506', cache=None, *args, **kwargs):
        self.timestamp = timestamp
        self.cache = cache
        super(Pingji2Spider, self).__init__(*args, **kwargs)

    def get_urls_from_cache_file(self, filePath=None):
        if not filePath: return []

        f = open(filePath, 'r')
        l = map(get_trunk, f.readlines())
        f.close()

        return l

    def start_requests(self):
        if self.cache:
            self.logger.info('Loading Exposure URLs From File %s.' % self.cache)
            self.start_urls = self.get_urls_from_cache_file(self.cache)

        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        symbol = (self.timestamp, response.url)
        self.logger.info('Parsing %s Wangjia Rating From Archive <%s>.' % symbol)

        item = PingjiItem()
        item['timestamp'] = symbol[0]

        detail = response.xpath('//div[contains(@class, "detailBox")]/p')
        if detail:
            item['name'] = get_content(detail[0].xpath('text()').extract())
            item['launch_time'] = get_content(detail[4].xpath('text()').extract())
            item['location'] = get_content(detail[3].xpath('text()').extract())

        record = response.xpath('//div[@class="recordHead"]/div[@class="con"]/p')
        if record:
            item['exponent'] = get_content(record.xpath('span[@class="num"]/text()').extract())

        exp = response.xpath('//div[contains(@class, "expBox")]/div[@class="bd"]/div[@class="detail"]/p')
        if not exp: return None
        item['deal'] = get_content(exp[0].xpath('span[@class="num"]/text()').extract())
        item['popularity'] = get_content(exp[1].xpath('span[@class="num"]/text()').extract())
        item['profit'] = get_content(exp[2].xpath('span[@class="num"]/text()').extract())
        item['revenue'] = get_content(exp[3].xpath('span[@class="num"]/text()').extract())
        item['lever'] = get_content(exp[4].xpath('span[@class="num"]/text()').extract())
        item['brand'] = get_content(exp[5].xpath('span[@class="num"]/text()').extract())
        item['dispersity'] = get_content(exp[7].xpath('span[@class="num"]/text()').extract())
        item['mobility'] = get_content(exp[8].xpath('span[@class="num"]/text()').extract())
        item['transparency'] = get_content(exp[6].xpath('span[@class="num"]/text()').extract())

        log_empty_fields(item, self.logger)
        return item
