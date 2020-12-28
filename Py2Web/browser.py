from PySide2.QtCore import QUrl, Qt
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtWebEngineCore import QWebEngineHttpRequest
from PySide2.QtWidgets import QDialog
from PySide2.QtNetwork import QNetworkCookie
from Py2Web.config import BaseConfig
from Py2Web.engine import Py2WebProfile


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

        self.req_obj = QWebEngineHttpRequest()

        profile = Py2WebProfile("pyweb", self.pwb, self.bconf)
        cookie_store = profile.cookieStore()

        cookie_store.cookieAdded.connect(self._on_cookie)

        wp = QWebEnginePage(profile, self.pwb)
        self.pwb.setPage(wp)

        self.pwb.show()

    def _loadFinished(self):
        if len(self.js_script) > 0:
            self._js_runner()
        self.pwb.page().toHtml(self._page_to_var)

    def _js_runner(self):
        self.pwb.page().runJavaScript(self.js_script, 0, self._js_callback)

    def _js_callback(self, jsr):
        self.js_return = jsr

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
            "content": str(self.page_source),
        }
        if len(self.js_script) > 0:
            self.return_.update({"js_response": self.js_return})
        self.accept()

    def get(self, url: str, script: str):
        self.js_script = script
        self.req_obj.setUrl(QUrl().fromUserInput(url))

        self.pwb.page().profile().cookieStore().deleteAllCookies()

        self.pwb.load(self.req_obj)
        self.pwb.loadFinished.connect(self._loadFinished)
