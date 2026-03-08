"""Module illustrate.py"""
import logging
import os

import folium
import folium.plugins
import geopandas
import pandas as pd

import config
import src.cartography.centroids
import src.cartography.membership


class Illustrate:
    """
    Illustrate
    """

    def __init__(self, data: geopandas.GeoDataFrame, latest: geopandas.GeoDataFrame):
        """

        :param data: The frame of gauge stations.
        :param latest: The overarching catchments
        """

        self.__data, self.__colour = src.cartography.membership.Membership().exc(data=data)
        self.__latest = latest

        # Configurations
        self.__configurations = config.Config()

        # Centroid
        self.__c_latitude, self.__c_longitude = src.cartography.centroids.Centroids(blob=self.__data)()

    def exc(self) -> str:
        """

        :return:
        """

        # Base Layer: TileLayer objects aid the security of map service details.
        segments = folium.Map(location=[self.__c_latitude, self.__c_longitude], zoom_start=7)

        # Uncontrollable Layer
        fields = ['warningLikelihood', 'warningLevel', 'warningStatus', 'warningHeadline',
                  'affectedAreas', 'warningImpact', 'geometry']
        folium.GeoJson(
            data=self.__latest[fields].to_crs(epsg=3857),
            name='Boundaries',
            style_function=lambda feature: {
                "fillColor": "#598BAF", "color": "#598BAF", "opacity": 0.95, "weight": 0.25, "dashArray": "2"},
            tooltip=folium.GeoJsonTooltip(fields=["warningLevel", "warningLikelihood", "warningStatus"],
                                          aliases=["Warning Level", "Warning Likelihood", "Warning Status"]),
            control=False,
            highlight_function=lambda feature: {
                "fillColor": "#6b8e23", "fillOpacity": 0.1}
        ).add_to(segments)

        # Gauge Stations
        for c in self.__data.columns:
            if self.__data[c].dtype == pd.Timestamp:
                logging.info('TIMESTAMP: %s', c)

        instances = self.__data.copy()[['catchment_name', 'station_name', 'river_name',
                                        'latitude', 'longitude', 'decimal', 'geometry']]

        clustering = folium.plugins.MarkerCluster(overlay=True, control=False, name='Gauge Stations',
                                                  options={'maxClusterRadius': 60})
        for i in range(instances.shape[0]):
            marking = folium.Marker(
                location=[instances.iloc[i]['latitude'], instances.iloc[i]['longitude']],
                popup= '<b>' + instances.iloc[i]['station_name'] + '</b><br><br><b>Catchment: </b>' +
                         instances.iloc[i]['catchment_name'] + '<br><br><b>River/Water: </b>' + instances.iloc[i]['river_name'] +
                       '<br>',
                icon=folium.Icon(
                    prefix='fa', icon='circle', icon_size=(0.5,0.5), color='white',
                    icon_color=self.__colour(instances.iloc[i]['decimal']))
            )
            clustering.add_child(marking)
        clustering.add_to(segments)

        # Control Layer
        folium.LayerControl().add_to(segments)

        # Drawing Tool
        folium.plugins.Draw(
            export=False, position='bottomleft', show_geometry_on_click=False,
            draw_options={'polyline': False, 'polygon': False, 'rectangle': False, 'marker': False,
                          'circle': {'shapeOptions': {'color': '#6495ed', 'stroke': True, 'dashArray': '', 'opacity': 0.35}},
                          'circlemarker': {'color': '#000000', 'opacity': 0.85, 'fillOpacity': 0.35}}
        ).add_to(segments)

        # Persist
        outfile = os.path.join(self.__configurations.warning_, '_latest.html')
        segments.save(outfile=outfile)

        return f'{os.path.basename(outfile)}'
