from MSMetaEnhancer.libs.utils.Job import Job


class LogRecord:
    def __init__(self, metadata):
        self.metadata = metadata
        self.logs = []

    def format_log(self, level: str) -> str:
        """Format log message according to level.

        Args:
            level (str): Log level to use for formatting.

        Returns:
            str: Formatted log message
        """
        message = f'Issues related to metadata:\n\n{self.metadata}\n\n'
        filtered_logs = [log['msg'] for log in self.logs if level >= log['level']]
        if filtered_logs:
            for log in filtered_logs:
                message += f'{log}\n'
        else:
            return None
        return f'{message}\n'

    def update(self, exc: Exception, job: Job, level: str):
        """
        Process given log record.

        :param exc: exception
        :param job: related job
        :param level: log level
        """
        self.logs.append({'level': level, 'msg': f'-> {type(exc).__name__} - {job}:\n{exc}'})
