from PySide2.QtWidgets import QDialog
from PySide2.QtNetwork import QNetworkCookie
from typing import Union
from Py2Web.browser import Py2WebBrowser
import time


def get(
        url: str,
        script: Union[str, list] = "",
        wait_bs: int = 0,
        wait_as: int = 0,
        cookies: Union[QNetworkCookie, list[QNetworkCookie], None] = None,
        p2wb: Py2WebBrowser = Py2WebBrowser
):
    pw = p2wb()
    st = time.time()
    pw.get(
        url=url,
        script=script,
        wait_bs=wait_bs,
        wait_as=wait_as,
        cookies=cookies
    )
    if pw.exec_() == QDialog.Accepted:
        ret = pw.return_
        ret.update({"process_time": time.time() - st})
        return ret
