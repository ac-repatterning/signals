"""Module setup.py"""
import sys

import config
import src.functions.cache
import src.functions.directories


class Setup:
    """
    Description
    -----------

    Sets up local environments
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__directories = src.functions.directories.Directories()

    def __local(self) -> bool:
        """

        :return:
        """

        self.__directories.cleanup(path=self.__configurations.warehouse)

        return self.__directories.create(path=self.__configurations.warning_)

    def exc(self) -> bool:
        """

        :return:
        """

        if self.__local():
            return True

        src.functions.cache.Cache().exc()

        sys.exit('Error: Unable to clear and re-create the local warehouse')
