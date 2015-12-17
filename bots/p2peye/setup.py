# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name         = 'p2peye',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = p2peye.settings']},
)
