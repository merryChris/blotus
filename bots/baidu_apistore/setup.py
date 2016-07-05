# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name         = 'baidu_apistore',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = baidu_apistore.settings']},
)
