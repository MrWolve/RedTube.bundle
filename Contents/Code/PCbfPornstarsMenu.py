@route(PREFIX+'/pornstarsmenu')
def PornstarsMenu():
	oc = ObjectContainer(title2='Porn Stars')
	availAlphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	oc.add(DirectoryObject(key=Callback(PornstarsList, mainTitle='All', searchQuery='all'), title='All'))
	for alphabetItem in availAlphabet:
		oc.add(DirectoryObject(key=Callback(PornstarsList, mainTitle=alphabetItem.capitalize(), searchQuery=alphabetItem), title=alphabetItem.capitalize()))
	return oc

@route(PREFIX+'/pornstarsfilter')
def PornstarsListFilter(stars, searchQuery='a'):
	stars['stars'] = [value for value in stars['stars'] if value['star']['star_name'].lower().startswith(str(searchQuery))]
	return stars

@route(PREFIX+'/pornstarslist', page=int)
def PornstarsList(mainTitle, searchQuery='all', page=1):
	oc = ObjectContainer(title2='Porn Stars: '+mainTitle)
	pageFormat = 'PornStar'
	start = (int(page)-1) * RT_API_LIMIT
	try: stars = JSON.ObjectFromURL(RT_API_PORNSTARS)
	except: PCbfLogging('event',PCbfLoggingDH,'/pornstar',TITLE+' - Porn Stars: '+mainTitle+' (API)','Error','Loading Porn Stars','API Not Found!',page)
	if searchQuery != 'all':
		stars = PornstarsListFilter(stars, searchQuery)
	for x in range (start, start + RT_API_LIMIT):
		if x >= len(stars['stars']):
			break
		star = stars['stars'][int(x)]
		if not 'star' in star:
			break
		else:
			star = star['star']
		try: pornstarItemTitle = star['star_name']
		except: pornstarItemTitle = None
		try: pornstarItemQuery = star['star_url'].rsplit('/',1)[1].strip()
		except: pornstarItemQuery = None
		try:
			pornstarItemThumb = star['star_thumb']
			HTTP.PreCache(pornstarItemThumb, cacheTime=CACHE_1WEEK)
		except: pornstarItemThumb = None
		if ((pornstarItemTitle == None) or (pornstarItemQuery == None) or (pornstarItemThumb == None)):
			PCbfLogging('event',PCbfLoggingDH,'/pornstar',TITLE+' - Porn Stars: '+mainTitle+' (API)','Error','Loading Porn Stars','Problem with Content! API changed?',page)
			Log(str(pornstarItemTitle)+'_'+str(pornstarItemQuery)+'_'+str(pornstarItemThumb))
		oc.add(DirectoryObject(key=Callback(SortOrderSubMenu, url=RT_HTML_PORNSTAR, mainTitle=pornstarItemTitle, searchQuery=pornstarItemQuery, pageFormat=pageFormat), title=pornstarItemTitle, thumb=pornstarItemThumb))
	if len(oc) > 0:
		PCbfLogging('pageview',PCbfLoggingDH,'/pornstar',TITLE+' - Porn Stars: '+mainTitle+' .'+str(page)+' (API)')
		if len(oc) == RT_API_LIMIT:
			oc.add(NextPageObject(key=Callback(PornstarsList, mainTitle=mainTitle, searchQuery=searchQuery, page=int(page)+1), title='More...'))
	else:
		PCbfLogging('event',PCbfLoggingDH,'/pornstar',TITLE+' - Porn Stars: '+mainTitle+' (API)','Error','Loading Porn Stars: '+mainTitle,'No Content! API changed?',page)
	return oc
