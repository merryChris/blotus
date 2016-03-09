import scrapy, json
from utils.webpage import get_url_param, get_content
from weidai.items import ToubiaoItem, BiaorenItem

#############################################################################################
#                                                                                           #
# USAGE: nohup scrapy crawl biaoren -a from_id=1 -a to_id=1 --loglevel=INFO --logfile=log & #
#                                                                                           #
#############################################################################################

class BiaorenSpider(scrapy.Spider):
    name = 'biaoren'
    allowed_domains = ['www.weidai.com.cn']
    start_formated_url = 'https://www.weidai.com.cn/bid/tenderListPage?page=1&rows=100&bid={bid}'
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, from_id=1, to_id=1, *args, **kwargs):
        to_id = max(int(from_id), int(to_id))
        self.shortlist = range(int(from_id), int(to_id)+1)
        self.mapping = {}
        super(BiaorenSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in self.shortlist:
            obj = ToubiaoItem.get_object_by_pk(i)
            self.mapping[obj.pin] = obj.id
            url = self.start_formated_url.format(bid=obj.pin)
            yield self.make_requests_from_url(url)

    def parse(self, response):
        symbol = (self.mapping.get(get_url_param(response.url, 'bid')), response.url)
        self.logger.info('Parsing ID.%d Weidai Bidder Info From <%s>.' % symbol)

        item_list = []
        content = json.loads(response.body_as_unicode())['rows']
        for row in content:
            if not row['bid']: continue

            item = BiaorenItem()
            item['pin'] = row['bid']
            item['user'] = row['mobile']
            item['amount'] = row['currentTenderAmount']
            item['timestamp'] = row['tenderTime']
            item['source'] = row['source']

            item_list.append(item)

        return item_list
