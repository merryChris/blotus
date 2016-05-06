# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class ExporterItem(scrapy.Item):

    count = scrapy.Field()

    def __init__(self):
        #NOTE: (zacky, 2016.MAY.5th) DEFINED AS LIST HERE FOR EXPORTER PIPELINE.
        self._record = []
        super(ExporterItem, self).__init__()

    def set_record(self, rc):
        self._record.append(rc)
        self['count'] = len(self._record)

    def get_record(self):
        for rc in self._record:
            yield str(rc)
