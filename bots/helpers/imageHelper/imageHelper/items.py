import scrapy

class ImageItem(scrapy.Item):
    slug = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
