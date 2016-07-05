import scrapy, json
from utils.webpage import get_url_param, trans_list_from_unicode_to_utf8
from baidu_apistore.items import YiyuanCaijingItem

###################################################################################
#                                                                                 #
# USAGE: nohup scrapy crawl yiyuan_caijing -a channel_id=5572a108b3cdc86cf39001d0 #
#        -a api_key=xxxx -a page_count=1 --loglevel=INFO --logfile=log &          #
#                                                                                 #
###################################################################################

class YiyuanCaijingSpider(scrapy.Spider):
    name = 'yiyuan_caijing'
    allowed_domains = ['baidu.com']
    start_formated_url = ('http://apis.baidu.com/showapi_open_bus/channel_news/search_news?'
                          'channelId={channel_id}&page={page_id}&needContent=0&needHtml=0')
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, channel_id='', api_key=None, page_count=0, *args, **kwargs):
        self.channel_id = channel_id
        self.api_key = api_key

        self.shortlist = xrange(1, int(page_count)+1)
        super(YiyuanCaijingSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'apikey': self.api_key}

        for i in self.shortlist:
            url = YiyuanCaijingSpider.start_formated_url.format(channel_id=self.channel_id, page_id=i)
            from scrapy.http import Request
            #yield Request(url, headers=headers, dont_filter=True)
            yield Request(url, headers=headers)

    def parse(self, response):
        symbol = (get_url_param(response.url, 'page'), get_url_param(response.url, 'channelId'), response.url)
        self.logger.info('Parsing No.%s Page [%s] Channel Info From <%s>.' % symbol)

        try:
            content = json.loads(response.body_as_unicode())
            internal_content = content.get('showapi_res_body', {})
            if int(content.get('showapi_res_code', -1)) != 0 or not internal_content or \
               int(internal_content.get('ret_code', -1)) != 0:
                raise ValueError
        except Exception:
            self.logger.warning('Fail To Receive No.%s [%s] Plat Page Count From <%s>.' % symbol)
            return None

        item_list = []
        for ct in internal_content.get('pagebean', {}).get('contentlist'):
            item = YiyuanCaijingItem()

            content = trans_list_from_unicode_to_utf8(ct.get('allList'))
            item['all_list'] = ''.join(map(str, content))

            content = trans_list_from_unicode_to_utf8(ct.get('imageurls'))
            item['image_urls'] = ''.join(map(str, content))

            item['link'] = ct.get('link')
            item['pub_date'] = ct.get('pubDate')
            item['title'] = ct.get('title')
            item['channel_name'] = ct.get('channelName')
            item['desc'] = ct.get('desc')
            item['source'] = ct.get('source')

            item_list.append(item)

        return item_list
