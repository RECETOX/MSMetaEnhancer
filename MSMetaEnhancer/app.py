import asyncio

import aiohttp

from MSMetaEnhancer.libs.Annotator import Annotator
from MSMetaEnhancer.libs.Converter import Converter
from MSMetaEnhancer.libs.Curator import Curator
from MSMetaEnhancer.libs.data import Spectra, DataFrame
from MSMetaEnhancer.libs.utils import logger
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from MSMetaEnhancer.libs.utils.Errors import UnknownSpectraFormat
from MSMetaEnhancer.libs.utils.Job import convert_to_jobs
from MSMetaEnhancer.libs.utils.Monitor import Monitor


class Application:
    def __init__(self, log_level='info', log_file=None):
        self.data = None
        logger.setup(log_level, log_file)

    def load_data(self, filename, file_format):
        """
        High level method to load Spectra data from given file.

        :param filename: path to source spectra file
        :param file_format: format of spectra
        """
        if file_format in ['msp']:
            self.data = Spectra()
        elif file_format in ['csv']:
            self.data = DataFrame()
        else:
            raise UnknownSpectraFormat(f'Format {file_format} not supported.')
        getattr(self.data, f'load_from_{file_format}')(filename)

    def save_data(self, filename, file_format):
        """
        High level method to save Spectra data to given file.

        :param filename: path to target file
        :param file_format: desired format of spectra
        """
        try:
            getattr(self.data, f'save_to_{file_format}')(filename)
        except Exception:
            raise UnknownSpectraFormat(f'Format {file_format} not supported.')

    def curate_metadata(self):
        """
        Updates metadata by curation process.

        This includes e.g. normalisation of CAS numbers.
        """
        curated_metadata = Curator().curate_metadata(self.data.get_metadata())
        self.data.fuse_metadata(curated_metadata)

    async def annotate_spectra(self, converters, jobs=None, repeat=False, monitor=Monitor(), annotator=Annotator()):
        """
        Annotates current Spectra data by specified jobs.

        Used converters must be specified.
        Jobs do not have to be given, all available jobs will be executed instead.

        :param converters: given list of converters names
        :param jobs: list specifying jobs to be executed
        :param repeat: if some metadata was added, all jobs are executed again
        :param monitor: given Monitor object to observe status of services
        :param annotator: given Annotator object to run the actual annotation
        """
        async with aiohttp.ClientSession() as session:
            builder = ConverterBuilder()
            builder.validate_converters(converters)
            converters, web_converters = builder.build_converters(session, converters)

            annotator.set_converters(converters)
            monitor.set_converters(web_converters)

            # start converters status checker and wait for first status
            try:
                monitor.start()
                monitor.first_check.wait()

                # create all possible jobs if not given
                if not jobs:
                    jobs = []
                    converter: Converter
                    for converter in converters.values():
                        jobs += converter.get_conversion_functions()
                jobs = convert_to_jobs(jobs)

                metadata_list = self.data.get_metadata()

                logger.set_target_attributes(jobs, len(metadata_list))

                results = await asyncio.gather(*[annotator.annotate(metadata, jobs, repeat)
                                                 for metadata in metadata_list])
            finally:
                monitor.join()

        self.data.fuse_metadata(results)
        logger.write_metrics()
