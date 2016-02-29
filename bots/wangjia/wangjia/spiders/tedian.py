import scrapy
from utils.webpage import get_trunk, get_content
from wangjia.items import DaohangItem, TedianItem

#############################################################################################
#                                                                                           #
# USAGE: nohup scrapy crawl feature -a from_id=1 -a to_id=5 --loglevel=INFO --logfile=log & #
#                                                                                           #
#############################################################################################

class TedianSpider(scrapy.Spider):
    name = 'tedian'
    allowed_domains = ['wdzj.com']
    start_formated_url = 'http://www.wdzj.com/dangan/{plat_pin}/'
    pipeline = ['RelatedItemPersistencePipeline']

    def __init__(self, from_id=1, to_id=5, *args, **kwargs):
        self.shortlist = xrange(int(from_id), int(to_id)+1)
        self.mapping = {}
        super(TedianSpider, self).__init__(*args, **kwargs)

    def get_pin_from_url(self, url):
        return url.split('/')[-2]

    def start_requests(self):
        for i in self.shortlist:
            obj = DaohangItem.get_object_by_pk(i)
            self.mapping[obj.pin] = obj.id
            url = self.start_formated_url.format(plat_pin=obj.pin)
            yield self.make_requests_from_url(url)

    def parse(self, response):
        symbol = (self.mapping.get(self.get_pin_from_url(response.url)), response.url)
        self.logger.info('Parsing ID.%d Wangjia Feature From <%s>.' % symbol)
        self.object = DaohangItem.get_object_by_pk(symbol[0])

        item = TedianItem()
        item['name'] = self.object.name

        rtag = response.xpath('//div[@class="rTags"]')
        if rtag:
            item['status'] = get_content(rtag.xpath('./span[@class="tag3"]/text()').extract())
            item['company_tag'] = get_content(rtag.xpath('./span[@class="tag tag2"]/text()').extract())

            tag_info = rtag.xpath('./span[@class = "tag"]')
            item['illustration'] = '/'.join([get_trunk(info) for info in tag_info.xpath('text()').extract()])

        comment_info = response.xpath('//div[contains(@class,"box commentBox")]')
        if comment_info:
            commentScores = comment_info.xpath('./dl[@class="comment"]')
            item['recommendation'] = get_content(commentScores.xpath('./dt/span/text()').extract())

            score = commentScores.xpath('./dd/span[@class="num"]')
            item['withdraw_num'] = get_content(score[0].xpath('text()').extract())
            item['guard_num'] = get_content(score[1].xpath('text()').extract())
            item['service_num'] = get_content(score[2].xpath('text()').extract())
            item['experience_num'] = get_content(score[3].xpath('text()').extract())
    
            scoreInfo = commentScores.xpath('.//span[not(@class="num")]')
            item['withdraw_day'] = get_content(scoreInfo[0].xpath('text()').extract())
            item['guard_day'] = get_content(scoreInfo[1].xpath('text()').extract())
            item['service_status'] = get_content(scoreInfo[2].xpath('text()').extract())
            item['experience_status'] = get_content(scoreInfo[3].xpath('text()').extract())

            impress_info = comment_info.xpath('./dl[@class="impression"]/dd//span')
            item['impression'] = '\001'.join([get_trunk(impress) for impress in impress_info.xpath('text()').extract()])

        return item
