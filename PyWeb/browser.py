from PySide2.QtCore import QUrl, QTimer
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import QApplication, QMainWindow
import sys


class PyWebBrowser(QMainWindow):
    def __init__(self, url: str):
        super(PyWebBrowser, self).__init__()

        self.pwb = QWebEngineView()
        self.pwb.setUrl(QUrl().fromUserInput(url))

        self.pwb.show()

        self.source_timer = QTimer()
        self.source_timer.setInterval(5000)
        self.source_timer.timeout.connect(self._get_page_source)
        self.source_timer.start()

    def _get_page_source(self):
        def _print(html):
            print(html)

        if self.pwb.loadFinished:
            self.pwb.page().toHtml(_print)
            self.source_timer.stop()
