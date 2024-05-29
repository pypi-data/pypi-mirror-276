import abc
import datetime
from types import MappingProxyType
from typing import Optional
from typing import Union

from tecton._internals.tecton_pydantic import StrictModel
from tecton._internals.tecton_pydantic import pydantic_v1
from tecton.aggregation_functions import AggregationFunction
from tecton.framework.configs import LifetimeWindow
from tecton.framework.configs import TimeWindow
from tecton.framework.configs import TimeWindowSeries
from tecton.framework.configs import build_aggregation_proto
from tecton.types import SdkDataType
from tecton_proto.args import feature_view_pb2


class Feature(StrictModel, abc.ABC):
    column: str
    column_dtype: SdkDataType

    @abc.abstractmethod
    def _to_proto(self):
        pass


class Aggregate(Feature):
    function: AggregationFunction
    time_window: Union[TimeWindow, TimeWindowSeries, LifetimeWindow]
    name: Optional[str] = None

    def __init__(
        self,
        column: str,
        column_dtype: SdkDataType,
        function: AggregationFunction,
        time_window: Union[TimeWindow, TimeWindowSeries, LifetimeWindow],
        name: Optional[str] = None,
    ):
        super().__init__(
            column=column, column_dtype=column_dtype, function=function, time_window=time_window, name=name
        )

    @pydantic_v1.validator("time_window", pre=True)
    def timedelta_to_time_window(cls, v):
        if isinstance(v, datetime.timedelta):
            return TimeWindow(window_size=v)
        return v

    @pydantic_v1.validator("function", pre=True)
    def str_to_aggregation_function(cls, v):
        if isinstance(v, str):
            return AggregationFunction(base_name=v, resolved_name=v, params=MappingProxyType({}))
        return v

    def _to_proto(
        self,
        aggregation_interval: datetime.timedelta,
        is_continuous: bool,
        compaction_enabled: bool = False,
        is_streaming_fv: bool = False,
    ) -> feature_view_pb2.FeatureAggregation:
        proto = build_aggregation_proto(
            self.name,
            self.column,
            self.function,
            self.time_window,
            aggregation_interval,
            is_continuous,
            compaction_enabled,
            is_streaming_fv,
        )
        proto.column_dtype.CopyFrom(self.column_dtype.tecton_type.proto)
        return proto


class Attribute(Feature):
    def __init__(self, column: str, column_dtype: SdkDataType):
        super().__init__(column=column, column_dtype=column_dtype)

    def _to_proto(self):
        return feature_view_pb2.Attribute(
            column=self.column,
            column_dtype=self.column_dtype.tecton_type.proto,
        )


class Embedding(Feature):
    model: str
    name: Optional[str] = None

    def __init__(self, column: str, column_dtype: SdkDataType, model: str, name: Optional[str] = None):
        super().__init__(column=column, column_dtype=column_dtype, model=model, name=name)

    def _to_proto(self) -> feature_view_pb2.Embedding:
        name = self.name if self.name else f"{self.column}_embedding"
        return feature_view_pb2.Embedding(
            name=name, column=self.column, column_dtype=self.column_dtype.tecton_type.proto, model=self.model
        )
