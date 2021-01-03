from PySide2.QtWebEngineWidgets import QWebEngineProfile
from PySide2.QtWebEngineWidgets import QWebEngineSettings as ws
import random


class Py2WebProfile(QWebEngineProfile):
    def __init__(self, name, parent, bconf):
        super(Py2WebProfile, self).__init__(name, parent)
        self.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies)
        self.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)

        self.settings().setAttribute(ws.AutoLoadImages, bconf.AUTO_LOAD_IMAGES)
        self.settings().setAttribute(ws.JavascriptEnabled, bconf.JAVASCRIPT_ENABLED)
        self.settings().setAttribute(ws.JavascriptCanOpenWindows, bconf.JAVASCRIPT_CAN_OPEN_WINDOWS)
        self.settings().setAttribute(ws.LocalStorageEnabled, bconf.LOCAL_STORAGE_ENABLED)
        self.settings().setAttribute(ws.LocalContentCanAccessRemoteUrls, bconf.LOCAL_CONTENT_CAN_ACCESS_REMOTE_URLS)
        self.settings().setAttribute(ws.LocalContentCanAccessFileUrls, bconf.LOCAL_CONTENT_CAN_ACCESS_FILE_URLS)
        self.settings().setAttribute(ws.ErrorPageEnabled, bconf.ERROR_PAGES_ENABLED)
        self.settings().setAttribute(ws.PluginsEnabled, bconf.PLUGINS_ENABLED)
        self.settings().setAttribute(ws.WebGLEnabled, bconf.WEBGL_ENABLED)
        self.settings().setAttribute(ws.AllowRunningInsecureContent, bconf.ALLOW_RUNNING_INSECURE_CONTENT)
        self.settings().setAttribute(ws.AllowGeolocationOnInsecureOrigins, bconf.ALLOW_GEOLOCATION_ON_INSECURE_ORIGINS)
        self.settings().setAttribute(ws.ShowScrollBars, bconf.SHOW_SCROLL_BARS)
        self.settings().setAttribute(ws.DnsPrefetchEnabled, bconf.DNS_PREFETCH_ENABLED)
        self.settings().setDefaultTextEncoding(bconf.DEFAULT_TEXT_ENCODING)

        self.setHttpUserAgent(random.choice(bconf.USER_AGENT_LIST))
