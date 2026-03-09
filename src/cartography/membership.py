"""Module membership.py"""

import typing

import branca.colormap
import numpy as np
import pandas as pd
import geopandas


class Membership:
    """
    Catchment membership & colours
    """

    def __init__(self):
        """

        Constructor
        """

        self.__seed = 5

    def __get_decimals(self, size: int):
        """

        :param size: The number of required random numbers
        :return:
        """

        rng = np.random.default_rng(seed=self.__seed)

        return rng.uniform(low=0.05, high=0.95, size=size)

    @staticmethod
    def __get_colours(n_catchments: int) -> branca.colormap.StepColormap:
        """

        :param n_catchments:
        :return:
        """

        # Colours
        colours: branca.colormap.StepColormap = branca.colormap.LinearColormap(
            ['black', 'brown', 'orange']).to_step(n_catchments)

        return colours

    def exc(self, data: geopandas.GeoDataFrame) -> typing.Tuple[geopandas.GeoDataFrame, branca.colormap.StepColormap]:
        """

        :param data:
        :return:
        """

        catchments: np.ndarray = data.copy()['catchment_id'].unique()
        intermediary = pd.DataFrame(
            data={'catchment_id': catchments, 'decimal': self.__get_decimals(size=catchments.shape[0])})

        data = data.copy().merge(intermediary, how='left', on=['catchment_id'])
        colours = self.__get_colours(n_catchments=catchments.shape[0])

        return data, colours
