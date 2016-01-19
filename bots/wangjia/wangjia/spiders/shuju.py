import scrapy
from utils.webpage import log_empty_fields, get_trunk, get_content
from utils.datetime import get_date_list,get_next_date
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
    start_url = 'http://shuju.wdzj.com/platdata-custom.html'
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, from_date='20150505', to_date='20150505', cache=None, *args, **kwargs):
        #if cache:
        #    self.logger.info('Loading Candidates From File %s.' % cache)
        #    self.shortlist = self.get_ids_from_cache_file(cache)
        if from_date <= to_date: self.from_date, self.to_date = from_date, to_date
        else: self.from_date = self.to_date = '20150505'
        super(ShujuSpider, self).__init__(*args, **kwargs)

    def get_timestamp_from_date(self, date):
        return ''.join(date.split('-'))

    def start_requests(self):
        #NOTE: (zacky, 2015.MAY.19th) WE MAYNOT NEED TO SET COOKIE.
        for d in get_date_list(from_date=self.from_date, to_date=self.to_date, delimiter='-'):
            headers = {
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0',
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            }
            post_data = {
                'startTime':d,
                'endTime':d,
                'custom':'0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17',
                'status':'1'
            }
            yield scrapy.FormRequest(
                self.start_url,
                method = 'POST',
                headers = headers,
                formdata = post_data
                )

    def parse(self, response):
        jsonData = response.xpath('//text()').extract()
        data = json.loads(jsonData[0])
        data_list = []
        for i in range(len(data)):
            item = ShujuItem()
            item['timestamp'] = self.from_date
            item['name'] = data[i]['platName']
            item['volume'] = data[i]['amount']
            item['investment_passenger'] = data[i]['bidderNum']
            item['loan_passenger'] = data[i]['borrowerNum']
            item['average_interest_rate'] = data[i]['incomeRate']
            item['average_loan_period'] = data[i]['loanPeriod']
            item['loan_bid'] = data[i]['totalLoanNum']
            item['registered_capital'] = data[i]['regCapital']
            item['time_for_full_bid'] = data[i]['fullloanTime']
            item['accounted_revenue'] = data[i]['stayStillOfTotal']
            item['capital_inflow_in_30_days'] = data[i]['netInflowOfThirty']
            item['volumn_weighted_time'] = data[i]['weightedAmount']
            item['accounted_revenue_in_60_days'] = data[i]['stayStillOfNextSixty']
            item['proportion_of_top_10_tuhao_accounted_revenue'] = data[i]['top10DueInProportion']
            item['average_investment_amount'] = data[i]['avgBidMoney']
            item['proportion_of_top_10_borrower_accounted_revenue'] = data[i]['top10StayStillProportion']
            item['average_loan_amount'] = data[i]['avgBorrowMoney']
            item['capital_lever'] = data[i]['currentLeverageAmount']
            item['operation_time'] = data[i]['timeOperation']

            log_empty_fields(item, self.logger)
            if item.get_uk(): data_list.append(item)
        self.from_date = self.get_timestamp_from_date(get_next_date(self.from_date,'-'))
        return data_list
