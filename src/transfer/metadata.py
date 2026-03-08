"""Module metadata.py"""

class Metadata:
    """
    https://weather.metoffice.gov.uk/guides/warnings
    """

    # pylint: disable=R0903
    def __init__(self):
        """
        Constructor
        """

        self.metadata = {
            "times.json": {
                "desc": "The starting and ending times of the latest warning."
            },
            "latest.html": {
                "desc": "The latest geospatial map.",
            },
            "latest.geojson": {
                "desc": "The latest geospatial warning data."
            },
            "data.csv": {
                'ts_id': 'The unique identification of the time series of a gauge.',
                 'catchment_id': 'A catchment identification code.',
                 'latitude': 'Latitude',
                 'longitude': 'Longitude',
                 'issued_date': 'The day the warning was issued',
                 'warning_level': 'The warning level.',
                 'warning_id': 'The identification code of the warning.',
                 'modified': 'If the warning modified, this value will differ from the issue date.',
                 'starting': "The warning period's starting time point.",
                 'ending': "The warning period's ending time point"
            }
        }
