from bots import setup_django_env, check_db_connection
setup_django_env()

from scrapyd.utils import get_spider_list, JsonResource, UtilsCache
from scrapyd.webservice import WsResource

from bots.base.items import JobItem

class PersistJobs(WsResource):

    def render_POST(self, txrequest):
        project = txrequest.args['project'][0]

        check_db_connection()
        finished = [{'job_id': s.job, 'project': s.project, 'spider': s.spider,
                     'start_time': s.start_time, 'end_time': s.end_time}
                     for s in self.root.launcher.finished if s.project == project or project == 'all']

        failed_items = []
        for fj in finished:
            item = JobItem()
            for key in fj.keys():
                item[key] = fj.get(key)
            if not item.save_only():
                failed_items.append(item['job_id'])

        if failed_items:
            return {"node_name": self.root.nodename, "status":"error", \
                    "message": "%d items failed" % len(failed_items)}

        backup = []
        for s in self.root.launcher.finished:
            if project != 'all' and s.project != project:
                backup.append(s)
        del self.root.launcher.finished
        self.root.launcher.finished = backup
        return {"node_name": self.root.nodename, "status":"ok"}

class ListDBJobs(WsResource):

    def render_GET(self, txrequest):
        project = txrequest.args['project'][0]
        page_id = int(txrequest.args['page_id'][0])
        page_count = int(txrequest.args['page_count'][0])

        check_db_connection()
        cnt, qs = JobItem.get_jobs_by_project(project, page_id, page_count)
        finished = [{'id': j.job_id, 'spider': j.spider, 'start_time': j.start_time.isoformat(' '),
                     'end_time': j.end_time.isoformat(' ')} for j in qs]
        return {"node_name": self.root.nodename, "status":"ok", "count": cnt, "finished": finished}
