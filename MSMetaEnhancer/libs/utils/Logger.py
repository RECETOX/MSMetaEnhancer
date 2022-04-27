import logging
from datetime import datetime
from typing import List

from MSMetaEnhancer.libs.utils.LogRecord import LogRecord
from MSMetaEnhancer.libs.utils.Metrics import Metrics
from MSMetaEnhancer.libs.utils.Job import Job


class Logger:
    def __init__(self):
        self.logger = logging.getLogger('log')
        self.logger.setLevel('INFO')

        # statistical values
        self.metrics = Metrics()

        self.LEVELS = {'error': 1, 'warning': 2, 'info': 3}

        self.log_level = 3

    def setup(self, log_level: int, log_file: str):
        """Initialize log level and log file.

        Args:
            log_level (int): Log level to set ['error': 1, 'warning': 2, 'info': 3]
            log_file (str): Path to log file.
        """
        self.log_level = self.LEVELS[log_level]
        self.add_filehandler(log_file)

    def add_filehandler(self, file_name: str = None):
        """Initialize filehandler for logfile.

        Args:
            file_name (str, optional): Log filename. Defaults to None.
        """
        if file_name is None:
            file_name = datetime.now().strftime('MSMetaEnhancer_%Y%m%d%H%M%S.log')

        filehandler_dbg = logging.FileHandler(file_name, mode='w')
        filehandler_dbg.setLevel('DEBUG')

        streamformatter = logging.Formatter(fmt='%(levelname)s: %(message)s')

        # Apply formatters to handlers
        filehandler_dbg.setFormatter(streamformatter)

        # Add handlers to logger
        self.logger.addHandler(filehandler_dbg)

    def set_target_attributes(self, jobs: List[Job], length: int):
        """
        Gather all target attributes from specified jobs

        :param jobs: given list of jobs
        :param length: number of analysed spectra
        """
        target_attributes = {job.target for job in jobs}
        self.metrics.set_params(target_attributes, length)

    def add_logs(self, log_record: LogRecord):
        """
        Flush logs to log file.

        :param log_record: log record to write and format to file
        """
        message = log_record.format_log(self.log_level)
        if message:
            self.logger.warning(message)

    def add_coverage_before(self, metadata_keys: List[str]):
        """
        Increase counts of already present attributes.

        :param metadata_keys: present attributes
        """
        self.metrics.update_before_annotation(metadata_keys)

    def add_coverage_after(self, metadata_keys: List[str]):
        """
        Increase counts of annotated attributes

        :param metadata_keys: discovered attributes
        """
        self.metrics.update_after_annotation(metadata_keys)

    def write_metrics(self):
        """
        Write obtained statistical values.
        """
        self.logger.info(str(self.metrics))
