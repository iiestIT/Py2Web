from PySide2.QtCore import QUrl, Qt
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PySide2.QtWebEngineWidgets import QWebEngineSettings as ws
from PySide2.QtWebEngineCore import QWebEngineHttpRequest
from PySide2.QtWidgets import QDialog
from PySide2.QtNetwork import QNetworkCookie
from Py2Web.config import BaseConfig
import random


class Py2WebBrowser(QDialog):
    def __init__(self, settings=None):
        super(Py2WebBrowser, self).__init__()
        self.pwb = QWebEngineView()
        self.pwb.setAttribute(Qt.WA_DeleteOnClose, True)

        if settings is not None:
            self.bconf = settings
        else:
            self.bconf = BaseConfig()

        self.raw_cookies = []
        self.cookie_list = []

        self.req_obj = QWebEngineHttpRequest()

        profile = QWebEngineProfile("pyweb", self.pwb)
        profile.setHttpUserAgent(random.choice(self.bconf.USER_AGENT_LIST))
        cookie_store = profile.cookieStore()

        cookie_store.cookieAdded.connect(self._on_cookie)

        wp = QWebEnginePage(profile, self.pwb)
        self.pwb.setPage(wp)

        self._settings()
        self.pwb.show()

    def _settings(self):
        self.pwb.settings().setAttribute(ws.AutoLoadImages, self.bconf.AUTO_LOAD_IMAGES)
        self.pwb.settings().setAttribute(ws.JavascriptEnabled, self.bconf.JAVASCRIPT_ENABLED)
        self.pwb.settings().setAttribute(ws.JavascriptCanOpenWindows, self.bconf.JAVASCRIPT_CAN_OPEN_WINDOWS)
        self.pwb.settings().setAttribute(ws.LocalStorageEnabled, self.bconf.LOCAL_STORAGE_ENABLED)
        self.pwb.settings().setAttribute(ws.LocalContentCanAccessRemoteUrls, self.bconf.LOCAL_CONTENT_CAN_ACCESS_REMOTE_URLS)
        self.pwb.settings().setAttribute(ws.LocalContentCanAccessFileUrls, self.bconf.LOCAL_CONTENT_CAN_ACCESS_FILE_URLS)
        self.pwb.settings().setAttribute(ws.ErrorPageEnabled, self.bconf.ERROR_PAGES_ENABLED)
        self.pwb.settings().setAttribute(ws.PluginsEnabled, self.bconf.PLUGINS_ENABLED)
        self.pwb.settings().setAttribute(ws.WebGLEnabled, self.bconf.WEBGL_ENABLED)
        self.pwb.settings().setAttribute(ws.AllowRunningInsecureContent, self.bconf.ALLOW_RUNNING_INSECURE_CONTENT)
        self.pwb.settings().setAttribute(ws.AllowGeolocationOnInsecureOrigins, self.bconf.ALLOW_GEOLOCATION_ON_INSECURE_ORIGINS)
        self.pwb.settings().setAttribute(ws.ShowScrollBars, self.bconf.SHOW_SCROLL_BARS)
        self.pwb.settings().setAttribute(ws.DnsPrefetchEnabled, self.bconf.DNS_PREFETCH_ENABLED)

    def _loadFinished(self):
        self.pwb.page().toHtml(self._page_to_var)
        self.pwb.page().runJavaScript(self.s)

    def _page_to_var(self, html):
        self.page_source = html
        self._to_json()
        self._return()

    def _on_cookie(self, cookie):
        for i in self.raw_cookies:
            if i.hasSameIdentifier(cookie):
                return
        self.raw_cookies.append(QNetworkCookie(cookie))

    def _to_json(self):
        for i in self.raw_cookies:
            data = {
                "name": bytearray(i.name()).decode(),
                "domain": i.domain(),
                "value": bytearray(i.value()).decode(),
                "path": i.path(),
                "expireData": i.expirationDate().toString(),
                "secure": i.isSecure(),
                "httpOnly": i.isHttpOnly()
            }
            self.cookie_list.append(data)

    def _return(self):
        self.return_ = {
            "url": str(self.req_obj.url().toString()),
            "cookies": self.cookie_list,
            "content": str(self.page_source)
        }
        self.accept()

    def get(self, url: str, script: str = None):
        self.s = script
        self.req_obj.setUrl(QUrl().fromUserInput(url))

        self.pwb.page().profile().cookieStore().deleteAllCookies()

        self.pwb.load(self.req_obj)
        self.pwb.loadFinished.connect(self._loadFinished)
