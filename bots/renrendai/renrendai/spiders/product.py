import scrapy
from utils.webpage import get_url_param
from renrendai.items import ProductItem, BorrowerItem, LoanInfoItem

class ProductSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['we.com']
    start_formated_url = 'http://www.we.com/lend/detailPage.action?loanId={loan_id}'

    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, jsessionid=None, from_id=1, to_id=1, *args, **kwargs):
        self.jsessionid = jsessionid
        to_id = max(int(from_id), int(to_id))
        self.shortlist = xrange(int(from_id), int(to_id) + 1)
        self.mapping = {}
        super(ProductSpider,self).__init__(*args,**kwargs)

    def start_requests(self):
        for i in self.shortlist:
            obj = LoanInfoItem.get_object_by_pk(i)
            self.mapping[obj.loan_id] = obj.id
            url = self.start_formated_url.format(loan_id=obj.loan_id)
            #NOTE: (lwh, 2016.MAR.9th) JSESSIONID MAY BE EXPIRED AFTER SOME IDEL PERIOD.
            yield scrapy.http.Request(
                url,
                cookies = {'JSESSIONID':self.jsessionid},
                dont_filter=True
            )

    def parse(self,response):
        symbol = (self.mapping.get(get_url_param(response.url, 'loanId')), response.url)
        self.logger.info('Parsing ID.%d Renrendai Product and Borrower Info From <%s>.' % symbol)
        self.object = LoanInfoItem.get_object_by_pk(symbol[0])

        pitem = ProductItem()
        pitem['loan_id'] = response.url.split('=')[1]
        pitem['product_name'] = response.xpath('//em[@class="title-text"]/text()').extract()[0]
        pitem['amount'] = float(response.xpath('//dl[@class="fn-left w300"]/dd/em/text()').extract()[0].replace(',',''))
        pitem['income_ratio'] = float(response.xpath('//dl[@class="fn-left w240"]/dd/em/text()').extract()[0])
        pitem['pay_period'] = int(response.xpath('//dl[@class="fn-left w140"]/dd/em/text()').extract()[0])
        path = response.xpath('//div[@class="fn-left pt10 loaninfo "]/ul/li')
        pitem['guarantee_method'] = path[0].xpath('./span[2]/text()').extract()[0]
        pitem['pre_pay_ratio'] = float(path[0].xpath('./span[4]/em/text()').extract()[0])
        pitem['pay_method'] = path[1].xpath('./span[2]/text()').extract()[0]
        pitem['loan_detail'] = response.xpath('//div[@class = "ui-tab-list color-dark-text"]/text()').extract()[0].strip()

        bitem = BorrowerItem()
        detail = response.xpath('//table[@class="ui-table-basic-list"]/tr')
        bitem['loan_id'] = response.url.split('=')[1]
        bitem['user_id'] = detail[0].xpath('./td[@class="basic-filed-1"]/div/em/a/@href').extract()[0].split('=')[1]
        bitem['user_nickname'] = detail[0].xpath('./td[1]/div/em/a/text()').extract()[0]
        bitem['credit_level'] = filter(lambda x: x.isdigit(), detail[0].xpath('./td[2]/div/em/@title').extract()[0])

        # basic information
        bitem['age'] = int(detail[2].xpath('./td[1]/div/em/text()').extract()[0])
        bitem['education'] = detail[2].xpath('./td[2]/div/em/text()').extract()[0]
        bitem['marriage'] = detail[2].xpath('./td[3]/div/em/text()').extract()[0]

        # credit information
        bitem['loan_application_num'] = int(detail[4].xpath('./td[1]/div/em/text()').extract()[0].encode('utf-8')[:-3])
        bitem['credit_line'] = float(detail[4].xpath('./td[2]/div/em/text()').extract()[0].encode('utf-8')[:-3].replace(',',''))
        bitem['overdue_amount'] = float(detail[4].xpath('./td[3]/div/em/text()').extract()[0].encode('utf-8')[:-3].replace(',',''))
        bitem['success_application_num'] = int(detail[5].xpath('./td[1]/div/em/text()').extract()[0].encode('utf-8')[:-3])
        bitem['total_loan_amount'] = float(detail[5].xpath('./td[2]/div/em/text()').extract()[0].encode('utf-8')[:-3].replace(',',''))
        bitem['overdue_times'] = int(detail[5].xpath('./td[3]/div/em/text()').extract()[0].encode('utf-8')[:-3])
        bitem['payoff_num'] = int(detail[6].xpath('./td[1]/div/em/text()').extract()[0].encode('utf-8')[:-3])
        bitem['total_left_to_pay'] = float(detail[6].xpath('./td[2]/div/em/text()').extract()[0].encode('utf-8')[:-3].replace(',',''))
        bitem['critical_overdue_times'] = int(detail[6].xpath('./td[3]/div/em/text()').extract()[0].encode('utf-8')[:-3])

        # property information
        bitem['income_scale'] = detail[8].xpath('./td[1]/div/em/text()').extract()[0]

        # job information
        bitem['city'] = detail[11].xpath('./td[1]/div/em/text()').extract()[0]
        bitem['length_of_service'] = detail[11].xpath('./td[2]/div/em/text()').extract()[0]

        return pitem, bitem
