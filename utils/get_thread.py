#!/usr/bin/env python

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','core.settings')

from django.db import connection

def get_max_thread(dbname):
	cursor = connection.cursor()
	sql = 'select max(thread) from '+dbname
	cursor.execute(sql)
	max_thread = cursor.fetchone()
	if max_thread[0]:
		return max_thread[0]
	else:
		return -1

def get_thread_from_exposure(url):
    if url.find('-') != -1:
        return url.split('-')[1]
    if url.find('=') != -1:
        return url.split('=')[-1]
    return None

def get_thread_from_news(url):
    pos = url.find('.html')
    if pos != -1: return url[:pos].split('/')[-1]
    return None

if __name__ == '__main__':
	print get_max_thread('wangjia_news')
	print get_max_thread('wangjia_exposure')
