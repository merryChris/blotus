import scrapy
from utils.webpage import log_empty_fields, get_trunk, get_content
from wangjia.items import DaohangItem, DanganItem

###############################################################################################
#                                                                                             #
# USAGE: nohup scrapy crawl dangan -a from_id=1 -a to_id=1291 --loglevel=INFO --logfile=log & #
#                                                                                             #
###############################################################################################

class DanganSpider(scrapy.Spider):
    name = 'dangan'
    allowed_domains = ['wdzj.com']
    start_url_prefix = 'http://www.wdzj.com/dangan/'
    pipeline = ['RelatedItemPersistencePipeline']

    def __init__(self, from_id=1, to_id=5, *args, **kwargs):
        self.shortlist = xrange(int(from_id), int(to_id)+1)
        self.mapping = {}
        super(DanganSpider, self).__init__(*args, **kwargs)

    def get_pin_from_url(self, url):
        return url.split('/')[-2]

    def start_requests(self):
        for i in self.shortlist:
            obj = DaohangItem.get_object_by_pk(i)
            self.mapping[obj.pin] = obj.id
            url = self.start_url_prefix + obj.pin + '/'
            yield self.make_requests_from_url(url)

    def parse(self, response):
        #NOTE: (zacky, APR.27th) PIPELINE FUNCTIONS RELATED WILL BE PROCESSED IN THE FOLLOWING STEP, SO WE KEEP THE OBJECT STATE HERE.
        symbol = (self.mapping.get(self.get_pin_from_url(response.url)), response.url)
        self.logger.info('Parsing ID.%d Wangjia Archive From <%s>.' % symbol)
        self.object = DaohangItem.get_object_by_pk(symbol[0])

        item = DanganItem()
        item['name'] = self.object.name
        item['logo_url'] = get_content(response.xpath('//div[@class="rLogo"]/a/img/@src').extract())

        detail = response.xpath('//div[contains(@class, "detailBox")]/p')
        if detail:
            item['link'] = get_content(detail[1].xpath('a/@href').extract())
            item['location'] = get_content(detail[3].xpath('text()').extract())
            item['launch_time'] = get_content(detail[4].xpath('text()').extract())

        about = response.xpath('//div[contains(@class, "aboutBd")]/p')
        if about:
            item['introduction'] = ' '.join([get_trunk(c) for c in about.xpath('.//text()').extract()])

        info = response.xpath('//div[contains(@class, "inforBd")]/p[not(contains(@class, "line"))]')
        if info:
            item['company_name'] = get_content(info[0].xpath('text()').extract())
            item['artificial_person'] = get_content(info[1].xpath('text()').extract())
            item['company_type'] = get_content(info[2].xpath('text()').extract())
            item['shareholder_stucture'] = get_content(info[3].xpath('text()').extract())
            item['registered_capital'] = get_content(info[4].xpath('text()').extract())
            item['contributed_capital'] = get_content(info[5].xpath('text()').extract())
            item['registered_address'] = get_content(info[6].xpath('text()').extract())
            item['opening_date'] = get_content(info[7].xpath('text()').extract())
            item['approved_date'] = get_content(info[8].xpath('text()').extract())
            item['registration_authority'] = get_content(info[9].xpath('text()').extract())
            item['business_licence'] = get_content(info[10].xpath('text()').extract())
            item['institutional_framework'] = get_content(info[11].xpath('text()').extract())
            item['tax_registration_num'] = get_content(info[12].xpath('text()').extract())

        record = response.xpath('//div[contains(@class, "webRecordBd")]/table/tbody/tr')[1].xpath('td')
        if record:
            item['domain_name'] = get_content(record[0].xpath('text()').extract())
            item['domain_date'] = get_content(record[1].xpath('text()').extract())
            item['domain_company_type'] = get_content(record[2].xpath('text()').extract())
            item['domain_company_name'] = get_content(record[3].xpath('text()').extract())
            item['icp'] = get_content(record[4].xpath('text()').extract())

        people = response.xpath('//div[contains(@class, "peopleBd")]/ul/li')
        if people:
            avatar_url = []
            content = []
            for i in xrange(len(people)):
                avatar_url.extend(people[i].xpath('div[@class="avatar"]/img/@src').extract())
                content.extend([get_trunk(c) for c in people[i].xpath('p//text()').extract()])
            item['company_person_avatar_url'] = '#'.join(avatar_url)
            item['company_person'] = ' '.join(content)

        cost = response.xpath('//div[contains(@class, "costBd")]')[0].xpath('p')
        if cost:
            item['management_fee'] = get_content(cost[0].xpath('text()').extract())
            item['prepaid_fee'] = get_content(cost[1].xpath('text()').extract())
            item['cash_withdrawal_fee'] = get_content(cost[2].xpath('text()').extract())
            item['vip_fee'] = get_content(cost[3].xpath('text()').extract())
            item['transfer_fee'] = get_content(cost[4].xpath('text()').extract())
            item['mode_of_payment'] = get_content(cost[5].xpath('text()').extract())

        contact = response.xpath('//div[contains(@class, "costBd")]')[1].xpath('p')
        if contact:
            item['contact_address'] = get_content(contact[0].xpath('text()').extract())
            item['phone_400'] = get_content(contact[1].xpath('text()').extract())
            item['phone'] = get_content(contact[2].xpath('text()').extract())
            item['fax'] = get_content(contact[3].xpath('text()').extract())
            item['email'] = get_content(contact[4].xpath('text()').extract())

        record = response.xpath('//div[contains(@class, "recordListBox")]/ul/li')
        if record:
            item['is_automatic_bid'] = get_content(record[3].xpath('.//text()').extract(), skipFirst=True)
            item['is_equitable_assignment'] = get_content(record[4].xpath('.//text()').extract(), skipFirst=True)
            item['trust_fund'] = get_content(record[5].xpath('.//text()').extract(), skipFirst=True)
            item['tender_security'] = get_content(record[6].xpath('.//text()').extract(), skipFirst=True)
            item['security_mode'] = get_content(record[7].xpath('.//text()').extract(), skipFirst=True)
            item['guarantee_institution'] = get_content(record[8].xpath('.//text()').extract(), skipFirst=True)
            item['business_type'] = len(record) >= 10 and get_content(record[9].xpath('.//text()').extract(), skipFirst=True)

        log_empty_fields(item, self.logger)
        return item
