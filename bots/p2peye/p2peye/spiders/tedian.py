import scrapy
from utils.webpage import get_content
from p2peye.items import FeatureItem

###############################################################################################
#                                                                                             #
# USAGE: nohup scrapy crawl tedian -a from_id=1 -a to_id=1291 --loglevel=INFO --logfile=log & #
#                                                                                             #
###############################################################################################

class TedianSpider(scrapy.Spider):
    name = 'tedian'
    allowed_domains = ['p2peye.com']
    pipeline = ['UniqueItemPersistencePipeline']

    def __init__(self, from_id=1, to_id=5, cache=None, *args, **kwargs):
        self.shortlist = xrange(int(from_id), int(to_id)+1)
        super(TedianSpider, self).__init__(*args, **kwargs)

    def get_pin_from_url(self, url):
        purl = url.split('/')
        while not purl[-1]: purl.pop()

        return purl.pop().split('.')[0]

    def start_requests(self):
        for i in self.shortlist:
            obj = FeatureItem.get_object_by_pk(i)
            yield self.make_requests_from_url(obj.link)

    def parse(self, response):
        self.logger.info('Parsing P2peye Archive Feature From <%s>.' % response.url)

        item = FeatureItem()
        item['pin'] = self.get_pin_from_url(response.url)

        feature_list = response.xpath('//div[@class="bd ui-yun-parent"]/a')
        features = []
        if feature_list:
            for fl in feature_list:
                fc = get_content(fl.xpath('text()').extract())
                if fc: features.append(fc)
        item['feature'] = ' '.join(features)

        return item
