"""Module compute/timings.py"""
import datetime


class Timings:
    """
    Calculates event bridge times
    """

    def __init__(self, arguments: dict, starting: datetime.datetime, ending: datetime.datetime, future: datetime.datetime):
        """

        :param arguments: A set of arguments vis-à-vis computation & data operations objectives.
        :param starting:
        :param ending:
        :param future:
        """

        self.__arguments = arguments
        self.__starting = starting
        self.__ending = ending
        self.__future = future

    def __events_forecasting(self, scheduler: str) -> dict:
        """
        Builds cron expressions, e.g., "cron(45 09,21 * * ? *)"

        :param scheduler:
        :return:
        """

        __scheduler = self.__arguments.get(scheduler)

        # The cron expression template
        expression = "cron({minute} {initial},{later} * * ? *)"

        # Arithmetic
        start = self.__starting + datetime.timedelta(minutes=25)
        additional = start + datetime.timedelta(hours=12)

        # Hence
        __scheduler['schedule_expression'] = expression.format(
            minute=start.minute, initial=start.hour, later=additional.hour)
        __scheduler['starting'] = self.__starting
        __scheduler['ending'] = self.__ending

        return __scheduler

    def __events_fundamental(self, scheduler: str) -> dict:
        """

        :param scheduler:
        :return:
        """

        __scheduler = self.__arguments.get(scheduler)

        # Hence
        __scheduler['starting'] = self.__starting
        __scheduler['ending'] = self.__ending

        return __scheduler

    def __continuous(self, scheduler: str) -> dict:
        """

        :param scheduler:
        :return:
        """

        __scheduler = self.__arguments.get(scheduler)

        # Arithmetic
        __ending = datetime.datetime(
            year=__scheduler.get('terminate').get('year'), month=__scheduler.get('terminate').get('month'),
            day=__scheduler.get('terminate').get('day'), tzinfo=self.__future.tzinfo)
        __ending = __ending if __ending > self.__future else (self.__future + datetime.timedelta(days=1))

        # Hence
        __scheduler['starting'] = self.__future
        __scheduler['ending'] = __ending

        return __scheduler

    def exc(self, scheduler: str) -> dict:
        """

        :param scheduler:
        :return:
        """

        match scheduler:
            case 'scheduler_events_forecasting':
                return self.__events_forecasting(scheduler=scheduler)
            case 'scheduler_events_fundamental':
                return self.__events_fundamental(scheduler=scheduler)
            case 'scheduler_continuous':
                return self.__continuous(scheduler=scheduler)
            case _:
                raise ValueError(f'{scheduler} is not an option.')
