import os


class BaseConfig:
    DEBUG = int(os.environ.get("DEBUG"))
    SOURCE_WAIT_INTERVAL = int(os.environ.get("SOURCE_WAIT_INTERVAL", 5000))
