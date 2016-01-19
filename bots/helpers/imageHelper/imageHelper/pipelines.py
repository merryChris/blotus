from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class ImagePersistencePipeline(ImagesPipeline):

    def alter_image_key(self, spider, meta, url):
        category = getattr(spider, 'category') or 'tmp'
        slug = meta.get('slug')
        anchor = meta.get('anchor') or url.split('/')[-1]
        #NOTE: (zacky, 2015.JUN.11th) THE FORMAT CONVERTED BY SCRAPY IS 'JPEG', SO WE NEED TO KEEP CONSISTENT HERE.
        extension = '.jpg'
        return '/'.join((category, slug, anchor)) + extension

    def get_media_requests(self, item, info):
        for idx in xrange(len(item['image_urls'])):
            image_url = item['image_urls'][idx]
            slug = item['slug']
            info.spider.logger.info('Downloading No.%(anchor)d image of %(category)s_%(slug)s from %(url)s.', \
                    {'anchor': idx+1, 'category': info.spider.category.upper(), 'slug': slug.upper(), 'url': image_url})
            yield Request(image_url, meta={'slug': slug, 'anchor': str(idx+1)})

    def get_images(self, response, request, info):
        for key, image, buf in super(ImagePersistencePipeline, self).get_images(response, request, info):
            key = self.alter_image_key(info.spider, response.meta, response.url)
            yield key, image, buf

    #NOTE: (zacky, 2015.JUN.11th) IF WE WANT TO SAVE THE IMAGE FORMAT AS IT IS, WE MAY OVERRIDE 'convert_image' METHOD.
    #from cStringIO import StringIO
    #from PIL import Image
    #def convert_image(self, image, size=None):
    #    buf = StringIO()
    #    image.save(buf, image.format)
    #    return image, buf

    def item_completed(self, results, item, info):
        info.spider.logger.info('Downloaded all image(s) of %(category)s_%(slug)s.', \
                {'category': info.spider.category.upper(), 'slug': item['slug'].upper()})
        return super(ImagePersistencePipeline, self).item_completed(results, item, info)
