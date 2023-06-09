from pathlib import Path
from typing import Any, Dict, Optional, Union

import pandas as pd

from bids2table.extractors.entities import BIDSEntities


def join_bids_path(
    row: Union[pd.Series, Dict[str, Any]],
    prefix: Optional[Union[str, Path]] = None,
    valid_only: bool = True,
) -> Path:
    """
    Reconstruct a BIDS path from a table row/record or entities dict.

    Example::

        df = pd.read_parquet("dataset.parquet")
        paths = df.apply(join_bids_path, axis=1)
    """
    if isinstance(row, pd.Series):
        row = row.to_dict()

    entities = BIDSEntities.from_dict(row)
    path = entities.to_path(prefix=prefix, valid_only=valid_only)
    return path


def flat_to_multi_columns(df: pd.DataFrame, sep: str = "__") -> pd.DataFrame:
    """
    Convert a flat column index to a MultiIndex by splitting on `sep`.
    """
    # Do nothing if already a MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        return df

    columns = df.columns
    split_columns = [col.split(sep) for col in columns]
    num_levels = max(map(len, split_columns))

    def _pad_col(col):
        return tuple((num_levels - len(col)) * [None] + col)

    df = df.copy(deep=False)
    df.columns = pd.MultiIndex.from_tuples(map(_pad_col, split_columns))
    return df


def multi_to_flat_columns(df: pd.DataFrame, sep: str = "__") -> pd.DataFrame:
    """
    Convert a column MultiIndex to a flat index by joining on `sep`.
    """
    # Do nothing if already flat
    if not isinstance(df.columns, pd.MultiIndex):
        return df

    columns = df.columns.to_flat_index()
    join_columns = [sep.join(col) for col in columns]

    df = df.copy(deep=False)
    df.columns = pd.Index(join_columns)
    return df
