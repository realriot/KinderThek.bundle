import datetime, re
from mod_helper import *

debug = True

def sesamstrasseShow():
	mediaList = ObjectContainer(no_cache=True)
	if debug == True: Log("Running sesamstrasseShow()...")

	try:
		urlMain = "http://www.sesamstrasse.de"
		content = getURL(urlMain+"/home/homepage1077.html")
		spl = content.split('<div class="thumb">')
		for i in range(1, len(spl), 1):
			entry = spl[i]
			match = re.compile('title="(.+?)"', re.DOTALL).findall(entry)
			title = match[0]
			match = re.compile('href="(.+?)"', re.DOTALL).findall(entry)
			url = urlMain+match[0]
			match = re.compile('src="(.+?)"', re.DOTALL).findall(entry)
			thumb = urlMain+match[0]
			thumb = thumb[:thumb.find("_")]+"_v-original.jpg"
			match = re.compile('<div class="subline">(.+?)&nbsp;\\|&nbsp;(.+?):', re.DOTALL).findall(entry)
			date = ""
			duration = ""
			if match:
				date = match[0][0]
				date = date[:date.rfind('.')].strip()
				duration = match[0][1]
				title = date+" - "+title
	
			item = {
				'title':title,
				'url':url,
				'thumb':thumb,
				'duration':int(duration)*60000
			}
			if debug == True: Log("Adding: " + title)
			vo = sesamstrasseCreateVideoObject(item)
			mediaList.add(vo)
		return mediaList
	except Exception as e:
		if debug == True: Log("ERROR: " + str(e))

def sesamstrasseCreateVideoObject(item, container = False):
	if debug == True: Log("Running sesamstrasseCreateVideoObject()...")
	if debug == True: Log("Creating VideoObject: " + str(item))

	try:
		vo = VideoClipObject(
			key = Callback(sesamstrasseCreateVideoObject, item = item, container = True),
			title = item['title'],
			thumb = item['thumb'],
			duration = item['duration'],
			rating_key = item['url'],
			items = []
		)

		# Lookup URL and create MediaObject.
		mo = MediaObject(parts = [PartObject(key = Callback(sesamstrasseGetStreamingUrl, url = item['url']))])

		# Append mediaobject to clipobject.
		vo.items.append(mo)

		if container:
			return ObjectContainer(objects = [vo])
		else:
			return vo
	except Exception as e:
		if debug == True: Log("ERROR: " + str(e))

def sesamstrasseGetStreamingUrl(url):
	if debug == True: Log("Running sesamstrasseGetStreamingUrl()...")

	try:
		quality = 'hd'
		if ',sesamstrasse' in url:
			regex_suffix_id = ',sesamstrasse(.+?).html'
			try: suffix_id = re.findall(regex_suffix_id, url)[0]
			except: suffix_id = '3000'
		else: suffix_id = '3000'
		content = getURL(url)
		json_uuid = re.findall('player_image-(.+?)_', content)[0]
		json_url = 'http://www.sesamstrasse.de/sendungsinfos/sesamstrasse%s-ppjson_image-%s.json' % (suffix_id, json_uuid)
		json = getURL(json_url)
		regex_qualities = '\.,(.+?),\.'
		qualities = re.findall(regex_qualities, json)[-1].split(',')
		if not (quality in qualities): quality = qualities[-1]
		regex_url = '"src": "http://(.+?)"'
		urls = re.findall(regex_url, json)
		stream_url = ''
		for url in urls:
			if url.endswith('.mp4'):
				stream_url = 'http://' + url[:-6] + quality + '.mp4'
				break
		if not stream_url: return

		if debug == True: Log("Playing video URL: " + stream_url)
		return Redirect(stream_url)
	except Exception as e:
		if debug == True: Log("ERROR: " + str(e))
