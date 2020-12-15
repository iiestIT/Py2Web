import os


class BaseConfig:
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
    USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    ]
