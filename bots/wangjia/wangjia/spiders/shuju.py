import scrapy
from utils.webpage import log_empty_fields, get_url_param, get_trunk, get_content
from utils.datetime import get_timestamp, get_date_list
from wangjia.items import ShujuItem
import json

#############################################################################################################
#                                                                                                           #
# USAGE: nohup scrapy crawl shuju -a from_date=20150501 -a to_date=20150531 --loglevel=INFO --logfile=log & #
#                                                                                                           #
#############################################################################################################

class ShujuSpider(scrapy.Spider):
    name = 'shuju'
    allowed_domains = ['wdzj.com']
    start_formated_url = 'http://shuju.wdzj.com/platdata-custom.html?timestamp={timestamp}'
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, from_date='', to_date='', *args, **kwargs):
        if not (from_date and to_date and from_date <= to_date):
            from_date = to_date = ''
        self.from_date, self.to_date = from_date, to_date
        super(ShujuSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        #NOTE: (zacky, 2015.MAY.19th) WE MAYNOT NEED TO SET COOKIE.
        headers   = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0',
                     'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',}
        post_data = {'custom':'0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17',
                     'status':'1',}
        for date in get_date_list(from_date=self.from_date, to_date=self.to_date, delimiter='-'):
            post_data['startTime'] = post_data['endTime'] = date
            yield scrapy.FormRequest(self.start_formated_url.format(timestamp=date), method='POST', headers=headers, formdata=post_data)

    def parse(self, response):
        symbol = (get_url_param(response.url, 'timestamp'), response.url)
        self.logger.info('Parsing %s Wangjia Data From <%s>.' % symbol)

        try:
            content = json.loads(response.body_as_unicode())
            if not content or not len(content):
                raise ValueError
        except Exception as e:
            self.logger.warning('Empty Response Of %s Wangjia Data From <%s>.' % symbol)
            return None

        timestamp, data_list = get_timestamp(symbol[0], '-'), []
        for data in content:
            item = ShujuItem()
            item['timestamp'] = timestamp
            item['name'] = data['platName']
            item['volume'] = data['amount']
            item['investment_passenger'] = data['bidderNum']
            item['loan_passenger'] = data['borrowerNum']
            item['average_interest_rate'] = data['incomeRate']
            item['average_loan_period'] = data['loanPeriod']
            item['loan_bid'] = data['totalLoanNum']
            item['registered_capital'] = data['regCapital']
            item['time_for_full_bid'] = data['fullloanTime']
            item['accounted_revenue'] = data['stayStillOfTotal']
            item['capital_inflow_in_30_days'] = data['netInflowOfThirty']
            item['volumn_weighted_time'] = data['weightedAmount']
            item['accounted_revenue_in_60_days'] = data['stayStillOfNextSixty']
            item['proportion_of_top_10_tuhao_accounted_revenue'] = data['top10DueInProportion']
            item['average_investment_amount'] = data['avgBidMoney']
            item['proportion_of_top_10_borrower_accounted_revenue'] = data['top10StayStillProportion']
            item['average_loan_amount'] = data['avgBorrowMoney']
            item['capital_lever'] = data['currentLeverageAmount']
            item['operation_time'] = data['timeOperation']

            #log_empty_fields(item, self.logger)
            if item.get_uk(): data_list.append(item)

        return data_list
