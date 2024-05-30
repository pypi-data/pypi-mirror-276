import pandas as pd

from typing import Tuple

def describe_date(series: pd.Series, summary: dict)-> Tuple[pd.Series, dict]:
    """
    Describes a series with information for date data type.

    Args:
        series: series to describe
        summary: dict containing the descriptions of the series so far

    Return:
        The series and the updated summary dict
        """
    
    min_date = series.min()
    max_date = series.max()
    mid_date = series.median()
    time_range = (max_date - min_date).dt.days
    histogram_counts = series.value_counts.to_dict()

    return summary.update(
            {'min_date': min_date,
            'max_date': max_date,
            'mid_date': mid_date,
            'time_range': time_range})
