from scrapy.exporters import JsonItemExporter
import os, sys, json

class JsonExporterPersistencePipeline(JsonItemExporter):

    def __init__(self, **kwargs):
        filename = 'cache'
        print len(sys.argv), sys.argv
        if len(sys.argv) > 3 and '_job' in sys.argv[3]:
            filename = os.path.join('items', 'cache', sys.argv[3].split('=')[-1]+'.ch')

        file = open(filename, 'ab')
        super(JsonExporterPersistencePipeline, self).__init__(file, **kwargs)

    def process_item(self, item, spider):
        #self.export_item(item)
        product = self._get_serialized_fields(item).next()[1]
        self.file.write(product+'\n')

        return item
