from PySide2.QtCore import QUrl, QTimer
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PySide2.QtWebEngineCore import QWebEngineHttpRequest
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtNetwork import QNetworkCookie
from PyWeb.config import BaseConfig as bconf
import sys


class PyWebBrowser(QMainWindow):
    def __init__(self):
        super(PyWebBrowser, self).__init__()

        self.pwb = QWebEngineView()
        self._init_settings()

        self.raw_cookies = []
        self.cookie_list = []

        self.req_obj = QWebEngineHttpRequest()
        self.source_timer = QTimer()

        profile = QWebEngineProfile("pyweb", self.pwb)
        cookie_store = profile.cookieStore()

        cookie_store.cookieAdded.connect(self._on_cookie)

        wp = QWebEnginePage(profile, self.pwb)
        self.pwb.setPage(wp)

    def _get_page_source(self):
        if self.pwb.loadFinished:
            self.pwb.page().toHtml(self._page_to_var)

    def _page_to_var(self, html):
        self.page_source = html
        self.source_timer.stop()
        self._to_json()

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
        print("Cookies")
        print(self.cookie_list)

    def _init_settings(self):
        self.pwb.settings().setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)
        self.pwb.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.pwb.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, False)
        self.pwb.settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)

    def get(self, url: str):
        self.req_obj.setUrl(QUrl().fromUserInput(url))

        self.source_timer.setInterval(bconf.SOURCE_WAIT_INTERVAL)
        self.source_timer.timeout.connect(self._get_page_source)
        self.source_timer.start()

        self.pwb.load(self.req_obj)

        if bconf.DEBUG == 1:
            self.pwb.show()
