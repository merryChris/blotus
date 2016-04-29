import scrapy
from utils.webpage import get_content, get_thread_from_news_url
from utils.get_thread import get_max_thread_from_news
from exporterHelper.items import ExporterItem

################################################################################################################
#                                                                                                              #
# USAGE: nohup scrapy crawl wangjia_news -a from_id=1 -a to_id=1 -a category=1 --loglevel=INFO --logfile=log & #
#                                                                                                              #
################################################################################################################

class WangjiaNewsJsonSpider(scrapy.Spider):
    name = 'wangjia_news'
    allowed_domains = ['wdzj.com']
    start_formated_url = 'http://www.wdzj.com/news/{category}/p{page_id}.html'
    pipeline = ['CacheFileExporterPersistencePipeline']
    tab = ['', 'hangye', 'zhengce', 'pingtai', 'shuju', 'licai', 'guowai', 'guandian', 'yanjiu']

    def __init__(self, from_id=1, to_id=1, category=0, *args, **kwargs):
        to_id = max(int(from_id), int(to_id))
        self.shortlist = xrange(int(from_id), int(to_id)+1)
        self.max_thread = get_max_thread_from_news(category)
        self.category = self.tab[int(category)]
        super(WangjiaNewsJsonSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for i in self.shortlist:
            url = self.start_formated_url.format(category=self.category, page_id=i)
            yield self.make_requests_from_url(url)

    def parse(self, response):
        self.logger.info('Parsing Wangjia News %s URLs From <%s>.' % (self.category, response.url))

        item_list = []
        elements = response.xpath('//div[contains(@class, "specialBox")]//div[@class="news_title"]')
        for ele in elements:
            url = get_content(ele.xpath('a/@href').extract())
            if url.find(self.category) == -1: continue

            item = ExporterItem()
            item['record'] = url
            thread = get_thread_from_news_url(url)
            if int(self.max_thread) < int(thread):
                item_list.append(item)

        return item_list
