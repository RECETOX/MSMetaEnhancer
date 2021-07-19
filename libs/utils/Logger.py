import logging
from asyncio import Queue
from tabulate import tabulate


class Logger:
    def __init__(self):
        self.logger = logging.getLogger('log')
        self.logger.setLevel('INFO')

        filehandler_dbg = logging.FileHandler('MSPannotator.log', mode='w')
        filehandler_dbg.setLevel('DEBUG')

        streamformatter = logging.Formatter(fmt='%(levelname)s: %(message)s')

        # Apply formatters to handlers
        filehandler_dbg.setFormatter(streamformatter)

        # Add handlers to logger
        self.logger.addHandler(filehandler_dbg)

        # to store logs before emitting them to a file
        self.queue = Queue()

        # statistical values
        self.passes = 0
        self.fails = 0
        self.attribute_discovery_rates = dict()
        self.base_coverage = dict()

    def set_target_attributes(self, jobs):
        """
        Gather all target attributes from specified jobs

        :param jobs: given list of jobs
        """
        target_attributes = {job.target for job in jobs}
        self.attribute_discovery_rates = {key: 0 for key in target_attributes}
        self.base_coverage = dict(self.attribute_discovery_rates)

    def error(self, exc: Exception):
        """
        Log an error message.

        :param exc: given Exception
        """
        self.queue.put_nowait(f'{exc}')

    def add_warning(self, warning):
        """
        Logs given exception as a Warning.
        Increases number of failed jobs.

        :param warning: LogWarning
        """
        self.queue.put_nowait(warning)

    def add_success(self):
        """
        Increase number of passed jobs.
        """
        self.passes += 1

    def add_fails(self, number):
        """
        Increase number of failed jobs.
        """
        self.fails += number

    def write_logs(self, logs):
        """
        Writes all logs from queue.
        """
        for level, log in logs:
            if level == 'warning':
                self.logger.warning(log)
            else:
                self.logger.error(log)

    def update_discovery_rates(self, log):
        for key in log.target_attributes_success.keys():
            self.attribute_discovery_rates[key] = (self.attribute_discovery_rates[key] +
                                                   log.target_attributes_success[key])/2
            self.base_coverage[key] = (self.base_coverage[key] +
                                       log.base_coverage[key])/2

    def process_log(self, log):
        """
        Pretty format single log and compute global attribute discovery rate

        :param log: given log
        :return: level and formatted message
        """
        if isinstance(log, LogWarning):
            self.update_discovery_rates(log)
            message = f'Errors related to metadata:\n\n{log.metadata}\n\n'
            for warning in log.warnings:
                message += f'{warning}\n'
            return 'warning', f'{message}\n'
        else:
            return 'error', '-'*30 + f'\n{log}\n' + '-'*30

    def log_statistics(self):
        """
        Preprocess all logs and write obtained statistical values.
        """
        logs = []
        while not self.queue.empty():
            log = self.queue.get_nowait()
            if isinstance(log, LogWarning):
                logs.append(self.process_log(log))

        table = tabulate([[key, f'{self.base_coverage[key]*100}%', f'{self.attribute_discovery_rates[key]*100}%']
                          for key in self.attribute_discovery_rates],
                         headers=['Target\nattribute', 'Coverage\nbefore', 'Coverage\nafter'])

        self.logger.info(f'Job success rate: {self.passes}/{self.passes + self.fails} '
                         f'({self.passes/(self.passes + self.fails)}%) \n'
                         f'Attribute discovery rates:\n\n{table}'
                         '\n' + '='*50 + '\n')
        self.write_logs(logs)


class LogWarning:
    def __init__(self, metadata, attribute_discovery_rates):
        self.metadata = metadata
        self.target_attributes_success = dict(attribute_discovery_rates)
        self.base_coverage = {key: 1 if key in self.metadata.keys() else 0 for key in attribute_discovery_rates.keys()}

        self.fails = 0
        self.warnings = []
        self.attribute_discovery_rate = 0

    def add_warning(self, exc: Exception):
        """
        Logs given exception as a Warning.
        Increases number of failed jobs.

        :param exc: given exception
        """
        self.fails += 1
        self.warnings.append(f'-> {exc}')

    def compute_success_rate(self, metadata):
        """
        Compute general success rate based on ratio of found attributes to requested attributes
        """
        for key in self.target_attributes_success.keys():
            self.target_attributes_success[key] = 1 if key in metadata.keys() else 0
