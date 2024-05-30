import logging
from typing import Any

import pandas as pd

from ..structure.validation.subject import Column

# TODO: Create one big configuration with SCHEMA (validation) and RESAMPLING

logger = logging.getLogger("default")


def log_downsample(id: str, from_sf: float, to_sf: float, origin: str):
    message = f"Subject's data downsampled from {from_sf}s to {to_sf}s."

    logger.info(message, extra={"origin": origin, "object": id})


def mode(x):
    vals = x.to_list()

    if not vals:
        return None

    return max(vals, key=vals.count)


DOWNSAMPLING = [
    {"column": Column.SUBJECT_ID, "method": "first"},
    {"column": Column.WEAR, "method": mode},
    {"column": Column.TIMEDELTA, "method": "sum"},
    # ---
    {"column": Column.VERTICAL_COUNTS, "method": "sum"},
    {"column": Column.HORIZONTAL_COUNTS, "method": "sum"},
    {"column": Column.PERPENDICULAR_COUNTS, "method": "sum"},
    {"column": Column.VM_COUNTS, "method": "mean"},
    {"column": Column.POSITION, "method": mode},
    {"column": Column.STEPS, "method": "sum"},
    # ---
    {"column": Column.LATITUDE, "method": "first"},
    {"column": Column.LONGITUDE, "method": "first"},
    {"column": Column.GNSS_ACCURACY, "method": "first"},
    {"column": Column.NSAT_VIEWED, "method": "first"},
    {"column": Column.NSAT_USED, "method": "first"},
    {"column": Column.NSAT_RATIO, "method": "first"},
    {"column": Column.SNR_VIEWED, "method": "first"},
    {"column": Column.SNR_USED, "method": "first"},
    {"column": Column.PDOP, "method": "first"},
    {"column": Column.HDOP, "method": "first"},
    {"column": Column.VDOP, "method": "first"},
    # ---
    {"column": Column.DISTANCE, "method": "sum"},
    {"column": Column.ELEVATION, "method": "first"},
    {"column": Column.SPEED, "method": "mean"},
    {"column": Column.ACCELERATION, "method": "mean"},
    {"column": Column.DIRECTION, "method": "first"},
    {"column": Column.ENVIRONMENT, "method": mode},
    # ---
    {"column": Column.HEART_RATE, "method": "mean"},
    {"column": Column.LUX, "method": "mean"},
    # ---
    {"column": Column.ACTIVITY_INTENSITY, "method": mode},
    # TODO: ACTIVITY_VALUE - This is should be discussed a lot.
    {"column": Column.ACTIVITY_VALUE, "method": "mean"},
    {"column": Column.ACTIVITY, "method": mode},
]


def downsample(
    id: str,
    df: pd.DataFrame,
    from_sf: float,
    to_sf: float,
    mapper: list[dict[str, Any]] | None = None,
) -> pd.DataFrame:
    if from_sf > to_sf:
        raise ValueError(f"Downsampling is not supported | {from_sf} > {to_sf}")
    elif from_sf == to_sf:
        print(f"Sampling frequencies are the same | {from_sf} = {to_sf}")
        return df

    df = df.copy()

    if not mapper:
        mapper = DOWNSAMPLING

    resampling = {v["column"]: v["method"] for v in mapper if v["column"] in df.columns}

    dropped = [
        colname for colname in df.columns if colname not in resampling.keys()
    ]  # TODO: Check that it works properly.
    if dropped:
        print(
            f"Columns that are not in the resampling configuration will be dropped | Dropping: {dropped}"
        )  # TODO: Write warning what columns are dropped.

    df = df.resample(f"{to_sf}s").agg(resampling)  # type: ignore
    df.dropna(
        axis=0, how="all", inplace=True
    )  # Dropping rows with all NaN values - they were created by resampling.

    log_downsample(id, from_sf, to_sf, origin="Subject.upsample")

    return df
