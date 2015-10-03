debug = True

def getURL(url):
	if debug == True: Log("Fetching content from url: " + url)
	try:
		content = HTTP.Request(url, cacheTime = CACHE_1HOUR).content
	except Exception as e:
		if debug == True: Log(str(e))
	return content
