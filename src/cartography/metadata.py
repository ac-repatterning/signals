"""Module metadata.py"""


class Metadata:
    """
    The popup & tooltip text of the gauge stations.
    """

    def __init__(self):
        pass

    def __call__(self) -> str:
        """
        For a gauge station.

        :return:
        """

        return """
                function(feature, layer) {
                    layer.bindTooltip(
                        '<b>' + feature.properties.station_name + '</b><br><br>' +
                        'River/Water: ' + feature.properties.river_name + '<br>' +
                        'Catchment: ' + feature.properties.catchment_name + '<br><br>'
                    );
                }
                """