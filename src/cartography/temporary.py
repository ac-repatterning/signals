"""Module temporary.py"""
import datetime
import uuid

import geopandas
import pytz

import config


class Temporary:
    """
    Retrieves a temporary data set for testing
    """

    def __init__(self):
        """
        Constructor
        """

        self.__minutes = 35

        # Instances
        self.__configurations = config.Config()

    def __call__(self) -> geopandas.GeoDataFrame:
        """

        :return:
        """

        baseline = datetime.datetime.now(pytz.utc)

        try:
            frame = geopandas.read_file(
                filename=self.__configurations.area_)
            frame['warningId'] = str(uuid.uuid4())
            frame['validFromDate'] = baseline + datetime.timedelta(minutes=self.__minutes)
            frame['validToDate'] = baseline + datetime.timedelta(minutes=3*self.__minutes)
            frame.info()
            return frame
        except FileNotFoundError as err:
            raise err from err
