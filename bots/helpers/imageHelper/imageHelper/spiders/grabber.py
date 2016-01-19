import scrapy
from imageHelper.items import ImageItem

# For model support.
from bots.wangjia.wangjia.items import DaohangItem, DanganItem, BaoguangItem, XinwenItem

####################################################################################
#                                                                                  #
# USAGE: nohup scrapy crawl grabber -a from_id=1 -a to_id=2 -a category=exposure \ #
#        -a model=BaoguangItem -a field=image_url --loglevel=INFO --logfile=log &  #
#                                                                                  #
####################################################################################

class GrabberSpider(scrapy.Spider):
    name = 'grabber'
    allowed_domains = ['wdzj.com']
    #NOTE: (zacky, 2015.JUN.2nd) FAKE URL TO PROCESS SUCCESSFULLY.
    fake_url = 'https://www.baidu.com/'
    start_urls = []

    def __init__(self, from_id=1, to_id=2, category='', model='', field='', *args, **kwargs):
        self.shortlist = xrange(int(from_id), int(to_id)+1)
        self.category = category
        self.model = model
        self.field = field
        self.queue = []
        super(GrabberSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in self.shortlist:
            obj = eval(self.model).get_object_by_pk(i)
            urls = getattr(obj, self.field)
            if not urls: continue

            self.queue.append((urls, obj.get_uk_code()))
            yield self.make_requests_from_url(self.fake_url)

    def parse(self, response):
        if not self.model or not self.field: return None

        urls, uk_code = self.queue.pop(0)
        item = ImageItem()
        item['slug'] = uk_code
        item['image_urls'] = urls.split('#')

        return item
