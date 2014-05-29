@route(PREFIX+'/getvideobyid', videoID=int)
def getVideoById(videoID, ocML=None):
	isVideoActiveCheck = False
	if (ocML != None):
		isVideoActiveCheck = True
	else:
		try:
			isVideoActive = JSON.ObjectFromURL(RT_API_BASE+RT_API_isVideoActive % videoID, cacheTime=3600)
			if isVideoActive['active']['is_active'] == 1: isVideoActiveCheck = True
		except:
			PCbfLogging('event',PCbfLoggingDH,'/'+str(videoID),TITLE+' - Video (API)','Error','Loading Video','Is Active Fail!',videoID)
	if (isVideoActiveCheck == True):
		try: data = JSON.ObjectFromURL(RT_API_BASE+RT_API_getVideoById % videoID, cacheTime=3600)
		except:
			PCbfLogging('event',PCbfLoggingDH,'/'+str(videoID),TITLE+' - Video (API)','Error','Loading Video','API Not Found!',videoID)
			data = None
		if 'video' in data:
			try: data = data['video']
			except: data = None
			try: videoURL = data['url']
			except: videoURL = None
			videoTAGS = []
			if 'tags' in data:
				for key in data['tags']:
					videoTAGS.append(data['tags'][key])
			try: videoDURATION = Datetime.MillisecondsFromString(data['duration'])
			except: videoDURATION = None
			try: videoRATING = float(data['rating']) * 2
			except: videoRATING = None
			try:
				videoTITLE = data['title']
				oc = ObjectContainer(title2=videoTITLE)
			except: videoTITLE = None
			try: videoYEAR = int(data['publish_date'].split('-')[0])
			except: videoYEAR = None
			try: videoOAAT = Datetime.ParseDate(data['publish_date']).date()
			except: videoOAAT = None
			try: videoSUMMARY = 'Duration: '+data['duration']+' | Tags: '+', '.join(videoTAGS)
			except: videoSUMMARY = None
			try:
				videoTHUMB = data['default_thumb'].replace('m.jpg', 'b.jpg')
				HTTP.PreCache(videoTHUMB, cacheTime=CACHE_1WEEK)
			except: videoTHUMB = None
			if ((data == None) or (videoURL == None) or (len(videoTAGS)<1) or (videoDURATION == None) or (videoRATING == None) or (videoTITLE == None) or (videoYEAR == None) or (videoOAAT == None) or (videoSUMMARY == None) or (videoTHUMB == None)):
				PCbfLogging('event',PCbfLoggingDH,'/'+str(videoID),TITLE+' - Video (API)','Error','Loading Video','Problem with Content! API changed?',videoID)
				Log(str(videoID)+'_'+str(videoURL)+'_'+str(len(videoTAGS))+'_'+str(videoDURATION)+'_'+str(videoRATING)+'_'+str(videoTITLE)+'_'+str(videoYEAR)+'_'+str(videoOAAT)+'_'+str(videoSUMMARY)+'_'+str(videoTHUMB))
			if (ocML == None):
				oc = ObjectContainer(title2=videoTITLE, no_cache=True)
				oc.add(VideoClipObject(
					url = videoURL,
					genres = ['XXX','Adult','18+'],
					tags = videoTAGS,
					duration = videoDURATION,
					rating = videoRATING,
					title = 'Play: '+videoTITLE,
					year = videoYEAR,
					originally_available_at = videoOAAT,
					tagline = videoSUMMARY,
					summary = videoSUMMARY,
					content_rating = 'XXX',
					content_rating_age = 18,
					thumb = Resource.ContentsOfURLWithFallback(videoTHUMB, fallback=R(ICON)),
					art = Resource.ContentsOfURLWithFallback(videoTHUMB, fallback=R(ART)))
				)
#				oc.add(InputDirectoryObject(
#					key=Callback(SetRatingRT, videoID=videoID),
#					title='Rate video on RedTube',
#					tagline='',
#					summary='Rate video on RedTube',
#					thumb=R(ICON),
#					art='',
#					prompt='Rate video on RedTube - only 1-5')
#				)
				if Data.Exists('PCbfFavorites'):
					favs = Data.LoadObject('PCbfFavorites')
					if videoID in favs:
						oc.add(DirectoryObject(key=Callback(RemoveVideoFromFavorites, id=videoID, name=str(videoTITLE)), title='Remove from Favorites', summary='Remove this video from your Favorites.', thumb=R(ICON)))
					else:
						oc.add(DirectoryObject(key=Callback(AddVideoToFavorites, id=videoID, name=str(videoTITLE)), title='Add to Favorites', summary='Add this video to your Favorites.', thumb=R(ICON)))
				else:
					oc.add(DirectoryObject(key=Callback(AddVideoToFavorites, id=videoID, name=str(videoTITLE)), title='Add to Favorites', summary='Add this video to your Favorites.', thumb=R(ICON)))
			#	if len(oc) == 3:
				if len(oc) == 2:
					PCbfLogging('pageview',PCbfLoggingDH,'/'+str(videoID),TITLE+' - '+str(videoTITLE)+' (API)')
					return oc
				else:
					PCbfLogging('event',PCbfLoggingDH,'/'+str(videoID),TITLE+' - Video','Error','Loading Video','Unknown Error!',videoID)
					return ObjectContainer(header='Sorry, an Error occurred!', message='Not sure why, but there occured an error retrieving data for this video.', no_cache=True)
			else:
				return ocML.add(DirectoryObject(
					key = Callback(getVideoById, videoID=videoID),
					title = videoTITLE,
					tagline = videoSUMMARY,
					summary = videoSUMMARY,
					thumb = Resource.ContentsOfURLWithFallback(videoTHUMB, fallback=R(ICON)),
					art = Resource.ContentsOfURLWithFallback(videoTHUMB, fallback=R(ART)),
					duration = videoDURATION)
				)
		else:
			PCbfLogging('event',PCbfLoggingDH,'/'+str(videoID),TITLE+' - Video (API)','Error','Loading Video','Problem with Content! API changed?',videoID)
			return ObjectContainer(header='Sorry, an Error occurred!', message='Not sure why, but there occured an error retrieving data for this video.', no_cache=True)
	else:
		try: RemoveVideoFromFavorites(videoID)
		except: pass
		PCbfLogging('event',PCbfLoggingDH,'/'+str(videoID),TITLE+' - Video','Error','Loading Video','Video failed isVideoActiveCheck!',videoID)
		return ObjectContainer(header='Sorry, an Error occurred!', message='This video is not available on RedTube anymore.', no_cache=True)
