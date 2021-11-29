import asyncio
import aiohttp

from MSMetaEnhancer.libs.Annotator import Annotator
from MSMetaEnhancer.libs.Curator import Curator
from MSMetaEnhancer.libs.Spectra import Spectra
from MSMetaEnhancer.libs.utils import logger
from MSMetaEnhancer.libs.utils.Errors import UnknownService, UnknownSpectraFormat
from MSMetaEnhancer.libs.utils.Job import convert_to_jobs
from MSMetaEnhancer.libs.services import *


class Application:
    def __init__(self, log_level='warning', log_file=None):
        self.log_level = log_level
        self.log_file = log_file
        self.spectra = Spectra()

    @staticmethod
    def validate_services(services):
        """
        Check if services do exist.
        Raises UnknownService if a service does not exist.

        :param services: given list of services names
        """
        for service in services:
            try:
                eval(service)
            except NameError:
                raise UnknownService(f'Service {service} unknown.')

    def load_spectra(self, filename, file_format):
        """
        High level method to load Spectra data from given file.

        :param filename: path to source spectra file
        :param file_format: format of spectra
        """
        try:
            getattr(self.spectra, f'load_from_{file_format}')(filename)
        except AttributeError:
            raise UnknownSpectraFormat(f'Format {file_format} not supported.')

    def save_spectra(self, filename, file_format):
        """
        High level method to save Spectra data to given file.

        :param filename: path to target file
        :param file_format: desired format of spectra
        """
        try:
            getattr(self.spectra, f'save_to_{file_format}')(filename)
        except Exception:
            raise UnknownSpectraFormat(f'Format {file_format} not supported.')

    def curate_spectra(self):
        """
        Updates current Spectra data by curation process.
        """
        self.spectra = Curator().curate_spectra(self.spectra)

    def get_service_conversions(self, service):
        """
        Method to get all conversions for given service.

        :param service: given Converter subclass
        :return: a list of available conversion functions
        """
        return service.get_conversions()

    async def annotate_spectra(self, services, jobs=None, repeat=False):
        """
        Annotates current Spectra data by specified jobs.
         Used services must be specified.
         Jobs do not have to be given, all available jobs will be executed instead.

        :param services: given list of services names
        :param jobs: list specifying jobs to be executed
        :param repeat: if some metadata was added, all jobs are executed again
        """
        async with aiohttp.ClientSession() as session:
            self.validate_services(services)
            services = {service: eval(service)(session) for service in services}
            annotator = Annotator(services)

            # create all possible jobs if not given
            if not jobs:
                jobs = []
                for service in services.values():
                    jobs += self.get_service_conversions(service)
            jobs = convert_to_jobs(jobs)

            logger.set_target_attributes(jobs, len(self.spectra.spectrums))

            results = await asyncio.gather(*[annotator.annotate(spectra, jobs, repeat)
                                             for spectra in self.spectra.spectrums])

        self.spectra.spectrums = results
        logger.write_log(self.log_level, self.log_file)
