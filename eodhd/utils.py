import pandas as pd
import numpy as np


def format_history_data(data):
    if not isinstance(data, list):
        return data
    if len(data) == 0:
        return data

    df = pd.DataFrame(data)
    df.set_index(["date"], inplace=True)

    return df


def empty_df(index=None):
    if index is None:
        index = []
    empty = pd.DataFrame(index=index, data={
        'open': np.nan, 'high': np.nan, 'low': np.nan,
        'close': np.nan, 'adjusted_close': np.nan, 'volume': np.nan
    })
    empty.index.name = 'date'
    return empty
