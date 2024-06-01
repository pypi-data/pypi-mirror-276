import logging
from pythonjsonlogger import jsonlogger
from sys import stdout

from ..config.singleton import singleton
from ..dig_ass.db import make_session_id


class JsonFormatter(jsonlogger.JsonFormatter):
    pass
    ####
    # additional json formatting possible
    ####

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.json_ensure_ascii = False


@singleton
class LoggerSingleton:
    def __init__(self, loggerConfig) -> None:
        self.logger = logging.getLogger(name=loggerConfig['name'])
        self.logger.setLevel(loggerConfig['level_common'])

        logFilePath = f'{loggerConfig["file_dir"]}/{loggerConfig["name"]}_{make_session_id()}.json'
        fileHandler = logging.FileHandler(logFilePath, mode='a')
        jsonFormatter = JsonFormatter(loggerConfig['format_file'])
        fileHandler.setFormatter(jsonFormatter)
        fileHandler.setLevel(loggerConfig['level_file_handler'])

        stdoutHandler = logging.StreamHandler(stdout)
        stdoutHandler.setFormatter(logging.Formatter(loggerConfig['format_stdout']))
        stdoutHandler.setLevel(loggerConfig['level_stdout_handler'])

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(stdoutHandler)

    def get(self):
        return self.logger
