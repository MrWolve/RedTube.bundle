@route(PREFIX+'/doprecache')
def doPreCache():
	doPreCacheV = 1
	HTTP.PreCache(RT_HTML_BASE+'/?page=1', cacheTime=3600)
	HTTP.PreCache(RT_HTML_CHANNELS, cacheTime=CACHE_1WEEK)
	HTTP.PreCache(RT_HTML_TAGS, cacheTime=CACHE_1WEEK)
	HTTP.PreCache(RT_API_TAGS, cacheTime=CACHE_1WEEK)
	HTTP.PreCache(RT_API_PORNSTARS, cacheTime=CACHE_1WEEK)
	return doPreCacheV