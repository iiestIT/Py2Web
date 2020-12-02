from PySide2.QtCore import QUrl, QTimer
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PySide2.QtWebEngineCore import QWebEngineHttpRequest
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtNetwork import QNetworkCookie
from PyWeb.config import BaseConfig as bconf
import sys


class PyWebBrowser(QMainWindow):
    def __init__(self, url: str):
        super(PyWebBrowser, self).__init__()

        self.pwb = QWebEngineView()
        self.raw_cookies = []
        self.cookie_list = []

        self.req_obj = QWebEngineHttpRequest()
        self.req_obj.setUrl(QUrl().fromUserInput(url))

        profile = QWebEngineProfile("pyweb", self.pwb)
        cookie_store = profile.cookieStore()

        cookie_store.cookieAdded.connect(self._on_cookie)

        wp = QWebEnginePage(profile, self.pwb)
        self.pwb.setPage(wp)
        self.pwb.load(self.req_obj)

        if bconf.DEBUG == 1:
            self.pwb.show()

        self.source_timer = QTimer()
        self.source_timer.setInterval(bconf.SOURCE_WAIT_INTERVAL)
        self.source_timer.timeout.connect(self._get_page_source)
        self.source_timer.start()

    def _get_page_source(self):
        if self.pwb.loadFinished:
            self.pwb.page().toHtml(self._page_to_var)
            self.source_timer.stop()
            self._to_json()

    def _page_to_var(self, html):
        self.page_source = html

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
        print("Cookies as list of dicts")
        print(self.cookie_list)
