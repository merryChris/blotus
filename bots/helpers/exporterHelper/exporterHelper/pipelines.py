from bots.base.pipelines import BaseCacheExporterPersistencePipeline

class CacheFileExporterPersistencePipeline(BaseCacheExporterPersistencePipeline):

    def get_type(self):
        return 'cache'

    def get_filename(self, spider):
        filename = 'cache'

        import os, sys
        if len(sys.argv) > 3 and '_job' in sys.argv[3]:
            filename = os.path.join('items', 'cache', sys.argv[3].split('=')[-1])

        return filename+'.ch'

class TokenFileExporterPersistencePipeline(BaseCacheExporterPersistencePipeline):

    def get_type(self):
        return 'tokens'

    def get_filename(self, spider):
        return (getattr(spider, spider.token_field) or 'test')+'.tk'

    def log_successful_info(self, item, spider):
        symbol = (item['record'], getattr(spider, spider.token_field) or 'test')
        spider.logger.info('Successfully Receive Token <%s> From No.%s Plat.' % symbol)

    def log_failure_info(self, spider):
        spider.logger.info('Fail To Receive Token From No.%s Plat.' % (getattr(spider, spider.token_field) or 'test'))
