from PySide2.QtCore import QUrl, Qt
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtWebEngineCore import QWebEngineHttpRequest
from PySide2.QtWidgets import QDialog
from PySide2.QtNetwork import QNetworkCookie
from typing import Union
from Py2Web.config import BaseConfig
from Py2Web.engine import Py2WebProfile
import time


class Py2WebBrowser(QDialog):
    def __init__(self, settings=BaseConfig):
        super(Py2WebBrowser, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WA_DontShowOnScreen, True)

        self.pwb = QWebEngineView()
        self.pwb.setAttribute(Qt.WA_DeleteOnClose, True)

        self.bconf = settings()

        self.raw_cookies = []
        self.cookie_list = []
        self.js_return = []

        self.req_obj = QWebEngineHttpRequest()

        profile = Py2WebProfile("pyweb", self.pwb, self.bconf)
        cookie_store = profile.cookieStore()

        cookie_store.cookieAdded.connect(self._on_cookie)

        wp = QWebEnginePage(profile, self.pwb)
        self.pwb.setPage(wp)

        self.pwb.show()

    def _loadFinished(self):
        if self.wait_bs > 0:
            time.sleep(self.wait)
        if len(self.js_script) > 0:
            self._js_runner()
        if self.wait_as > 0:
            time.sleep(self.wait)
        self.pwb.page().toHtml(self._page_to_var)

    def _js_runner(self):
        if type(self.js_script) == list:
            for i in self.js_script:
                self.pwb.page().runJavaScript(i, 0, self._js_callback)
        else:
            self.pwb.page().runJavaScript(self.js_script, 0, self._js_callback)

    def _js_callback(self, jsr):
        self.js_return.append(jsr)

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
            "raw_cookies": self.raw_cookies,
            "content": str(self.page_source),
        }
        if len(self.js_script) > 0:
            self.return_.update({"js_response": self.js_return})
        self.accept()

    def get(
            self,
            url: str,
            script: Union[str, list],
            wait_bs: int = 0,
            wait_as: int = 0,
            cookies: Union[QNetworkCookie, list[QNetworkCookie], None] = None
    ):
        self.js_script = script
        self.wait_bs = wait_bs
        self.wait_as = wait_as
        self.req_obj.setUrl(QUrl().fromUserInput(url))

        self.pwb.page().profile().cookieStore().deleteAllCookies()
        if not cookies == None:
            if type(cookies) == list:
                [self.pwb.page().profile().cookieStore().setCookie(i) for i in cookies]
            else:
                self.pwb.page().profile().cookieStore().setCookie(cookies)

        self.pwb.load(self.req_obj)
        self.pwb.loadFinished.connect(self._loadFinished)
