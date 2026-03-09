"""Module system.py"""
import typing

import numpy as np
import pandas as pd
import shapely


class System(typing.NamedTuple):
    """
    The data type class ⇾ System

    Attributes
    ----------

    """

    Index: int
    issuedDate: pd.Timestamp
    warningLikelihood: np.int32
    warningLevel: str
    warningStatus: str
    warningHeadline: str
    warningId: str
    warningVersion: str
    warningFurtherDetails: str
    modifiedDate: pd.Timestamp
    validFromDate: pd.Timestamp
    affectedAreas: str
    warningImpact: np.int32
    validToDate: pd.Timestamp
    geometry: shapely.geometry.polygon.Polygon
