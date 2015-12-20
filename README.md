Spiders Framework Focus on Internet Finance
=======


## Description

* Used to crawl specific internet finance infomation related from thrid-party platforms.
* Offer raw data supports to [LAB Internet Finance Platform Demo](http://10.214.192.66:8080/businessfbi_id/index/home).
* Cover ['wangdaizhijia'](http://www.wdzj.com/) and ['p2peye'](http://www.p2peye.com/) data sources now.
* Mainly includes `stalk` and `bots` supporting as db adapter and spider entities.
* Called `blotus`, which can be explained as __Blue Lotus__. ;)

## Installation

1. Install python-django 1.7.6. [Here](https://docs.djangoproject.com) is official docs.
2. Install python-scrapy 1.0.3. [Here](http://doc.scrapy.org)  is official docs.
3. Install scrapyd 1.1.0. [Here](https://scrapyd.readthedocs.org) is official docs. 
4. Clone the code repository.
5. Set bash variables. Add `export PYTHONPATH=path/to/blotus` to `~/.profile` or else.
6. DB configuration and synchronization.
  * Modify DB related settings in `/path/to/blotus/core/settings.py`.
  * Accessing into `/path/to/blotus/` directory and run `python manage.py syncdb`.

## Directions

  1.  wangjia/spiders/daohang.py

        Description: Get Navigation Info From Wangjia Navigation Page.

        URL Source:
          1. 'http://www.wdzj.com/wdzj/html/json/nav_search.json'
          2. 'http://www.wdzj.com/wdzj/html/json/dangan_search.json'
          3. 'http://www.wdzj.com/front_navigation-query'
          4. 'http://www.wdzj.com/daohang.html'

        Parameters: None


  2.  wangjia/spiders/dangan.py

        Description: Get Plat Archive Info From Wangjia Archive Page According To IDs FROM 'wangjia_navigation' Table.

        URL Source: 'http://www.wdzj.com/dangan/xxxx'

        Parameters:
          from_id: Starting Plat ID
          to_id: Ending Plat ID


  3.  wangjia/spiders/wenti.py

        Description: Get Problem Plat Info From Wangjia Data Page.

        URL Source: 'http://shuju.wdzj.com/problem-1.html'

        Parameters: None


  4.  wangjia/wangjia/spiders/wenti2.py

        Description: Get Problem Plat Info From Wangjia Navigation Page.

        URL Source: 'http://www.wdzj.com/daohang.html'

        Parameters: None


  5.  wangjia/spiders/pingji.py

        Description: Get Rating Info From Wangjia Rating Page. (PS: INCLUDE [from_id, to_id]+[CURRENT_MONTH_BY_DEFAULT])

        URL Source: 'http://www.wdzj.com/pingji.html'

        Parameters:
          from_id: First ID In URL
          to_id: Last ID In URL
          end_time: Last Month Timestamp (FORMAT: yyyymm)


  6.  wangjia/spiders/pingji2.py

        Description: Get Rating Info From Wangjia Archive Page According To URLs From Wangjia Rating Page.

        URL Source: 'http://www.wdzj.com/dangan/xxxx'

        Parameters:
          timestamp: Timestamp To Record


  7.  wangjia/spiders/shuju.py

        Description: Get Data Info From Wangjia Data Page.

        URL Source: 'http://shuju.wdzj.com/platdata-1.html'

        Parameters:
          from_date: Starting Date (FORMAT: xxxxxxxx)
          to_date: Ending Date (FORMAT: xxxxxxxx)


  8.  wangjia/spiders/xinwen.py

        Description: Get News Info From Wangjia News Page.

        URL Source: 'http://www.wdzj.com/news/xxxx/yyyy.html'

        Parameters:
          from_id: Starting Page ID
          to_id: Ending Page ID
          category: Category ID Of News


  9.  wangjia/spiders/baoguang.py

        Description: Get Exposure Info From Wangjia Exposure Page.

        URL Source: 'http://bbs.wdzj.com/thread-xxxx-y-z.html'

        Parameters:
          from_id: Starting Page ID
          to_id: Ending Page ID


  10. p2peye/spiders/daohang.py

        Description: Get Navigation Info From P2peye Navigation Page.

        URL Source: http://www.p2peye.com/dh.php'

        Parameters: None


  11. p2peye/spiders/tedian.py

        Description: Get Plat Archive Feature Info From P2peye Archive Page.

        URL Source: 'http://xxxx.p2peye.com'

        Parameters:
          from_id: Starting Plat ID
          to_id: Ending Plat ID


  12. imageHelper/spiders/grabber.py

        Description: Get Images From Tables According To Specific Field & Save To Specific DIR.

        URL Source: None

        Parameters:
          from_id: Starting Record ID
          to_id: Ending Record ID
          category: DIR Name
          model: Model Name
          field: Field Name
