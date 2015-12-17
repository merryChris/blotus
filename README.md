Spiders With Scrapy For Specific Internet Finance Infomation
======

* This project offers raw data supports to [LAB Internet Finance Platform Demo](http://10.214.192.66:8080/businessfbi_id/index/home)
* It includes ['wangdaizhijia'](http://www.wdzj.com/) and ['p2peye'](http://www.p2peye.com/) namespaces now


## Description

  This whole project is used to crawl internet finance infomation related from web. It is called 'Blotus', which includes 'stalk' and 'bots' sub-projects supporting as db adapter and crawler entities.

  PS: Blotus can be explained as Blue Lotus. ;)

## Setup

  1. Install Python 2.7.

  2. Install python-django 1.7.6 OFFICIAL DOCS: https://docs.djangoproject.com/

  3. Install python-scrapy 1.0.3 OFFICIAL DOCS: http://doc.scrapy.org/en/0.24/intro/tutorial.html

  4. Install scrapyd 1.1.0 OFFICIAL DOCS: https://scrapyd.readthedocs.org

  5. Install git. Clone code from remote repository respectively('stalk' and 'tasks').

      For example: git clone git@10.214.192.55:/home/git/xxx.git  (PASSWORD: git)

  6. Set bash variables. Add 'export PYTHONPATH=path/to/blotus' to '~/.profile'.

  7. DB configuration and synchronization.

      (1) Modify related items in '/path/to/blotus/core/settings.py'.

      (2) Accessing into '/path/to/blotus/' dir and run 'python manage.py syncdb'. Double check after that.

## Directory

  </path/to/blotus/>
  |-manage.py                  # DJANGO MANAGEMENT SCRIPT
  |
  |-README.md                  # README
  |
  |-bots/
  | |
  | |-helpers/
  | | |
  | | |+helpers/exporterHelper/ # FOR GRABBING IMAGE FILES
  | | |
  | | |+helpers/imageHelper/    # FOR GRABBING SPECIFIC STATIC TEXT FILES
  | |
  | |+wangjia/                  # FOR 'WANGDAIZHIJIA' BOT
  | |
  | |+p2peye/                   # FOR 'P2PEYE' BOT
  |
  |+core/                       # DJANGO SETTINGS
  |
  |+server/                     # FOR RUNNING 'SCRAPYD' SERVER
  |
  |-stalk/
  | |
  | |+models/                   # DB MODELS ADAPTER SUPPORT
  |
  |+tools/                      # SCRIPTS TO DO SOME STATISTICS
  |
  |+utils/                      # FOR USAGES

## Directions

  1.  wangjia/wangjia/spiders/daohang.py

        Description: Get Navigation Info From Wangjia Navigation Page.

        URL Source:
          1. 'http://www.wdzj.com/wdzj/html/json/nav_search.json'
          2. 'http://www.wdzj.com/wdzj/html/json/dangan_search.json'
          3. 'http://www.wdzj.com/front_navigation-query'
          4. 'http://www.wdzj.com/daohang.html'

        Parameters: None


  2.  wangjia/wangjia/spiders/dangan.py

        Description: Get Plat Archive Info From Wangjia Archive Page According To IDs FROM 'wangjia_navigation' Table.

        URL Source: 'http://www.wdzj.com/dangan/xxxx'

        Parameters:
          from_id: Starting Plat ID
          to_id: Ending Plat ID


  3.  wangjia/wangjia/spiders/wenti.py

        Description: Get Problem Plat Info From Wangjia Data Page.

        URL Source: 'http://shuju.wdzj.com/problem-1.html'

        Parameters: None


  4.  wangjia/wangjia/spiders/wenti2.py

        Description: Get Problem Plat Info From Wangjia Navigation Page.

        URL Source: 'http://www.wdzj.com/daohang.html'

        Parameters: None


  5.  wangjia/wangjia/spiders/pingji.py

        Description: Get Rating Info From Wangjia Rating Page. (PS: INCLUDE [from_id, to_id]+[CURRENT_MONTH_BY_DEFAULT])

        URL Source: 'http://www.wdzj.com/pingji.html'

        Parameters:
          from_id: First ID In URL
          to_id: Last ID In URL
          end_time: Last Month Timestamp (FORMAT: yyyymm)


  6.  wangjia/wangjia/spiders/pingji2.py

        Description: Get Rating Info From Wangjia Archive Page According To URLs From Wangjia Rating Page.

        URL Source: 'http://www.wdzj.com/dangan/xxxx'

        Parameters:
          timestamp: Timestamp To Record


  7.  wangjia/wangjia/spiders/shuju.py

        Description: Get Data Info From Wangjia Data Page.

        URL Source: 'http://shuju.wdzj.com/platdata-1.html'

        Parameters:
          from_date: Starting Date (FORMAT: xxxxxxxx)
          to_date: Ending Date (FORMAT: xxxxxxxx)


  8.  wangjia/wangjia/spiders/xinwen.py

        Description: Get News Info From Wangjia News Page.

        URL Source: 'http://www.wdzj.com/news/xxxx/yyyy.html'

        Parameters:
          from_id: Starting Page ID
          to_id: Ending Page ID
          category: Category ID Of News


  9.  wangjia/wangjia/spiders/baoguang.py

        Description: Get Exposure Info From Wangjia Exposure Page.

        URL Source: 'http://bbs.wdzj.com/thread-xxxx-y-z.html'

        Parameters:
          from_id: Starting Page ID
          to_id: Ending Page ID


  10. p2peye/p2peye/spiders/daohang.py

        Description: Get Navigation Info From P2peye Navigation Page.

        URL Source: http://www.p2peye.com/dh.php'

        Parameters: None


  11. p2peye/p2peye/spiders/tedian.py

        Description: Get Plat Archive Feature Info From P2peye Archive Page.

        URL Source: 'http://xxxx.p2peye.com'

        Parameters:
          from_id: Starting Plat ID
          to_id: Ending Plat ID


  12. helpers/imageHelper/imageHelper/spiders/grabber.py

        Description: Get Images From Tables According To Specific Field & Save To Specific DIR.

        URL Source: None

        Parameters:
          from_id: Starting Record ID
          to_id: Ending Record ID
          category: DIR Name
          model: Model Name
          field: Field Name

## OPTIONS

  If you have questions about how to get cache files related, please have a glance at [Helper Spiders](/bots/helpers/exporterHelper/exporterHelper/spiders/*), which will help you a lot.
