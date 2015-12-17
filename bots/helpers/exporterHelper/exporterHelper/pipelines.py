from scrapy.contrib.exporter import JsonItemExporter
import json

class JsonExporterPersistencePipeline(JsonItemExporter):

    filename = 'cache'

    def __init__(self, **kwargs):
        file = open(self.filename, 'ab')
        super(JsonExporterPersistencePipeline, self).__init__(file, **kwargs)

    def process_item(self, item, spider):
        #self.export_item(item)
        product = self._get_serialized_fields(item).next()[1]
        self.file.write(product+'\n')

        return item
