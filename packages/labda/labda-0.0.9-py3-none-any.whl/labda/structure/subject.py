from datetime import datetime, timedelta
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

import geopandas as gpd

if TYPE_CHECKING:
    # This is a workaround to avoid circular imports.
    # TODO: Is there a better way to do this?
    from .collection import Collection
import logging

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pydantic import BaseModel, Field, SkipValidation
from shapely.geometry import MultiPolygon

from ..expanders import (
    add_acceleration,
    add_direction,
    add_distance,
    add_speed,
    add_timedelta,
)
from ..processing.accelerometer import detect_activity_intensity, detect_wear
from ..processing.context import detect_contexts
from ..processing.spatial import detect_transportation, detect_trips, get_timeline
from ..processing.wear_validity import get_wear_time
from ..structure.resampling import downsample
from ..visualisation.spatial import plot
from .validation.subject import SCHEMA, Column

logger = logging.getLogger("default")


def log_message(subject: "Subject", message: str, origin: str):
    meta = subject.metadata
    logger.info(message, extra={"origin": origin, "object": meta.id})


class Vendor(StrEnum):
    ACTIGRAPH = "ActiGraph"
    XIAOMI = "Xiaomi"
    SENS = "Sens"
    GARMIN = "Garmin"
    QSTARZ = "Qstarz"
    GGIR = "GGIR"
    SENSECAP = "SenseCap"
    TRACCAR = "Traccar"


class Sensor(BaseModel):
    id: str
    serial_number: str | None = None
    model: str | None = None
    vendor: Vendor | None = None
    firmware_version: str | None = None
    extra: dict[str, Any] | None = None

    class Config:
        coerce_numbers_to_str = True


class Metadata(BaseModel):
    id: str
    sensor: list[Sensor] = Field(default_factory=list)
    sampling_frequency: float = Field(ge=0, description="Sampling frequency in seconds")
    crs: str | None = None
    timezone: str | None = None

    class Config:
        coerce_numbers_to_str = True


class Context(BaseModel):
    id: str = Field(validation_alias="context")
    start: datetime | None = None
    end: datetime | None = None
    geometry: MultiPolygon | None = None
    priority: int | None = None
    indexes: list[datetime] | None = None

    class Config:
        arbitrary_types_allowed = True


class Subject(BaseModel):
    metadata: Metadata
    collection: Optional["Collection"] = None
    df: pd.DataFrame
    timeline: pd.DataFrame | None = None
    contexts: list[Context] = Field(default_factory=list)

    # TODO: Add check for not empty dataframe.

    class Config:
        arbitrary_types_allowed = True

    def __str__(self):
        return str(f"{self.metadata}\n{self.df}")

    @property
    def domains(self):
        # TODO: Implement this property.
        raise NotImplementedError("This method is not implemented yet.")

    def to_parquet(
        self,
        path: str | Path,
        *,
        overwrite: bool = False,
        validate: bool = True,
    ) -> None:
        """
        Writes the subject's data to a Parquet file. The metadata is stored in the file's schema.

        Before saving, the subject's DataFrame is validated to ensure it conforms to the schema LABDA standard format.

        Args:
            path (str | Path): The path to write the Parquet file to.
            overwrite (bool, optional): Whether to overwrite an existing file at the path.

        Raises:
            FileExistsError: If a file already exists at the path and `overwrite` is `False`.
        """
        if isinstance(path, str):
            path = Path(path)

        if path.exists() and not overwrite:
            raise FileExistsError(
                f"The file '{path}' already exists. If you want to overwrite it, set the 'overwrite' argument to 'True'."
            )
        else:
            path.parent.mkdir(parents=True, exist_ok=True)

        custom_metadata = {"labda".encode(): self.metadata.model_dump_json().encode()}
        if validate:
            self.validate()
        table = pa.Table.from_pandas(self.df)

        existing_metadata = table.schema.metadata
        combined_meta = {**custom_metadata, **existing_metadata}

        table = table.replace_schema_metadata(combined_meta)
        pq.write_table(table, path)
        log_message(self, f"Subject exported: {path}", origin=f"{__name__}.to_parquet")

    @classmethod
    def from_parquet(
        cls,
        path: str | Path,
        *,
        validate: bool = True,
    ) -> "Subject":
        """
        Loads a subject from a Parquet file. While loading, subject's data is validated to ensure
        it conforms to the schema LABDA standard format.

        Args:
            path (str | Path): The path to read the Parquet file from.

        Returns:
            Subject: A new Subject instance with the data read from the Parquet file.

        Raises:
            FileNotFoundError: If no file exists at the path.
        """
        if isinstance(path, str):
            path = Path(path)

        table = pq.read_table(path)
        df = table.to_pandas()
        custom_metadata = Metadata.model_validate_json(
            table.schema.metadata["labda".encode()]
        )
        cls = cls(metadata=custom_metadata, df=df)

        if validate:
            cls.validate()

        log_message(cls, f"Subject imported: {path}", origin=f"{__name__}.from_parquet")

        return cls

    def validate(
        self,
        *,
        extra_columns: bool = False,
    ):
        if self.df.empty:
            raise ValueError("DataFrame is empty.")

        self.df = SCHEMA.validate(self.df)

        # Order columns as defined in Column
        records_columns = [col.value for col in Column]
        ordered_columns = [col for col in records_columns if col in self.df.columns]

        # Append extra columns that are not in Column at the end, alphabetically
        if extra_columns:
            extra = sorted(set(self.df.columns) - set(records_columns))
            ordered_columns.extend(extra)

        self.df = self.df[ordered_columns]

    def add_timedelta(
        self,
        *,
        name: str = Column.TIMEDELTA,
        overwrite: bool = False,
    ):
        """
        Adds a timedelta column to the subject's DataFrame.

        This function calculates the time difference between each row and the previous row in the
        subject's DataFrame. The calculated timedelta is added as a new column to the DataFrame.

        Args:
            name (str, optional): The name of the new timedelta column.
            overwrite (bool, optional): Whether to overwrite the existing timedelta column if it exists.

        Raises:
            ValueError: If a column with the specified name already exists and 'overwrite' is False.
        """
        self.df = add_timedelta(self.df, name=name, overwrite=overwrite)
        log_message(self, "Timedelta column added.", origin=f"{__name__}.add_timedelta")

    def add_distance(
        self,
        *,
        name: str = Column.DISTANCE,
        overwrite: bool = False,
    ):
        """
        Adds a distance column to the subject's DataFrame.

        This function calculates the distance between each row and the previous row in the
        subject's DataFrame. The calculated distance is added as a new column to the DataFrame.
        Units are based on the CRS.

        Args:
            name (str, optional): The name of the new distance column. Defaults to Column.DISTANCE.
            overwrite (bool, optional): Whether to overwrite the existing distance column if it exists.

        Raises:
            ValueError: If a column with the specified name already exists and 'overwrite' is False.
        """
        self.df = add_distance(
            self.df, crs=self.metadata.crs, name=name, overwrite=overwrite
        )
        log_message(self, "Distance column added.", origin=f"{__name__}.add_distance")

    def add_speed(
        self,
        *,
        name: str = Column.SPEED,
        overwrite: bool = False,
    ):
        """
        Adds a speed column to the subject's DataFrame.

        This function calculates the speed for each row in the subject's DataFrame based on the distance and time
        difference to the previous row. The calculated speed is added as a new column to the DataFrame.
        Units are based on the CRS. If units are in metres, the speed is converted to km/h.

        Args:
            name (str, optional): The name of the new speed column.
            overwrite (bool, optional): Whether to overwrite the existing speed column if it exists.

        Raises:
            ValueError: If a column with the specified name already exists and 'overwrite' is False.
        """
        self.df = add_speed(
            self.df, crs=self.metadata.crs, name=name, overwrite=overwrite
        )
        log_message(self, "Speed column added.", origin=f"{__name__}.add_speed")

    def add_acceleration(
        self,
        *,
        name: str = Column.ACCELERATION,
        overwrite: bool = False,
    ):
        self.df = add_acceleration(
            self.df, crs=self.metadata.crs, name=name, overwrite=overwrite
        )

    def add_direction(
        self,
        *,
        name: str = Column.DIRECTION,
        overwrite: bool = False,
    ):
        """
        Adds a direction column to the subject's DataFrame.

        This function calculates the direction of movement for each row in the
        subject's DataFrame. The calculated direction is added as a new column to the DataFrame.
        The direction value is a bearing in degrees.

        Args:
            name (str, optional): The name of the new direction column.
            overwrite (bool, optional): Whether to overwrite the existing direction column if it exists.

        Raises:
            ValueError: If a column with the specified name already exists and 'overwrite' is False.
        """
        self.df = add_direction(self.df, name=name, overwrite=overwrite)
        log_message(self, "Direction column added.", origin=f"{__name__}.add_direction")

    def detect_trips(
        self,
        gap_duration: timedelta,
        stop_radius: int | float,
        stop_duration: timedelta,
        *,
        max_speed: int | float | None = None,
        min_distance: int | float | None = None,
        pause_radius: int | float | None = None,
        pause_duration: timedelta | None = None,
        pause_fill: str | None = None,
        min_duration: timedelta | None = None,
        min_length: int | float | None = None,
        cut_points: dict[str, Any] | None = None,
        window: int | None = None,
        activity: bool = False,
        indoor_limit: float | None = None,
        overwrite: bool = False,
    ) -> None:
        """Detects trips and transportation modes in the subject's data based on the specified parameters.
        The detected trips are stored in the subject's timeline and DataFrame is annotated with trip and
        transportation mode information.

        You can load prepared cut points for transportation mode detection or provide your own, see the example below.

        Args:
            gap_duration (timedelta): The minimum duration to consider a gap, i.e. if there is missing data for longer than this duration, the data is split into a new segment and analysed separately.
            stop_radius (int | float): The maximum radius that subject needs to stay in to be considered a stop.
            stop_duration (timedelta): The minimum duration to subject need to stay in specified radius to be considered a stop.
            max_speed (int | float | None): The maximum speed between points. If the speed between points is higher than this value, data are split into a new segment and analysed separately.
            min_distance (int | float | None): The minimum distance between points. Points that are closer than this distance are filtered out.
            pause_radius (int | float | None): The maximum radius that subject needs to stay in to be considered a as a trip pause.
            pause_duration (timedelta | None): The minimum duration to subject need to stay in specified radius to be considered as a trip pause.
            pause_fill (str | None): If pauses should also have transportation mode. Options are "forward" or "backward" fill (based on the previous or next transportation mode of the trip).
            min_duration (timedelta | None): The minimum duration of a trip. Trips shorter than this duration are annotated as stationary (stop) points.
            min_length (int | float | None): The minimum length of a trip. Trips shorter than this length are annotated as stationary (stop) points.
            cut_points (dict[str, Any] | None): Dictionary of cut points for transportation modes identification. If not provided, transportation modes are not detected.
            window (int | None): The window size for moving average for transportation mode detection.
            activity (bool): Wheter to use data from activity intensity column for transportation mode detection (combination of cut points and activity intensity column is used for detection).
            indoor_limit (float | None): How much of the data needs to be identified as indoor for the whole trip to be removed (changed to stationary).
            overwrite (bool): Whether to overwrite existing trip data.

        Raises:
            ValueError: If the subject's CRS is not defined.
            ValueError: If the timeline already exists and 'overwrite' is False.

        Returns:
            None

        Examples:
            Here's how to call the function. For this example we assume that the subject's data has information for physical activity intensity
            and environment (indoor/outdoor) and data are collected in less than 1 minute intervals.

            ```python
            from datetime import timedelta

            from labda import Subject
            from labda.assets import TRANSPORTATION_CUT_POINTS

            subject = Subject.from_parquet("subject.parquet")

            subject.detect_trips(
                "gap_duration": timedelta(minutes=1),
                "stop_radius": 25,
                "stop_duration": timedelta(minutes=3),
                "max_speed": 220,
                "min_distance": None,
                "pause_radius": 15,
                "pause_duration": timedelta(minutes=1.5),
                "pause_fill": "forward",
                "min_duration": timedelta(minutes=2),
                "min_length": None,
                "cut_points": TRANSPORTATION_CUT_POINTS[1],
                "window": 3,
                "activity": True,
                "indoor_limit": 92.5,
                "overwrite": True,
                )
            ```
        """
        if not self.metadata.crs:
            raise ValueError("Subject CRS is not defined.")

        self.df = detect_trips(
            self.df,
            crs=self.metadata.crs,
            sampling_frequency=self.metadata.sampling_frequency,
            overwrite=overwrite,
            gap_duration=gap_duration,
            stop_radius=stop_radius,
            stop_duration=stop_duration,
            pause_radius=pause_radius,
            pause_duration=pause_duration,
            min_duration=min_duration,
            min_length=min_length,
            min_distance=min_distance,
            max_speed=max_speed,
            indoor_limit=indoor_limit,
        )

        if cut_points:
            self.df = detect_transportation(
                self.df,
                self.metadata.crs,
                cut_points,
                window=window,
                pause_fill=pause_fill,
                activity=activity,
                overwrite=overwrite,
            )

        if not overwrite and self.timeline:
            raise ValueError("Timeline already exists. Set 'overwrite' to 'True'.")
        else:
            self.timeline = get_timeline(self.df, crs=self.metadata.crs)

        number_of_trips = self.timeline["trip_id"].nunique()
        log_message(
            self,
            f"Number of trips detected: {number_of_trips}.",
            origin=f"{__name__}.detect_trips",
        )

    def detect_contexts(
        self,
        contexts: gpd.GeoDataFrame,
    ) -> None:
        self.df, contexts_dicts = detect_contexts(
            self.metadata.id, self.df, contexts, self.metadata.crs
        )
        self.contexts = [Context(**context) for context in contexts_dicts]

    def detect_activity_intensity(
        self,
        cut_points: dict[str, Any],
        *,
        overwrite: bool = False,
    ) -> None:
        self.df = detect_activity_intensity(
            self.df,
            cut_points,
            self.metadata.sampling_frequency,
            overwrite=overwrite,
        )

    def detect_wear(
        self,
        min_duration: timedelta,
        interruption_duration: timedelta,
        *,
        overwrite: bool = False,
    ) -> None:
        self.df = detect_wear(
            self.df,
            self.metadata.sampling_frequency,
            min_duration,
            interruption_duration=interruption_duration,
            overwrite=overwrite,
        )

    @property
    def wear_time(
        self,
    ) -> pd.DataFrame:
        return get_wear_time(self.df, self.metadata.sampling_frequency)

    def downsample(
        self,
        sampling_frequency: float,
        *,
        mapper: list[dict[str, Any]] | None = None,
    ) -> None:
        """
        Downsamples the subject's data to the specified sampling frequency.

        This function downsamples the data in the DataFrame from the original sampling frequency to a new sampling frequency.
        The downsampling is done using the methods specified in the mapper for each column. If no mapper is provided, a default
        mapper is used. Columns not included in the mapper are dropped from the DataFrame.

        Args:
            sampling_frequency (float): The new sampling frequency to downsample to in seconds.
            mapper (list[dict[str, Any]], optional): A list of dictionaries that map the columns in the DataFrame to the
                methods used to downsample the data in those columns. Each dictionary should have a 'column' key that specifies
                the column and a 'method' key that specifies the method. Methods are based on the pandas resample method. If not provided, a default mapper is used.

        Returns:
            pd.DataFrame: The downsampled DataFrame.

        Raises:
            ValueError: If the new sampling frequency is less than the original sampling frequency.
        """
        self.df = downsample(
            self.metadata.id,
            self.df,
            self.metadata.sampling_frequency,
            sampling_frequency,
            mapper,
        )
        self.metadata.sampling_frequency = sampling_frequency

    def plot(
        self,
        kind: str,
        *,
        path: Path | str | None = None,
    ) -> Any:
        """
        Plots the subject's data based on the specified kind.

        The kind of plot to produce is specified by the 'kind' argument. The following kinds are supported:
        - 'gps': Plots the subject's raw GPS data.
        - 'timeline': Plots the subject's timeline data (trips with pauses and stationary points).

        Args:
            kind (str): The kind of plot to produce. Must be either 'timeline' or 'gps'.

        Returns:
            Any: The resulting plot.

        Raises:
            ValueError: If 'kind' is not 'timeline' or 'gps', or if 'kind' is 'timeline' but the timeline data does not exist.
        """
        match kind:
            case "timeline":
                if isinstance(self.timeline, pd.DataFrame):
                    df = self.timeline
                else:
                    raise ValueError("Timeline does not exist. Run 'detect_trips'.")
            case "gps":
                df = self.df
            case _:
                raise ValueError(f"Kind '{kind}' not supported.")

        return plot(df, kind, crs=self.metadata.crs, path=path)
