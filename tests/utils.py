import aiohttp
from threading import Thread, Event
import time


async def wrap_with_session(converter, method, args):
    async with aiohttp.ClientSession() as session:
        converter = converter(session)
        return await getattr(converter, method)(*args)


class FakeMonitor(Thread):
    """
    Fake Monitor to test basic functionality.
    """
    def __init__(self):
        super(FakeMonitor, self).__init__()
        self.converters = None
        self.stop_request = Event()
        self.first_check = Event()

    def set_converters(self, converters):
        self.converters = converters

    def run(self):
        while not self.stop_request.is_set():
            self.first_check.set()
            time.sleep(10)

    def join(self, timeout=None):
        self.stop_request.set()


class FakeAnnotator:
    """
    Fake Annotator to test basic functionality.
    """
    def __init__(self, raise_exception=False):
        self.converters = None
        self.raise_exception = raise_exception

    def set_converters(self, converters):
        self.converters = converters

    async def annotate(self, spectra, jobs, repeat=False):
        if self.raise_exception:
            raise Exception
        else:
            time.sleep(1)
            return spectra
