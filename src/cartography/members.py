"""Module members.py"""
import logging
import os
import sys

import geopandas
import pandas as pd

import config
import src.cartography.cuttings
import src.cartography.temporary
import src.elements.system as stm
import src.functions.cache


class Members:
    """
    Members
    """

    def __init__(self, arguments: dict):
        """

        :param arguments:
        """

        self.__arguments = arguments

        # Instances
        self.__configurations = config.Config()

        # Fields
        self.__fields = [field for field in list(stm.System._fields) if field != 'Index']

    # noinspection PyTypeChecker
    def __persist(self, data: geopandas.GeoDataFrame):
        """

        :param data:
        :return:
        """

        try:
            data.to_file(
                filename=os.path.join(self.__configurations.warehouse, self.__configurations.warning_latest_),
                driver='GeoJSON')
        except OSError as err:
            raise err from err

    def __members(self, latest: geopandas.GeoDataFrame, reference: geopandas.GeoDataFrame) -> geopandas.GeoDataFrame:
        """
        Which gauges, if any, lie within a warning area?

        :param latest:
        :param reference:
        :return:
        """

        initial: list[geopandas.GeoDataFrame] = [
            src.cartography.cuttings.Cuttings(reference=reference).members(_elements=stm.System._make(_elements))
            for _elements in latest[self.__fields].itertuples()]

        if len(initial) == 0:
            return geopandas.GeoDataFrame()

        # noinspection PyTypeChecker
        return pd.concat(initial, axis=0, ignore_index=True)

    @staticmethod
    def __exit():
        """

        :return:
        """

        logging.info('no warnings')
        src.functions.cache.Cache().exc()
        sys.exit(0)

    def exc(self, latest: geopandas.GeoDataFrame, reference: geopandas.GeoDataFrame) -> geopandas.GeoDataFrame:
        """
        Before determining the gauges within a warning area, ensure the warning area data & `reference` have the same
        coördinate reference system.

        :param latest: The latest warning area/s
        :param reference: The reference inventory of gauges
        :return:
        """

        # If there are no live warnings, and we are not testing
        if latest.empty & (not self.__arguments.get('testing')):
            self.__exit()

        # Placeholders
        members = geopandas.GeoDataFrame()

        # Hence
        if not latest.empty:
            self.__persist(data=latest)
            latest: geopandas.GeoDataFrame = latest.to_crs(epsg=int(reference.crs.srs.split(':')[1]))
            members = self.__members(latest=latest, reference=reference)

        # Or
        if members.empty & self.__arguments.get('testing'):
            latest = src.cartography.temporary.Temporary().__call__()
            self.__persist(data=latest)
            latest: geopandas.GeoDataFrame = latest.to_crs(epsg=int(reference.crs.srs.split(':')[1]))
            members = self.__members(latest=latest, reference=reference)

        if members.empty:
            self.__exit()

        logging.info(latest)
        logging.info(members)

        return members
