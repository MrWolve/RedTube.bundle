@route(PREFIX+'/search')
def Search(query):
	try:
		querySEND = String.StripTags(str(query))
		querySEND = querySEND.replace('%20',' ')
		querySEND = querySEND.replace('  ',' ')
		querySEND = querySEND.strip(' \t\n\r')
		querySEND = " ".join(querySEND.split())
		oc = SortOrderSubMenu(RT_API_SEARCH, 'Search Results', searchQuery=querySEND, pageFormat='Search')
		return oc
	except:
		return ObjectContainer(header=TITLE, message="No search results found", no_cache=True)