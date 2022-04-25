from datetime import datetime
import logging

from MSMetaEnhancer.libs.utils.Metrics import Metrics


class Logger:
    def __init__(self):
        self.logger = logging.getLogger('log')
        self.log_level = 'INFO'
        self.logger.setLevel(self.log_level)

        # statistical values
        self.metrics = Metrics()

        self.LEVELS = {'warning': 2, 'info': 1}

        # to avoid stacking the same errors
        self.last_error = ''

    def setup(self, log_level, log_file):
        self.log_level = log_level
        self.logger.setLevel(self.LEVELS[self.log_level])
        self.add_filehandler(log_file)

    def add_filehandler(self, file_name):
        if file_name is None:
            file_name = datetime.now().strftime('MSMetaEnhancer_%Y%m%d%H%M%S.log')

        filehandler_dbg = logging.FileHandler(file_name, mode='w')
        filehandler_dbg.setLevel('DEBUG')

        streamformatter = logging.Formatter(fmt='%(levelname)s: %(message)s')

        # Apply formatters to handlers
        filehandler_dbg.setFormatter(streamformatter)

        # Add handlers to logger
        self.logger.addHandler(filehandler_dbg)

    def set_target_attributes(self, jobs, length):
        """
        Gather all target attributes from specified jobs

        :param jobs: given list of jobs
        :param length: number of analysed spectra
        """
        target_attributes = {job.target for job in jobs}
        self.metrics.set_params(target_attributes, length)

    def error(self, exc: Exception):
        """
        Log an error message.

        Store the last error to avoid stacking the same errors.

        :param exc: given Exception
        """
        if str(exc) != self.last_error:
            message = self.process_log(str(exc))
            self.logger.error(message)
            self.last_error = str(exc)

    def add_warning(self, warning):
        """
        Logs given exception as a Warning.

        :param warning: LogWarning
        """
        self.last_error = ''
        message = self.process_log(warning)
        if message:
            self.logger.warning(message)

    def add_coverage_before(self, metadata_keys):
        """
        Increase counts of already present attributes.

        :param metadata_keys: present attributes
        """
        self.metrics.update_before_annotation(metadata_keys)

    def add_coverage_after(self, metadata_keys):
        """
        Increase counts of annotated attributes

        :param metadata_keys: discovered attributes
        """
        self.metrics.update_after_annotation(metadata_keys)

    def process_log(self, log):
        """
        Pretty format single log and compute global attribute discovery rate

        :param log: given log
        :return: level and formatted message
        """
        if isinstance(log, LogWarning):
            message = f'Errors related to metadata:\n\n{log.metadata}\n\n'

            filtered_warnings = [w['msg'] for w in log.warnings if w['level'] >= self.LEVELS[self.log_level]]
            if filtered_warnings:
                for warning in filtered_warnings:
                    message += f'{warning}\n'
            else:
                return None
            return f'{message}\n'
        else:
            return f'{log}\n'

    def write_metrics(self):
        """
        Write obtained statistical values.
        """
        self.logger.info(str(self.metrics))


class LogWarning:
    def __init__(self, metadata):
        self.metadata = metadata
        self.warnings = []

    def add_warning(self, exc: Exception):
        """
        Logs given exception as a Warning.

        :param exc: given exception
        """
        self.warnings.append({'level': 2, 'msg': f'-> {exc}'})

    def add_info(self, info):
        """
        Logs given info.

        :param info: given info message
        """
        self.warnings.append({'level': 1, 'msg': f'-> {info}'})
