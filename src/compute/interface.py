"""Module compute/interface.py"""
import datetime
import logging

import boto3
import geopandas
import pandas as pd

import zoneinfo

import src.compute.schedule
import src.compute.settings


class Interface:
    """
    The interface to the compute package programs
    """

    def __init__(self, connector: boto3.session.Session, arguments: dict):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param arguments: A set of arguments vis-à-vis computation & data operations objectives.
        """

        self.__connector = connector
        self.__arguments = arguments

        # Time & Place
        # self.__place = pytz.timezone('Europe/Dublin')

    @staticmethod
    def __timestamp(value: pd.Timestamp) -> datetime.datetime:
        """

        :param value:
        :return:
        """

        _initial = value.to_pydatetime()
        _reset = datetime.datetime.fromtimestamp(_initial.timestamp(), tz=zoneinfo.ZoneInfo('Europe/Dublin'))

        return _reset

    def __future(self, ending: datetime.datetime) -> datetime.datetime:
        """

        :param ending:
        :return:
        """

        __next = ending + datetime.timedelta(days=1)
        value = pd.Timestamp(
            year=__next.year, month=__next.month, day=__next.day, hour=2, minute=5, second=0)

        return self.__timestamp(value=value)

    def exc(self, data: geopandas.GeoDataFrame):
        """

        :param data:
        :return:
        """

        # Cloud Compute Times: The data times and the cloud compute times exist within different zones
        value: pd.Timestamp = max(data['starting'].min(), pd.Timestamp(datetime.datetime.now(), tz='UTC'))
        value: pd.Timestamp = value.ceil(freq='h')
        starting = self.__timestamp(value = value + datetime.timedelta(minutes=10))
        ending = self.__timestamp(value = max(data['ending'].max().ceil(freq='h'), value + datetime.timedelta(hours=1)))

        # Schedule Client
        __schedule_client = self.__connector.client(service_name='scheduler')

        # Settings
        __settings = src.compute.settings.Settings(
            connector=self.__connector, arguments=self.__arguments, starting=starting,
            ending=ending, future=self.__future(ending=ending))

        # Hence
        for scheduler in ['scheduler_events_forecasting']:

            # Schedule Settings
            settings = __settings.exc(scheduler=scheduler)

            # If the schedule does not exist, create; otherwise, update.
            try:
                response: dict = __schedule_client.get_schedule(
                    GroupName=settings.get('GroupName'), Name=settings.get('Name'))
            except __schedule_client.exceptions.ResourceNotFoundException:
                src.compute.schedule.Schedule(
                    connector=self.__connector).create_schedule(settings=settings)
            else:
                logging.info('The event bridge schedule - %s - exists; updating.',
                             response.get('Name'))
                src.compute.schedule.Schedule(
                    connector=self.__connector).create_schedule(settings=settings, update=True)
