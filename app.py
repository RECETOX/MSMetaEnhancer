import asyncio
import aiohttp

from libs.Annotator import Annotator
from libs.utils.Errors import UnknownService
from libs.services import *


class Application:
    def __init__(self, services):
        # check if services exist
        for service in services:
            try:
                eval(service)
            except NameError:
                raise UnknownService(f'Service {service} unknown.')
        self.services = services

    async def annotate_spectra(self, spectra, jobs=None, batch_size=10, repeat=False):
        results = []
        async with aiohttp.ClientSession() as session:
            services = {service: eval(service)(session) for service in self.services}
            annotator = Annotator(services)

            # create all possible jobs if not given
            if not jobs:
                jobs = annotator.get_all_conversions()

            for size in range(len(spectra.spectrums) // batch_size + 1):
                results += await asyncio.gather(*[annotator.annotate(spectra, jobs, repeat) for spectra in
                                                  spectra.spectrums[size * batch_size:(size + 1) * batch_size]])

        return results
