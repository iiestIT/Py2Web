import sys


class VirtualDisplay:
    def __init__(self):
        try:
            from xvfbwrapper import Xvfb
            self.V_DISPLAY = Xvfb()
        except ImportError:
            self.V_DISPLAY = None

    def init_xvfb(self):
        if not sys.platform.startswith("linux"):
            return
        self.V_DISPLAY.start()

    def stop_xvfb(self):
        if not sys.platform.startswith("linux"):
            return
        self.V_DISPLAY.stop()
