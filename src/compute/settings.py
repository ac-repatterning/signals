"""Module settings.py"""
import datetime

import boto3

import src.functions.secret
import src.compute.timings


class Settings:
    """
    Creates a schedule's dictionary of arguments.
    """

    def __init__(self, connector: boto3.session.Session, arguments: dict, starting: datetime.datetime,
                 ending: datetime.datetime, future: datetime.datetime):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param arguments: A set of arguments vis-à-vis computation & data operations objectives.
        :param starting: The start time.<br>
        :param ending: The end time.<br>
        :param future: The re-start point of the continuous-states schedule.<br>
        """

        # Project
        self.__project_key_name: str = arguments.get('project_key_name')

        # Instances
        self.__secret = src.functions.secret.Secret(connector=connector)
        self.__timings = src.compute.timings.Timings(arguments=arguments, starting=starting, ending=ending, future=future)

    def exc(self, scheduler: str) -> dict:
        """
        For more about a schedule's parameters & arguments visit
        <a
        href="https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/create_schedule.html"
        target="_blank">EventBridgeScheduler.Client.create_schedule()</a><br><br>

        name: The schedule's name.<br>
        schedule expression: The timing schedule.<br>
        group name: The name of the schedule group.<br>
        arn: The Amazon Resource Name (ARN) of the target.<br>
        role arn: The Amazon Resource Name (ARN) of the execution IAM role.<br>
        action after completion: Either `delete` or `none`.<br>
        flexible time window:
            mode: `OFF`|`FLEXIBLE`<br>
            maximum window in minutes: The span of the afore flexible time window.<br><br>


        :param scheduler: A string for identifying the scheduler details in focus
        :return:
        """

        __scheduler = self.__timings.exc(scheduler=scheduler)

        settings = {
            'Name': __scheduler.get('name'),
            'ScheduleExpression': __scheduler.get('schedule_expression'),
            'ScheduleExpressionTimezone': __scheduler.get('schedule_expression_timezone'),
            'StartDate': __scheduler.get('starting'),
            'EndDate': __scheduler.get('ending'),
            'GroupName': self.__secret.exc(secret_id=self.__project_key_name, node='schedule-group'),
            'Target': {
                'Arn': self.__secret.exc(
                    secret_id=self.__project_key_name,
                    node=__scheduler.get('target').get('arn_node')),
                'RoleArn': self.__secret.exc(secret_id=self.__project_key_name, node='schedule-target-execution-role-arn'),
                'RetryPolicy': {
                    'MaximumEventAgeInSeconds': __scheduler.get(
                        'target').get('retry_policy').get('maximum_event_age_in_seconds'),
                    'MaximumRetryAttempts': __scheduler.get(
                        'target').get('retry_policy').get('maximum_retry_attempts')
                }
            },
            'ActionAfterCompletion': __scheduler.get('action_after_completion'),
            'FlexibleTimeWindow': {
                'Mode': __scheduler.get('flexible_time_window').get('mode'),
                'MaximumWindowInMinutes': __scheduler.get('flexible_time_window').get('maximum_window_in_minutes')
            }
        }

        return settings
