from datetime import timedelta

import pandas as pd

from ..utils import columns_not_exists


def gap_splitter(
    df: pd.DataFrame,
    *,
    min_duration: timedelta,
    name: str = "segment",
    overwrite: bool = False,
) -> pd.DataFrame:
    # TODO: Option to remove small segments
    columns_not_exists(df, [name], overwrite=overwrite)

    df = df.copy()

    df[name] = df.index.diff() > min_duration  # type: ignore
    df[name] = df[name].apply(lambda x: 1 if x else 0).cumsum() + 1

    return df.astype({name: "UInt16"})
