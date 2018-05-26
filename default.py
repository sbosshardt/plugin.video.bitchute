import sys
import xbmcaddon
addon = xbmcaddon.Addon('plugin.video.bitchute')


# Connect to a debugger (local or remote) if remote_debugger is "true" in addon.xml.
remote_debugger = False
remote_debugger_host = "localhost"
remote_debugger_port = 5678
pysrc_path = ""

try:
    remote_debugger = addon.getSetting('remote_debugger')
    print "Value of remote_debugger is: " + remote_debugger
except:
    pass

try:
    remote_debugger_host = addon.getSetting('remote_debugger_host')
    print "Value of remote_debugger_host is: " + remote_debugger_host
except:
    pass

try:
    remote_debugger_port = addon.getSetting('remote_debugger_port')
    remote_debugger_port = int(remote_debugger_port)
    print "Value of remote_debugger_port is: " + remote_debugger_port
except:
    pass

try:
    pysrc_path = addon.getSetting('pysrc_path')
    print "Value of pysrc_path is: " + pysrc_path
except:
    pass

# append pydev remote debugger
if remote_debugger == "true":
    if pysrc_path != "":
        try:
            sys.path.append(pysrc_path);
        except:
            print "Unable to append pysrc_path \"" + pysrc_path + "\"."
            pass
    
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pysrc.pydevd as pydevd # with the addon script.module.pydevd, only use `import pydevd`
    except:
        try:
            import pydevd
        except ImportError:
            sys.stderr.write("Error: Debugging could not be enabled." +
            "Unable to determine directory where org.python.pydev.debug.pysrc is stored. " +
            "Please add this path either to your PYTHONPATH, or in the \"pysrc_path\" setting in addon.xml. " +
            "If you are not sure where this is, try searching your computer for a \"pysrc\" directory.")
            sys.exit(1)
    
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
    pydevd.settrace(host=remote_debugger_host, stdoutToServer=True, stderrToServer=True, port=remote_debugger_port)


# -*- coding: cp1252 -*-
from bs4 import BeautifulSoup
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc

# Set default encoding to 'UTF-8' instead of 'ascii'
reload(sys)
sys.setdefaultencoding("UTF8")

__language__  = addon.getLocalizedString
__icon__ = addon.getAddonInfo('icon')
__fanart__ = addon.getAddonInfo('fanart')

#headers = ['User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
headers = [['User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0 SeaMonkey/2.46'],
    ['Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8']]

def CATEGORIES():

#Video categories on Main Page
    addLink('Latest - All','listing-all',1,__icon__,True)
    addLink('Latest - Popular','listing-popular',1,__icon__,True)
    addLink('Latest - Trending','listing-trending',1,__icon__,True)
    req = urllib2.Request("http://www.bitchute.com/")
    for header in headers:
        req.add_header(*header)
    url = urllib2.urlopen(req)
    body = url.read()

    soup = BeautifulSoup(body, "html.parser")
    
    links = {}
    
    for link in soup.find_all('li'):
        for link2 in link.find_all('a'):
             href = link2.get('href')
             if not href: continue
             href = ("https://www.bitchute.com"+href if href[0] == "/" else href)
             if "/category/" in href:
                 links[href] = {}

    iconImage='DefaultVideo.png'
    for link in links:
        addLink(link[link.index("/category/")+10:].title(),link,2,iconImage,True)
        
def LATESTVIDS(url):
    #Latest Videos on Main Page
    req = urllib2.Request("https://www.bitchute.com/")
    for header in headers:
        req.add_header(*header)
    urlx = urllib2.urlopen(req)
    bodyx = urlx.read()
    soup = BeautifulSoup(bodyx, "html.parser")

    links = {}
    # note: url variable is actually storing an HTML element id
    for link in soup.select('#'+url+' a'):
        href = link.get('href')
        className = link.get('class')
        if href and href.startswith('/video'):
            if className and 'btn' in className:
                continue
            children = link.find_all('img',{'class':'img-responsive'})
            if link.parent.name.lower() == "img":
                if "img-responsive" in link.parent.get('class'):
                    children += link.parent.parent.find_all('img',{'class':'img-responsive'})
            for child in children:
                if href not in links:
                    links[href] = {}
                child_data_src = child.get("data-src")
                if child_data_src and "play-button" not in child_data_src and "thumbnail" not in links[href]:
                    links[href]["thumbnail"] = child_data_src
                childsrc = child.get("src")
                if "play-button.png" not in childsrc and "thumbnail" not in links[href]:
                    links[href]["thumbnail"] = childsrc
            if len(children) == 0:
                if href not in links:
                    links[href] = {}
                links[href]["name"] = link.contents[0].strip("\n").strip()
    links2 = []
    for index, link in enumerate(links.iteritems()):
        if index >= 60:
            break
        thumbnail = None if "thumbnail" not in link[1] else link[1]["thumbnail"]
        if thumbnail != None and thumbnail[0] == "/":
            thumbnail = "https://www.bitchute.com"+thumbnail
        if thumbnail == None:
            thumbnail = __icon__
        linkToURL = link[0] if link[0][0] != "/" else "https://www.bitchute.com"+link[0]
        addLink(link[1]["name"].encode("utf8"),linkToURL.encode("utf8"),3,thumbnail,False)
              
def INDEX(url):
    req = urllib2.Request(url)
    for header in headers:
        req.add_header(*header)
    urlx = urllib2.urlopen(req)
    bodyx = urlx.read()
    soup = BeautifulSoup(bodyx, "html.parser")

    links = {}
    for link in soup.find_all('a'):
        href = link.get('href')
        className = link.get('class')
        if href and href.startswith('/video'):
            if className and 'btn' in className:
                continue
            children = link.find_all('img',{'class':'img-responsive'})
            if link.parent.name.lower() == "img":
                if "img-responsive" in link.parent.get('class'):
                    children += link.parent.parent.find_all('img',{'class':'img-responsive'})
            for child in children:
                if href not in links:
                    links[href] = {}
                child_data_src = child.get("data-src")
                if child_data_src and "play-button" not in child_data_src and "thumbnail" not in links[href]:
                    links[href]["thumbnail"] = child_data_src
                childsrc = child.get("src")
                if "play-button.png" not in childsrc and "thumbnail" not in links[href]:
                    links[href]["thumbnail"] = childsrc
            if len(children) == 0:
                if href not in links:
                    links[href] = {}
                links[href]["name"] = link.contents[0].strip("\n").strip()
    links2 = []
    for index, link in enumerate(links.iteritems()):
        if index >= 60:
            break
        thumbnail = None if "thumbnail" not in link[1] else link[1]["thumbnail"]
        if thumbnail != None and thumbnail[0] == "/":
            thumbnail = "https://www.bitchute.com"+thumbnail
        if thumbnail == None:
            thumbnail = __icon__
        linkToURL = link[0] if link[0][0] != "/" else "https://www.bitchute.com"+link[0]
        addLink(link[1]["name"].encode("utf8"),linkToURL.encode("utf8"),3,thumbnail,False)


def VIDEOLINKS(url,name,icon):
        req = urllib2.Request(url)
        for header in headers:
            req.add_header(*header)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=(re.compile("torrent.addWebSeed\('(.+?)'\)").findall(link)+re.compile('torrent.addWebSeed\("(.+?)"\)').findall(link))
        if len(match) == 0:
            match += re.compile(r'<source src="(.+?)"(?:\s*)\/?>').findall(link)
        for url in match:
            playLink(name,url,icon)
            break
        

                
# Examples of sys.argv:
# ['plugin://plugin.video.bitchute/', '4', '?mode=2&name=Music&url=https%3a%2f%2fwww.bitchute.com%2fcategory%2fmusic']
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def playLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        #ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        player = xbmc.Player()
        player.play(url, liz);
        return ok


def addLink(name,url,mode,iconimage,isfolder):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isfolder)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
        
elif mode==1:
        print ""
        LATESTVIDS(url)
       
elif mode==2:
        print ""+url
        INDEX(url)       
       
elif mode==3:
        print ""+url
        VIDEOLINKS(url,name,__icon__)
else:
        print ""+url
        CATEGORIES()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
