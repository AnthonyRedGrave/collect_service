import logging


class InformationFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < 40
