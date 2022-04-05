from threading import Thread, Event
from urllib.parse import urlparse
import time
import requests


class Monitor(Thread):
    """
    Class to periodically monitor status of used web.
    """
    def __init__(self):
        super(Monitor, self).__init__()
        self.converters = dict()
        self.stop_request = Event()
        self.first_check = Event()

    def set_converters(self, converters):
        self.converters = converters

    @staticmethod
    def get_base_url(converter):
        """
        Extract base URL from the converter.

        :param converter: given converter
        :return: base URL
        """
        url = urlparse(list(converter.endpoints.values())[0])
        return url.scheme + "://" + url.netloc

    @staticmethod
    def check_service(url):
        """
        Send a GET request to given URL with 5 sec timeout.

        :param url: given URL
        :return: True if request is successful with status code 200
        """
        try:
            result = requests.get(url, timeout=5)
            return result.status_code == 200
        except (requests.exceptions.ConnectionError, TimeoutError, requests.exceptions.ReadTimeout):
            return False

    def run(self):
        """
        Main loop of the Monitor thread.

        Monitor checks if GET on base URL of every converter give status code 200.
        Such a converter is considered available.
        This is checked periodically to always have up-to-date information.
        """
        while not self.stop_request.isSet():
            for converter in self.converters.values():
                url = self.get_base_url(converter)
                converter.is_available = self.check_service(url)
            self.first_check.set()
            time.sleep(10)

    def join(self, timeout=None):
        self.stop_request.set()
