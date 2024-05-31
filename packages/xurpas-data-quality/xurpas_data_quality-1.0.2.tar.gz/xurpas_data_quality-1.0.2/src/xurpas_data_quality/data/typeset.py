from typing import Callable, Sequence, Set

from visions import create_type
from visions import Categorical, DateTime, Date, Integer, Float, String, Generic
from visions.relations import IdentityRelation, InferenceRelation,TypeRelation
from visions.typesets import StandardSet, VisionsTypeset

import pandas as pd
import warnings
from pandas.api import types as pdt

warnings.filterwarnings("ignore", category=UserWarning, module='visions.typesets.typeset')

"""class Numerical(VisionsBaseType):
    @staticmethod
    def get_relations() -> TypeRelation:
        relations = [
            IdentityRelation(Generic),
            IdentityRelation(Integer),
            IdentityRelation(Float),
        ]
        return relations

    @staticmethod
    def contains_op(series: pd.Series, state: dict) -> bool:
        return pd.api.types.is_integer_dtype(series) or pd.api.types.is_float_dtype(series)"""

def float_is_myfloat(series: pd.Series, state):
    return super().contains_op(series, state) & ~series.str.contains('e', na=False)

def float_to_myfloat(series: pd.Series) -> pd.Series:
    return series.astype(float)

XFloat = create_type(
    "Float",
    contains=Float.contains_op,
    identity=Generic,
    inference=[{
        "relationship": float_is_myfloat,
        "transformer": float_to_myfloat,
        "related_type": Float,
    }]
)

types = [XFloat, Integer, String, Categorical, Date, DateTime, Generic]
XTypeSet = VisionsTypeset(types)



