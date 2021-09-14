from datetime import datetime
import logging
from asyncio import Queue

from pyMSPannotator.libs.utils.Metrics import Metrics


class Logger:
    def __init__(self):
        self.logger = logging.getLogger('log')
        self.logger.setLevel('INFO')

        # to store logs before emitting them to a file
        self.queue = Queue()

        # statistical values
        self.metrics = Metrics()

        self.LEVELS = {'warning': 2, 'info': 1}

        # to avoid stacking the same errors
        self.last_error = ''

    def add_filehandler(self, file_name):
        if file_name is None:
            file_name = datetime.now().strftime('MSPannotator_%Y%m%d%H%M%S.log')

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
            self.queue.put_nowait(f'{exc}')
            self.last_error = str(exc)

    def add_warning(self, warning):
        """
        Logs given exception as a Warning.
        Increases number of failed jobs.

        :param warning: LogWarning
        """
        self.last_error = ''
        self.queue.put_nowait(warning)

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

    def write_logs(self, logs):
        """
        Writes all logs from queue.
        """
        for level, log in logs:
            if level == 'warning':
                self.logger.warning(log)
            else:
                self.logger.error(log)

    def process_log(self, log, log_level):
        """
        Pretty format single log and compute global attribute discovery rate

        :param log: given log
        :param log_level: level of issues to be included in log
        :return: level and formatted message
        """
        if isinstance(log, LogWarning):
            message = f'Errors related to metadata:\n\n{log.metadata}\n\n'

            filtered_warnings = [w['msg'] for w in log.warnings if w['level'] >= self.LEVELS[log_level]]
            if filtered_warnings:
                for warning in filtered_warnings:
                    message += f'{warning}\n'
            else:
                return None
            return 'warning', f'{message}\n'
        else:
            return 'error', f'{log}\n'

    def write_log(self, log_level, log_file):
        """
        Preprocess all logs and write obtained statistical values.
        """
        logs = []
        while not self.queue.empty():
            log = self.queue.get_nowait()
            processed_log = self.process_log(log, log_level)
            if processed_log:
                logs.append(processed_log)

        self.add_filehandler(log_file)

        # write obtained metrics
        self.logger.info(str(self.metrics))
        self.write_logs(logs)


class LogWarning:
    def __init__(self, metadata):
        self.metadata = metadata
        self.warnings = []

    def add_warning(self, exc: Exception):
        """
        Logs given exception as a Warning.
        Increases number of failed jobs.

        :param exc: given exception
        """
        self.warnings.append({'level': 2, 'msg': f'-> {exc}'})

    def add_info(self, info):
        """
        Logs given info.

        :param info: given info message
        """
        self.warnings.append({'level': 1, 'msg': f'-> {info}'})
