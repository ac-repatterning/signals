"""Module cuttings.py"""
import datetime

import geopandas
import pandas as pd
import pytz
import shapely

import src.elements.system as stm


class Cuttings:
    """
    Intersections of polygons
    """

    def __init__(self, reference: geopandas.GeoDataFrame):
        """

        :param reference: The reference sheet of gauges.  Each instance encodes the attributes of a gauge.
        """

        self.__reference = reference

        # Fields
        self.__r_fields = ['ts_id', 'catchment_id', 'latitude', 'longitude', 'geometry']

        # Time & Place
        self.__place = pytz.timezone('UTC')

    def __is_member(self, _polygon: shapely.geometry.polygon.Polygon):
        """
        Determines whether a reference gauge location lies within a polygon; per reference gauge

        :param _polygon: The polygon of a weather warning area
        :return:
        """

        return self.__reference.geometry.apply(lambda y: y.within(_polygon))

    def __timestamp(self, value: pd.Timestamp) -> datetime.datetime:
        """

        :param value:
        :return:
        """

        _initial = value.to_pydatetime()
        _free = datetime.datetime.fromtimestamp(_initial.timestamp(), tz=None)

        return self.__place.localize(_free)

    def members(self, _elements: stm.System) -> geopandas.GeoDataFrame:
        """
        .geometry: shapely.geometry.polygon.Polygon -> The polygon of a weather warning area

        :param _elements:
        :return:
        """

        states = self.__is_member(_polygon=_elements.geometry)

        frame = self.__reference.copy().loc[states, self.__r_fields]
        frame['issued_date'] = self.__timestamp(value=_elements.issuedDate)
        frame['warning_level'] = _elements.warningLevel
        frame['warning_id'] = _elements.warningId
        frame['modified'] = self.__timestamp(value=_elements.modifiedDate)
        frame['starting'] = self.__timestamp(value=_elements.validFromDate)
        frame['ending'] = self.__timestamp(value=_elements.validToDate)

        return frame
