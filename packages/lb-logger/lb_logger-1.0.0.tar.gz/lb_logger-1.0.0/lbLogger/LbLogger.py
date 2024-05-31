# -*- coding: utf-8 -*-
__author__ = 'Lucas Barros'
__version__ = 2.0
__maintainer__ = 'Lucas Barros'
__email__ = 'lucas.barros@hitechnologies.com.br'
__status__ = 'Production'


import logging


class LbLogger:

    def __init__(self):
        self.__logger: logging = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s -- %(levelname)s-- %(funcName)s -- %(message)s --', level=logging.INFO,
                            datefmt='%Y-%m-%d %H:%M:%S', )

    def debug(self, message: str) -> None:
        """
        Function for return debug log
        :param message: Message for log with debug
        :return: None
        """
        self.__logger.debug(message)

    def info(self, message: str) -> None:
        """
        Function for return info log
        :param message: Message for log with info
        :return: None
        """
        self.__logger.info(message)

    def warning(self, message: str) -> None:
        """
        Function for return warning log
        :param message: Message for log with warning
        :return: None
        """
        self.__logger.warning(message)

    def error(self, message: str) -> None:
        """
        Function for return error log
        :param message: Message for log with error
        :return: None
        """
        self.__logger.error(message)

    def critical(self, message: str) -> None:
        """
        Function for return critical log
        :param message: Message for log with critical
        :return: None
        """
        self.__logger.critical(message)
