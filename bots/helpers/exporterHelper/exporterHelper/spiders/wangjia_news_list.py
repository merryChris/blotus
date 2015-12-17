import scrapy
from scrapy import log
from utils.webpage import get_content
from utils.get_thread import get_max_thread,get_thread_from_news
from exporterHelper.items import URLItem

################################################################################################################
#                                                                                                              #
# USAGE: nohup scrapy crawl wangjia_news -a from_id=1 -a to_id=2 -a category=1 --loglevel=INFO --logfile=log & #
#                                                                                                              #
################################################################################################################

class WangjiaNewsJsonSpider(scrapy.Spider):
    name = 'wangjia_news'
    allowed_domains = ['wdzj.com']
    start_url_prefix = 'http://www.wdzj.com/news/'
    tab = ['', 'hangye', 'zhengce', 'pingtai', 'shuju', 'licai', 'guowai', 'guandian', 'yanjiu']
    max_thread = get_max_thread(name)

    def __init__(self, from_id=2, to_id=1, category=0, *args, **kwargs):
        self.from_id = int(from_id)
        self.to_id= int(to_id)
        self.category = self.tab[int(category)]
        super(WangjiaNewsJsonSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in ['']+['p'+str(x)+'.html' for x in xrange(self.from_id, self.to_id+1)]:
            url = self.start_url_prefix + self.category + '/' + i
            yield self.make_requests_from_url(url)

    def parse(self, response):
        #NOTE: (zacky, APR.27th) PIPELINE FUNCTIONS RELATED WILL BE PROCESSED IN THE FOLLOWING STEP, SO WE KEEP THE OBJECT STATE HERE.
        self.log('Parsing Wangjia News %s URLs From <%s>.' % (self.category, response.url), level=log.INFO)

        item_list = []
        elements = response.xpath('//div[contains(@class, "specialBox")]//div[@class="news_title"]')
        for ele in elements:
            url = get_content(ele.xpath('a/@href').extract())
            if url.find(self.category) == -1: continue

            item = URLItem()
            item['url'] = url
            thread = get_thread_from_news(url)
            if int(self.max_thread) < int(thread):
                item_list.append(item)

        return item_list
