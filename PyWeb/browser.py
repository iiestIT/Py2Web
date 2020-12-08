from PySide2.QtCore import QUrl, QTimer, Qt
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PySide2.QtWebEngineWidgets import QWebEngineSettings as ws
from PySide2.QtWebEngineCore import QWebEngineHttpRequest
from PySide2.QtWidgets import QDialog
from PySide2.QtNetwork import QNetworkCookie
from PyWeb.config import BaseConfig as bconf
import random


class PyWebBrowser(QDialog):
    def __init__(self):
        super(PyWebBrowser, self).__init__()
        self.pwb = QWebEngineView()
        self.pwb.setAttribute(Qt.WA_DeleteOnClose, True)

        self.raw_cookies = []
        self.cookie_list = []

        self.req_obj = QWebEngineHttpRequest()
        self.source_timer = QTimer()

        profile = QWebEngineProfile("pyweb", self.pwb)
        profile.setHttpUserAgent(random.choice(bconf.USER_AGENT_LIST))
        cookie_store = profile.cookieStore()

        cookie_store.cookieAdded.connect(self._on_cookie)

        wp = QWebEnginePage(profile, self.pwb)
        self.pwb.setPage(wp)

        self._settings()

    def _settings(self):
        s = self.pwb.settings()
        s.setAttribute(ws.AutoLoadImages, bconf.AUTO_LOAD_IMAGES)
        s.setAttribute(ws.JavascriptEnabled, bconf.JAVASCRIPT_ENABLED)
        s.setAttribute(ws.JavascriptCanOpenWindows, bconf.JAVASCRIPT_CAN_OPEN_WINDOWS)
        s.setAttribute(ws.LocalStorageEnabled, bconf.LOCAL_STORAGE_ENABLED)
        s.setAttribute(ws.LocalContentCanAccessRemoteUrls, bconf.LOCAL_CONTENT_CAN_ACCESS_REMOTE_URLS)
        s.setAttribute(ws.LocalContentCanAccessFileUrls, bconf.LOCAL_CONTENT_CAN_ACCESS_FILE_URLS)
        s.setAttribute(ws.ErrorPageEnabled, bconf.ERROR_PAGES_ENABLED)
        s.setAttribute(ws.PluginsEnabled, bconf.PLUGINS_ENABLED)
        s.setAttribute(ws.WebGLEnabled, bconf.WEBGL_ENABLED)
        s.setAttribute(ws.AllowRunningInsecureContent, bconf.ALLOW_RUNNING_INSECURE_CONTENT)
        s.setAttribute(ws.AllowGeolocationOnInsecureOrigins, bconf.ALLOW_GEOLOCATION_ON_INSECURE_ORIGINS)
        s.setAttribute(ws.ShowScrollBars, bconf.SHOW_SCROLL_BARS)
        s.setAttribute(ws.DnsPrefetchEnabled, bconf.DNS_PREFETCH_ENABLED)

    def _get_page_source(self):
        if self.pwb.loadFinished:
            self.pwb.page().toHtml(self._page_to_var)
            self.pwb.page().runJavaScript(self.s)

    def _page_to_var(self, html):
        self.page_source = html
        self.source_timer.stop()
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
        self.return_dict = {
            "url": str(self.req_obj.url().toString()),
            "cookies": self.cookie_list,
            "content": str(self.page_source)
        }
        self.accept()

    def get(self, url: str, script: str = None):
        self.s = script
        self.req_obj.setUrl(QUrl().fromUserInput(url))

        self.source_timer.setInterval(bconf.SOURCE_WAIT_INTERVAL)
        self.source_timer.timeout.connect(self._get_page_source)
        self.source_timer.start()

        self.pwb.load(self.req_obj)
