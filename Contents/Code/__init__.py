import base64, simplejson, time, datetime, re
from mod_sesamstrasse import *
from mod_kikaninchen import *
from mod_disneychannel import *
json = simplejson

# Static text. 
TEXT_NAME = 'Mediathek für Kindet'
TEXT_TITLE = 'KinderThek' 

# Image resources.
ICON_DEFAULT = 'icon-default.png'
ART_DEFAULT = 'art-default.jpg'

ICON_FOLDER = R('icon-folder.png')

# Other definitions.
PLUGIN_PREFIX = '/video/kinderthek'
debug = True

####################################################################################################

def Start():
	ObjectContainer.art = R(ART_DEFAULT)
	HTTP.CacheTime = 300

####################################################################################################
@handler(PLUGIN_PREFIX, TEXT_TITLE, ICON_DEFAULT, ART_DEFAULT)
def MainMenu():
	oc = ObjectContainer(no_cache=False)	

	oc.title1 = TEXT_TITLE
	oc.header = None
	oc.message = None 

	count = 0
	if Prefs['enable_sesamstrasse'] == True:
		count = count + 1
		oc.add(DirectoryObject(key=Callback(sesamstrasseShow), title='Sesamstrasse', thumb=ICON_FOLDER))
	if Prefs['enable_kikaninchen'] == True:
		count = count + 1
		oc.add(DirectoryObject(key=Callback(kikaninchenShow), title='Kikaninchen', thumb=ICON_FOLDER))
	if Prefs['enable_disneychannel'] == True:
		count = count + 1
		oc.add(DirectoryObject(key=Callback(disneychannelShow), title='Disneychannel', thumb=ICON_FOLDER))

	if count == 0:
		oc.header = 'Fehler' 
		oc.message = 'Es wurden keine Mediatheken zur Anzeige eingeschaltet!' 

	return oc

####################################################################################################
@route(PLUGIN_PREFIX + '/ValidatePrefs')
def ValidatePrefs():
	return True
