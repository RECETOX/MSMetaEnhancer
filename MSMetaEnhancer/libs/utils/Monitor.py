from threading import Thread, Event
from urllib.parse import urlparse
import time
import requests


class Monitor(Thread):
    def __init__(self, converters):
        super(Monitor, self).__init__()
        self.converters = converters
        self.stop_request = Event()

    def get_base_url(self, converter):
        url = urlparse(list(converter.services.values())[0])
        return url.scheme + "://" + url.netloc

    def check_service(self, url):
        return requests.get(url, timeout=5)

    def run(self):
        while not self.stop_request.isSet():
            for converter in self.converters.values():
                url = self.get_base_url(converter)
                try:
                    result = self.check_service(url)
                    if result.status_code == 200:
                        converter.is_available = True
                except (requests.exceptions.ConnectionError, TimeoutError):
                    converter.is_available = False
            time.sleep(10)

    def join(self, timeout=None):
        self.stop_request.set()
