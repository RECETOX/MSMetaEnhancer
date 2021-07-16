import logging


class Logger:
    def __init__(self):
        self.logger = logging.getLogger('log')
        self.logger.setLevel('WARNING')

        filehandler_dbg = logging.FileHandler('MSPannotator.log', mode='w')
        filehandler_dbg.setLevel('DEBUG')

        streamformatter = logging.Formatter(fmt='%(levelname)s: %(message)s')

        # Apply formatters to handlers
        filehandler_dbg.setFormatter(streamformatter)

        # Add handlers to logger
        self.logger.addHandler(filehandler_dbg)

    def warning(self, exc: Exception, message=None):
        self.logger.warning(f'{exc}\nMetadata: {message}\n' if message else f'{exc}\n')
