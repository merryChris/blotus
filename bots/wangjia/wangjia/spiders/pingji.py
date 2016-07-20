import scrapy
from utils.webpage import log_empty_fields, get_content
from wangjia.items import PingjiItem

####################################################################################################
#                                                                                                  #
# USAGE: nohup scrapy crawl pingji -a page_id= -a timestamp=201606 --loglevel=INFO --logfile=log & #
#                                                                                                  #
####################################################################################################

class PingjiSpider(scrapy.Spider):
    name = 'pingji'
    allowed_domains = ['wdzj.com']
    start_formated_url = 'http://www.wdzj.com/pingji{page_id}.html'
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, page_id='', timestamp='201606', *args, **kwargs):
        self.page_id = page_id
        self.timestamp = timestamp
        super(PingjiSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        pid = '_'+str(self.page_id) if self.page_id else ''
        url = self.start_formated_url.format(page_id=pid)
        yield self.make_requests_from_url(url)

    def parse(self, response):
        symbol = (self.timestamp, response.url)
        self.logger.info('Parsing %s Wangjia Rating From <%s>.' % symbol)

        rating_list = []
        ratings = response.xpath('//div[@class="main_con1"]/table/tbody/tr')
        for rt in ratings:
            content = rt.xpath('td')
            # Decimal fields can be transformed by django itself.
            item = PingjiItem()
            item['timestamp'] = symbol[0]
            item['name'] = get_content(content[0].xpath('a/text()').extract())
            item['exponent'] = get_content(content[1].xpath('.//text()').extract())
            item['launch_time'] = get_content(content[2].xpath('.//text()').extract())
            item['location'] = get_content(content[3].xpath('span/text()').extract())
            item['deal'] = get_content(content[4].xpath('.//text()').extract())
            item['popularity'] = get_content(content[5].xpath('.//text()').extract())
            item['profit'] = get_content(content[6].xpath('.//text()').extract())
            item['dispersity'] = get_content(content[7].xpath('.//text()').extract())
            item['mobility'] = get_content(content[8].xpath('.//text()').extract())
            item['transparency'] = get_content(content[9].xpath('.//text()').extract())


            #log_empty_fields(item, self.logger)
            if item.get_uk(): rating_list.append(item)

        return rating_list
