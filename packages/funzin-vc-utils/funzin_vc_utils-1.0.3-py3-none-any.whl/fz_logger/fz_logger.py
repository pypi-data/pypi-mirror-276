import logging
import os
import sys
from datetime import datetime
from logging import handlers

import colorlog


class Logger:
    def __init__(self, config:dict):
        self.save_path = config["logger"]["save_path"]
        if self.save_path is not None:
            save = True
            os.makedirs(self.save_path, exist_ok=True)
        else:
            save = False

        self.settings = {
            "LEVEL": self.lookup_table(config["logger"]["level"]),
            "FILENAME": self.__class__.__module__,
            "MAYBYTES": 15 * 1024 * 1024,
            "BACKUPCOUNT": 100,
            "FORMAT": "%(log_color)s[%(levelname)-8s]%(reset)s [%(name)s]: %(module)s:%(lineno)d:  %(message)s",
            "SAVE": save,
        }

        self.logger_initialize()

    def lookup_table(self, idx):
        lvl = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

        return lvl.get(idx, "INFO")

    def logger_initialize(self):
        self.logger = colorlog.getLogger(self.settings["FILENAME"])
        self.logger.setLevel(self.settings["LEVEL"])
        if len(self.logger.handlers) > 0:
            return self.logger
        stream_formatter = colorlog.ColoredFormatter(self.settings["FORMAT"])
        stream_handler = colorlog.StreamHandler(sys.stdout)
        now_date_time = "{:%Y-%m-%d}".format(datetime.now())
        stream_handler.setFormatter(stream_formatter)
        self.logger.addHandler(stream_handler)
        if self.settings["SAVE"]:
            file_formatter = logging.Formatter(
                "%(asctime)s [%(levelname)-8s] [%(name)s]: %(module)s:%(lineno)d: %(message)s"
            )
            file_handler = handlers.TimedRotatingFileHandler(
                os.path.abspath(f"{self.save_path}/{now_date_time}-{self.settings['FILENAME']}.log"),
                when="midnight",
                interval=1,
                backupCount=self.settings["BACKUPCOUNT"],
                encoding="utf-8",
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)


if __name__ == "__main__":
    level = "INFO"
    log = Logger(
        level=level,
        save_path="logs",
    )
    logger = log.logger
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
