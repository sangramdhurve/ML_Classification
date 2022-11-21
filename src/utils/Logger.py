import os
import sys
import time
import logging
try:
    from config.common_config import options
except ModuleNotFoundError:
    from ...config.common_config import options

from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler


class CustomFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super(CustomFormatter, self).formatException(exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        message = record.msg
        lines = []
        for line in message.split('\n'):
            record.msg = line
            formatted_msg = super(CustomFormatter, self).format(record)
            lines.append(formatted_msg)

        s = "\n".join(lines)
        return s


class Logger:
    def __init__(self, log_file_name: str):
        self.__log_file_path = os.path.join(options["log_path"], log_file_name)
        self.__formatter = CustomFormatter("%(asctime)s.%(msecs)03d %(levelname)s %(name)s %(filename)s:%(lineno)s "
                                           "%(message)s",
                                           '%Y-%m-%d %H:%M:%S')

        self.__logger = logging.getLogger("Rotating Log")
        self.__logger.setLevel(logging.INFO)

    def create_size_rotating_log(self, max_bytes, backup_count=10) -> logging:
        # add a rotating handler
        path = self.__log_file_path
        handler = RotatingFileHandler(path, maxBytes=max_bytes,
                                      backupCount=backup_count)
        handler.setFormatter(self.__formatter)
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(self.__formatter)

        self.__logger.addHandler(handler)
        self.__logger.addHandler(sh)
        return self.__logger

    def create_time_rotating_log(self, when="minute", interval=1, backup_count=10) -> logging:
        valid_when_params = {"minute": "m", "second": "s", "hour": "h", "day": "d", "midnight": "MIDNIGHT"}
        when = valid_when_params.get(when)
        if when is None:
            raise Exception("invalid when param")

        path = self.__log_file_path

        handler = TimedRotatingFileHandler(path,
                                           when=when,
                                           interval=interval,
                                           backupCount=backup_count)
        handler.setFormatter(self.__formatter)

        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(self.__formatter)

        self.__logger.addHandler(handler)
        self.__logger.addHandler(sh)
        return self.__logger


if __name__ == '__main__':
    logger_handler = Logger("test.log")
    logger = logger_handler.create_time_rotating_log(when="second")
    for i in range(10):
        logger.info("This is test log line %s" % i)
        time.sleep(2)
