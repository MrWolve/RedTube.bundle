@route(PREFIX+'/addvideotofavorites', id=int)
def AddVideoToFavorites(id, name=''):
	try:
		favs = {}
		if Data.Exists('PCbfFavorites'):
			favs = Data.LoadObject('PCbfFavorites')
		if str(id) not in favs:
			favs[id] = [id]
			Data.SaveObject('PCbfFavorites', favs)
		PCbfLogging('event',PCbfLoggingDH,'/'+str(id),TITLE+' - '+str(name),'Favorites','Add Favorite','Video added to Favorites.',id)
		return ObjectContainer(header='Added to Favorites', message='This Video has been added to your Favorites.', no_cache=True)
	except: PCbfLogging('event',PCbfLoggingDH,'/'+str(id),TITLE+' - '+str(name),'Error','Add Favorite','Unable to add video to Favorites.',id)

@route(PREFIX+'/removevideofromfavorites', id=int)
def RemoveVideoFromFavorites(id, name=''):
	try:
		favs = Data.LoadObject('PCbfFavorites')
		if id in favs:
			del favs[id]
			Data.SaveObject('PCbfFavorites', favs)
			PCbfLogging('event',PCbfLoggingDH,'/'+str(id),TITLE+' - '+str(name),'Favorites','Remove Favorite','Video removed from Favorites.',id)
			return ObjectContainer(header='Removed from Favorites', message='This Video has been removed from your Favorites.', no_cache=True)
	except: PCbfLogging('event',PCbfLoggingDH,'/'+str(id),TITLE+' - '+str(name),'Error','Remove Favorite','Unable to remove video from Favorites.',id)

@route(PREFIX+'/listfavorites')
def ListFavorites():
	if Data.Exists('PCbfFavorites'):
		try:
			favs = Data.LoadObject('PCbfFavorites')
			values = favs.values()
			output = [(f[0]) for f in values]
			output.sort()
			pageContent = ''
			for id in output:
				#pageContent needs to have the same format as defined in RT_HTML_VIDEO_xpath!!!
				pageContent += '<a href="/'+str(id)+'" class="video">'
			if pageContent == '':
				PCbfLogging('event',PCbfLoggingDH,'/',TITLE+' - Favorites','Error','List Favorites','PCbfFavorites is empty!')
				return None
			else:
				PCbfLogging('event',PCbfLoggingDH,'/',TITLE+' - Favorites','Favorites','List Favorites','Reading Data from PCbfFavorites successful!')
				pageContent = HTML.ElementFromString(pageContent)
				return pageContent
		except:
			PCbfLogging('event',PCbfLoggingDH,'/',TITLE+' - Favorites','Error','List Favorites','Reading Data from PCbfFavorites failed!')
			return None
	else:
		PCbfLogging('event',PCbfLoggingDH,'/',TITLE+' - Favorites','Error','List Favorites','Data.Exists.PCbfFavorites failed!!')
		return None
