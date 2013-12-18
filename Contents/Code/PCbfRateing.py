@route(PREFIX+'/setratingrt', videoID=int)
def SetRatingRT(query, videoID):
	try:
		page = HTTP.Request(RT_HTML_BASE+'/?page=1', cacheTime=3600, timeout=5, immediate=True).content
		ufAC = REGEXufAC.search(page)
		asdf = ufAC.group('ufAC')
		try:
#			setRateing = JSON.ObjectFromURL(RT_HTML_RATE % (str(videoID), str(query), str(asdf)), cacheTime=3600, timeout=5)
			setRateing = HTTP.Request(RT_HTML_RATE % (str(videoID), str(query), str(asdf)), cacheTime=3600, timeout=5).content.strip()
			Log(str(setRateing))
			setRateingJSON = JSON.ObjectFromString(str(setRateing))
			Log(str(setRateingJSON))
		except:
#			PCbfLogging('event',PCbfLoggingDH,'/'+str(videoID),TITLE+' - Video (API)','Error','Set Rateing','Is Active Fail!',videoID)
			setRateing = None
#		Log(str(setRateing['success']))
		if setRateing['success'] == 'true':
			return ObjectContainer(header='Thank You!', message='Thank you for rateing this video.', no_cache=True)
	except: pass


@route(PREFIX+'/setrating')
def SetRating(key,rating):
	Log(key+" - "+str(rating))