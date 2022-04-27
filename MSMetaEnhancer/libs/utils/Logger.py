from datetime import datetime
import logging

from MSMetaEnhancer.libs.utils.Metrics import Metrics


class Logger:
    def __init__(self):
        self.logger = logging.getLogger('log')
        self.logger.setLevel('INFO')

        # statistical values
        self.metrics = Metrics()

        self.LEVELS = {'error': 1, 'warning': 2, 'info': 3}

        self.log_level = 3

    def setup(self, log_level, log_file):
        self.log_level = self.LEVELS[log_level]
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

    def add_logs(self, log_record):
        """
        Flush logs to log file.
        """
        message = log_record.format_log(self.log_level)
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

    def write_metrics(self):
        """
        Write obtained statistical values.
        """
        self.logger.info(str(self.metrics))


class LogRecord:
    def __init__(self, metadata):
        self.metadata = metadata
        self.logs = []

    def format_log(self, level):
        message = f'Issues related to metadata:\n\n{self.metadata}\n\n'
        filtered_logs = [log['msg'] for log in self.logs if level >= log['level']]
        if filtered_logs:
            for log in filtered_logs:
                message += f'{log}\n'
        else:
            return None
        return f'{message}\n'

    def update(self, exc, job, level):
        """
        Process given log record.

        :param exc: exception
        :param job: related job
        :param level: log level
        """
        self.logs.append({'level': level, 'msg': f'-> {type(exc).__name__} - {job}:\n{exc}'})
