import scrapy
import json
from utils.webpage import get_url_param
from renrendai.items import InvestRecordItem, LoanInfoItem


class InvestRecordSpider(scrapy.Spider):
    name = 'investrecord'
    allowed_domains = ['we.com']
    start_formated_url = 'http://www.we.com/lend/getborrowerandlenderinfo.action?id=lenderRecords&loanId={loan_id}'

    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, from_id=1, to_id=1, *args, **kwargs):
        to_id = max(int(from_id), int(to_id))
        self.shortlist = xrange(int(from_id), int(to_id) + 1)
        self.mapping = {}
        super(InvestRecordSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in self.shortlist:
            obj = LoanInfoItem.get_object_by_pk(i)
            self.mapping[obj.loan_id] = obj.id
            url = self.start_formated_url.format(loan_id=obj.loan_id)
            yield self.make_requests_from_url(url)

    def parse(self,response):
        symbol = (self.mapping.get(get_url_param(response.url, 'loanId')), response.url)
        self.logger.info('Parsing ID.%d Renrendai InvestRecord Info From <%s>.' % symbol)
        self.object = LoanInfoItem.get_object_by_pk(symbol[0])

        jsonData = response.xpath('//text()').extract()
        data = json.loads(jsonData[0])
        record = data['data']['lenderRecords']
        item_list = []
        if not record:
            return item_list
        for i in range(len(record)):
            item = InvestRecordItem()
            item['loan_id'] = record[i]['loanId']
            item['user_id'] = record[i]['userId']
            item['amount'] = record[i]['amount']
            datetime = record[i]['lendTime'].split('T')
            item['lend_time'] = datetime[0]+' '+datetime[1]
            item_list.append(item)
        return item_list
