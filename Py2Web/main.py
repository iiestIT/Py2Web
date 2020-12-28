from PySide2.QtWidgets import QDialog
from Py2Web.browser import Py2WebBrowser
import time


def get(url: str, script: str = "", p2wb: Py2WebBrowser = Py2WebBrowser):
    pw = p2wb()
    st = time.time()
    pw.get(url, script)
    if pw.exec_() == QDialog.Accepted:
        ret = pw.return_
        ret.update({"process_time": time.time() - st})
        return ret
