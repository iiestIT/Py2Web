from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QDialog
from PyWeb.browser import PyWebBrowser
from PyWeb.utils.xvfb import VirtualDisplay


def get(url: str):
    # vd = VirtualDisplay()
    # vd.init_xvfb()
    app = QApplication([])
    pw = PyWebBrowser()
    pw.get(url)
    pw.setAttribute(Qt.WA_DeleteOnClose, True)
    pw.setAttribute(Qt.WA_DontShowOnScreen, True)
    if pw.exec_() == QDialog.Accepted:
        # vd.stop_xvfb()
        return pw.return_dict
