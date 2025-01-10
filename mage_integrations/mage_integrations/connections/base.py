from typing import Dict

from mage_integrations.utils.logger import Logger


class Connection:
    def __init__(self, verbose: int = 1, **kwargs):
        self.logger = Logger(caller=self, verbose=verbose)
        self.verbose = verbose

    def build_tags(self, **kwargs):
        return self.logger.build_tags(**kwargs)

    def error(self, message, tags:Dict=None, **kwargs):
        self.logger.error(message, tags, **kwargs)

    def exception(self, message, tags:Dict=None, **kwargs):
        self.logger.exception(message, tags, **kwargs)

    def info(self, message, tags:Dict=None, **kwargs):
        self.logger.info(message, tags, **kwargs)
