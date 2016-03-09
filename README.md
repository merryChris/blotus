Spiders Framework Focus on Internet Finance
=======


## Description

* Used to crawl specific internet finance infomation related from thrid-party platforms.
* Offer raw data supports to [LAB Internet Finance Platform Demo](http://10.214.192.66:8080/businessfbi_id/index/home).
* Cover ['wangdaizhijia'](http://www.wdzj.com/), ['p2peye'](http://www.p2peye.com/), and ['weidai'](https://www.weidai.com.cn/) data sources now.
* Mainly includes `stalk` and `bots` supporting as db adapter and spider entities.
* Called `blotus`, which can be explained as __Blue Lotus__. ;)

## Installation

1. Install python-django 1.9.0. [Here](https://docs.djangoproject.com) is official docs.
2. Install python-scrapy 1.0.3. [Here](http://doc.scrapy.org)  is official docs.
3. Install scrapyd 1.1.0. [Here](https://scrapyd.readthedocs.org) is official docs. 
4. Clone the code repository.
5. DB configuration and synchronization.
	* Modify DB related settings in `/path/to/blotus/core/settings.py`.
	* Accessing into `/path/to/blotus/` directory and run `python manage.py migrate`.
6. Set bash variables. Add `export PYTHONPATH=path/to/blotus` to `~/.profile` or else.
7. Set scrapyd configuration. Add following snippets to `~/.scrapyd.conf`.
```python
    [services]
    persistjobs.json     = utils.webservice.PersistJobs
    listdbjobs.json      = utils.webservice.ListDBJobs
```

## Directions

### About `'wangdaizhijia'` Bot

1.  Spider for navigation info

		Entry: wangjia/spiders/daohang.py

		Description: Get Navigation Info.

		URL Reference:
			1. http://www.wdzj.com/wdzj/html/json/nav_search.json
			2. http://www.wdzj.com/wdzj/html/json/dangan_search.json
			3. http://www.wdzj.com/front_navigation-query
			4. http://www.wdzj.com/daohang.html

		Parameters: None

2.  Spider for archive info

		Entry: wangjia/spiders/dangan.py

		Description: Get Plat Archive Info According To IDs FROM 'wangjia_navigation' Table.

		URL Reference: http://www.wdzj.com/dangan/{plat_pin}

		Parameters:
			from_id: Starting Plat ID
			to_id: Ending Plat ID

		Prerequisites:
			Completed job about navigation and make sure 'from_id' & 'to_id' in the range.

3.  Spider for problem plats info from data page

		Entry: wangjia/spiders/wenti.py

		Description: Get Problem Plat Info.

		URL Reference: http://shuju.wdzj.com/problem-1.html

		Parameters: None

4.  Spider for problem plats info from navigation page

		Entry: wangjia/wangjia/spiders/wenti2.py

		Description: Get Problem Plat Info.

		URL Reference: http://www.wdzj.com/daohang.html

		Parameters: None

5.  Spider for rating info from rating page

		Entry: wangjia/spiders/pingji.py

		Description: Get Rating Info. (INCLUDES [from_id, to_id]+[CURRENT_MONTH_BY_DEFAULT])

		URL Reference: http://www.wdzj.com/pingji.html

		Parameters:
			from_id: First ID In URL
			to_id: Last ID In URL
			end_time: Last Month Timestamp (FORMAT: yyyymm)

6.  Spider for rating info from archive page

		Entry: wangjia/spiders/pingji2.py

		Description: Get Rating Info According To URLs From Rating Page.

		URL Reference: http://www.wdzj.com/dangan/{plat_pin}

		Parameters:
			timestamp: Timestamp To Record
			cache: path to URL 'cache' file

		Prerequisites:
			Completed 'exporterHelper' job for getting cached rating urls. See more at entry 'exporterHelper/spiders/wangjia_rating_list.py'.

7.  Spider for data info

		Entry: wangjia/spiders/shuju.py

		Description: Get Data Info.

		URL Reference: http://shuju.wdzj.com/platdata-1.html

		Parameters:
			from_date: Starting Date (FORMAT: yyyymmdd)
			to_date: Ending Date (FORMAT: yyyymmdd)

8.  Spider for news info

		Entry: wangjia/spiders/xinwen.py

		Description: Get News Info.

		URL Reference: http://www.wdzj.com/news/{category}/yyyy.html

		Parameters:
			category: Category ID Of News
			cache: path to URL 'cache' file

		Prerequisites:
			Completed 'exporterHelper' job for getting cached news urls. See more at entry 'exporterHelper/spiders/wangjia_news_list.py'.

9.  Spider for exposure info

		Entry: wangjia/spiders/baoguang.py

		Description: Get Exposure Info.

		URL Reference: http://bbs.wdzj.com/thread-xxxx-y-z.html

		Parameters:
			cache: path to URL 'cache' file

		Prerequisites:
			Completed 'exporterHelper' job for getting cached exposure urls. See more at entry 'exporterHelper/spiders/wangjia_exposure_list.py'.

10.	Spider for feature info

		Entry: wangjia/spiders/tedian.py

		Description: Get Plat Feature Info According To IDs From 'wangjia_navigation' Table.

		URL Reference: http://www.wdzj.com/dangan/{plat_pin}

		Parameters:
			from_id: Starting Plat ID
			to_id: Ending Plat ID

		Prerequisites:
			Completed job about navigation and make sure 'from_id' & 'to_id' in the range.

### About `'p2peye'` Bot

1.  Spider for navigation info

		Entry: p2peye/spiders/daohang.py

		Description: Get Navigation Info.

		URL Reference: http://www.p2peye.com/dh.php

		Parameters: None

2.  Spider for plat archive feature info

		Entry: p2peye/spiders/tedian.py

		Description: Get Plat Archive Feature Info.

		URL Reference: http://{plat_pin}.p2peye.com

		Parameters:
			from_id: Starting Plat ID
			to_id: Ending Plat ID

### About `'weidai'` Bot

1.  Spider for tender info

		Entry: weidai/spiders/toubiao.py

		Description: Get Tender List Info.

		URL Reference: https://www.weidai.com.cn/bid/tenderList?searchFlag=search&typeCondition={bid_type}&page={page_id}&credit={credit}

		Parameters:
			bid_type: Bid Type
			credit: Credit Bid Or Not ('2' for yes)
			start_page_id: Starting Page ID
			end_page_id: Ending Page Id

2.  Spider for bid info

		Entry: weidai/spiders/biaodi.py

		Description: Get Bid Info According To IDs FROM 'weidai_tender' Table.

		URL Reference: https://www.weidai.com.cn/bid/showBorrowDetail?bid={bid}

		Parameters:
			from_id: Starting Bid ID
			to_id: Ending Bid ID

		Prerequisites:
			Completed job about tender list and make sure 'from_id' & 'to_id' in the range.

3.  Spider for bidder info from bid detail page

		Entry: weidai/spiders/biaoren.py

		Description: Get Bidder Info.

		URL Reference: https://www.weidai.com.cn/bid/tenderListPage?page=1&rows=100&bid={bid}

		Parameters:
			from_id: Starting Bid ID
			to_id: Ending Bid ID

		Prerequisites:
			Completed job about tender list and make sure 'from_id' & 'to_id' in the range.

### About `'yirendai'` Bot

1.  Spider for yirendai tender info

		Entry: yirendai/spiders/toubiao.py

		Description: Get Yirendai Tender List Info.

		URL Reference: http://www.yirendai.com/loan/list/{page_id}

		Parameters:
			from_page: Starting Page ID
			end_page: Ending Page ID

2.  Spider for yirendai bid info

		Entry: yirendai/spiders/biaodi.py

		Description: Get Yirendai Bid Info According To IDs From 'yirendai_tender' Table.

		URL Reference: https://www.yirendai.com/loan/view/{pin}?page=1&tabflag=0

		Parameters:
			from_id: Starting Bid ID
			to_id: Ending Bid ID

		Prerequisites:
			Completed job about yirendai tender list and make sure 'from_id' & 'to_list' in the range.

3.  Spider for yirendai bidder info

		Entry: yirendai/spiders/biaoren.py

		Description: Get Yirendai Bidder Info For Each Bid Detail.

		URL Reference: https://www.yirendai.com/loan/view/{pin}?page=1&tabflag=1

		Parameters:
			from_id: Starting Bid ID
			to_id: Ending Bid ID

		Prerequisites:
			Completed job about yirendai tender list and make sure 'from_id' & 'to_list' in the range.

### About `'renrendai'` Bot

1.  Spider for loan list info

			Entry: renrendai/spiders/loanid.py

			Description: Get Loan List Info

			URL Reference: http://www.we.com/lend/loanList!json.action?pageIndex={page_id}

			Parameters:
				start_page_id: Starting Page Index
				end_page_id: Ending Page Index

2.  Spider for invest record info

			Entry: renrendai/spiders/investrecord.py

			Description: Get Invest Record Info

			URL Reference: http://www.we.com/lend/getborrowerandlenderinfo.action?id=lenderRecords&loanId={loanId}

			Parameters:
				from_id: Starting Bid ID
				to_id: Ending Bid ID

			Prerequisites:
				Completed job about renrendai loan list and make sure 'from_id' & 'to_id' in the range.

3.  Spider for product and borrower info

			Entry: renrendai/spiders/product.py

			Description: Get Product and Borrower Info

			URL Reference: http://www.we.com/lend/detailPage.action?loanId={loanId}

			Parameters:
				from_id: Starting Bid ID
				to_id: Ending Bid ID
				jsessionid: Login in http://www.we.com and get JSESSIONID from Cookies, remember to remain logining status until finish crawling

			Prerequisites:
				Completed job about renrendai loan list and make sure 'from_id' & 'to_id' in the range.

			Cmdline Example:
				curl http://localhost:6800/schedule.json -d project=renrendai -d spider=product -d from_id=1 -d to_id=2 -d jsessionid='6C1C829649C22D8C48E5C86AF950E99AE7F30630E0CAEDD9D50A81CE35374ECD'

### About `'helpers'` Bot

#### About `'exporterHelper'` Bot

1.  Spider for 'wangdaizhijia' rating URLs.

		Entry: exporterHelper/spiders/wangjia_rating_list.py

		Description: Get 'wangdaizhjia' Rating URLs From Rating Page. (Just Current Month Only)

		URL Reference: http://www.wdzj.com/pingji.html

		Parameters: None

		Export File: 'cache'

2.  Spider for 'wangdaizhijia' specific category news URLs.

		Entry: exporterHelper/spiders/wangjia_news_list.py

		Description: Get 'wangdaizhjia' News URLs From News Overview Page.

		URL Reference: http://www.wdzj.com/news/{category}/

		Parameters:
			from_id: Starting News Anchor
			to_id: Ending News Anchor
			category: Category ID

		Export File: 'cache'

3.  Spider for 'wangdaizhijia' exposure URLs.

		Entry: exporterHelper/spiders/wangjia_exposure_list.py

		Description: Get 'wangdaizhjia' Exposure URLs From Exposure Overview Page.

		URL Reference: http://bbs.wdzj.com/comeing-guide-408.html

		Parameters:
			from_id: Starting News Anchor
			to_id: Ending News Anchor

		Export File: 'cache'

#### About `'imageHelper'` Bot

1.  Spider for images

		Entry: imageHelper/spiders/grabber.py

		Description: Get Images From Tables According To Specific Field & Save To Specific Directory.

		URL Reference: None

		Parameters:
			from_id: Starting Record ID
			to_id: Ending Record ID
			category: DIR Name
			model: Model Name
			field: Field Name

		Prerequisites:
			Make sure 'from_id' & 'to_id' in the range.
			Make sure 'category' & 'models' & 'field' exsits.
