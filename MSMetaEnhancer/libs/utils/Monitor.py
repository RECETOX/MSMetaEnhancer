from threading import Thread, Event
from urllib.parse import urlparse
import time
import requests


class Monitor(Thread):
    """
    Class to periodically monitor status of used services.
    """
    def __init__(self, converters):
        super(Monitor, self).__init__()
        self.converters = converters
        self.stop_request = Event()

    @staticmethod
    def get_base_url(converter):
        """
        Extract base URL from the converter.

        :param converter: given service
        :return: base URL
        """
        url = urlparse(list(converter.services.values())[0])
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
        except (requests.exceptions.ConnectionError, TimeoutError):
            return False

    def run(self):
        """
        Main loop of the Monitor thread.

        Monitor checks if GET on base URL of every service give status code 200.
        Such a service is considered available.
        This is checked periodically to always have up-to-date information.
        """
        while not self.stop_request.isSet():
            for converter in self.converters.values():
                url = self.get_base_url(converter)
                converter.is_available = self.check_service(url)
            time.sleep(10)

    def join(self, timeout=None):
        self.stop_request.set()
