import logging


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

    def warning(self, exc: Exception, metadata=None):
        """
        Logs given exception as a Warning.
        Increases number of failed jobs.

        :param exc: given exception
        :param metadata: additional metadata
        """
        self.fails += 1
        self.logger.warning(f'{exc}\nMetadata: {metadata}\n' if metadata else f'{exc}\n')

    def info(self, message):
        """
        Logs given message as a Warning.

        :param message: message to be logged
        """
        self.logger.warning(message + '\n')

    def success(self):
        """
        Increase number of passed jobs.
        """
        self.passes += 1

    def compute_success_rate(self, metadata):
        """
        Compute success rate of attribute discovery.

        Based on ratio of found attributes to target attributes.

        :param metadata: found metadata (includes also already present attributes)
        """
        rate = len(metadata.keys() & self.target_attributes)/len(self.target_attributes)
        self.attribute_discovery_rate = (self.attribute_discovery_rate + rate)/2

    def log_statistics(self):
        """
        Log obtained statistical values as Info.
        """
        self.logger.info(f'Job success rate: {self.passes}/{self.passes + self.fails} '
                         f'({self.passes/(self.passes + self.fails)}%)')
        self.logger.info(f'Attribute discovery rate: {self.attribute_discovery_rate*100}%')
