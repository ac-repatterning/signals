"""Module illustrate.py"""

import os

import folium
import folium.plugins
import geopandas

import config
import src.cartography.centroids
import src.cartography.metadata


class Illustrate:
    """
    Illustrate
    """

    def __init__(self, data: geopandas.GeoDataFrame, latest: geopandas.GeoDataFrame):
        """

        :param data: The frame of gauge stations.
        :param latest: The overarching catchments
        """

        self.__data = data
        self.__latest = latest

        # Configurations
        self.__configurations = config.Config()

        # Metadata: Gauge Station
        self.__metadata = src.cartography.metadata.Metadata()

        # Centroid
        self.__c_latitude, self.__c_longitude = src.cartography.centroids.Centroids(blob=self.__data).__call__()

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
                "fillColor": "#598BAF", "color": "#598BAF", "opacity": 0.95, "weight": 0.25, "dashArray": "2"
            },
            tooltip=folium.GeoJsonTooltip(fields=["warningLevel", "warningLikelihood", "warningStatus"],
                                          aliases=["Warning Level", "Warning Likelihood", "Warning Status"]),
            control=False,
            highlight_function=lambda feature: {
                "fillColor": "#6b8e23", "fillOpacity": 0.1
            }
        ).add_to(segments)

        # Gauge Stations
        instances = self.__data.copy()[['catchment_name', 'station_name', 'river_name', 'latitude', 'longitude', 'geometry']]
        on_each_feature = folium.utilities.JsCode(self.__metadata())
        folium.GeoJson(
            data = instances.to_crs(epsg=3857),
            name = 'Gauge Stations',
            marker=folium.CircleMarker(
                radius=11.5, weight=4, stroke=False, fill=True, fillColor='#000000', fillOpacity=0.85, ),
            zoom_on_click=True,
            on_each_feature=on_each_feature,
            show=True
        ).add_to(segments)

        folium.LayerControl().add_to(segments)

        # Drawing Tool
        folium.plugins.Draw(
            export=False, position='bottomleft', show_geometry_on_click=False,
            draw_options={'polyline': False, 'polygon': False, 'rectangle': False, 'marker': False,
                          'circle': {'shapeOptions': {'color': '#6495ed', 'stroke': True, 'dashArray': '', 'opacity': 0.35}},
                          'circlemarker': {'color': '#000000', 'opacity': 0.85, 'fillOpacity': 0.35}}
        ).add_to(segments)

        # Persist
        outfile = os.path.join(self.__configurations.warning_, 'latest.html')
        segments.save(outfile=outfile)

        return f'{os.path.basename(outfile)}'
