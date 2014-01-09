@route(PREFIX+'/doprecache')
def doPreCache():
	doPreCacheV = 2
	HTTP.PreCache(RT_HTML_BASE+'/?page=1', cacheTime=3600)
	HTTP.PreCache(RT_HTML_CHANNELS, cacheTime=CACHE_1WEEK)
	HTTP.PreCache(RT_HTML_TAGS, cacheTime=CACHE_1WEEK)
	HTTP.PreCache(RT_API_TAGS, cacheTime=CACHE_1WEEK)
	HTTP.PreCache(RT_API_PORNSTARS, cacheTime=CACHE_1WEEK)
	HTTP.PreCache(RT_HTML_BASE+'/top?period=weekly&page=1', cacheTime=3600)
	HTTP.PreCache(RT_HTML_BASE+'/top?period=alltime&page=1', cacheTime=CACHE_1WEEK)
	HTTP.PreCache(RT_HTML_BASE+'/top?period=monthly&page=1', cacheTime=CACHE_1WEEK)
	HTTP.PreCache(RT_HTML_BASE+'/mostviewed?period=alltime&page=1', cacheTime=CACHE_1WEEK)
	HTTP.PreCache(RT_HTML_BASE+'/mostfavored?period=alltime&page=1', cacheTime=CACHE_1WEEK)
	return doPreCacheV
