import os


class BaseConfig:
    DEBUG = int(os.environ.get("DEBUG"))
    SOURCE_WAIT_INTERVAL = int(os.environ.get("SOURCE_WAIT_INTERVAL", 5000))
    AUTO_LOAD_IMAGES = bool(os.environ.get("AUTO_LOAD_IMAGES", True))
    JAVASCRIPT_ENABLED = bool(os.environ.get("JAVASCRIPT_ENABLED", True))
    JAVASCRIPT_CAN_OPEN_WINDOWS = bool(os.environ.get("JAVASCRIPT_CAN_OPEN_WINDOWS", False))
    LOCAL_STORAGE_ENABLED = bool(os.environ.get("LOCAL_STORAGE_ENABLED", True))
    LOCAL_CONTENT_CAN_ACCESS_REMOTE_URLS = bool(os.environ.get("LOCAL_CONTENT_CAN_ACCESS_REMOTE_URLS", True))
    LOCAL_CONTENT_CAN_ACCESS_FILE_URLS = bool(os.environ.get("LOCAL_CONTENT_CAN_ACCESS_FILE_URLS", True))
    ERROR_PAGES_ENABLED = bool(os.environ.get("ERROR_PAGES_ENABLED", False))
    PLUGINS_ENABLED = bool(os.environ.get("PLUGINS_ENABLED", False))
    WEBGL_ENABLED = bool(os.environ.get("WEBGL_ENABLED", True))
    ALLOW_RUNNING_INSECURE_CONTENT = bool(os.environ.get("ALLOW_RUNNING_INSECURE_CONTENT", False))
    ALLOW_GEOLOCATION_ON_INSECURE_ORIGINS = bool(os.environ.get("ALLOW_GEOLOCATION_ON_INSECURE_ORIGINS", False))
    SHOW_SCROLL_BARS = bool(os.environ.get("SHOW_SCROLL_BARS", False))
    DNS_PREFETCH_ENABLED = bool(os.environ.get("DNS_PREFETCH_ENABLED", False))
