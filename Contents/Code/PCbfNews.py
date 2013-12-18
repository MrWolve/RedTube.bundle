@route(PREFIX+'/pcbfnews', limit=int)
def PCbfNews(oc=None, limit=10):
	try: newsContent = JSON.ObjectFromURL('http://plexchannels.com/c/%s-news/?json=1&count=%s' % ("".join(TITLE.lower().split()), limit))
	except: PCbfLogging('event','plexchannels.com',('/c/%s-news/' % (TITLE.lower())),TITLE+' - Plex Channel by flow - News','Error','News','Error reading News!',limit)
	if (oc == None):
		oc = ObjectContainer(title2='Plex Channel by flow - News')
		for news in newsContent['posts']:
			try: newsExcerpt = String.StripTags(news['excerpt']).replace(' et&#46;&#46;&#46','...')
			except: newsExcerpt = 'No excerpt for this news.'
			try: newsUrl = news['custom_fields']['shorturl'][0]
			except:
				try: newsUrl = news['url']
				except: newsUrl = 'http://plexchannels.com'
			oc.add(DirectoryObject(
				key = Callback(PCbfNewsDetail, headline=news['title_plain'], url=newsUrl),
				title = news['title_plain'],
				tagline = newsExcerpt,
				summary = newsExcerpt,
				thumb = Resource.ContentsOfURLWithFallback(news['thumbnail'], fallback=R(ICON)))
			)
		PCbfLogging('event','plexchannels.com',('/c/%s-news/' % ("".join(TITLE.lower().split()))),TITLE+' - Plex Channel by flow - News','News','News','News read.',limit)
		return oc
	else:
		for news in newsContent['posts']:
			try: newsExcerpt = String.StripTags(news['excerpt']).replace(' et&#46;&#46;&#46','...')
			except: newsExcerpt = 'No excerpt for this news.'
			return oc.add(DirectoryObject(
				key = Callback(PCbfNews),
				title = news['title_plain'],
				tagline = newsExcerpt,
				summary = newsExcerpt,
				thumb = Resource.ContentsOfURLWithFallback(news['thumbnail'], fallback=R(ICON)))
			)

def PCbfNewsDetail(headline, url):
	PCbfLogging('event','plexchannels.com','/'+url.rsplit('/',1)[1].strip(),TITLE+' - '+headline,'News','NewsDetail','NewsDetail read.',0)
	return ObjectContainer(header=headline, message='For the complete news please enter this URL:\r\n'+url+'\r\nin your favored browser, or use the shown QR-Code.', no_cache=True)
