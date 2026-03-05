"""Module cartography/times.py"""
import logging
import os

import geopandas

import config
import src.functions.objects


class Times:
    """
    The start & end times vis-à-vis a weather warning period.
    """

    def __init__(self, arguments: dict):
        """

        :param arguments:
        """

        self.__arguments = arguments

        # Configurations
        self.__configurations = config.Config()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.__logger = logging.getLogger(__name__)

    def exc(self, data: geopandas.GeoDataFrame):
        """

        :param data: About the latest weather warning, and the stations therein.
        :return:
        """

        # The time limits
        nodes = {
            'starting': data['starting'].min().strftime('%Y-%m-%d %H:%M:%S'),
            'ending': data['ending'].max().strftime('%Y-%m-%d %H:%M:%S'),
            'testing': self.__arguments.get('testing')
        }
        self.__logger.info(nodes)

        # Storage
        path = os.path.join(self.__configurations.warning_, 'times.json')

        # Persist
        objects = src.functions.objects.Objects()
        objects.write(nodes=nodes, path=path)
