@route(PREFIX+'/categoriesmenu')
def CategoriesMenu():
	oc = ObjectContainer(title2='Categories')
	pageFormat = 'Channel'
	try: pageContent = HTML.ElementFromURL(RT_HTML_CHANNELS)
	except: PCbfLogging('event',PCbfLoggingDH,'/channels',TITLE+' - Categories (HTML)','Error','Loading Categories','Page Not Found!',0)
	if (len(pageContent.xpath('//ul[contains(@class,"videoThumbs")]/li'))>0):
		for categoryItem in pageContent.xpath('//ul[contains(@class,"videoThumbs")]/li'):
			try: categoryItemTitle = categoryItem.xpath('div/a')[0].get('title')
			except: categoryItemTitle = None
			try: categoryItemCatName = categoryItem.xpath('div/a/img')[0].get('id')
			except: categoryItemCatName = None
			try:
				categoryItemThumb = 'http:'+categoryItem.xpath('div/a/img')[0].get('data-src')
				HTTP.PreCache(categoryItemThumb, cacheTime=CACHE_1WEEK)
			except: categoryItemThumb = None
			try: categoryItemNrVids = categoryItem.xpath('p/text()')[0].strip().replace(',','.')
			except: categoryItemNrVids = None
			if ((categoryItemTitle == None) or (categoryItemCatName == None) or (categoryItemThumb == None) or (categoryItemNrVids == None)):
				PCbfLogging('event',PCbfLoggingDH,'/channels',TITLE+' - Categories (HTML)','Error','Loading Categories','Problem with Content! HTML changed?',0)
				Log(str(categoryItemTitle)+'_'+str(categoryItemCatName)+'_'+str(categoryItemThumb)+'_'+str(categoryItemNrVids))
			oc.add(DirectoryObject(key=Callback(SortOrderSubMenu, mainTitle=categoryItemTitle, url=RT_HTML_CHANNEL, searchQuery=categoryItemCatName, pageFormat=pageFormat), title=categoryItemTitle, thumb=categoryItemThumb, tagline=categoryItemNrVids, summary=categoryItemNrVids))
	else:
		PCbfLogging('event',PCbfLoggingDH,'/channels',TITLE+' - Categories (HTML)','Error','Loading Categories','XPath failed! HTML changed?',0)
	if len(oc) > 0:
		PCbfLogging('pageview',PCbfLoggingDH,'/channels',TITLE+' - Categories (HTML)')
	else:
		PCbfLogging('event',PCbfLoggingDH,'/channels',TITLE+' - Categories (HTML)','Error','Loading Categories','No Content! HTML changed?',0)
		try: categories = JSON.ObjectFromURL(RT_API_CHANNELS)
		except: PCbfLogging('event',PCbfLoggingDH,'/channels',TITLE+' - Categories (API)','Error','Loading Categories','API Not Found!',0)
		for key in categories['categories']:
			try: categoryItemTitle = key['category'].capitalize()
			except: categoryItemTitle = None
			try: categoryItemCatName = key['category']
			except: categoryItemCatName = None
			if ((categoryItemTitle == None) or (categoryItemCatName == None)):
				PCbfLogging('event',PCbfLoggingDH,'/channels',TITLE+' - Categories (API)','Error','Loading Categories','Problem with Content! API changed?',0)
				Log(str(categoryItemTitle)+'_'+str(categoryItemCatName))
			oc.add(DirectoryObject(key=Callback(SortOrderSubMenu, mainTitle=categoryItemTitle, url=RT_HTML_CHANNEL, searchQuery=categoryItemCatName, pageFormat=pageFormat), title=categoryItemTitle))
		if len(oc) > 0:
			PCbfLogging('pageview',PCbfLoggingDH,'/channels',TITLE+' - Categories (API)')
		else:
			PCbfLogging('event',PCbfLoggingDH,'/channels',TITLE+' - Categories (API)','Error','Loading Categories','No Content! API changed?',0)
	return oc
