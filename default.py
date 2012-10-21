import urllib, urllib2, re, sys, os, string, day9tv
import xbmc, xbmcaddon, xbmcgui, xbmcplugin

__version__ = "0.0.1"
__plugin__ = "Day9tv-" + __version__
__author__ = "Robert"
__settings__ = xbmcaddon.Addon(id='plugin.video.day9tv')
__language__ = __settings__.getLocalizedString

Day9tv = day9tv.Day9tv()

if (not sys.argv[2]):
    Day9tv.root()
else:
	print __plugin__

	params = Day9tv.getParams(sys.argv[2])
	get = params.get
	if (get("action")):
		Day9tv.action(params)
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))
