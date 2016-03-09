import scrapy, json
from utils.webpage import get_content
from wangjia.items import ProvinceItem, DaohangItem

#####################################################################
#                                                                   #
# USAGE: nohup scrapy crawl daohang --loglevel=INFO --logfile=log & #
#                                                                   #
#####################################################################

class DaohangSpider(scrapy.Spider):
    name = 'daohang'
    allowed_domains = ['wdzj.com']
    start_urls = ['http://www.wdzj.com/wdzj/html/json/nav_search.json',    \
                  'http://www.wdzj.com/wdzj/html/json/dangan_search.json', \
                  #NOTE: (zacky, 2015.APR.21st) NEED TO ADD FORM DATA. SEE MORE AT http://ju.outofmemory.cn/entry/105646.
                  #'http://www.wdzj.com/front_select-plat'
                  'http://www.wdzj.com/front_navigation-query',            \
                  'http://www.wdzj.com/daohang.html']
    pipeline = ['UniqueItemPersistencePipeline']

    def parse(self, response):
        item_list = []
        if response.url.endswith('html'):
            # For Regular Platform.
            content = response.xpath('//div[@id="platList"]/div[starts-with(@class, "rnav")]')
            for sel_ct in content:
                province_name = get_content(sel_ct.xpath('div[@class="til"]/div/p[not(@class="til_num")]/text()').extract())
                province_id = ProvinceItem.get_id_by_name(province_name)

                plat_list = sel_ct.xpath('ul[@class="til_cn"]/li')
                for sel_pt in plat_list:
                    daohang = DaohangItem()
                    purl = get_content(sel_pt.xpath('a/@purl').extract()).split('/')
                    while not purl[-1]: purl.pop()
                    daohang['pin'] = purl.pop()
                    daohang['name'] = get_content(sel_pt.xpath('a/text()').extract())
                    daohang['link'] = get_content(sel_pt.xpath('a/@href').extract())
                    daohang['province_id'] = province_id

                    item_list.append(daohang)

            # For Problematic Platform.
            # Disabled Here Temporarily.
            #content = response.xpath('//div[@id="issuePlatList"]/div[starts-with(@class, "rnav")]')
            #for sel_ct in content:
            #    province_name = get_content(sel_ct.xpath('div[@class="til"]/div/p[not(@class="til_num")]/text()').extract())
            #    province_id = ProvinceItem.get_id_by_name(province_name)

            #    plat_list = sel_ct.xpath('ul[@class="til_cn"]/li')
            #    for sel_pt in plat_list:
            #        daohang = DaohangItem()
            #        purl = get_content(sel_pt.xpath('a/@purl').extract()).split('/')
            #        while not purl[-1]: purl.pop()
            #        daohang['pin'] = purl.pop()
            #        daohang['name'] = get_content(sel_pt.xpath('a/text()').extract())
            #        # Invalid Link For Problematic Platform.
            #        #daohang['link'] = get_content(sel_pt.xpath('a/@href').extract())
            #        daohang['province_id'] = province_id

            #        item_list.append(daohang)
        else:
            content = json.loads(response.body_as_unicode())
            if response.url.endswith('json'):
                for ct in content:
                    daohang = DaohangItem()
                    daohang['pin']    = ct.get('platPin', None)
                    daohang['allPin'] = ct.get('allPlatPin', None)
                    daohang['name']   = ct.get('platName', None)
                    daohang['link']   = ct.get('platUrl', None)

                    item_list.append(daohang)
            else:
                for ct in content:
                    if not ct.get('city'): continue

                    province_id = ProvinceItem.get_id_by_name(ct.get('city'))
                    plat_list = ct.get('platList')
                    for pt in plat_list:
                        daohang = DaohangItem()
                        daohang['pin']         = pt.get('platLetter', None)
                        daohang['name']        = pt.get('platName', None)
                        daohang['link']        = pt.get('platUrl', None)
                        daohang['province_id'] = province_id
                        daohang['launch_time'] = pt.get('onlineDateStr', None)
                        daohang['icon_url']    = pt.get('platIconUrl', None)

                        item_list.append(daohang)

        return item_list
