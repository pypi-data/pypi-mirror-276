import pandas as pd

from dataclasses import dataclass
from visions import VisionsTypeset, Generic, Float, Integer, Categorical
from typing import Dict, List, Callable

from xurpas_data_quality.data.type_descriptions import describe_numeric, describe_categorical, describe_generic

@dataclass
class TableDescription:
    df: pd.DataFrame
    dataset_statistics: Dict
    variable_types: Dict
    variables: Dict
    correlation: pd.DataFrame

class Describer():
    """Describer of series. Contains mapping per type"""

    def __init__(self, 
                type_mapping: Dict[str, List[Callable]] = {
                     Generic : [
                         describe_generic,
                     ],
                     Float : [
                         describe_generic,
                         describe_numeric
                     ],
                     Integer : [
                         describe_generic,
                         describe_numeric
                     ],
                     Categorical : [
                         describe_generic,
                         describe_categorical
                     ]}):

        self.mapping = type_mapping
    
    def summarize(self, dtype, series, **kwargs)-> dict:
        # give the series and typeset
        # for every applicable type apply the function to the series
        # update the summary dict with the new
        summary = {}

        if dtype in self.mapping:
            for func in self.mapping[dtype]:
                summary.update(func(series,summary))
        else:
            for func in self.mapping[Generic]:
                summary.update(func(series,summary))

        return summary
