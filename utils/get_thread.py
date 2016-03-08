from bots import setup_django_env
setup_django_env()

from stalk.models.wangjia import Exposure, News

def get_max_thread_from_exposure():
    max_thread_item = Exposure.objects.order_by('thread').last()
    return max_thread_item.thread if max_thread_item else -1

def get_max_thread_from_news(category):
    max_thread_item = News.objects.filter(category_id = category).order_by('thread').last()
    return max_thread_item.thread if max_thread_item else -1
