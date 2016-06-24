from bots.base.pipelines import BaseCacheExporterPersistencePipeline

class CacheFileExporterPersistencePipeline(BaseCacheExporterPersistencePipeline):

    def get_type(self):
        return 'cache'

    def get_filename(self, spider):
        filename = 'cache'

        import sys
        if len(sys.argv) > 3 and any(['_job' in arg for arg in sys.argv]):
            for arg in sys.argv:
                if '_job' not in arg: continue
                filename = arg.split('=')[-1]
                break

        return filename+'.ch'

class TokenFileExporterPersistencePipeline(BaseCacheExporterPersistencePipeline):

    def get_type(self):
        return 'tokens'

    def get_filename(self, spider):
        filename = 'token'

        if getattr(spider, 'token_field') and getattr(spider, spider.token_field):
            filename = getattr(spider, spider.token_field)

        return filename+'.tk'

    def log_successful_info(self, item, spider):
        spider.logger.info('Successfully Receive Token From No.%s Plat.' % (getattr(spider, spider.token_field) or 'test'))

    def log_failure_info(self, spider):
        spider.logger.info('Fail To Receive Token From No.%s Plat.' % (getattr(spider, spider.token_field) or 'test'))
