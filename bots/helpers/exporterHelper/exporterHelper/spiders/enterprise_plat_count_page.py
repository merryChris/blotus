import scrapy, json
from utils.webpage import get_url_host
from utils.exporter import read_cache, parse_cookies
from exporterHelper.items import ExporterItem

#######################################################################################
#                                                                                     #
# USAGE: nohup scrapy crawl enterprise_plat_count_page -a plat_id=1 -a need_token=1   #
#        -a formated_url='http://www.xxx.com/api/category?token={token}&page_index=1' #
#        --loglevel=INFO --logfile=log &                                              #
#                                                                                     #
#######################################################################################

class EnterprisePlatCountPageSpider(scrapy.Spider):
    name = 'enterprise_plat_count_page'
    allowed_domains = []
    start_formated_url = None
    token_field = 'plat_id'
    pipeline = ['CacheFileExporterPersistencePipeline']

    def __init__(self, plat_id=None, need_token='0', formated_url=None, *args, **kwargs):
        self.plat_id = plat_id
        self.need_token = bool(int(need_token))
        self.start_formated_url = formated_url
        super(EnterprisePlatCountPageSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        token = ''
        lines = read_cache('tokens', (self.plat_id or 'test')+'.tk')
        if self.need_token and lines: token = lines[0]
        url = self.start_formated_url.format(token=token)

        from scrapy.http import Request
        cookies = parse_cookies(lines[1])
        yield Request(url, cookies=cookies)

    def parse(self, response):
        symbol = (self.plat_id, get_url_host(response.url), response.url)
        self.logger.info('Parsing No.%s [%s] Plat Page Count From <%s>.' % symbol)

        item = ExporterItem()
        try:
            content = json.loads(response.body_as_unicode())
            #content = {'result': '1', 'data': {'token': 'yamiedie'}}
            if int(content.get('result_code', 0)) != 1:
                raise ValueError
        except Exception as e:
            self.logger.warning('Fail To Receive No.%s [%s] Plat Page Count From <%s>.' % symbol)
            return None

        item.set_record(content.get('page_count', 0))
        return item
