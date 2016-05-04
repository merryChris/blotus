import scrapy
from utils.webpage import get_trunk, get_content
from utils.exporter import read_cache
from wangjia.items import BaoguangItem

#####################################################################################
#                                                                                   #
# USAGE: nohup scrapy crawl baoguang -a cache=cache --loglevel=INFO --logfile=log & #
#                                                                                   #
#####################################################################################

class BaoguangSpider(scrapy.Spider):
    name = 'baoguang'
    allowed_domains = ['wdzj.com']
    start_urls = []
    image_url_prefix = 'http://bbs.wdzj.com/'
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, cache='cache', *args, **kwargs):
        self.cache = cache+'.ch'
        super(BaoguangSpider, self).__init__(*args, **kwargs)

    def get_thread_from_url(self, url):
        if url.find('-') != -1: return url.split('-')[1]
        if url.find('=') != -1: return url.split('=')[-1]

        return None

    def modify_image_url(self, url):
        if not url.startswith('http'):
            return self.image_url_prefix + url

        return url

    def start_requests(self):
        if self.cache:
            self.logger.info('Loading Exposure URLs From File %s.' % self.cache)
            self.start_urls = read_cache('cache', self.cache)

        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        symbol = (self.get_thread_from_url(response.url), response.url)
        if not symbol[0]:
            self.logger.warning('Invalid Wangjia Exposure Item From <%s>.' % symbol[1])
            return None

        if response.xpath('//div[@class="wrap"]'):
            self.logger.warning('May Redirect To Warning Page Of Wangjia.')
            return None

        if response.xpath('//div[@id="messagetext" and @class="alert_info"]'):
            self.logger.warning('No.%s Wangjia Exposure Item From <%s> Maybe Limited.' % symbol)
            return None

        self.logger.info('Parsing No.%s Wangjia Exposure Item From <%s>.' % symbol)

        item = BaoguangItem()
        item['thread'] = int(symbol[0])
        item['source'] = symbol[1]

        title = response.xpath('//span[@id="thread_subject"]')
        item['title'] = get_content(title.xpath('text()').extract())

        subtitle = response.xpath('//em[starts-with(@id, "authorposton")]')[0]
        poston = get_content(subtitle.xpath('text()').extract(), skipBlank=False)
        item['created'] = poston[poston.index(' ')+1:]

        header = response.xpath('//div[@class="typeoption"]/table/tbody/tr/td')
        if header:
            item['name'] = get_content(header[0].xpath('.//text()').extract())
            item['link'] = get_content(header[1].xpath('.//text()').extract())
            item['reason'] = get_content(header[2].xpath('.//text()').extract())

        body = response.xpath('//td[starts-with(@id, "postmessage")]')[0]
        #item['content'] = ''.join([get_trunk(c) for c in body.xpath('text()|*[not(@class="pstatus")]/text()|*[not(@class="pstatus")]/*/text()').extract()])
        item['content'] = ''.join([get_trunk(c) for c in body.xpath('.//text()').extract()])
        item['raw_content'] = get_content(body.extract())
        item['image_url'] = '#'.join([self.modify_image_url(get_trunk(c)) for c in body.xpath('.//@file').extract()]) or None

        return item
