import asyncio

import aiohttp

from MSMetaEnhancer.libs.Annotator import Annotator
from MSMetaEnhancer.libs.Converter import Converter
from MSMetaEnhancer.libs.Curator import Curator
from MSMetaEnhancer.libs.data import Spectra, DataFrame
from MSMetaEnhancer.libs.utils import logger
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from MSMetaEnhancer.libs.utils.Errors import UnknownFileFormat
from MSMetaEnhancer.libs.utils.Job import convert_to_jobs
from MSMetaEnhancer.libs.utils.Monitor import Monitor


class Application:
    def __init__(self, log_level="info", log_file=None):
        self.data = None
        logger.setup(log_level, log_file)

    def load_data(self, filename, file_format):
        """
        High level method to load Spectra data from given file.

        :param filename: path to source spectra file
        :param file_format: format of spectra
        """
        if file_format in ["msp", "mgf", "json"]:
            self.data = Spectra()
        elif file_format in ["csv", "tsv", "tabular", "xlsx"]:
            self.data = DataFrame()
        else:
            raise UnknownFileFormat(f"Format {file_format} not supported.")
        self.data.load_data(filename, file_format)

    def load_dataframe(self, df, column_mapping=None):
        """
        High level method to use a pandas DataFrame as data.

        :param df: pandas DataFrame with metadata (one row per record)
        :param column_mapping: optional dictionary {original name: new name}
                               to rename columns to the names used by the library
        """
        self.data = DataFrame()
        self.data.load_dataframe(df, column_mapping)

    def get_dataframe(self, column_mapping=None):
        """
        Returns current data as a pandas DataFrame.

        :param column_mapping: optional dictionary {current name: new name}
        """
        if not isinstance(self.data, DataFrame):
            raise TypeError("Current data is not stored as a DataFrame.")
        return self.data.get_dataframe(column_mapping)

    def save_data(self, filename, file_format):
        """
        High level method to save Spectra data to given file.

        :param filename: path to target file
        :param file_format: desired format of spectra
        """
        self.data.save_data(filename, file_format)

    def curate_metadata(self):
        """
        Updates metadata by curation process.

        This includes e.g. normalisation of CAS numbers.
        """
        curated_metadata = Curator().curate_metadata(self.data.get_metadata())
        self.data.fuse_metadata(curated_metadata)

    async def annotate_spectra(
        self,
        converters,
        jobs=None,
        repeat: bool = False,
        monitor: Monitor = Monitor(),
        annotator: Annotator = Annotator(),
    ):
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
            compute_converters, web_converters = builder.build_converters(
                session, converters
            )

            annotator.set_converters(compute_converters | web_converters)
            monitor.set_converters(web_converters)

            # start converters status checker and wait for first status
            try:
                if not monitor.is_alive():
                    monitor.start()
                monitor.first_check.wait()

                # create all possible jobs if not given
                if not jobs:
                    jobs = []
                    converter: Converter
                    for converter in annotator.converters.values():
                        jobs += converter.get_conversion_functions()
                jobs = convert_to_jobs(jobs)

                metadata_list = self.data.get_metadata()

                logger.set_target_attributes(jobs, len(metadata_list))

                results = await asyncio.gather(
                    *[
                        annotator.annotate(metadata, jobs, repeat)
                        for metadata in metadata_list
                    ]
                )
            finally:
                monitor.join()

        self.data.fuse_metadata(results)
        logger.write_metrics()
