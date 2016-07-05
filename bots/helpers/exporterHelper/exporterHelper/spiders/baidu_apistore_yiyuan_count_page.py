import scrapy, json
from exporterHelper.items import ExporterItem

#####################################################################################################
#                                                                                                   #
# USAGE: nohup scrapy crawl baidu_apistore_yiyuan_count_page -a channel_id=5572a108b3cdc86cf39001d0 #
#        -a api_key=xxxx --loglevel=INFO --logfile=log &                                            #
#                                                                                                   #
#####################################################################################################

class BaiduApistoreYiyuanCountPageSpider(scrapy.Spider):
    name = 'baidu_apistore_yiyuan_count_page'
    allowed_domains = ['baidu.com']
    start_formated_url = ('http://apis.baidu.com/showapi_open_bus/channel_news/search_news?'
                          'channelId={channel_id}&page=1&needContent=0&needHtml=0')
    pipeline = ['CacheFileExporterPersistencePipeline']

    def __init__(self, channel_id='', api_key=None, *args, **kwargs):
        self.channel_id = channel_id
        self.api_key = api_key
        super(BaiduApistoreYiyuanCountPageSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        url = BaiduApistoreYiyuanCountPageSpider.start_formated_url.format(channel_id=self.channel_id)
        print "### URL ###", url

        from scrapy.http import Request
        headers = {'apikey': self.api_key}
        yield Request(url, headers=headers)

    def parse(self, response):
        symbol = (self.channel_id, response.url)
        self.logger.info('Parsing [%s] Channel Count From <%s>.' % symbol)

        item = ExporterItem()
        try:
            content = json.loads(response.body_as_unicode())
            internal_content = content.get('showapi_res_body', {})
            if int(content.get('showapi_res_code', -1)) != 0 or not internal_content or \
               int(internal_content.get('ret_code', -1)) != 0:
                raise ValueError
        except Exception:
            self.logger.warning('Fail To Receive No.%s [%s] Plat Page Count From <%s>.' % symbol)
            return None

        item.set_record(internal_content.get('pagebean', {}).get('allPages', 0))
        return item
