import datetime, re, json
from mod_helper import *

debug = True

def disneychannelShow():
	oc = ObjectContainer(no_cache=True)
	if debug == True: Log("Running disneychannelShow()...")

	urlMain = "http://disneychannel.de"

	url = urlMain+"/_fta_stream/search.json?q=video&filter[type]=Video&filter[start_date_s]="+(datetime.date.today()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")+"&limit=50&offset=0"
	oc.add(DirectoryObject(key=Callback(disneychannelListVideos, url = url), title='Gestern'))

	url = urlMain+"/_fta_stream/search.json?q=video&filter[type]=Video&filter[start_date_s]="+(datetime.date.today()-datetime.timedelta(days=2)).strftime("%Y-%m-%d")+"&limit=50&offset=0"
	oc.add(DirectoryObject(key=Callback(disneychannelListVideos, url = url), title='Vorgestern'))

	title = (datetime.date.today()-datetime.timedelta(days=3)).strftime("%b %d, %Y")
	url = urlMain+"/_fta_stream/search.json?q=video&filter[type]=Video&filter[start_date_s]="+(datetime.date.today()-datetime.timedelta(days=3)).strftime("%Y-%m-%d")+"&limit=50&offset=0"
	oc.add(DirectoryObject(key=Callback(disneychannelListVideos, url = url), title=title))

	title = (datetime.date.today()-datetime.timedelta(days=4)).strftime("%b %d, %Y")
	url = urlMain+"/_fta_stream/search.json?q=video&filter[type]=Video&filter[start_date_s]="+(datetime.date.today()-datetime.timedelta(days=4)).strftime("%Y-%m-%d")+"&limit=50&offset=0"
	oc.add(DirectoryObject(key=Callback(disneychannelListVideos, url = url), title=title))

	title = (datetime.date.today()-datetime.timedelta(days=5)).strftime("%b %d, %Y")
	url = urlMain+"/_fta_stream/search.json?q=video&filter[type]=Video&filter[start_date_s]="+(datetime.date.today()-datetime.timedelta(days=5)).strftime("%Y-%m-%d")+"&limit=50&offset=0"
	oc.add(DirectoryObject(key=Callback(disneychannelListVideos, url = url), title=title))

	title = (datetime.date.today()-datetime.timedelta(days=6)).strftime("%b %d, %Y")
	url = urlMain+"/_fta_stream/search.json?q=video&filter[type]=Video&filter[start_date_s]="+(datetime.date.today()-datetime.timedelta(days=6)).strftime("%Y-%m-%d")+"&limit=50&offset=0"
	oc.add(DirectoryObject(key=Callback(disneychannelListVideos, url = url), title=title))

	title = (datetime.date.today()-datetime.timedelta(days=7)).strftime("%b %d, %Y")
	url = urlMain+"/_fta_stream/search.json?q=video&filter[type]=Video&filter[start_date_s]="+(datetime.date.today()-datetime.timedelta(days=7)).strftime("%Y-%m-%d")+"&limit=50&offset=0"
	oc.add(DirectoryObject(key=Callback(disneychannelListVideos, url = url), title=title))

	return oc

def disneychannelCreateVideoObject(item, container = False):
	if debug == True: Log("Running disneychannelCreateVideoObject()...")
	if debug == True: Log("Creating VideoObject: " + str(item))

	try:
		vo = VideoClipObject(
			key = Callback(disneychannelCreateVideoObject, item = item, container = True),
			title = item['title'],
			summary = item['summary'],
			thumb = item['thumb'],
			duration = item['duration'],
			rating_key = item['url'],
			items = []
		)

		# Lookup URL and create MediaObject.
		mo = MediaObject(parts = [PartObject(key = Callback(disneychannelGetStreamingUrl, url = item['url']))])

		# Append mediaobject to clipobject.
		vo.items.append(mo)

		if container:
			return ObjectContainer(objects = [vo])
		else:
			return vo
	except Exception as e:
		if debug == True: Log("ERROR: " + str(e))

def disneychannelGetStreamingUrl(url):
        if debug == True: Log("Running disneychannelGetStreamingUrl()...")

	try:
		content = getURL(url)
		match = re.compile('embedURL":"(.+?)",', re.DOTALL).findall(content)
		content = getURL(match[0])
		match2 = re.compile('url":"https://once-eu.unicornmedia.com(.+?)"', re.DOTALL).findall(content)
		finalURL = 'http://once-eu.unicornmedia.com' + match2[0]
		return Redirect(finalURL)
	except Exception as e:
                if debug == True: Log("ERROR: " + str(e))

def disneychannelListVideos(url):
	if debug == True: Log("Running disneychannelListVideos()...")
	mediaList = ObjectContainer(no_cache=True)

	try:
		content = getURL(url)
		content = json.loads(content)
		for item in content["data"]["results"]:
			title = item["title"].encode('utf-8')
			desc = item["ptitle"][0].encode('utf-8')
			url = item["href"]
			thumb = item["thumb"]
			duration = item["duration"]

			video = {
				'title':title,
				'summary':item["description"],
				'url':url,
				'thumb':thumb,
				'duration':int(item["duration_sec"])*60000
			}
			vo = disneychannelCreateVideoObject(video)
			mediaList.add(vo)

		return mediaList
	except Exception as e:
                if debug == True: Log("ERROR: " + str(e))
