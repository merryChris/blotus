#!/usr/bin/env python

import sys, os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

db_table_mapper = {
    'wangjia': {
        'daohang':  'Navigation',
        'dangan':   'Archive',
        'baoguang': 'Exposure',
        'pingji':   'Rating',
        'pingji2':  'Rating',
        'shuju':    'Data',
        'wenti':    'Problem',
        'wenti2':   'Problem',
        'xinwen':   'News'
    }
}

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Arguments Error."
        sys.exit(1)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    from stalk.models.wangjia import *

    namespace, spider = sys.argv[1:]
    model = db_table_mapper[namespace][spider]
    print len(eval(model).objects.all())

    sys.exit(0)
