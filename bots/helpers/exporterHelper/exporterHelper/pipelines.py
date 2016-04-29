from bots.base.pipelines import BaseCacheExporterPersistencePipeline

class CacheFileExporterPersistencePipeline(BaseCacheExporterPersistencePipeline):

    def get_type(self):
        return 'cache'

    def get_filesuffix(self):
        return 'ch'

    def get_filename(self, spider):
        filename = 'cache'

        import os, sys
        if len(sys.argv) > 3 and '_job' in sys.argv[3]:
            filename = os.path.join('items', 'cache', sys.argv[3].split('=')[-1]+'.ch')

        return filename+'.'+self.get_filesuffix()
