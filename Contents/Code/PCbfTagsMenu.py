@route(PREFIX+'/tagsmenu')
def TagsMenu():
	oc = ObjectContainer(title2='Tags')
	pageFormat = 'Tag'
	try: pageContent = HTML.ElementFromURL(RT_HTML_TAGS)
	except: PCbfLogging('event',PCbfLoggingDH,'/tag',TITLE+' - Tags (HTML)','Error','Loading Tags','Page Not Found!',0)
	if (len(pageContent.xpath('//ul[contains(@class,"most-popular-tags")]/li'))>0):
		for tagItem in pageContent.xpath('//ul[contains(@class,"most-popular-tags")]/li'):
			try: tagItemTitle = tagItem.xpath('a[contains(@class,"tag-link")]/text()')[0].strip()
			except: tagItemTitle = None
			try: tagItemTagName = tagItem.xpath('a[contains(@class,"tag-link")]')[0].get('href').replace('/tag','')
			except: tagItemTagName = None
			try:
				tagItemThumb = tagItem.xpath('a/img')[0].get('src')
				HTTP.PreCache(tagItemThumb, cacheTime=CACHE_1WEEK)
			except: tagItemThumb = None
			try: tagItemNrVids = tagItem.xpath('span[contains(@class,"number-videos")]/text()')[0].strip().replace(',','.')
			except: tagItemNrVids = None
			if ((tagItemTitle == None) or (tagItemTagName == None) or (tagItemThumb == None) or (tagItemNrVids == None)):
				PCbfLogging('event',PCbfLoggingDH,'/tag',TITLE+' - Tags (HTML)','Error','Loading Tags','Problem with Content! HTML changed?',0)
				Log(str(tagItemTitle)+'_'+str(tagItemTagName)+'_'+str(tagItemThumb)+'_'+str(tagItemNrVids))
			oc.add(DirectoryObject(key=Callback(SortOrderSubMenu, mainTitle=tagItemTitle, url=RT_HTML_TAG, searchQuery=tagItemTagName, pageFormat=pageFormat), title=tagItemTitle, thumb=tagItemThumb, tagline=tagItemNrVids, summary=tagItemNrVids))
	else:
		PCbfLogging('event',PCbfLoggingDH,'/tag',TITLE+' - Tags (HTML)','Error','Loading Tags','XPath_1 failed! HTML changed?',0)
	if (len(pageContent.xpath('//ul[contains(@class,"list-tags")]/li'))>0):
		for tagItem in pageContent.xpath('//ul[contains(@class,"list-tags")]/li'):
			try: tagItemTitle = tagItem.xpath('a[contains(@class,"tag-link")]/text()')[0].strip()
			except: tagItemTitle = None
			try: tagItemTagName = tagItem.xpath('a[contains(@class,"tag-link")]')[0].get('href').replace('/tag','')
			except: tagItemTagName = None
			try: tagItemNrVids = tagItem.xpath('span[contains(@class,"number-videos")]/text()')[0].strip().replace(',','.')
			except: tagItemNrVids = None
			if ((tagItemTitle == None) or (tagItemTagName == None) or (tagItemNrVids == None)):
				PCbfLogging('event',PCbfLoggingDH,'/tag',TITLE+' - Tags (HTML)','Error','Loading Tags','Problem with Content! HTML changed?',0)
				Log(str(tagItemTitle)+'_'+str(tagItemTagName)+'_'+str(tagItemNrVids))
			oc.add(DirectoryObject(key=Callback(SortOrderSubMenu, mainTitle=tagItemTitle, url=RT_HTML_TAG, searchQuery=tagItemTagName, pageFormat=pageFormat), title=tagItemTitle, tagline=tagItemNrVids, summary=tagItemNrVids))
	else:
		PCbfLogging('event',PCbfLoggingDH,'/tag',TITLE+' - Tags (HTML)','Error','Loading Tags','XPath_2 failed! HTML changed?',0)
	if len(oc) > 0:
		PCbfLogging('pageview',PCbfLoggingDH,'/tag',TITLE+' - Tags (HTML)')
	else:
		PCbfLogging('event',PCbfLoggingDH,'/tag',TITLE+' - Tags (HTML)','Error','Loading Tags','No Content! HTML changed?',0)
		try: tags = JSON.ObjectFromURL(RT_API_TAGS)
		except: PCbfLogging('event',PCbfLoggingDH,'/tag',TITLE+' - Tags (API)','Error','Loading Tags','API Not Found!',0)
		for tag in tags['tags']:
			try: tagItemTitle = tag['tag']['tag_name'].capitalize()
			except: tagItemTitle = None
			try: tagItemTagName = tag['tag']['tag_name']
			except: tagItemTagName = None
			if ((tagItemTitle == None) or (tagItemTagName == None)):
				PCbfLogging('event',PCbfLoggingDH,'/tag',TITLE+' - Tags (API)','Error','Loading Tags','Problem with Content! API changed?',0)
				Log(str(tagItemTitle)+'_'+str(tagItemTagName))
			oc.add(DirectoryObject(key=Callback(SortOrderSubMenu, mainTitle=tagItemTitle, url=RT_HTML_TAG, searchQuery=tagItemTagName, pageFormat=pageFormat), title=tagItemTitle))
		if len(oc) > 0:
			PCbfLogging('pageview',PCbfLoggingDH,'/tag',TITLE+' - Tags (API)')
		else:
			PCbfLogging('event',PCbfLoggingDH,'/tag',TITLE+' - Tags (API)','Error','Loading Tags','No Content! API changed?',0)
	return oc
