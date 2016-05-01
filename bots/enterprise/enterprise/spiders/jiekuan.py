import scrapy
from utils.webpage import log_empty_fields, get_url_host, get_url_param
from utils.exporter import read_cache
from enterprise.items import JiekuanItem

###############################################################################################
#                                                                                             #
# USAGE: nohup scrapy crawl jiekuan -a plat_id=1 -a plat_name=ymd -a need_token=1             #
#        -a formated_url='http://www.xxx.com/api/loans?token={token}&page_index={page_index}' #
#        -a total_page=1 --loglevel=INFO --logfile=log &                                      #
#                                                                                             #
###############################################################################################

class JiekuanSpider(scrapy.Spider):
    name = 'jiekuan'
    allowed_domains = []
    start_formated_url = None
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, plat_id=None, plat_name=None, need_token='0', formated_url=None, total_page=0, *args, \
                 **kwargs):
        self.plat_id = plat_id
        self.plat_name = plat_name
        self.need_token = bool(int(need_token))
        self.start_formated_url = formated_url
        self.shortlist = xrange(1, int(total_page)+1)
        super(JiekuanSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in self.shortlist:
            token = ''
            if self.need_token:
                lines = read_cache('tokens', (self.plat_id or 'test')+'.tk')
                if lines: token = lines[0]
            url = self.start_formated_url.format(token=token, page_index=i)
            yield self.make_requests_from_url(url)

    def parse(self, response):
        symbol = (get_url_param(response.url, 'page_index'), get_url_host(response.url), response.url)
        self.logger.info('Parsing No.%s Page %s Loan Info From <%s>.' % symbol)

        try:
            content = json.loads(response.body_as_unicode())
            if int(content.get('result_code', 0)) != 1:
                raise ValueError
        except Exception as e:
            self.logger.warning('Response Error In No.%s Page %s Loan Info From <%s>.' % symbol)
            return None

        item_list = []
        for dj in content.get('data', []):
            item = JiekuanItem()
            item['bid_id'] = dj.get('bid_id')
            item['plat_id'] = self.plat_id
            item['plat_name'] = self.plat_name
            item['title'] = dj.get('title')
            item['amount'] = dj.get('amount')
            item['process'] = dj.get('process')
            item['interest_rate'] = dj.get('interest_rate')
            item['borrow_period'] = dj.get('borrow_period')
            item['borrow_unit'] = dj.get('borrow_unit')
            item['reward'] = dj.get('reward')
            item['type'] = dj.get('type')
            item['repay_type'] = dj.get('repay_type')
            item['username'] = dj.get('username')
            item['user_id'] = dj.get('user_id')
            item['user_avatar_url'] = dj.get('user_avatar_url')
            item['province'] = dj.get('province')
            item['city'] = dj.get('city')
            item['borrow_detail'] = dj.get('borrow_detail')
            item['url'] = dj.get('url')
            item['success_time'] = dj.get('success_time')
            item['publish_time'] = dj.get('publish_time')
            item['invest_count'] = dj.get('invest_count')
            item_list.append(item)

        return item_list
