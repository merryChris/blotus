import scrapy, json
from utils.webpage import log_empty_fields, get_url_host, get_url_param
from utils.exporter import read_cache, parse_cookies
from enterprise.items import YuqiItem

##################################################################################################
#                                                                                                #
# USAGE: nohup scrapy crawl yuqi -a plat_id=1 -a plat_name=ymd -a need_token=1                   #
#        -a formated_url='http://www.xxx.com/api/overdues?token={token}&page_index={page_index}' #
#        -a cache=cache --loglevel=INFO --logfile=log &                                          #
#                                                                                                #
##################################################################################################

class YuqiSpider(scrapy.Spider):
    name = 'yuqi'
    allowed_domains = []
    start_formated_url = None
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, plat_id=None, plat_name=None, need_token='0', formated_url=None, cache='cache', \
                 *args, **kwargs):
        self.plat_id = plat_id
        self.plat_name = plat_name
        self.need_token = bool(int(need_token))
        self.start_formated_url = formated_url

        lines, total_page = read_cache('cache', cache+'.ch'), 0
        if lines: total_page = int(lines[0])
        self.shortlist = xrange(1, total_page+1)
        super(YuqiSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in self.shortlist:
            token = ''
            lines = read_cache('tokens', (self.plat_id or 'test')+'.tk')

            if self.need_token and lines: token = lines[0]
            url = self.start_formated_url.format(token=token, page_index=i)

            from scrapy.http import Request
            cookies = parse_cookies(lines[1])
            yield Request(url, cookies=cookies)

    def parse(self, response):
        symbol = (get_url_param(response.url, 'page_index'), get_url_host(response.url), response.url)
        self.logger.info('Parsing No.%s Page %s Overdue Info From <%s>.' % symbol)

        try:
            content = json.loads(response.body_as_unicode())
            if int(content.get('result_code', 0)) != 1:
                raise ValueError
        except Exception:
            self.logger.warning('Response Error In No.%s Page %s Overdue Info From <%s>.' % symbol)
            return None

        item_list = []
        for dy in content.get('data', []):
            item = YuqiItem()
            item['plat_id'] = self.plat_id
            item['plat_name'] = self.plat_name
            item['user_id'] = dy.get('user_id')
            item['username'] = dy.get('username')
            item['idcard'] = dy.get('idcard')
            item['overdue_count'] = dy.get('overdue_count')
            item['overdue_total'] = dy.get('overdue_total')
            item['overdue_principal'] = dy.get('overdue_principal')
            item['payment_total'] = dy.get('payment_total')
            item['payment_count'] = dy.get('payment_count')
            item['payment_period'] = dy.get('payment_period')
            item['repay_amount'] = dy.get('repay_amount')
            item['wait_amount'] = dy.get('wait_amount')

            log_empty_fields(item, self.logger)
            item_list.append(item)

        return item_list
