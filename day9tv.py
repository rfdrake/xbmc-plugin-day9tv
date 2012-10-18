import urllib, urllib2, re, sys, os
import xbmc, xbmcaddon, xbmcgui, xbmcplugin

from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import BeautifulSoup
pluginhandle=int(sys.argv[1])

class Day9tv:

    USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"
    __settings__ = xbmcaddon.Addon(id='plugin.video.day9tv')
    __language__ = __settings__.getLocalizedString

    def action(self, params):
        get = params.get
        if (get("action") == "showTitles"):
            self.showTitles(params)
        if (get("action") == "showGames"):
            self.showGames(params)
        if (get("action") == "showSearch"):
            self.showSearch(params)
        if (get("action") == "showVideo"):
            self.showVideo(params)

    # ------------------------------------- Menu functions ------------------------------------- #

    # display the root menu
    def root(self):
        self.addCategory(self.__language__(31000), 'http://day9.tv/archives', 'showTitles', 1)
        self.addCategory('Search', '', 'showSearch', 1)
        # these need to be dynamic
        self.addCategory('Funday Monday', 'http://day9.tv/archives?q=%22Funday%20Monday%22', 'showTitles', 1)
        self.addCategory('Newbie Tuesday', 'http://day9.tv/archives?q=%22Newbie%20Tuesday%22', 'showTitles', 1)
        self.addCategory('MetaDating', 'http://day9.tv/archives?q=MetaDating', 'showTitles', 1)
        self.addCategory('Red Bull LAN', 'http://day9.tv/archives?q=%22Red%20Bull%20LAN%22', 'showTitles', 1)
        self.addCategory('Amnesia: The Dark Descent', 'http://day9.tv/archives?q=%22Amnesia%3A%20The%20Dark%20Descent%22', 'showTitles', 1)
        self.addCategory('IEM GamesCom', 'http://day9.tv/archives?q=%22IEM%20GamesCom%22', 'showTitles', 1)
        self.addCategory('Protoss', 'http://day9.tv/archives?q=protoss', 'showTitles', 1)
        self.addCategory('Zerg', 'http://day9.tv/archives?q=zerg', 'showTitles', 1)
        self.addCategory('Terran', 'http://day9.tv/archives?q=terran', 'showTitles', 1)


    # ------------------------------------- Add functions ------------------------------------- #


    def addCategory(self, title, url, action, page = 1):
        url=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&title="+title+"&action="+urllib.quote_plus(action)+"&page="+str(page)
        listitem=xbmcgui.ListItem(title,iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
        listitem.setInfo( type="Video", infoLabels={ "Title": title } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=True)

    def addVideo(self,title,youtubeid,description='',picture=''):
        url=sys.argv[0]+"?youtubeid="+youtubeid+"&action=showVideo"
        liz=xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png")
        liz.setInfo( type="Video", infoLabels={ "Title": title } )
        liz.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

    # ------------------------------------- Show functions ------------------------------------- #

    def showSearch(self, params = {}):
        get = params.get
        self.addCategory('New Search', 'url', 'nothing', '')
        #for entry in saved_searches:


    def showTitles(self, params = {}):
        get = params.get
        link = self.getRequest(get("url"))
        tree = BeautifulSoup(link)
        # narrow down the search to get rid of upcoming shows
        # I'd like to add them just to inform people of what/when things are
        # happening but there isn't good markup to isolate them
        results=tree.find('ul', { "id" : "results" })
        # need to figure out how to do this as one regex.  Also not done
        # figuring out soup yet so these are still re on general HTML.
        title = re.compile('<h3><a href=".*?">(.*)</a></h3>').findall(str(results))
        url = re.compile('<a href="(/d/Day9/.*?)"').findall(str(results))
        airdate = re.compile('<h3><a href=".*?">.*?</a></h3>.*?<time datetime="(.*)"').findall(str(results))

        for i in range(len(title)):
            self.addCategory(title[i], 'http://day9.tv/'+url[i], 'showGames', '')

        page = int(get("page"))+1
        url = 'http://day9.tv/archives/?page='+str(page)
        self.addCategory('more episodes...', url, 'showTitles', page)

    def showGames(self, params = {}):
        get = params.get
        link = self.getRequest(get("url"))
        # look at cinemassecre plugin for inspiration on how to do this nice
        # if we can parse it
        # lack of markup is killing me.. nothing can safely parse this
        #tree = BeautifulSoup(link)
        #picture = tree.find('div', id='content').find('img')
        #description = tree.find('div', id='content').div.find('p')
        videos = re.findall('<iframe .*? src="http://www.youtube.com/embed/(.*?)">', link)
        i=0
        for v in videos:
            i=i+1
            self.addVideo(get("title")+' Part '+str(i), youtubeid=v)

    def showVideo(self, params = {}):
        get = params.get
        youTubeId = get("youtubeid")
        # need to start a video before you can hand it over youtube plugin
        req = urllib2.Request('http://www.youtube.com/embed/'+youTubeId)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()

        stream_url = "plugin://plugin.video.youtube/?action=play_video&videoid=" + youTubeId
        item = xbmcgui.ListItem(path=stream_url)
        item.setProperty("IsPlayable","true")
        xbmcplugin.setResolvedUrl(pluginhandle, True, item)
        return False

    # ------------------------------------- Data functions ------------------------------------- #

    def getParams(self, paramList):
        splitParams = paramList[paramList.find('?')+1:].split('&')
        paramsFinal = {}
        for value in splitParams:
            splitParams = value.split('=')
            type = splitParams[0]
            content = splitParams[1]
            if type == 'url':
                content = urllib.unquote_plus(content)
            paramsFinal[type] = content
        return paramsFinal

    def getRequest(self, url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', self.USERAGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
