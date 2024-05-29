# -*- coding: utf-8 -*
# #!/usr/bin/python3

# How to use: from ppw_util.log import Log
import logging


class Log:

    def __init__(self, log_path: str, format: str = "%(asctime)s %(message)s", level: int = logging.INFO):

        handlers = [logging.StreamHandler()]
        if log_path is not None:
            handlers.append(logging.FileHandler(log_path))

        logging.basicConfig(level=level,
                            format=format,
                            handlers=handlers)

    def info(self, message: str):
        logging.info(message)

    def debug(self, message: str):
        logging.debug(message)

    def warning(self, message: str):
        logging.warning(message)

    def error(self, message: str):
        logging.error(message)
