Spiders Framework Focus on Internet Finance
=======


## Description

* Used to crawl specific internet finance infomation related from thrid-party platforms.
* Offer raw data supports to [LAB Internet Finance Platform Demo](http://10.214.192.66:8080/businessfbi_id/index/home).
* Cover ['wangdaizhijia'](http://www.wdzj.com/) and ['p2peye'](http://www.p2peye.com/) data sources now.
* Mainly includes `stalk` and `bots` supporting as db adapter and spider entities.
* Called `blotus`, which can be explained as __Blue Lotus__. ;)

## Installation

1. Install python-django 1.9.0. [Here](https://docs.djangoproject.com) is official docs.
2. Install python-scrapy 1.0.3. [Here](http://doc.scrapy.org)  is official docs.
3. Install scrapyd 1.1.0. [Here](https://scrapyd.readthedocs.org) is official docs. 
4. Clone the code repository.
5. Set bash variables. Add `export PYTHONPATH=path/to/blotus` to `~/.profile` or else.
6. DB configuration and synchronization.
	* Modify DB related settings in `/path/to/blotus/core/settings.py`.
	* Accessing into `/path/to/blotus/` directory and run `python manage.py syncdb`.

## Directions

### About `'wangdaizhijia'` Bot

1.  Spider for navigation info

		Entry: `wangjia/spiders/daohang.py`

		Description: Get Navigation Info.

		URL Reference:
			1. `http://www.wdzj.com/wdzj/html/json/nav_search.json`
			2. `http://www.wdzj.com/wdzj/html/json/dangan_search.json`
			3. `http://www.wdzj.com/front_navigation-query`
			4. `http://www.wdzj.com/daohang.html`

		Parameters: None

2.  Spider for archive info

		Entry: `wangjia/spiders/dangan.py`

		Description: Get Plat Archive Info According To IDs FROM `wangjia_navigation` Table.

		URL Reference: `http://www.wdzj.com/dangan/(plat_pin)`

		Parameters:
			from_id: Starting Plat ID
			to_id: Ending Plat ID

		Prerequisites:
			Completed job about navigation and make sure `from_id` & `to_id` in the range.

3.  Spider for problem plats info from data page

		Entry: `wangjia/spiders/wenti.py`

		Description: Get Problem Plat Info.

		URL Reference: `http://shuju.wdzj.com/problem-1.html`

		Parameters: None

4.  Spider for problem plats info from navigation page

		Entry: `wangjia/wangjia/spiders/wenti2.py`

		Description: Get Problem Plat Info.

		URL Reference: `http://www.wdzj.com/daohang.html`

		Parameters: None

5.  Spider for rating info from rating page

		Entry: `wangjia/spiders/pingji.py`

		Description: Get Rating Info. (INCLUDES [from_id, to_id]+[CURRENT_MONTH_BY_DEFAULT])

		URL Reference: `http://www.wdzj.com/pingji.html`

		Parameters:
			from_id: First ID In URL
			to_id: Last ID In URL
			end_time: Last Month Timestamp (FORMAT: yyyymm)

6.  Spider for rating info from archive page

		Entry: `wangjia/spiders/pingji2.py`

		Description: Get Rating Info According To URLs From Rating Page.

		URL Reference: `http://www.wdzj.com/dangan/(plat_pin)`

		Parameters:
			timestamp: Timestamp To Record
			cache: path to URL `cache` file

		Prerequisites:
			Completed `exporterHelper` job for getting cached rating urls. See more at entry `exporterHelper/spiders/wangjia_rating_list.py`.

7.  Spider for data info

		Entry: `wangjia/spiders/shuju.py`

		Description: Get Data Info.

		URL Reference: `http://shuju.wdzj.com/platdata-1.html`

		Parameters:
			from_date: Starting Date (FORMAT: yyyymmdd)
			to_date: Ending Date (FORMAT: yyyymmdd)

8.  Spider for news info

		Entry: `wangjia/spiders/xinwen.py`

		Description: Get News Info.

		URL Reference: `http://www.wdzj.com/news/(category)/yyyy.html`

		Parameters:
			category: Category ID Of News
			cache: path to URL `cache` file

		Prerequisites:
			Completed `exporterHelper` job for getting cached news urls. See more at entry `exporterHelper/spiders/wangjia_news_list.py`.

9.  Spider for exposure info

		Entry: `wangjia/spiders/baoguang.py`

		Description: Get Exposure Info.

		URL Reference: `http://bbs.wdzj.com/thread-xxxx-y-z.html`

		Parameters:
			cache: path to URL `cache` file

		Prerequisites:
			Completed `exporterHelper` job for getting cached exposure urls. See more at entry `exporterHelper/spiders/wangjia_exposure_list.py`.


### About `'p2peye'` Bot

1.  Spider for navigation info

		Entry: `p2peye/spiders/daohang.py`

		Description: Get Navigation Info.

		URL Reference: `http://www.p2peye.com/dh.php`

		Parameters: None

2.  Spider for plat archive feature info

		Entry: `p2peye/spiders/tedian.py`

		Description: Get Plat Archive Feature Info.

		URL Reference: 'http://(plat_pin).p2peye.com'

		Parameters:
			from_id: Starting Plat ID
			to_id: Ending Plat ID


### About `'helpers'` Bot

#### About `'exporterHelper'` Bot

1.  Spider for `'wangdaizhijia'` rating URLs.

		Entry: `exporterHelper/spiders/wangjia_rating_list.py`

		Description: Get `'wangdaizhjia'` Rating URLs From Rating Page. (Just Current Month Only)

		URL Reference: `http://www.wdzj.com/pingji.html`

		Parameters: None

		Export File: `cache`

2.  Spider for `'wangdaizhijia'` specific category news URLs.

		Entry: `exporterHelper/spiders/wangjia_news_list.py`

		Description: Get `'wangdaizhjia'` News URLs From News Overview Page.

		URL Reference: `http://www.wdzj.com/news/(category)/`

		Parameters:
			from_id: Starting News Anchor
			to_id: Ending News Anchor
			category: Category ID

		Export File: `cache`

3.  Spider for `'wangdaizhijia'` exposure URLs.

		Entry: `exporterHelper/spiders/wangjia_exposure_list.py`

		Description: Get `'wangdaizhjia'` Exposure URLs From Exposure Overview Page.

		URL Reference: `http://bbs.wdzj.com/comeing-guide-408.html`

		Parameters:
			from_id: Starting News Anchor
			to_id: Ending News Anchor

		Export File: `cache`

#### About `'imageHelper'` Bot

1.  Spider for images

		Entry: `imageHelper/spiders/grabber.py`

		Description: Get Images From Tables According To Specific Field & Save To Specific Directory.

		URL Reference: None

		Parameters:
			from_id: Starting Record ID
			to_id: Ending Record ID
			category: DIR Name
			model: Model Name
			field: Field Name

		Prerequisites:
			Make sure `from_id` & `to_id` in the range.
			Make sure `category` & `models` & `field` exsits.
