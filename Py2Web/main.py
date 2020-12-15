from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog
from Py2Web.browser import Py2WebBrowser
from Py2Web.utils.xvfb import VirtualDisplay


def get(url: str):
    # vd = VirtualDisplay()
    # vd.init_xvfb()
    pw = Py2WebBrowser()
    pw.get(url)
    pw.setAttribute(Qt.WA_DeleteOnClose, True)
    pw.setAttribute(Qt.WA_DontShowOnScreen, True)
    if pw.exec_() == QDialog.Accepted:
        # vd.stop_xvfb()
        return pw.return_dict
