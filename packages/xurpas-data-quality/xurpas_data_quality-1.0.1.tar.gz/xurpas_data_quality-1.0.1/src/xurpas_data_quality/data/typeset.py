from typing import Callable, Sequence, Set

from visions import Generic, Integer, Float, VisionsBaseType, Date
from visions.relations import IdentityRelation, InferenceRelation,TypeRelation
from visions.typesets import StandardSet, VisionsTypeset

import pandas as pd
from pandas.api import types as pdt


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
    

XTypeSet = StandardSet()+ Date #+ Numerical



