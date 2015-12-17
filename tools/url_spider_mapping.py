import sys

url_spider_mapper = {
	'wangjia':{
		'baoguang':'wangjia_exposure',
		'xinwen':'wangjia_news',
		'pingji2':'wangjia_rating'
	}
}

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print "Arguments Error."
		sys.exit(1)
	namespace, spider = sys.argv[1:]
	print url_spider_mapper[namespace][spider]
	sys.exit(0)