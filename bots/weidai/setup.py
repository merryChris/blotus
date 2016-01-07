# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name         = 'weidai',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = weidai.settings']},
)
