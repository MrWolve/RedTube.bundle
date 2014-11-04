TITLE		=	'RedTube'
PREFIX	=	'/video/redtube'
PCVer		=	str('1.0.20131224')

#https://developers.google.com/analytics/devguides/collection/protocol/v1/parameters
PCbfLoggingDH		=	String.Quote('redtube.com')
PCbfLoggingTID	=	'UA-40179636-2'	#tid

from PCbfCommon import *
import random

ART					=	'artwork-'+str(random.randint(1,4))+'.jpg'
ICON				=	'icon-default.png'
SEARCH_ICON =	'icon-search.png'


###################################################################################################
RT_HTML_BASE				=	'http://www.redtube.com'
RT_HTML_NewestSP		=	'/?page=%s'
RT_HTML_TopRated		=	'/top?period=%s&page=%s'
RT_HTML_MostViewed	=	'/mostviewed?period=%s&page=%s'
RT_HTML_MostFavored	=	'/mostfavored?period=%s&page=%s'
RT_HTML_CHANNELS		=	RT_HTML_BASE+'/channels'
RT_HTML_TAGS				=	RT_HTML_BASE+'/tag'
#RT_HTML_PORNSTARS	=	RT_HTML_BASE+'/pornstar/%s/%s'
RT_HTML_CHANNEL			=	'/redtube/%s?sorting=%s&page=%s'
RT_HTML_TAG					=	'/tag/%s/%s?page=%s'
RT_HTML_PORNSTAR		=	'/pornstar/%s/%s?page=%s'
RT_HTML_PCbf				=	'/plexchannels'

RT_API_BASE						= 'http://api.redtube.com/?data=redtube.'
RT_API_searchVideos		=	'Videos.searchVideos&output=json&thumbsize=big&%s'
RT_API_getVideoById		=	'Videos.getVideoById&output=json&thumbsize=big&video_id=%s'
RT_API_isVideoActive	=	'Videos.isVideoActive&output=json&video_id=%s'
RT_API_Newest					=	'ordering=newest&page=%s'
RT_API_TopRated				=	'ordering=rating&period=%s&page=%s'
RT_API_MostViewed			=	'ordering=mostviewed&period=%s&page=%s'
RT_API_CHANNEL				=	'category=%s&ordering=%s&page=%s'
RT_API_TAG						=	'tags[]=%s&ordering=%s&page=%s'
RT_API_PORNSTAR				=	'stars[]=%s&ordering=%s&page=%s'
RT_API_SEARCH					=	'search=%s&ordering=%s&page=%s'
RT_API_CHANNELS				=	RT_API_BASE+'Categories.getCategoriesList&output=json'
RT_API_TAGS						=	RT_API_BASE+'Tags.getTagList&output=json'
RT_API_PORNSTARS			=	RT_API_BASE+'Stars.getStarDetailedList&output=json'
RT_API_LIMIT					=	int(26)

RT_HTML_VIDEO_xpath		=	'//div[@class="video"]/a/@href'
RT_HTML_NEXTa_xpath		=	'//a[@id="navNext"]'
RT_HTML_NEXTb_xpath		=	'//link[@rel="next"]'
#RT_HTML_RATE					=	RT_HTML_BASE+'/rate?object_type=1&object_id=%s&rate=%s&ufAC=%s'
#REGEXufAC						=	Regex("'ufAC', '(?P<ufAC>\w+)'")


####################################################################################################
from PCbfNews import *
from PCbfPreCache import *
from PCbfSetHeaders import *


####################################################################################################
def Start():
	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON)
	VideoClipObject.art = R(ART)
	try:
		SetHeadersDone = doSetHeaders()
		PCbfLogging('pageview',PCbfLoggingDH,'/',TITLE)
		try: PCbfLogging('event',PCbfLoggingDH,'/',TITLE,'Notice','SetHeaders','doSetHeaders done.',SetHeadersDone)
		except: PCbfLogging('event',PCbfLoggingDH,'/',TITLE,'Error','SetHeaders','doSetHeaders failed!',SetHeadersDone)
	except:
		PCbfLogging('pageview',PCbfLoggingDH,'/',TITLE)
		try: PCbfLogging('event',PCbfLoggingDH,'/',TITLE,'Error','SetHeaders','doSetHeaders completly failed!',0)
		except: pass


###################################################################################################
@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():
	oc = ObjectContainer()
	oc.add(DirectoryObject(key=Callback(MovieList, mainTitle='Newest (Staff Picks)', url=RT_HTML_NewestSP, pageFormat='NewestSP'), title='Newest (Staff Picks)', summary='The newest RedTube Staff Picks.', thumb=R(ICON)))
	oc.add(DirectoryObject(key=Callback(SortOrderSubMenu, mainTitle='Top Rated', url=RT_HTML_TopRated, pageFormat='TopRated'), title='Top Rated', summary='Watch the Top Rated videos on RedTube.', thumb=R(ICON)))
	oc.add(DirectoryObject(key=Callback(SortOrderSubMenu, mainTitle='Most Viewed', url=RT_HTML_MostViewed, pageFormat='MostViewed'), title='Most Viewed', summary='Watch the Most Viewed videos on RedTube.', thumb=R(ICON)))
	oc.add(DirectoryObject(key=Callback(SortOrderSubMenu, mainTitle='Most Favored', url=RT_HTML_MostFavored, pageFormat='MostFavored'), title='Most Favored', summary='Watch the Most Favored videos on RedTube.', thumb=R(ICON)))
	oc.add(DirectoryObject(key=Callback(CategoriesMenu), title='Categories', summary='Browse videos by Categories.', thumb=R(ICON)))
	oc.add(DirectoryObject(key=Callback(TagsMenu), title='Tags', summary='Browse videos by Tags.', thumb=R(ICON)))
	oc.add(DirectoryObject(key=Callback(PornstarsMenu), title='Porn Stars', summary='Browse videos of your favorite Porn Star.', thumb=R(ICON)))
	oc.add(DirectoryObject(key=Callback(MovieList, mainTitle='Favorites', url=RT_HTML_PCbf, pageFormat='Favorites'), title='Favorites', summary='Your favorite RedTube videos.', thumb=R(ICON)))
	oc.add(InputDirectoryObject(key=Callback(Search), title="Search", summary="Search RedTube for videos", prompt="Search for", thumb=R(SEARCH_ICON)))
	oc.add(PrefsObject(title='Preferences',summary='Change RedTube Channel Settings.'))
	PCbfNews(oc=oc, limit=1)
	try:
		PCbfReferer = {'Referer': 'http://plexchannels.com/channels/'+TITLE.lower()}
		try:
			FakeReq = HTTP.Request(RT_HTML_BASE, headers=PCbfReferer, cacheTime=3600, immediate=True).content
			PCbfLogging('event',PCbfLoggingDH,'/',TITLE,'Information','Platform.OS and Client.Platform and Client.Product',str(Platform.OS)+' and '+str(Client.Platform)+' and '+str(Client.Product),0)
		except: PCbfLogging('event',PCbfLoggingDH,'/',TITLE,'Error','PCbfReferer','PCbfReferer failed!',0)
	except: pass
	try:
		PreCacheDone = doPreCache()
		try: PCbfLogging('event',PCbfLoggingDH,'/',TITLE,'Notice','PreCache','doPreCache done.',PreCacheDone)
		except: PCbfLogging('event',PCbfLoggingDH,'/',TITLE,'Error','PreCache','doPreCache failed!',PreCacheDone)
	except:
		try: PCbfLogging('event',PCbfLoggingDH,'/',TITLE,'Notice','PreCache','doPreCache completly failed!',0)
		except: pass
	return oc


####################################################################################################
@route(PREFIX+'/sortordersubmenu')
def SortOrderSubMenu(url, mainTitle, searchQuery=None, pageFormat=None):
	oc = ObjectContainer(title2=mainTitle, no_cache=True)
	if ((pageFormat == 'TopRated') or (pageFormat == 'MostViewed') or (pageFormat == 'MostFavored')):
		oc.add(DirectoryObject(key=Callback(MovieList, url=url, mainTitle=mainTitle, searchQuery=searchQuery, pageFormat=pageFormat, sortOrder='weekly'), title='Weekly'))
		oc.add(DirectoryObject(key=Callback(MovieList, url=url, mainTitle=mainTitle, searchQuery=searchQuery, pageFormat=pageFormat, sortOrder='monthly'), title='Monthly'))
		oc.add(DirectoryObject(key=Callback(MovieList, url=url, mainTitle=mainTitle, searchQuery=searchQuery, pageFormat=pageFormat, sortOrder='alltime'), title='All Time'))
	elif (pageFormat == 'Search'):
		oc.add(DirectoryObject(key=Callback(MovieList, url=url, mainTitle=mainTitle, searchQuery=searchQuery, pageFormat=pageFormat, sortOrder='newest'), title='Newest'))
		oc.add(DirectoryObject(key=Callback(MovieList, url=url, mainTitle=mainTitle, searchQuery=searchQuery, pageFormat=pageFormat, sortOrder='rating'), title='Top Rated'))
		oc.add(DirectoryObject(key=Callback(MovieList, url=url, mainTitle=mainTitle, searchQuery=searchQuery, pageFormat=pageFormat, sortOrder='mostviewed'), title='Most Viewed'))
	else:
		oc.add(DirectoryObject(key=Callback(MovieList, url=url, mainTitle=mainTitle, searchQuery=searchQuery, pageFormat=pageFormat, sortOrder='newest'), title='Newest'))
		if (pageFormat == 'Channel'):
			oc.add(DirectoryObject(key=Callback(MovieList, url=url, mainTitle=mainTitle, searchQuery=searchQuery, pageFormat=pageFormat, sortOrder='rating'), title='Top Rated'))
		else:
			oc.add(DirectoryObject(key=Callback(MovieList, url=url, mainTitle=mainTitle, searchQuery=searchQuery, pageFormat=pageFormat, sortOrder='toprated'), title='Top Rated'))
		oc.add(DirectoryObject(key=Callback(MovieList, url=url, mainTitle=mainTitle, searchQuery=searchQuery, pageFormat=pageFormat, sortOrder='mostviewed'), title='Most Viewed'))
		oc.add(DirectoryObject(key=Callback(MovieList, url=url, mainTitle=mainTitle, searchQuery=searchQuery, pageFormat=pageFormat, sortOrder='mostfavored'), title='Most Favored'))
	return oc

from PCbfFavorites import *
from PCbfgetVideoById import *

@route(PREFIX+'/movielist', page=int)
def MovieList(url, mainTitle=None, searchQuery=None, pageFormat=None, sortOrder=None, page=1):
	ocML = ObjectContainer(title2=mainTitle+' | Page: '+str(page), no_cache=True)
	PCbfLoggingDT = TITLE
	if (pageFormat!=None): PCbfLoggingDT += ' - '+pageFormat
	if (mainTitle!=None): PCbfLoggingDT += ' - '+mainTitle
	if (sortOrder!=None): PCbfLoggingDT += ' - '+sortOrder.capitalize()
	PCbfLoggingDT += ' .'+str(page)
	pageContent = None
	apiContent = None
	if (pageFormat != 'Search'):
		if (pageFormat == 'Favorites'):
			PCbfLoggingDP = url
			try:
				pageContent = ListFavorites()
				if (pageContent==None):
					return ObjectContainer(header='You have no Favorites!', message='You need to add at least one video to your Favorites!', no_cache=True)
			except:
				PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (fake HTML)','Error','List Videos','ListFavorites() failed!',page)
		elif (pageFormat == 'NewestSP'):
			PCbfLoggingDP = (url % (str(page)))
			try: pageContent = HTML.ElementFromURL(RT_HTML_BASE+url % (str(page)))
			except: PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (HTML)','Error','List Videos','Page Not Found!',page)
		elif ((pageFormat == 'TopRated') or (pageFormat == 'MostViewed') or (pageFormat == 'MostFavored')):
			PCbfLoggingDP = (url % (sortOrder, str(page)))
			try: pageContent = HTML.ElementFromURL(RT_HTML_BASE+url % (sortOrder, str(page)))
			except: PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (HTML)','Error','List Videos','Page Not Found!',page)
		else:
			if (sortOrder=='newest'): sortOrderURL=''
			else: sortOrderURL=sortOrder
			PCbfLoggingDP = (url % (searchQuery, sortOrderURL, str(page)))
			try: pageContent = HTML.ElementFromURL(RT_HTML_BASE+url % (searchQuery, sortOrderURL, str(page)))
			except: PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (HTML)','Error','List Videos','Page Not Found!',page)
		if (pageContent!=None):
			if (len(pageContent.xpath(RT_HTML_VIDEO_xpath))>0):
				for videoID in pageContent.xpath(RT_HTML_VIDEO_xpath):
					try: getVideoById(videoID=videoID.strip('/'), ocML=ocML)
					except: PCbfLogging('event',PCbfLoggingDH,str(videoID),PCbfLoggingDT+' (API)','Error','List Videos','getVideoById failed!',int(videoID.strip('/')))
				if (len(ocML)>0):
					PCbfLogging('pageview',PCbfLoggingDP,PCbfLoggingDP,PCbfLoggingDT+' (HTML)')
					if ((len(pageContent.xpath(RT_HTML_NEXTa_xpath))>0) or (len(pageContent.xpath(RT_HTML_NEXTb_xpath))>0)):
						ocML.add(NextPageObject(key=Callback(MovieList, url=url, mainTitle=mainTitle, searchQuery=searchQuery, pageFormat=pageFormat, sortOrder=sortOrder, page=(int(page)+1)), title='More...'))
					else:
						PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (HTML)','Notice','List Videos','No NEXT. HTML changed?',page)
				else:
					PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (HTML)','Notice','List Videos','No Videos to list. Trying API instead of HTML.',page)
			else:
				PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (HTML)','Error','List Videos','XPath RT_HTML_VIDEO_xpath failed! HTML changed?',page)
	if ((pageFormat == 'Search') or (len(ocML)<1)):
		if (pageFormat == 'NewestSP'):
			PCbfLoggingDP = (url % (str(page)))
			try: apiContent = JSON.ObjectFromURL(RT_API_BASE+(RT_API_searchVideos % (RT_API_Newest % str(page))))
			except: PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (API)','Error','List Videos','API Not Found!',page)
		elif ((pageFormat == 'TopRated') or (pageFormat == 'MostViewed') or (pageFormat == 'MostFavored')):
			PCbfLoggingDP = (url % (sortOrder, str(page)))
			if (pageFormat == 'TopRated'):
				try: apiContent = JSON.ObjectFromURL(RT_API_BASE+(RT_API_searchVideos % (RT_API_TopRated % (sortOrder, str(page)))))
				except: PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (API)','Error','List Videos','Page Not Found!',page)
			else:
				try: apiContent = JSON.ObjectFromURL(RT_API_BASE+(RT_API_searchVideos % (RT_API_MostViewed % (sortOrder, str(page)))))
				except: PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (API)','Error','List Videos','Page Not Found!',page)
		elif ((pageFormat == 'Channel') or (pageFormat == 'Tag') or (pageFormat == 'PornStar') or (pageFormat == 'Search')):
			if (sortOrder=='newest'): sortOrderURL=''
			elif (sortOrder=='toprated'):
				sortOrderURL=sortOrder
				sortOrder='rating'
			elif (sortOrder=='mostfavored'):
				sortOrderURL=sortOrder
				sortOrder='mostviewed'
			else: sortOrderURL=sortOrder
			PCbfLoggingDP = (url % (searchQuery, sortOrderURL, str(page)))
			if (pageFormat == 'Channel'):
				try: apiContent = JSON.ObjectFromURL(RT_API_BASE+(RT_API_searchVideos % (RT_API_CHANNEL % (searchQuery, sortOrder, str(page)))))
				except: PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (API)','Error','List Videos','Page Not Found!',page)
			elif (pageFormat == 'Tag'):
				try: apiContent = JSON.ObjectFromURL(RT_API_BASE+(RT_API_searchVideos % (RT_API_TAG % (searchQuery, sortOrder, str(page)))))
				except: PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (API)','Error','List Videos','Page Not Found!',page)
			elif (pageFormat == 'PornStar'):
				try: apiContent = JSON.ObjectFromURL(RT_API_BASE+(RT_API_searchVideos % (RT_API_PORNSTAR % (searchQuery, sortOrder, str(page)))))
				except: PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (API)','Error','List Videos','Page Not Found!',page)
			else:
				if String.Quote(searchQuery, usePlus=True).isdigit():
					try: getVideoById(videoID=int(String.Quote(searchQuery, usePlus=True)), ocML=ocML)
					except: PCbfLogging('event',PCbfLoggingDH,str(videoID),PCbfLoggingDT+' (API)','Error','List Videos','getVideoById failed (Search)!',int(String.Quote(searchQuery, usePlus=True)))
				else:
					try: apiContent = JSON.ObjectFromURL(RT_API_BASE+(RT_API_searchVideos % (RT_API_SEARCH % (String.Quote(searchQuery, usePlus=True), sortOrder, str(page)))))
					except: PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (API)','Error','List Videos','Page Not Found!',page)
		if (apiContent!=None):
			if 'videos' in apiContent:
				for data in apiContent['videos']:
					if not 'video' in data: data = None
					else: data = data['video']
					try: videoID = data['video_id']
					except: videoID = None
					videoTAGS = []
					if 'tags' in data:
						for key in data['tags']:
							videoTAGS.append(key['tag_name'])
					try: videoDURATION = Datetime.MillisecondsFromString(data['duration'])
					except: videoDURATION = None
					try:
						videoTITLE = data['title']
						oc = ObjectContainer(title2=videoTITLE)
					except: videoTITLE = None
					try: videoSUMMARY = 'Duration: '+data['duration']+' | Tags: '+', '.join(videoTAGS)
					except: videoSUMMARY = None
					try:
						videoTHUMB = data['default_thumb'].replace('m.jpg', 'b.jpg')
						HTTP.PreCache(videoTHUMB, cacheTime=CACHE_1WEEK)
					except: videoTHUMB = None
					if ((data == None) or (videoID == None) or (len(videoTAGS)<1) or (videoDURATION == None) or (videoTITLE == None) or (videoSUMMARY == None) or (videoTHUMB == None)):
						PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (API)','Error','List Videos','Problem with Content! API changed?',page)
					ocML.add(DirectoryObject(
						key = Callback(getVideoById, videoID=videoID),
						title = videoTITLE,
						tagline = videoSUMMARY,
						summary = videoSUMMARY,
						thumb = Resource.ContentsOfURLWithFallback(videoTHUMB, fallback=R(ICON)),
						art = Resource.ContentsOfURLWithFallback(videoTHUMB, fallback=R(ART)),
						duration = videoDURATION)
					)
				if 'count' in apiContent: videoCOUNT = int(apiContent['count'])
				else: videoCOUNT = 0
				if (len(ocML)>0):
					PCbfLogging('pageview',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (API)')
					if (page<((int(videoCOUNT)/RT_API_LIMIT)+1)):
						ocML.add(NextPageObject(key=Callback(MovieList, url=url, mainTitle=mainTitle, searchQuery=searchQuery, pageFormat=pageFormat, sortOrder=sortOrder, page=(int(page)+1)), title='More...'))
					if (pageFormat == 'Search'):
						PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (API)','Search','Query',searchQuery,videoCOUNT)
			else:
				if (pageFormat == 'Search'):
					PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (API)','Notice','List Videos','No Videos found using Search.',0)
					return ObjectContainer(header='Search for: '+searchQuery, message="No Videos found!", no_cache=True)
				else:
					PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (API)','Error','List Videos','No Content! API changed?',page)
					return ObjectContainer(header='Sorry, an Error occurred!', message='Not sure why, but there occured an error retrieving data for your query.', no_cache=True)
		else:
			if (len(ocML)<1):
				PCbfLogging('event',PCbfLoggingDH,PCbfLoggingDP,PCbfLoggingDT+' (API)','Error','List Videos','Problem with Content! API changed?',page)
				return ObjectContainer(header='Sorry, an Error occurred!', message='Not sure why, but there occured an error retrieving data for your query.', no_cache=True)
	if (len(ocML)>0): return ocML
	else:
		PCbfLogging('event',PCbfLoggingDH,str(PCbfLoggingDP),str(PCbfLoggingDT),'Error','List Videos','FATAL ERROR!',page)
		return ObjectContainer(header='Sorry, an Error occurred!', message='Not sure what, but something went terribly wrong...', no_cache=True)

from PCbfCategoriesMenu import *
from PCbfTagsMenu import *
from PCbfPornstarsMenu import *
from PCbfSearch import *
#from PCbfRateing import *
#from PCbf import *
