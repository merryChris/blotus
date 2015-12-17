import scrapy
from utils.webpage import log_empty_fields, get_content
from wangjia.items import PingjiItem

################################################################################################################
#                                                                                                              #
# USAGE: nohup scrapy crawl pingji -a from_id=2 -a to_id=21 -a end_time=201506 --loglevel=INFO --logfile=log & #
#                                                                                                              #
################################################################################################################

class PingjiSpider(scrapy.Spider):
    name = 'pingji'
    allowed_domains = ['wdzj.com']
    start_url_prefix = 'http://www.wdzj.com/pingji.html'
    pipeline = ['UniqueItemPersistencePipeline']

    start_time = 201308
    end_time = 201506

    def __init__(self, from_id=2, to_id=1, start_time='201308', end_time='201506', cache=None, *args, **kwargs):
        #if cache:
        #    self.logger.info('Loading Candidates From File %s.' % cache)
        #    self.shortlist = self.get_ids_from_cache_file(cache)
        self.from_id = int(from_id)
        self.to_id = int(to_id)
        self.start_time = int(start_time)
        self.end_time = int(end_time)
        super(PingjiSpider, self).__init__(*args, **kwargs)

    def get_timestamp_from_url(self, url):
        pos = url.find('_')
        if pos == -1: return str(self.end_time)

        tmp_time = int(url[pos+1:url.rindex('.')]) - 2 + self.start_time
        return str((tmp_time / 100 + (tmp_time % 100 - 1) / 12) * 100 + ((tmp_time - 1) % 12) + 1)

    def start_requests(self):
        for i in ['_'+str(x) for x in xrange(self.from_id, self.to_id+1)] + ['']:
            pos = self.start_url_prefix.rindex('.')
            url = self.start_url_prefix[:pos] + i + self.start_url_prefix[pos:]
            yield self.make_requests_from_url(url)

    def parse(self, response):
        #NOTE: (zacky, APR.27th) PIPELINE FUNCTIONS RELATED WILL BE PROCESSED IN THE FOLLOWING STEP, SO WE KEEP THE OBJECT STATE HERE.
        symbol = (self.get_timestamp_from_url(response.url), response.url)
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


            log_empty_fields(item, self.logger)
            if item.get_uk(): rating_list.append(item)

        return rating_list
