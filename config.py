"""config.py"""
import datetime
import logging
import os


class Config:
    """
    Config
    """

    def __init__(self) -> None:
        """
        Constructor<br>
        -----------<br>

        Variables denoting a path - including or excluding a filename - have an underscore suffix; this suffix is
        excluded for names such as warehouse, storage, depository, etc.<br><br>
        """

        now = datetime.datetime.now()
        self.stamp = now.strftime('%Y-%m-%d')
        logging.info(self.stamp)

        # Testing
        self.area_ = 'https://raw.githubusercontent.com/ac-repatterning/.github/refs/heads/master/profile/latest.geojson'

        # Directories
        self.warehouse: str = os.path.join(os.getcwd(), 'warehouse')
        self.signals_ = os.path.join(self.warehouse, 'signals')

        # Keys, etc
        self.s3_parameters_key = 's3_parameters.yaml'
        self.argument_key = 'signals/_arguments.json'
        self.prefix: str = 'signals'
        self.signals_data_ = f'{self.prefix}/_data.csv'
        self.signals_latest_ = f'{self.prefix}/_latest.geojson'

        # Project metadata
        self.project_tag = 'hydrography'
        self.project_key_name = 'HydrographyProject'
