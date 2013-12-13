@route(PREFIX+'/pcbflogging', PCbfLoggingEV=int)
def PCbfLogging(PCbfLoggingT='pageview',PCbfLoggingDH='plexchannels.com',PCbfLoggingDP='/',PCbfLoggingDT='PlexChannels',PCbfLoggingEC='',PCbfLoggingEA='',PCbfLoggingEL='',PCbfLoggingEV=0):
	if Prefs['PCbfAOO'] == False:
		#https://developers.google.com/analytics/devguides/collection/protocol/v1/parameters
		#PCbfLoggingURLEndPoint	=	'http://www.google-analytics.com/collect?'
		PCbfLoggingURLEndPoint	=	'https://ssl.google-analytics.com/collect?'
		if Data.Exists('PCbfLoggingData'):
			try:
				Daten = Data.LoadObject('PCbfLoggingData')
				Inhalt = Daten.values()
				PCbfLoggingCID = str(Inhalt[0])
			except:
				Daten = Data.LoadObject('PCbfLoggingData')
				Inhalt = Daten.values()
				PCbfLoggingCID = str(Inhalt[0])
		else:
			PCbfLoggingCID =	str(String.UUID())	#cid
			PCbfLoggingCIDA = {}
			PCbfLoggingCIDA[0] = PCbfLoggingCID
			Data.SaveObject('PCbfLoggingData', PCbfLoggingCIDA)
		PCbfLoggingV				=	1	#v
		PCbfLoggingAIP			=	1	#aip
		PCbfLoggingUL				= ''	#Locale.CurrentLocale oder Locale.Geolocation - scheint beides nicht zu funktionieren!	#ul
		PCbfLoggingFL				= PCVer	#fl - genötigt für Plugin Version!!!
		PCbfLoggingHeaders	=	{'User-Agent': 'Mozilla/5.0 ('+str(Platform.OS)+'; '+str(Platform.CPU)+') AppleWebKit/537.36 (KHTML, like Gecko) '+str(Client.Platform).replace(' ','')+'/'+PCVer}
		#PCbfLoggingHeaders	=	{'User-Agent': 'Mozilla/5.0 ('+str(Platform.OS)+'; '+str(Platform.CPU)+') AppleWebKit/537.36 (KHTML, like Gecko) '+str(Client.Platform)+'/'+PCVer+' Safari/537.36'
		#PCbfLoggingHeaders	=	{'User-Agent': 'Mozilla/5.0 ('+str(Client.Platform)+'; '+str(Platform.OS)+'; '+str(Platform.CPU)+'; '+str(Client.Platform)+')'
		#PCbfLoggingHeaders	=	{'User-Agent': 'Mozilla/5.0 ('+str(Platform.OS)+'; '+str(Platform.CPU)+') '+str(Client.Platform)+'/'+PCVer
		#Log('PlexServer ID is '+PCbfLoggingCID)

		UrlGe		=	('v=%s&tid=%s&aip=%s' % (PCbfLoggingV, PCbfLoggingTID, PCbfLoggingAIP))
		UrlVi		=	('&cid=%s' % (String.Quote(str(PCbfLoggingCID))))
		UrlTrSo	= ''	#ungenutzt
		UrlSyIn	=	('&ul=%s&fl=%s' % (String.Quote(str(PCbfLoggingUL)), String.Quote(str(PCbfLoggingFL))))
		UrlHi		=	('&t=%s' % (String.Quote(str(PCbfLoggingT))))
		UrlCoIn	=	('&dh=%s&dp=%s&dt=%s' % (String.Quote(str(PCbfLoggingDH)), String.Quote(str(PCbfLoggingDP)), String.Quote(str(PCbfLoggingDT))))
		UrlEvTr	=	('&ec=%s&ea=%s&el=%s&ev=%s' % (String.Quote(str(PCbfLoggingEC)), String.Quote(str(PCbfLoggingEA)), String.Quote(str(PCbfLoggingEL)), String.Quote(str(PCbfLoggingEV))))
		url	=	PCbfLoggingURLEndPoint+UrlGe+UrlVi+UrlTrSo+UrlSyIn+UrlHi+UrlCoIn+UrlEvTr
		try:
			HTTP.Request(url, headers=PCbfLoggingHeaders, cacheTime=10, timeout=5, immediate=True).headers
			#HTTP.Request(url, cacheTime=0).content
			#Log(HTTP.Request(url, cacheTime=0).headers)
			#Log(str(HTTP.Request('http://api.plexchannels.com/brcheck.php', headers=PCbfLoggingHeaders, cacheTime=0).content))
		except:
			Log(HTTP.Request(url, headers=PCbfLoggingHeaders, cacheTime=10, timeout=5, immediate=True).content)
	else:
		if Data.Exists('PCbfLoggingData'):
			Data.Remove('PCbfLoggingData')
		Log('Anonymous Usage Statistics DEACTIVATED!')

@route(PREFIX+'/dosetheaders')
def doSetHeaders():
	doSetHeadersV = 1
	HTTP.Headers['Referer'] = 'http://plexchannels.com//channels/'+TITLE.lower()
	HTTP.Headers['User-Agent']	=	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
#'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0'
#'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0'
#'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'
#'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0'
#'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
#'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36'
#'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36'
#'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36'
#'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'
#'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)'
#'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'
#'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)'
	return doSetHeadersV
