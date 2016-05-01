import scrapy, json
from utils.webpage import get_url_host
from exporterHelper.items import ExporterItem

########################################################################################################
#                                                                                                      #
# USAGE: nohup scrapy crawl enterprise_plat_login -a plat_id=1 -a login_url='http://xxx.com/login?a=b' #
#        --loglevel=INFO --logfile=log &                                                               #
#                                                                                                      #
########################################################################################################

class EnterprisePlatLoginSpider(scrapy.Spider):
    name = 'enterprise_plat_login'
    allowed_domains = []
    start_formated_url = None
    token_field = 'plat_id'
    pipeline = ['TokenFileExporterPersistencePipeline']

    def __init__(self, plat_id=None, login_url=None, *args, **kwargs):
        self.plat_id = plat_id
        self.login_url = login_url
        super(EnterprisePlatLoginSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        if self.login_url:
            yield self.make_requests_from_url(self.login_url)

    def parse(self, response):
        symbol = (self.plat_id, get_url_host(response.url), response.url)
        self.logger.info('Parsing No.%s [%s] Plat Login Info From <%s>.' % symbol)

        item = ExporterItem()
        try:
            content = json.loads(response.body_as_unicode())
            if int(content.get('result', 0)) == 1:
                item['record'] = content.get('data', {}).get('token')
        except Exception as e:
            pass

        return item
