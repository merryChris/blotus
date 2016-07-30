import scrapy, json
from utils.webpage import log_empty_fields, get_url_param
from utils.exporter import read_cache
from aif.items import JibenItem

#################################################################################################
#                                                                                               #
# USAGE: nohup scrapy crawl jiben -a plat_id=1 -a need_token=1                                  #
#        -a formated_url='http://api.xxx.com/interface-basicdata?token={token}&date=yyyy-mm-dd' #
#        --loglevel=INFO --logfile=log &                                                        #
#                                                                                               #
#################################################################################################

class JibenSpider(scrapy.Spider):
    name = 'jiben'
    allowed_domains = ['zwgt.com']
    start_formated_url = None
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, plat_id=None, need_token='0', formated_url='', *args, **kwargs):
        self.plat_id = plat_id
        self.need_token = bool(int(need_token))
        self.start_formated_url = formated_url

        super(JibenSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        token = ''
        lines = read_cache('tokens', (self.plat_id or 'test')+'.tk')

        if self.need_token and lines: token = lines[0]
        url = self.start_formated_url.format(token=token)

        yield self.make_requests_from_url(url)

    def parse(self, response):
        symbol = (self.plat_id, response.url)
        self.logger.info('Parsing No.%s Plat Basic Data From <%s>.' % symbol)

        try:
            content = json.loads(response.body_as_unicode())
            internal_content = content.get('data', {})
            if int(content.get('result_code', -1)) != 1 or not internal_content:
                raise ValueError
        except Exception:
            self.logger.warning('Fail To Receive No.%s Plat Basic Data From <%s>.' % symbol)
            return None

        item = JibenItem()
        item['plat_id'] = self.plat_id
        item['date'] = get_url_param(response.url, 'date')
        item['turnover_amount'] = internal_content.get('turnover_amount')
        item['trade_amount'] = internal_content.get('trade_amount')
        item['borrower_amount'] = internal_content.get('borrower_amount')
        item['investor_amount'] = internal_content.get('investor_amount')
        item['loan_amount_per_capita'] = internal_content.get('loan_amount_per_capita')
        item['avg_loan_per_trade'] = internal_content.get('avg_loan_per_trade')
        item['invest_amount_per_capita'] = internal_content.get('invest_amount_per_capita')
        item['avg_invest_per_trade'] = internal_content.get('avg_invest_per_trade')
        item['loan_balance'] = internal_content.get('loan_balance')
        item['max_borrower_ratio'] = internal_content.get('max_borrower_ratio')
        item['topten_borrowers_ratio'] = internal_content.get('topten_borrowers_ratio')
        item['avg_full_time'] = internal_content.get('avg_full_time')
        item['accum_default_rate'] = internal_content.get('accum_default_rate')
        item['product_overdue_rate'] = internal_content.get('product_overdue_rate')
        item['three_month_overdue_rate'] = internal_content.get('three_month_overdue_rate')
        item['overdue_loan_amount'] = internal_content.get('overdue_loan_amount')
        item['compensatory_amount'] = internal_content.get('compensatory_amount')
        item['loan_overdue_rate'] = internal_content.get('loan_overdue_rate')
        item['bad_debt_rate'] = internal_content.get('bad_debt_rate')
        item['customer_complaints'] = internal_content.get('customer_complaints')
        item['customer_complaints_solve'] = internal_content.get('customer_complaints_solve')
        item['interest_rate'] = internal_content.get('interest_rate')
        item['avg_borrow_period'] = internal_content.get('avg_borrow_period')
        item['topten_investor_ratio'] = internal_content.get('topten_investor_ratio')
        item['financial_leverage'] = internal_content.get('financial_leverage')
        item['repaid_amount'] = internal_content.get('repaid_amount')

        log_empty_fields(item, self.logger)
        return item
