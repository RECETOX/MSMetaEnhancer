import logging
from asyncio import Queue


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
        self.target_attributes = set()
        self.attribute_discovery_rate = 1

    def set_target_attributes(self, jobs):
        """
        Gather all target attributes from specified jobs

        :param jobs: given list of jobs
        """
        self.target_attributes = {job.target for job in jobs}

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

    def process_log(self, log):
        """
        Pretty format single log and compute global attribute discovery rate

        :param log: given log
        :return: level and formatted message
        """
        if isinstance(log, LogWarning):
            self.attribute_discovery_rate = (self.attribute_discovery_rate + log.attribute_discovery_rate) / 2
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

        self.logger.info(f'Job success rate: {self.passes}/{self.passes + self.fails} '
                         f'({self.passes/(self.passes + self.fails)}%) \n'
                         f'Attribute discovery rate: {self.attribute_discovery_rate*100}%'
                         '\n' + '='*30 + '\n')
        self.write_logs(logs)


class LogWarning:
    def __init__(self, metadata, target_attributes):
        self.metadata = metadata
        self.target_attributes = target_attributes

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

    def compute_success_rate(self):
        """
        Compute general success rate based on ratio of found attributes to requested attributes
        """
        self.attribute_discovery_rate = len(self.metadata.keys() & self.target_attributes)/len(self.target_attributes)
