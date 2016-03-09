import scrapy
import json
from renrendai.items import LoanInfoItem

class LoanIdSpider(scrapy.Spider):
    name = 'loanid'
    allowed_domains = ['we.com']
    start_formated_url = 'http://www.we.com/lend/loanList!json.action?pageIndex={page_index}'

    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, start_page_id=1, end_page_id=1, *args, **kwargs):
        self.shortlist = xrange(int(start_page_id), int(end_page_id) + 1)
        super(LoanIdSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in self.shortlist:
            url = self.start_formated_url.format(page_index=i)
            yield self.make_requests_from_url(url)

    def parse(self,response):
        self.logger.info('Parsing Renrendai Loan List Info From <%s>.' % response.url)

        jsonData = response.xpath('//text()').extract()
        data = json.loads(jsonData[0])
        loaninfo = data['data']['loans']
        item_list = []
        if not loaninfo:
            return item_list
        for i in range(len(loaninfo)):
            item = LoanInfoItem()
            item['loan_id'] = int(loaninfo[i]['loanId'])
            item['title'] = loaninfo[i]['title']
            item['status'] = loaninfo[i]['status']
            item_list.append(item)
        return item_list