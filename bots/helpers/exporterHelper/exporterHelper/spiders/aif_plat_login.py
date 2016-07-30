import scrapy, json
from utils.webpage import get_url_host
from exporterHelper.items import ExporterItem

############################################################################################
#                                                                                          #
# USAGE: nohup scrapy crawl aif_login -a plat_id=1 -a login_url='http://xxx.com/login?a=b' #
#        --loglevel=INFO --logfile=log &                                                   #
#                                                                                          #
############################################################################################

class AIFPlatLoginSpider(scrapy.Spider):
    name = 'aif_plat_login'
    allowed_domains = []
    start_formated_url = None
    token_field = 'plat_id'
    pipeline = ['TokenFileExporterPersistencePipeline']

    def __init__(self, plat_id=None, login_url=None, *args, **kwargs):
        self.plat_id = plat_id
        self.login_url = login_url
        super(AIFPlatLoginSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        if self.login_url:
            yield self.make_requests_from_url(self.login_url)

    def parse(self, response):
        symbol = (self.plat_id, get_url_host(response.url), response.url)
        self.logger.info('Parsing No.%s [%s] Plat Login Info From <%s>.' % symbol)

        try:
            content = json.loads(response.body_as_unicode())
            #content = {'result': '1', 'data': {'token': 'yamiedie'}}
            if int(content.get('result', 0)) != 1:
                raise ValueError
        except Exception:
            self.logger.warning('Fail To Receive No.%s [%s] Plat Login Info From <%s>.' % symbol)
            return None

        item = ExporterItem()
        item.set_record(content.get('data', {}).get('token'))
        #item.set_record(json.dumps(response.headers.getlist('Set-Cookie')))
        return item
