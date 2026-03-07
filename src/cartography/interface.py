"""Module algorithms/interface.py"""
import boto3
import geopandas

import src.cartography.data
import src.cartography.latest
import src.cartography.reference
import src.cartography.times
import src.cartography.updating
import src.elements.s3_parameters as s3p


class Interface:
    """
    The interface to the programs of the algorithms package.
    """

    def __init__(self, connector: boto3.session.Session,
                 s3_parameters: s3p.S3Parameters, arguments: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        :param arguments: A set of arguments vis-à-vis computation & data operations objectives.
        """

        self.__connector = connector
        self.__s3_parameters = s3_parameters
        self.__arguments = arguments

    def exc(self) -> geopandas.GeoDataFrame:
        """
        Hence, filtering and limiting
        -----------------------------<br>
        data = self.__filtering(data=data.copy())<br>
        data = self.__limiting(data=data.copy())<br>

        :return:
        """

        # The country's gauge assets
        reference: geopandas.GeoDataFrame = src.cartography.reference.Reference(
            s3_parameters=self.__s3_parameters).exc()

        # The latest geo-spatial weather warning data
        latest: geopandas.GeoDataFrame = src.cartography.latest.Latest(
            connector=self.__connector, arguments=self.__arguments).exc()

        # Do any of the warnings apply to gauges within Scotland
        data: geopandas.GeoDataFrame = src.cartography.data.Data(
            arguments=self.__arguments).exc(latest=latest, reference=reference)

        # Update the warnings data library
        # src.cartography.updating.Updating(s3_parameters=self.__s3_parameters).exc(data=data)

        # Times
        src.cartography.times.Times(arguments=self.__arguments).exc(data=data)

        return data
