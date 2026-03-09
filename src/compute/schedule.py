"""Module schedule.py"""
import logging

import boto3
import botocore.exceptions


class Schedule:
    """
    Schedule
    """

    def __init__(self, connector: boto3.session.Session):
        """
        Constructor
        """

        self.__scheduler_client = connector.client(service_name='scheduler')

        # Logging
        logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def create_schedule(self, settings: dict, update: bool = False) -> str:
        """
        Creates a new schedule with the specified parameters.

        :param settings: refer to compute/settings.py
        :param update: Update?
        :return:
            The ARN of the created schedule.
        """

        try:
            if update:
                response = self.__scheduler_client.update_schedule(**settings)
            else:
                response = self.__scheduler_client.create_schedule(**settings)

            return response['ScheduleArn']

        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == 'ConflictException':
                self.__logger.error('Error creating schedule: %s\n%s', settings.get('name'), err.response['Error']['Message'])
            else:
                self.__logger.error('Error creating schedule: %s', err.response['Error']['Message'])
            raise
