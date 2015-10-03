import datetime, re
from mod_helper import *

debug = True

def kikaninchenShow():
	kikaList = ObjectContainer(no_cache=True)
	if debug == True: Log("Running kikaninchenShow()...")

	try:
		urlMain = "http://kikaninchen.de"
		content = getURL("http://www.kikaninchen.de/kikaninchen/filme/filme100-flashXml.xml")
		content = content[content.find('<links id="program">'):]
		spl = content.split('<multiMediaLink id="">')
		for i in range(1, len(spl), 1):
			entry = spl[i]
			match = re.compile('<description><!.CDATA.(.+?).></description>', re.DOTALL).findall(entry)
			desc = match[0].replace("]","")
			#desc = cleanTitle(desc)
			match = re.compile('<path type="intern" target="flashapp">(.+?)</path>', re.DOTALL).findall(entry)
			url = match[0]
			match = re.compile('/kikaninchen/filme/(.+?)/', re.DOTALL).findall(url)
			showID = match[0]
			showTitles = {'kikabaumhaus':'Baumhaus', 'zigbydaszebra':'Zigby das Zebra', 'einfallfuerfreunde':'Ein Fall für die drei Freunde', 'raketenfliegertimmi':'Raketenflieger Timmi', 'bummi':'Bummi', 'diesendungmitdemelefanten':'Die Sendung mit dem Elefanten', 'wdewlidh':'Weißt Du eigentlich, wie lieb ich dich hab?', 'mitmachmuehle':'Mit-Mach-Mühle', 'tauchtimmytauch':'tauch Timmy tauch', 'tillyundihrefreunde':'Tilly und Ihre Freunde', 'sesamstrassepraesentierteinemoehrefuerzwei':'Eine Möhre für Zwei', 'zoeszauberschrank':'Zoes Zauberschrank', 'unsersandmaennchen':'Unser Sandmännchen', 'enemenebuunddranbistdu':'ENE MENE BU - und dran bist du', 'ichkenneeintier':'Ich kenne ein Tier', 'meinbruderundich':'Mein Bruder und ich', 'sesamstrasse':'Die Sesamstraße', 'singasmusikbox':'Singas Musik Box', 'kallisgutenachtgeschichten':'Kallis GuteNachtGeschichten', 'tomunddaserdbeermarmeladebrot':'TOM und das Erdbeermarmeladebrot mit Honig', 'elefantastisch':'Elefantastisch!'}
			title = showTitles.get(showID, showID.title())
			match = re.compile('<image>(.+?)</image>', re.DOTALL).findall(entry)
			thumb = match[0]
			match = re.compile('<audio>(.+?)</audio>', re.DOTALL).findall(entry)
			audioUrl = ""
			if match:
				audioUrl = match[0]
			#GetImageHash - unable to stat url
			#thumb = thumb[:thumb.find('_h')]+"_v-galleryImage_-fc0f89b63e73c7b2a5ecbe26bac10a07631d8c2f.jpg"
			#if not "auswahlkikaninchenfilme" in url and not "kikaninchentrailer" in url:
			#    addDir(title, url, 'listVideosKN', thumb, desc, audioUrl)
			title = title.decode('utf-8', 'ignore')
			kikaList.add(DirectoryObject(key=Callback(kikaninchenListVideosKN, url = url, audiourl = audioUrl), title=title, thumb = thumb))
		return kikaList
	except Exception as e:
		if debug == True: Log("ERROR: " + str(e))

def kikaninchenListVideosKN(url, audiourl):
	mediaList = ObjectContainer(no_cache=True)
	if debug == True: Log("Running kikaninchenListVideosKN()...")

	try:
		if url.endswith("index.html"):
			content = getURL(url)
			match = re.compile('flashvars.page = "(.+?)"', re.DOTALL).findall(content)
			url = match[0]

		content = getURL(url)
		spl = content.split('<movie>')
		for i in range(1, len(spl), 1):
			entry = spl[i]
			match = re.compile('<title>(.+?)</title>', re.DOTALL).findall(entry)
			match2 = re.compile('<number>(.+?)</number>', re.DOTALL).findall(entry)
			if match2:
				title = match[0] + ' ' + match2[0]
			else:
				title = match[0]
			#title = cleanTitle(title)
			match = re.compile('<mediaType>WEBL</mediaType>.+?<flashMediaServerURL>(.+?)<', re.DOTALL).findall(entry)
			urltmp = match[0]
			url = urltmp.replace("mp4:mp4dyn/","")
			match = re.compile('<image>(.+?)</image>', re.DOTALL).findall(entry)
			thumb = match[0]
			#GetImageHash - unable to stat url
			#thumb = thumb[:thumb.find('_h')]+"_v-galleryImage_-fc0f89b63e73c7b2a5ecbe26bac10a07631d8c2f.jpg"

			if debug == True: Log("Creating VideoObject for title: " + title)
			item = {
				'title':title,
				'url':url,
				'thumb':thumb,
				#'duration':int(duration)*60000
			}
			vo = kikaninchenCreateVideoObject(item)
			mediaList.add(vo)
		return mediaList
	except Exception as e:
		if debug == True: Log("ERROR: " + str(e))

def kikaninchenCreateVideoObject(item, container = False):
	if debug == True: Log("Running kikaninchenCreateVideoObject()...")
	if debug == True: Log("Creating VideoObject: " + str(item))

	try:
		vo = VideoClipObject(
			key = Callback(kikaninchenCreateVideoObject, item = item, container = True),
			title = item['title'],
			thumb = item['thumb'],
			#duration = item['duration'],
			rating_key = item['url'],
			items = []
		)

		# Lookup URL and create MediaObject.
		mo = MediaObject(parts = [PartObject(key = Callback(kikaninchenGetStreamingUrl, url = item['url']))])

		# Append mediaobject to clipobject.
		vo.items.append(mo)

		if container:
			return ObjectContainer(objects = [vo])
		else:
			return vo
	except Exception as e:
		if debug == True: Log("ERROR: " + str(e))

def kikaninchenGetStreamingUrl(url):
	url = "http://pmdonline.kika.de/mp4dyn/" + url

	if debug == True: Log("Playing video URL: " + url)
	return Redirect(url)
