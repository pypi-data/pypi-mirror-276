from datetime import datetime
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import attrs
import pendulum
import pypika
import sqlparse
from pypika import NULL
from pypika import AliasedQuery
from pypika import Case
from pypika import Database
from pypika import Field
from pypika import Interval
from pypika import Order
from pypika import Query
from pypika import Table
from pypika import analytics as an
from pypika.analytics import Lag
from pypika.analytics import Lead
from pypika.analytics import RowNumber
from pypika.analytics import Sum
from pypika.functions import Cast
from pypika.functions import Coalesce
from pypika.functions import Length
from pypika.terms import Criterion
from pypika.terms import Function
from pypika.terms import LiteralValue
from pypika.terms import Term
from pypika.terms import WindowFrameAnalyticFunction

from tecton_core import conf
from tecton_core import specs
from tecton_core import time_utils
from tecton_core.aggregation_utils import get_aggregation_function_name
from tecton_core.aggregation_utils import get_simple_window_query
from tecton_core.compute_mode import ComputeMode
from tecton_core.embeddings.config import TextEmbeddingInferenceConfig
from tecton_core.errors import TectonValidationError
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.materialization_context import BoundMaterializationContext
from tecton_core.offline_store import TIME_PARTITION
from tecton_core.offline_store import OfflineStorePartitionParams
from tecton_core.offline_store import OfflineStoreType
from tecton_core.offline_store import PartitionType
from tecton_core.offline_store import get_offline_store_partition_params
from tecton_core.offline_store import get_offline_store_type
from tecton_core.offline_store import timestamp_to_partition_date_str
from tecton_core.offline_store import timestamp_to_partition_epoch
from tecton_core.query import compaction_utils
from tecton_core.query.aggregation_plans import AGGREGATION_PLANS
from tecton_core.query.aggregation_plans import QueryWindowSpec
from tecton_core.query.dialect import Dialect
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.node_interface import DataframeWrapper
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import QueryNode
from tecton_core.query.pipeline_sql_builder import PipelineSqlBuilder
from tecton_core.query.sql_compat import CustomQuery
from tecton_core.query.sql_compat import DuckDBList
from tecton_core.query.sql_compat import DuckDBTupleTerm
from tecton_core.query.sql_compat import LastValue
from tecton_core.query.sql_compat import Values
from tecton_core.query_consts import TECTON_TEMP_AGGREGATION_SECONDARY_KEY_COL
from tecton_core.query_consts import aggregation_group_id
from tecton_core.query_consts import aggregation_tile_id
from tecton_core.query_consts import anchor_time
from tecton_core.query_consts import default_case
from tecton_core.query_consts import tecton_secondary_key_aggregation_indicator_col
from tecton_core.query_consts import tecton_unique_id_col
from tecton_core.query_consts import temp_indictor_column_name
from tecton_core.query_consts import temp_struct_column_name
from tecton_core.query_consts import valid_from
from tecton_core.query_consts import valid_to
from tecton_core.schema import Schema
from tecton_core.specs import MaterializedFeatureViewType
from tecton_core.specs import create_time_window_spec_from_data_proto
from tecton_core.specs.feature_view_spec import OnlineBatchTablePart
from tecton_core.specs.time_window_spec import LifetimeWindowSpec
from tecton_core.specs.time_window_spec import RelativeTimeWindowSpec
from tecton_core.specs.time_window_spec import TimeWindowSeriesSpec
from tecton_core.specs.time_window_spec import TimeWindowSpec
from tecton_core.time_utils import convert_duration_to_seconds
from tecton_core.time_utils import convert_epoch_to_datetime
from tecton_core.time_utils import convert_timedelta_for_version
from tecton_core.time_utils import convert_timestamp_for_version
from tecton_core.time_utils import convert_to_effective_timestamp
from tecton_core.time_utils import get_timezone_aware_datetime
from tecton_proto.args.pipeline_pb2 import DataSourceNode
from tecton_proto.common.aggregation_function_pb2 import AggregationFunction
from tecton_proto.common.data_source_type_pb2 import DataSourceType
from tecton_proto.data import feature_view_pb2


TECTON_CORE_QUERY_NODE_PARAM = "tecton_core_query_node_param"


# If any attribute in a query node has TECTON_CORE_QUERY_NODE_PARAM set to True, that attribute isn't passed to the
# exec node constructor.
def exclude_query_node_params(attribute: attrs.Attribute, _) -> bool:
    return not attribute.metadata.get(TECTON_CORE_QUERY_NODE_PARAM, False)


@attrs.frozen
class MultiOdfvPipelineNode(QueryNode):
    """
    Evaluates multiple ODFVs:
        - Dependent feature view columns are prefixed `udf_internal` (query_constants.UDF_INTERNAL).
        - Each ODFV has a namespace to ensure their features do not conflict with other features
    """

    input_node: NodeRef
    feature_definition_wrappers_namespaces: List[Tuple[FeatureDefinitionWrapper, str]]
    use_namespace_feature_prefix: bool = True

    @property
    def columns(self) -> Sequence[str]:
        output_columns = list(self.input_node.columns)
        for fdw, namespace in self.feature_definition_wrappers_namespaces:
            sep = fdw.namespace_separator
            output_columns += [
                f"{namespace}{sep}{name}" if self.use_namespace_feature_prefix else name
                for name in fdw.view_schema.column_names()
            ]
        return tuple(output_columns)

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        fdw_names = [fdw.name for fdw, _ in self.feature_definition_wrappers_namespaces]
        return f"Evaluate multiple on-demand feature views in pipeline '{fdw_names}'"

    def _to_query(self) -> pypika.queries.QueryBuilder:
        raise NotImplementedError


@attrs.frozen
class FeatureViewPipelineNode(QueryNode):
    inputs_map: Dict[str, NodeRef]
    feature_definition_wrapper: FeatureDefinitionWrapper

    # Needed for correct behavior by tecton_sliding_window udf if it exists in the pipeline
    feature_time_limits: Optional[pendulum.Period]

    # If the node should assert that the schema of the returned data frame matches the feature definition's view schema. Currently only support for spark.
    check_view_schema: bool

    def deepcopy(self) -> "QueryNode":
        inputs_map_deepcopy = {}
        for k, v in self.inputs_map.items():
            inputs_map_deepcopy[k] = v.deepcopy()
        return FeatureViewPipelineNode(
            dialect=self.dialect,
            compute_mode=self.compute_mode,
            inputs_map=inputs_map_deepcopy,
            feature_definition_wrapper=self.feature_definition_wrapper,
            feature_time_limits=self.feature_time_limits,
            check_view_schema=self.check_view_schema,
        )

    @property
    def columns(self) -> Sequence[str]:
        return self.feature_definition_wrapper.view_schema.column_names()

    @property
    def schedule_interval(self) -> pendulum.Duration:
        # Note: elsewhere we set this to
        # pendulum.Duration(seconds=fv_proto.materialization_params.schedule_interval.ToSeconds())
        # but that seemed wrong for bwafv
        return self.feature_definition_wrapper.batch_materialization_schedule

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return list(self.inputs_map.values())

    @property
    def input_names(self) -> Optional[List[str]]:
        return list(self.inputs_map.keys())

    def as_str(self) -> str:
        s = f"Evaluate feature view pipeline '{self.feature_definition_wrapper.name}'"
        if self.feature_time_limits is not None:
            s += f" with feature time limits [{self.feature_time_limits.start}, {self.feature_time_limits.end})"
        return s

    def _to_query(self) -> pypika.queries.QueryBuilder:
        # maps input names to unique strings
        unique_inputs_map = {k: f"{k}_{self.node_id.hex[:8]}" for k in self.inputs_map}
        pipeline_builder = PipelineSqlBuilder(
            pipeline=self.feature_definition_wrapper.pipeline,
            id_to_transformation={t.id: t for t in self.feature_definition_wrapper.transformations},
            materialization_context=BoundMaterializationContext._create_from_period(
                self.feature_time_limits,
                self.schedule_interval,
            ),
            renamed_inputs_map=unique_inputs_map,
        )
        return pipeline_builder.get_pipeline_query(
            dialect=self.dialect, input_name_to_query_map={k: v._to_query() for k, v in self.inputs_map.items()}
        )

    @property
    def output_schema(self) -> Optional[Schema]:
        return self.feature_definition_wrapper.view_schema


@attrs.frozen
class StagingNode(QueryNode):
    """Stages results to the specified location (e.g. in-memory table or S3 bucket)."""

    input_node: NodeRef
    staging_table_name: str
    query_tree_step: QueryTreeStep

    @property
    def columns(self) -> Sequence[str]:
        return self.input_node.columns

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def staging_table_name_unique(self) -> str:
        return f"{self.staging_table_name}_{self.node_id.hex[:8]}"

    def as_str(self):
        return f"Staging data for {self.staging_table_name_unique()}"

    def _to_staging_query_sql(self) -> str:
        fields = [Field(col) for col in self.columns]
        input_query = self.input_node._to_query()
        aliased_input = self.input_node.name
        sql = (
            self.func.query()
            .with_(input_query, aliased_input)
            .from_(AliasedQuery(aliased_input))
            .select(*fields)
            .get_sql()
        )
        if conf.get_bool("DUCKDB_DEBUG"):
            sql = sqlparse.format(sql, reindent=True)
        return sql

    def _to_query(self) -> pypika.queries.QueryBuilder:
        # For non-DuckDB, this is just a passthrough
        return self.input_node._to_query()

    @property
    def output_schema(self):
        return self.input_node.output_schema


@attrs.frozen
class StagedTableScanNode(QueryNode):
    staged_columns: Sequence[str]
    staging_table_name: str

    @classmethod
    def from_staging_node(cls, dialect: Dialect, compute_mode: ComputeMode, query_node: StagingNode) -> QueryNode:
        return cls(
            dialect=dialect,
            compute_mode=compute_mode,
            staged_columns=query_node.columns,
            staging_table_name=query_node.staging_table_name_unique(),
        )

    @property
    def columns(self) -> Sequence[str]:
        return self.staged_columns

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return ()

    def as_str(self):
        return f"Scanning staged data from {self.staging_table_name}"

    def _to_query(self) -> pypika.queries.QueryBuilder:
        # Use table instead of database since otherwise pypika can complain about database
        # being unhashable
        from_str = Table(self.staging_table_name)
        return self.func.query().from_(from_str).select("*")


@attrs.frozen
class DataSourceScanNode(QueryNode):
    """Scans a batch data source and applies the given time range filter, or reads a stream source.

    Attributes:
        ds: The data source to be scanned or read.
        ds_node: The DataSourceNode (proto object, not QueryNode) corresponding to the data source. Used for rewrites.
        is_stream: If True, the data source is a stream source.
        start_time: The start time to be applied.
        end_time: The end time to be applied.
    """

    ds: specs.DataSourceSpec
    ds_node: Optional[DataSourceNode]
    is_stream: bool = attrs.field()
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @property
    def columns(self) -> Sequence[str]:
        if self.ds.type == DataSourceType.STREAM_WITH_BATCH:
            # TODO(brian) - mypy complains this is a Tuple[Any,...]
            return tuple(str(f.name) for f in self.ds.stream_source.spark_schema.fields)
        elif self.ds.type in (DataSourceType.PUSH_NO_BATCH, DataSourceType.PUSH_WITH_BATCH):
            return tuple(str(f.name) for f in self.ds.schema.tecton_schema.columns)
        elif self.ds.type == DataSourceType.BATCH:
            # TODO(TEC-19876): We no longer derive schemas on batch sources, so this field is empty
            # Verify this does not cause issues, and update to code to make the behavior explicit.
            return tuple(str(f.name) for f in self.ds.batch_source.spark_schema.fields)
        else:
            raise NotImplementedError

    # MyPy has a known issue on validators https://mypy.readthedocs.io/en/stable/additional_features.html#id1
    @is_stream.validator  # type: ignore
    def check_no_time_filter(self, _, is_stream: bool) -> None:
        if is_stream and (self.start_time is not None or self.end_time is not None):
            msg = "Raw data filtering cannot be run on a stream source"
            raise ValueError(msg)

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return ()

    def as_str(self) -> str:
        verb = "Read stream source" if self.is_stream else "Scan data source"
        s = f"{verb} '{self.ds.name}'"
        if self.start_time and self.end_time:
            s += f" and apply time range filter [{self.start_time}, {self.end_time})"
        elif self.start_time:
            s += f" and filter by start time {self.start_time}"
        elif self.end_time:
            s += f" and filter by end time {self.end_time}"
        elif not self.is_stream:
            # No need to warn for stream sources since they don't support time range filtering.
            s += ". WARNING: there is no time range filter so all rows will be returned. This can be very inefficient."
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            s += ". WARNING: since start time >= end time, no rows will be returned."
        return s

    def _to_query(self) -> pypika.queries.QueryBuilder:
        if self.is_stream:
            raise NotImplementedError
        source = self.ds.batch_source
        if hasattr(source, "table") and source.table:
            if hasattr(source, "database") and source.database:
                from_str = Database(source.database)
            else:
                from_str = Database(source.project_id)
            if hasattr(source, "schema") and source.schema:
                from_str = from_str.__getattr__(source.schema)
            elif hasattr(source, "dataset") and source.dataset:
                from_str = from_str.__getattr__(source.dataset)
            from_str = from_str.__getattr__(source.table)
        elif hasattr(source, "query") and source.query:
            from_str = CustomQuery(source.query)
        else:
            raise NotImplementedError
        timestamp_field = Field(source.timestamp_field)
        q = self.func.query().from_(from_str).select("*")
        if self.start_time:
            q = q.where(timestamp_field >= self.func.to_timestamp(self.start_time))
        if self.end_time:
            q = q.where(timestamp_field < self.func.to_timestamp(self.end_time))
        return q


@attrs.frozen
class RawDataSourceScanNode(QueryNode):
    """Scans a data source without applying the post processor.

    Attributes:
        ds: The data source to be scanned.
    """

    ds: specs.DataSourceSpec

    @property
    def columns(self) -> Sequence[str]:
        if self.ds.type in {DataSourceType.PUSH_WITH_BATCH, DataSourceType.PUSH_NO_BATCH}:
            return tuple(f.name for f in self.ds.schema.tecton_schema.columns)
        return tuple(f.name for f in self.ds.batch_source.spark_schema.fields)

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return ()

    def as_str(self) -> str:
        return f"Scan data source '{self.ds.name}' without applying a post processor"

    def _to_query(self) -> pypika.queries.QueryBuilder:
        raise NotImplementedError


@attrs.frozen
class OfflineStoreScanNode(QueryNode):
    """
    Fetch values from offline store. Note that time_filter only applies to partitions, not
    actual row timestamps, so you may have rows outside the time_filter range.
    """

    feature_definition_wrapper: FeatureDefinitionWrapper
    partition_time_filter: Optional[pendulum.Period] = None

    @property
    def columns(self) -> Sequence[str]:
        if self.feature_definition_wrapper.compaction_enabled:
            return self.feature_definition_wrapper.view_schema.column_names()

        store_type = get_offline_store_type(self.feature_definition_wrapper)
        cols = self.feature_definition_wrapper.materialization_schema.column_names()
        if store_type == OfflineStoreType.SNOWFLAKE:
            if self.feature_definition_wrapper.is_temporal_aggregate:
                # Snowflake stores the timestamp_key instead of _anchor_time in offline store, but it's not used in QT for aggregates
                cols.remove(default_case(self.feature_definition_wrapper.timestamp_key))
            # anchor time is not included in m13n schema for any snowflake fvs
            cols.append(anchor_time())
        if store_type == OfflineStoreType.PARQUET and self.feature_definition_wrapper.is_temporal:
            # anchor time is not included in m13n schema for bfv/sfv
            cols.append(anchor_time())
        return cols

    def as_str(self) -> str:
        s = f"Scan offline store for '{self.feature_definition_wrapper.name}'"
        if self.partition_time_filter:
            s += f" with feature time limits [{self.partition_time_filter.start}, {self.partition_time_filter.end}]"
        return s

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return ()

    @property
    def store_type(self) -> str:
        return self.feature_definition_wrapper.offline_store_config.WhichOneof("store_type")

    def _to_query(self) -> pypika.queries.QueryBuilder:
        where_conds = self._get_partition_filters()
        fields = self._get_select_fields()
        table_name = self._get_offline_table_name()
        q = self.func.query().from_(Table(table_name)).select(*fields)
        for w in where_conds:
            q = q.where(w)
        return q

    def _get_partition_filters(self) -> List[Term]:
        # Whenever the partition filtering logic is changed, also make sure the changes are applied to the spark
        # version in tecton_spark/offline_store.py
        if not self.partition_time_filter:
            return []

        partition_filters = []
        partition_params = get_offline_store_partition_params(self.feature_definition_wrapper)
        partition_col = Field(partition_params.partition_by)
        if partition_params.partition_by == anchor_time() or (
            partition_params.partition_by == TIME_PARTITION and partition_params.partition_type == PartitionType.EPOCH
        ):
            partition_col = Cast(partition_col, "bigint")
        partition_lower_bound, partition_upper_bound = self._get_partition_bounds(partition_params)

        if partition_lower_bound:
            partition_filters.append(partition_col >= partition_lower_bound)
        if partition_upper_bound:
            partition_filters.append(partition_col <= partition_upper_bound)
        return partition_filters

    def _get_partition_bounds(
        self, partition_params: OfflineStorePartitionParams
    ) -> Tuple[Optional[Union[int, str]], Optional[Union[int, str]]]:
        if not self.partition_time_filter:
            return None, None
        partition_lower_bound = None
        partition_upper_bound = None

        if partition_params.partition_type == PartitionType.DATE_STR:
            if self.partition_time_filter.start:
                partition_lower_bound = timestamp_to_partition_date_str(
                    self.partition_time_filter.start, partition_params
                )
            if self.partition_time_filter.end:
                partition_upper_bound = timestamp_to_partition_date_str(
                    self.partition_time_filter.end, partition_params
                )
        elif partition_params.partition_type == PartitionType.EPOCH:
            if self.partition_time_filter.start:
                partition_lower_bound = timestamp_to_partition_epoch(
                    self.partition_time_filter.start,
                    partition_params,
                    self.feature_definition_wrapper.get_feature_store_format_version,
                )
            if self.partition_time_filter.end:
                partition_upper_bound = timestamp_to_partition_epoch(
                    self.partition_time_filter.end,
                    partition_params,
                    self.feature_definition_wrapper.get_feature_store_format_version,
                )
        elif partition_params.partition_type == PartitionType.RAW_TIMESTAMP:
            if self.partition_time_filter.start:
                partition_lower_bound = self.partition_time_filter.start
            if self.partition_time_filter.end:
                partition_upper_bound = self.partition_time_filter.end

        return partition_lower_bound, partition_upper_bound

    def _get_select_fields(self) -> List[Term]:
        store_type = get_offline_store_type(self.feature_definition_wrapper)
        fields = []
        for col in self.columns:
            if col == TIME_PARTITION:
                continue
            elif col == anchor_time():
                if store_type == OfflineStoreType.SNOWFLAKE:
                    # Convert the timestamp column to unixtime to create the anchor time column
                    # For temporal fvs on snowflake: the offline table stores the event timestamp in the timestamp key column
                    # For temporal aggregate fvs on snowflake: the offline table stores the start of the aggregation tile in the timestamp key column
                    fields.append(
                        self.func.convert_epoch_seconds_to_feature_store_format_version(
                            self.func.to_unixtime(Field(self.feature_definition_wrapper.time_key)),
                            self.feature_definition_wrapper.get_feature_store_format_version,
                        ).as_(anchor_time())
                    )
                # Only parquet store and bwafv delta store have _anchor_time column
                # we probably dont need to actually keep this column in the general parquet case
                elif store_type == OfflineStoreType.PARQUET or self.feature_definition_wrapper.is_temporal_aggregate:
                    fields.append(Cast(Field(anchor_time()), "bigint").as_(anchor_time()))
            else:
                fields.append(col)
        return fields

    def _get_offline_table_name(self) -> str:
        if self.dialect == Dialect.ATHENA:
            workspace_prefix = self.feature_definition_wrapper.workspace.replace("-", "_")
            return f"{workspace_prefix}__{self.feature_definition_wrapper.name}"
        elif self.dialect == Dialect.SNOWFLAKE:
            return self.feature_definition_wrapper.fv_spec.snowflake_view_name
        else:
            raise NotImplementedError


@attrs.frozen
class JoinNode(QueryNode):
    """Join two inputs.

    Attributes:
        left: The left input of the join.
        right: The right input of the join.
        join_cols: The columns to join on.
        how: The type of join. For example, 'inner' or 'left'. This will be passed directly to pyspark.
    """

    left: NodeRef
    right: NodeRef
    join_cols: List[str]
    how: str
    allow_nulls: bool = False

    @property
    def columns(self) -> Sequence[str]:
        right_nonjoin_cols = set(self.right.columns) - set(self.join_cols)
        return tuple(list(self.left.columns) + sorted(right_nonjoin_cols))

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.left, self.right)

    @property
    def input_names(self) -> Optional[List[str]]:
        return ["left", "right"]

    def as_str(self) -> str:
        return f"{self.how.capitalize()} join on {self.join_cols}:"

    def _to_query(self) -> pypika.queries.QueryBuilder:
        left_q = self.left.node._to_query()
        if not conf.get_bool("QUERYTREE_SHORT_SQL_ENABLED"):
            right_q = self.right.node._to_query()
        else:
            right_q = Table(self._get_view_name())

        join_q = self.func.query().from_(left_q)
        if self.how == "inner":
            join_q = join_q.inner_join(right_q)
        elif self.how == "left":
            join_q = join_q.left_join(right_q)
        elif self.how == "right":
            join_q = join_q.right_join(right_q)
        elif self.how == "outer":
            join_q = join_q.outer_join(right_q)
        else:
            msg = f"Join Type {self.how} has not been implemented"
            raise NotImplementedError(msg)
        if self.allow_nulls:
            if self.dialect == Dialect.DUCKDB:
                # optimized join condition, which supports nulls
                left_struct = DuckDBTupleTerm(*[left_q.field(col) for col in self.join_cols])
                right_struct = DuckDBTupleTerm(*[right_q.field(col) for col in self.join_cols])
                join_conditions = left_struct == right_struct
            else:
                join_conditions = Criterion.all(
                    [
                        Criterion.any(
                            [
                                left_q.field(col) == right_q.field(col),
                                left_q.field(col).isnull() and right_q.field(col).isnull(),
                            ]
                        )
                        for col in self.join_cols
                    ]
                )
            right_nonjoin_cols = set(self.right.columns) - set(self.join_cols)
            return join_q.on(join_conditions).select(
                *(left_q.field(col) for col in self.left.columns), *(right_q.field(col) for col in right_nonjoin_cols)
            )
        else:
            return join_q.using(*self.join_cols).select("*")

    def get_sql_views(self, pretty_sql: bool = False) -> List[Tuple[str, str]]:
        if not conf.get_bool("QUERYTREE_SHORT_SQL_ENABLED"):
            return []
        view_sql = self.right.node.to_sql(pretty_sql=pretty_sql)
        return [(self._get_view_name(), view_sql)]

    def _get_view_name(self) -> str:
        return self.right.name + "_" + "view"


@attrs.frozen
class WildcardJoinNode(QueryNode):
    """Outer join two inputs, ensuring that columns being NULL doesn't duplicate rows.

    This behavior is important for wildcards to ensure that we don't grow duplicate NULL wildcard matches.

    Attributes:
        left: The left input of the join.
        right: The right input of the join.
        join_cols: The columns to join on.
    """

    left: NodeRef
    right: NodeRef
    join_cols: List[str]

    @property
    def columns(self) -> Sequence[str]:
        right_nonjoin_cols = set(self.right.columns) - set(self.join_cols)
        return tuple(list(self.left.columns) + list(right_nonjoin_cols))

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.left, self.right)

    def as_str(self, verbose: bool) -> str:
        return "Outer join (include nulls)" + (f" on {self.join_cols}:" if verbose else ":")

    def _to_query(self) -> pypika.queries.QueryBuilder:
        raise NotImplementedError


@attrs.frozen
class EntityFilterNode(QueryNode):
    """Filters the feature data by the entities with respect to a set of entity columns.

    Attributes:
        feature_data: The features to be filtered.
        entities: The entities to filter by.
        entity_cols: The set of entity columns to filter by.
    """

    feature_data: NodeRef
    entities: NodeRef
    entity_cols: List[str]

    @property
    def columns(self) -> Sequence[str]:
        return self.feature_data.columns

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.feature_data, self.entities)

    @property
    def input_names(self) -> Optional[List[str]]:
        return ["feature_data", "entities"]

    def as_str(self) -> str:
        return f"Filter feature data by entities with respect to {self.entity_cols}:"

    def _to_query(self) -> pypika.queries.QueryBuilder:
        if self.dialect == Dialect.DUCKDB:
            # use query optimized for DuckDB
            return self._to_duckdb_query()

        feature_data = self.feature_data._to_query()
        entities = self.entities._to_query()
        # Doing this to allow for nulls in the join columns
        join_conditions = Criterion.all(
            [
                Criterion.any(
                    [
                        feature_data.field(col) == entities.field(col),
                        feature_data.field(col).isnull() and entities.field(col).isnull(),
                    ]
                )
                for col in self.entity_cols
            ]
        )
        return (
            self.func.query()
            .from_(feature_data)
            .inner_join(entities)
            .on(join_conditions)
            .select(*[feature_data.field(col) for col in self.columns])
        )

    def _to_duckdb_query(self):
        """DuckDB switches to NestedLoopJoin when the query contains some extra conditions like `field is null`.
        To work around this we pack all join keys in struct (row in DuckDB terms).
        This will make DuckDB to use hash join and allow null values.
        """
        feature_data = self.feature_data._to_query()
        entities = self.entities._to_query()
        # Doing this to allow for nulls in the join columns
        left_struct = DuckDBTupleTerm(*[feature_data.field(col) for col in self.entity_cols])
        right_struct = DuckDBTupleTerm(*[entities.field(col) for col in self.entity_cols])
        return (
            self.func.query()
            .from_(feature_data)
            .inner_join(entities)
            .on(left_struct == right_struct)
            .select(*[feature_data.field(col) for col in self.columns])
        )

    @property
    def output_schema(self):
        return self.feature_data.output_schema


@attrs.frozen
class AsofJoinInputContainer:
    node: NodeRef
    timestamp_field: str  # spine or feature timestamp
    effective_timestamp_field: Optional[str] = None
    prefix: Optional[str] = None
    # The right side of asof join needs to know a schema to typecast
    # back to original types in snowflake, because the asof implementation loses
    # types in the middle.
    schema: Optional[Schema] = None

    def deepcopy(self) -> "AsofJoinInputContainer":
        return AsofJoinInputContainer(
            node=self.node.deepcopy(),
            timestamp_field=self.timestamp_field,
            effective_timestamp_field=self.effective_timestamp_field,
            prefix=self.prefix,
            schema=self.schema,
        )


@attrs.frozen
class AsofJoinNode(QueryNode):
    """
    A "basic" asof join on 2 inputs
    """

    left_container: AsofJoinInputContainer
    right_container: AsofJoinInputContainer
    join_cols: List[str]

    _right_struct_col: ClassVar[str] = "_right_values_struct"

    def deepcopy(self) -> "QueryNode":
        return AsofJoinNode(
            dialect=self.dialect,
            compute_mode=self.compute_mode,
            left_container=self.left_container.deepcopy(),
            right_container=self.right_container.deepcopy(),
            join_cols=self.join_cols,
        )

    @property
    def columns(self) -> Sequence[str]:
        return tuple(
            list(self.left_container.node.columns)
            + [
                f"{self.right_container.prefix}_{col}"
                for col in self.right_container.node.columns
                if col not in (self.join_cols)
            ]
        )

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.left_container.node, self.right_container.node)

    @property
    def input_names(self) -> Optional[List[str]]:
        return ["left", "right"]

    def as_str(self) -> str:
        return f"Left asof join right, where the join condition is right.{self.right_container.effective_timestamp_field} <= left.{self.left_container.timestamp_field}"

    def _to_query(self) -> pypika.queries.QueryBuilder:
        ASOF_JOIN_TIMESTAMP_COL_1 = "_ASOF_JOIN_TIMESTAMP_1"
        ASOF_JOIN_TIMESTAMP_COL_2 = "_ASOF_JOIN_TIMESTAMP_2"
        IS_LEFT = "IS_LEFT"
        left_df = self.left_container.node._to_query()
        right_df = self.right_container.node._to_query()
        # The left and right dataframes are unioned together and sorted using 2 columns.
        # The spine will use the spine timestamp and the features will be ordered by their
        # (effective_timestamp, feature_timestamp) because multiple features can have the same effective
        # timestamp. We want to return the closest feature to the spine timestamp that also satisfies
        # the condition => effective timestamp <= spine timestamp.
        # The ASOF_JOIN_TIMESTAMP_COL_1 and ASOF_JOIN_TIMESTAMP_COL_2 columns will be used for sorting.
        left_name = self.left_container.node.name
        right_name = self.right_container.node.name
        left_df = (
            self.func.query()
            .with_(left_df, left_name)
            .from_(AliasedQuery(left_name))
            .select(
                Table(left_name).star,
                Field(self.left_container.timestamp_field).as_(ASOF_JOIN_TIMESTAMP_COL_1),
                Field(self.left_container.timestamp_field).as_(ASOF_JOIN_TIMESTAMP_COL_2),
            )
        )
        right_df = (
            self.func.query()
            .with_(right_df, right_name)
            .from_(AliasedQuery(right_name))
            .select(
                Field(self.right_container.effective_timestamp_field).as_(ASOF_JOIN_TIMESTAMP_COL_1),
                Field(self.right_container.timestamp_field).as_(ASOF_JOIN_TIMESTAMP_COL_2),
                Table(right_name).star,
            )
        )

        # includes both fv join keys and the temporal asof join key
        timestamp_join_cols = [ASOF_JOIN_TIMESTAMP_COL_1, ASOF_JOIN_TIMESTAMP_COL_2]
        common_cols = self.join_cols + timestamp_join_cols
        left_nonjoin_cols = [col for col in self.left_container.node.columns if col not in common_cols]
        # we additionally include the right time field though we join on the left's time field.
        # This is so we can see how old the row we joined against is and later determine whether to exclude on basis of ttl
        right_nonjoin_cols = [
            col for col in self.right_container.node.columns if col not in set(self.join_cols + timestamp_join_cols)
        ]
        left_full_cols = (
            [LiteralValue(True).as_(IS_LEFT)]
            + [Field(x) for x in common_cols]
            + [Field(x) for x in left_nonjoin_cols]
            + [NULL.as_(self._right_struct_col)]
        )
        right_full_cols = (
            [LiteralValue(False).as_(IS_LEFT)]
            + [Field(x) for x in common_cols]
            + [NULL.as_(x) for x in left_nonjoin_cols]
            + [self.func.struct(right_nonjoin_cols).as_(self._right_struct_col)]
        )
        left_df = self.func.query().from_(left_df).select(*left_full_cols)
        right_df = self.func.query().from_(right_df).select(*right_full_cols)
        union = left_df.union_all(right_df)
        right_window_funcs = []
        # Also order by IS_LEFT because we want spine rows to be after feature rows if
        # timestamps are the same
        order_by_fields = [*timestamp_join_cols, IS_LEFT]
        right_window_funcs.append(
            LastValue(self.dialect, Field(self._right_struct_col))
            .over(*[Field(x) for x in self.join_cols])
            .orderby(*[Field(x) for x in order_by_fields])
            .rows(an.Preceding(), an.CURRENT_ROW)
            .ignore_nulls()
            .as_(self._right_struct_col)
        )

        # We use the right side of asof join to find the latest values to augment to the rows from the left side.
        # Then, we drop the right side's rows.
        res = (
            self.func.query()
            .from_(union)
            .select(*(common_cols + left_nonjoin_cols + right_window_funcs + [Field(IS_LEFT)]))
        )
        assert self.right_container.schema is not None
        right_fields = self.func.struct_extract(
            self._right_struct_col,
            right_nonjoin_cols,
            [f"{self.right_container.prefix}_{name}" for name in right_nonjoin_cols],
            self.right_container.schema.to_dict(),
        )
        res = (
            self.func.query().from_(res).select(*(common_cols + left_nonjoin_cols + right_fields)).where(Field(IS_LEFT))
        )
        return res


@attrs.frozen
class AsofJoinFullAggNode(QueryNode):
    """
    Asof join full agg rollup
    """

    spine: NodeRef
    partial_agg_node: NodeRef
    fdw: FeatureDefinitionWrapper

    # Whether QT should rewrite the subtree from this node to push down timestamps.
    enable_spine_time_pushdown_rewrite: bool = attrs.field(metadata={TECTON_CORE_QUERY_NODE_PARAM: True})

    # Whether QT should rewrite the subtree from this node to push down entity.
    enable_spine_entity_pushdown_rewrite: bool = attrs.field(metadata={TECTON_CORE_QUERY_NODE_PARAM: True})

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.spine, self.partial_agg_node)

    @property
    def input_names(self) -> Optional[List[str]]:
        return ["spine", "partial_aggregates"]

    def as_str(self) -> str:
        return "Events asof join partial aggregates, where the join condition is partial_aggregates._anchor_time <= events._anchor_time and partial aggregates are rolled up to compute full aggregates"

    @property
    def columns(self) -> Sequence[str]:
        cols = list(self.spine.columns)
        cols += [f.output_feature_name for f in self.fdw.trailing_time_window_aggregation.features]
        cols += (
            [
                temp_indictor_column_name(secondary_key_output.time_window)
                for secondary_key_output in self.fdw.materialized_fv_spec.secondary_key_rollup_outputs
            ]
            if self.fdw.aggregation_secondary_key
            else []
        )
        return cols

    def _timestamp_to_window_edge(self, timestamp: int) -> WindowFrameAnalyticFunction.Edge:
        """
        Creates a pypika window edge from a given timestamp.
        Negative timestamps are treated as PRECEDING boundry specifiers, and positives ones as FOLLOWING.
        """
        if timestamp <= 0:
            # pyspark converts negative edges into Preceding terms automagically,
            # but we need to handle these explicitly in the pypika world
            return an.Preceding(abs(timestamp))
        return an.Following(timestamp)

    def _get_time_range_for_window_spec(
        self, time_window: TimeWindowSpec
    ) -> Tuple[WindowFrameAnalyticFunction.Edge, WindowFrameAnalyticFunction.Edge]:
        if isinstance(time_window, RelativeTimeWindowSpec):
            range_start, range_end = self.fdw.time_range_for_relative_time_window(time_window)
            # We adjust the range by (*2 - 1) here to ensure the row is sorted just prior to the feature row (*2), followed by the spine row (*2 + 1)
            window_start, window_end = (
                self._timestamp_to_window_edge(range_start * 2 - 1),
                self._timestamp_to_window_edge(range_end * 2 - 1),
            )
            return window_start, window_end
        elif isinstance(time_window, TimeWindowSeriesSpec):
            range_start, range_end = self.fdw.time_range_for_relative_time_window(
                RelativeTimeWindowSpec(
                    window_start=time_window.window_series_start, window_end=time_window.window_series_end
                )
            )
            window_start, window_end = (
                self._timestamp_to_window_edge(range_start * 2 - 1),
                self._timestamp_to_window_edge(range_end * 2 - 1),
            )
            return window_start, window_end
        if isinstance(time_window, LifetimeWindowSpec):
            return an.Preceding(), an.CURRENT_ROW

        msg = f"Unsupported time_window type: {type(time_window)}"
        raise TypeError(msg)

    def _get_time_range_for_aggregation(
        self, feature: feature_view_pb2.AggregateFeature
    ) -> Tuple[Union[str, WindowFrameAnalyticFunction.Edge], Union[str, WindowFrameAnalyticFunction.Edge]]:
        """
        Returns the start and end time range markers for the given aggregate feature, based on its time_window spec
        """

        # Athena does not support RANGE BETWEEN queries very well, so we're continuing to use the legacy windowing logic for it.
        # This means aggregation offsets won't work for Athena.
        # See: https://github.com/tecton-ai/tecton/pull/19177#discussion_r1496697395
        if self.dialect != Dialect.ATHENA and feature.HasField("time_window"):
            time_window = create_time_window_spec_from_data_proto(feature.time_window)
            return self._get_time_range_for_window_spec(time_window)

        # Legacy flow for tecton SDK <=0.7 and Athena
        # We do + 1 since RangeBetween is inclusive, and we do not want to include the last row of the
        # previous tile. See https://github.com/tecton-ai/tecton/pull/1110
        if feature.HasField("window"):
            # This is the legacy way to specify an aggregation window
            window_duration = pendulum.Duration(seconds=feature.window.ToSeconds())
        else:
            time_window = create_time_window_spec_from_data_proto(feature.time_window)
            window_duration = pendulum.Duration(seconds=time_window.window_duration.total_seconds())
        if self.fdw.is_continuous:
            tile_interval = 1
        else:
            tile_interval = self.fdw.get_tile_interval_for_version
        earliest_anchor_time = (
            convert_timedelta_for_version(window_duration, self.fdw.get_feature_store_format_version) - tile_interval
        )
        # Adjust earliest_anchor_time by * 2 + 1 to account for the changes to TECTON_WINDOW_ORDER_COL
        earliest_anchor_time = an.Preceding(earliest_anchor_time * 2 + 1)
        return earliest_anchor_time, an.CURRENT_ROW

    def _get_aggregations(self, window_order_col: str, partition_cols: List[str]) -> List[Term]:
        time_aggregation = self.fdw.trailing_time_window_aggregation
        aggregations = []
        for feature in time_aggregation.features:
            aggregation_plan = AGGREGATION_PLANS.get(feature.function)
            if callable(aggregation_plan):
                aggregation_plan = aggregation_plan(
                    Field(anchor_time()), feature.function_params, time_aggregation.is_continuous
                )

            if not aggregation_plan or not aggregation_plan.is_supported(self.dialect):
                msg = (
                    f"Aggregation {get_aggregation_function_name(feature.function)} is not supported by "
                    f"{self.compute_mode.name} compute"
                )
                raise TectonValidationError(msg, can_drop_traceback=True)

            names = aggregation_plan.materialized_column_names(feature.input_feature_name)
            window_spec = create_time_window_spec_from_data_proto(feature.time_window)
            if isinstance(window_spec, TimeWindowSeriesSpec):
                for relative_time_window in window_spec.time_windows:
                    range_start, range_end = self._get_time_range_for_window_spec(relative_time_window)
                    query_window_spec = QueryWindowSpec(
                        partition_cols=partition_cols,
                        order_by_col=window_order_col,
                        range_start=range_start,
                        range_end=range_end,
                    )
                    aggregations.append(
                        aggregation_plan.full_aggregation_query_term(names, query_window_spec).as_(
                            feature.output_feature_name + "_" + relative_time_window.to_string()
                        )
                    )
            else:
                range_start, range_end = self._get_time_range_for_aggregation(feature)
                query_window_spec = QueryWindowSpec(
                    partition_cols=partition_cols,
                    order_by_col=window_order_col,
                    range_start=range_start,
                    range_end=range_end,
                )
                aggregations.append(
                    aggregation_plan.full_aggregation_query_term(names, query_window_spec).as_(
                        feature.output_feature_name
                    )
                )

        if self.fdw.aggregation_secondary_key:
            for secondary_key_output in self.fdw.materialized_fv_spec.secondary_key_rollup_outputs:
                range_start, range_end = self._get_time_range_for_window_spec(secondary_key_output.time_window)
                query_window_spec = QueryWindowSpec(
                    partition_cols=partition_cols,
                    order_by_col=window_order_col,
                    range_start=range_start,
                    range_end=range_end,
                )
                aggregations.append(
                    get_simple_window_query(
                        col=tecton_secondary_key_aggregation_indicator_col(),
                        query_window_spec=query_window_spec,
                        analytic_function=Sum,
                    ).as_(temp_indictor_column_name(secondary_key_output.time_window))
                )
        return aggregations

    def _to_query(self) -> pypika.queries.QueryBuilder:
        # Snowflake has its own implementation of asof join, and this only works for Athena, DuckDB, and Spark
        assert self.dialect in (Dialect.ATHENA, Dialect.DUCKDB, Dialect.SPARK)
        left_df = self.spine.node._to_query()
        right_df = self.partial_agg_node.node._to_query()
        join_keys = self.fdw.join_keys
        if self.fdw.aggregation_secondary_key:
            join_keys.append(self.fdw.aggregation_secondary_key)

        timestamp_join_cols = [anchor_time()]
        common_cols = join_keys + timestamp_join_cols
        left_nonjoin_cols = list(set(self.spine.node.columns) - set(common_cols))
        left_prefix = "_tecton_left"
        right_nonjoin_cols = list(set(self.partial_agg_node.node.columns) - set(join_keys + timestamp_join_cols))
        IS_LEFT = "_tecton_is_left"
        # Since the spine and feature rows are unioned together, the spine rows must be ordered after the feature rows
        # when they have the same ANCHOR_TIME for window aggregation to be correct. Window aggregation does not allow
        # ordering using two columns when range between is used. So we adjust the spine row ANCHOR_TIME by * 2 + 1, and the
        # feature row ANCHOR_TIME by * 2. Range between values will also be adjusted due to these changes.
        TECTON_WINDOW_ORDER_COL = "_tecton_window_order_col"
        left_full_cols = (
            [LiteralValue(True).as_(IS_LEFT)]
            + [Field(x) for x in common_cols]
            + [Field(x).as_(f"{left_prefix}_{x}") for x in left_nonjoin_cols]
            + [NULL.as_(x) for x in right_nonjoin_cols]
            + [(Cast(Field(anchor_time()) * 2 + 1, "bigint")).as_(TECTON_WINDOW_ORDER_COL)]
        )
        right_full_cols = (
            [LiteralValue(False).as_(IS_LEFT)]
            + [Field(x) for x in common_cols]
            + [NULL.as_(f"{left_prefix}_{x}") for x in left_nonjoin_cols]
            + [Field(x) for x in right_nonjoin_cols]
            + [(Cast(Field(anchor_time()) * 2, "bigint")).as_(TECTON_WINDOW_ORDER_COL)]
        )
        if self.fdw.aggregation_secondary_key:
            left_full_cols.append(NULL.as_(tecton_secondary_key_aggregation_indicator_col()))
            right_full_cols.append(LiteralValue("1").as_(tecton_secondary_key_aggregation_indicator_col()))

        left_df = self.func.query().from_(left_df).select(*left_full_cols)
        right_df = self.func.query().from_(right_df).select(*right_full_cols)
        union = left_df.union_all(right_df)
        aggregations = self._get_aggregations(TECTON_WINDOW_ORDER_COL, join_keys)
        output_columns = (
            common_cols
            + [Field(f"{left_prefix}_{x}").as_(x) for x in left_nonjoin_cols]
            + aggregations
            + [Field(IS_LEFT)]
        )

        array_features = []
        for feature in self.fdw.trailing_time_window_aggregation.features:
            window_spec = create_time_window_spec_from_data_proto(feature.time_window)
            if isinstance(window_spec, TimeWindowSeriesSpec):
                names = []
                for relative_time_window in window_spec.time_windows:
                    names.append(feature.output_feature_name + "_" + relative_time_window.to_string())
                array_features.append(
                    Function("LIST_VALUE", *[Field(n) for n in names]).as_(feature.output_feature_name)
                )

        res = self.func.query().from_(union).select(*output_columns, *array_features)

        return self.func.query().from_(res).select(*[Field(c) for c in self.columns]).where(Field(IS_LEFT))


@attrs.frozen
class AsofSecondaryKeyExplodeNode(QueryNode):
    """
    This node explodes a spine that misses the secondary key, into a spine that has the secondary key. This is needed
    in two scenarios:
        1. A Feature View with an aggregation_secondary_key: an aggregation_secondary_key is never in the spine,
        so we always need to explode the spine for it.
        2. A Feature View with a wild card join key: a wild card join key is optional in the spine, so we need to
        explode the spine if and only if the wild card join key is not present.

    This node looks back the max aggregation interval or TTL of the feature view to find the secondary key values by
    using a window based `collect_set` function with an as-of join between left and right dataframes. Using the max
    aggregation interval can help us find all the secondary key values in all windows with a single window based
    `collect_set` function.

    E.g. Let's say a FV has fully bound join_key `A` and a secondary key `C`.
    For every row `[a_0, anchor_0]` from the spine, we will have the following rows in the
    returned dataframe:
       [a_0  c_1  anchor_0]
       [a_0  c_2  anchor_0]
        .    .    .
       [a_0  c_k  anchor_0]
    where (`c_1`, ..., `c_k`) represent all the secondary key values such that, the following row is
    present inside `right`:
        [a_0, c_i, anchor_i]
    and:
        anchor_0 - max_feature_agg_period (or ttl) < anchor_i <= anchor_0.

    Attributes:
         left: The spine node that misses the secondary key.
         left_ts: The timestamp column of the spine node.
         right: The feature value node that contains the secondary key.
         right_ts: The timestamp column of the feature value node.
    """

    left: NodeRef
    left_ts: str
    right: NodeRef
    right_ts: str
    fdw: FeatureDefinitionWrapper

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.left, self.right)

    @property
    def input_names(self) -> Optional[List[str]]:
        return ["left", "right"]

    def as_str(self) -> str:
        return "Left asof wildcard match and explode right, where the join condition is left._anchor_time - ttl + 1 < right._anchor_time <= left._anchor_time."

    @property
    def columns(self) -> Sequence[str]:
        if self.fdw.is_temporal_aggregate and self.fdw.aggregation_secondary_key:
            return (*list(self.left.columns), self.fdw.aggregation_secondary_key)

        return (*list(self.left.columns), self.fdw.wildcard_join_key)

    def _to_query(self) -> pypika.queries.QueryBuilder:
        if self.dialect != Dialect.DUCKDB:
            raise NotImplementedError

        secondary_key = (
            self.fdw.aggregation_secondary_key
            if self.fdw.is_temporal_aggregate and self.fdw.aggregation_secondary_key
            else self.fdw.wildcard_join_key
        )

        spine_q = self.left._to_query()
        projected_features_q = (
            self.func.query().from_(self.right._to_query()).select(secondary_key, self.right_ts, *self.fdw.join_keys)
        )

        # using structs to handle null values in join keys
        left_struct = DuckDBTupleTerm(*[spine_q.field(col) for col in self.fdw.join_keys])
        right_struct = DuckDBTupleTerm(*[projected_features_q.field(col) for col in self.fdw.join_keys])
        join_condition = left_struct == right_struct

        spine_timestamp_field = spine_q.field(self.left_ts)
        features_timestamp_field = projected_features_q.field(self.right_ts)
        join_condition &= spine_timestamp_field >= features_timestamp_field

        if not (self.fdw.is_temporal_aggregate and self.fdw.has_lifetime_aggregate):
            # we use exclusive range at the lower boundary, so no need to do adjustments on earliest_anchor_time
            if self.fdw.is_temporal_aggregate:
                earliest_anchor_time = self.fdw.earliest_window_start
            else:
                earliest_anchor_time = -self.fdw.serving_ttl

            earliest_timestamp = convert_timedelta_for_version(
                earliest_anchor_time, self.fdw.get_feature_store_format_version
            )
            join_condition &= spine_timestamp_field + earliest_timestamp < features_timestamp_field

        secondary_key_field = Function("LIST", projected_features_q.field(secondary_key))
        secondary_key_field = Function("LIST_DISTINCT", secondary_key_field)
        # replace empty list with list(null) to keep the original row after unnest
        secondary_key_field = (
            Case().when(Length(secondary_key_field) == 0, LiteralValue("[null]")).else_(secondary_key_field)
        )
        secondary_key_field = Function("UNNEST", secondary_key_field)

        return (
            self.func.query()
            .from_(spine_q)
            .left_join(projected_features_q)
            .on(join_condition)
            .groupby(*self.left.columns)
            .select(*[spine_q.field(c).as_(c) for c in self.left.columns] + [secondary_key_field.as_(secondary_key)])
        )


@attrs.frozen
class AggregationSecondaryKeyExplodeNode(QueryNode):
    """
    This node returns all <entity, aggregation secondary key> pairs from the input node. It's used for retrieving
    secondary key aggregate features without spine.

    This node is similar to AsofSecondaryKeyExplodeNode but doesn't require as-of join. It uses entities and
    anchor time to look back the max aggregation window time to find all secondary key values, and build a spine with
    all of them.
    """

    input_node: NodeRef
    join_keys: List[str]
    aggregation_secondary_key: str
    has_lifetime_aggregate: bool
    earliest_anchor_time_from_window_start: Optional[int]

    @classmethod
    def for_feature_definition(
        cls, dialect: Dialect, compute_mode: ComputeMode, spine: NodeRef, fdw: FeatureDefinitionWrapper
    ) -> NodeRef:
        return cls(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=spine,
            join_keys=fdw.join_keys,
            aggregation_secondary_key=fdw.aggregation_secondary_key,
            has_lifetime_aggregate=fdw.has_lifetime_aggregate,
            earliest_anchor_time_from_window_start=fdw.earliest_anchor_time_from_window_start(fdw.earliest_window_start)
            if not fdw.has_lifetime_aggregate
            else None,
        ).as_ref()

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        return f"Use entities {self.join_keys} to find all values for aggregation secondary key '{self.aggregation_secondary_key}' to build a spine."

    @property
    def columns(self) -> Sequence[str]:
        return self.input_node.columns

    def _to_query(self) -> pypika.queries.QueryBuilder:
        if self.dialect != Dialect.DUCKDB:
            raise NotImplementedError

        input_query = self.input_node._to_query()

        window_start: WindowFrameAnalyticFunction.Edge = (
            an.Preceding()
            if self.has_lifetime_aggregate
            else an.Preceding(abs(self.earliest_anchor_time_from_window_start))
        )

        window_spec = QueryWindowSpec(
            partition_cols=self.join_keys,
            order_by_col=anchor_time(),
            range_start=window_start,
            range_end=an.CURRENT_ROW,
        )

        columns = [Field(col) for col in self.columns if col != self.aggregation_secondary_key and col != anchor_time()]

        # Collect all secondary key values within the aggregation window, and explode them to build a spine.
        # Note the window based `list` applies to every single row, so if a single join key has multiple
        # aggregation secondary keys with the same anchor time, the result dataframe will have multiple same rows for
        # that particular join key and anchor time. We select distinct here to deduplicate.
        pre_agg = Query.from_(input_query).select(
            *columns,
            anchor_time(),
            get_simple_window_query(
                col=self.aggregation_secondary_key,
                analytic_function=DuckDBList,
                query_window_spec=window_spec,
            ).as_(TECTON_TEMP_AGGREGATION_SECONDARY_KEY_COL),
        )

        main_query = (
            Query.from_(pre_agg)
            .select(
                *columns,
                anchor_time(),
                Function("UNNEST", Field(TECTON_TEMP_AGGREGATION_SECONDARY_KEY_COL)).as_(
                    self.aggregation_secondary_key
                ),
            )
            .distinct()
        )

        return main_query


@attrs.frozen
class PartialAggNode(QueryNode):
    """Performs partial aggregations.

    Should only be used on WAFVs.

    For non-continuous WAFV, the resulting dataframe will have an anchor time column that represents the start times of
    the tiles. For a continuous SWAFV, since there are no tiles, the resulting dataframe will have an anchor time column
    that is just a copy of the input timestamp column. And it will also call it "_anchor_time".

    Attributes:
        input_node: The input node to be transformed.
        fdw: The feature view to be partially aggregated.
        window_start_column_name: The name of the anchor time column.
        window_end_column_name: If set, a column will be added to represent the end times of the tiles, and it will
            have name `window_end_column_name`. This is ignored for continuous mode.
        aggregation_anchor_time: If set, it will be used to determine the offset for the tiles.
        create_tiles: If set to True, the resulting dataframe will be tiled by the aggregation interval. If set to False, the resulting dataframe will have an anchor time column
            that is just a copy of the input timestamp column. If set to None, the default behavior for the fv type will be used (ie continuous vs non-continuous).
    """

    input_node: NodeRef
    fdw: FeatureDefinitionWrapper = attrs.field()
    window_start_column_name: str
    window_end_column_name: Optional[str] = None
    aggregation_anchor_time: Optional[datetime] = None
    create_tiles: Optional[bool] = None

    @property
    def columns(self) -> Sequence[str]:
        cols = list(self.fdw.materialization_schema.column_names())
        # TODO(danny): Move this logic into just the Snowflake version of this node
        # Snowflake stores timestamp key in offline store, so it has timestamp key in materialized schema.
        # But we are returning _ANCHOR_TIME here for partial agg node.
        if self.dialect == Dialect.SNOWFLAKE:
            cols = [col for col in cols if col != self.fdw.timestamp_key] + [anchor_time()]
        # TODO(Felix) this is janky
        if self.window_end_column_name is not None and not self.fdw.is_continuous:
            cols.append(self.window_end_column_name)
        return tuple(cols)

    @fdw.validator
    def check_is_aggregate(self, _, value):
        if not value.is_temporal_aggregate:
            msg = "Cannot construct a PartialAggNode using a non-aggregate feature view."
            raise ValueError(msg)

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        actions = [
            f"Perform partial aggregations with column '{self.window_start_column_name}' as the start time of tiles."
        ]
        if self.window_end_column_name:
            actions.append(f"Add column '{self.window_end_column_name}' as the end time of tiles.")
        if self.aggregation_anchor_time:
            actions.append(
                f"Align column '{self.fdw.timestamp_key}' to the offset determined by {self.aggregation_anchor_time}."
            )
        return " ".join(actions)

    def _to_query(self) -> pypika.queries.QueryBuilder:
        q = self.func.query().from_(self.input_node._to_query())
        time_aggregation = self.fdw.trailing_time_window_aggregation
        timestamp_field = Field(time_aggregation.time_key)

        raw_agg_cols_and_names = self._get_partial_agg_columns_and_names()
        agg_cols = [agg_col.as_(alias) for agg_col, alias in raw_agg_cols_and_names]
        partition_cols = [Field(join_key) for join_key in self.fdw.partial_aggregate_group_by_columns]
        if not time_aggregation.is_continuous:
            slide_seconds = time_aggregation.aggregation_slide_period.seconds
            anchor_time_offset_seconds = 0
            if self.aggregation_anchor_time:
                # Compute the offset from the epoch such that anchor_time aligns to an interval boundary of size
                # aggregation_slide_period. i.e. `epoch + offset + (X * slide_period) = anchor_time`, where X is
                # an integer.
                anchor_time_epoch_secs = int(get_timezone_aware_datetime(self.aggregation_anchor_time).timestamp())
                anchor_time_offset_seconds = anchor_time_epoch_secs % slide_seconds

            adjusted_time_key_field = self.func.to_unixtime(timestamp_field) - anchor_time_offset_seconds
            window_start = (
                self.func.to_unixtime(
                    self.func.from_unixtime(adjusted_time_key_field - (adjusted_time_key_field % slide_seconds))
                )
                + anchor_time_offset_seconds
            )
            window_end = (
                self.func.to_unixtime(
                    self.func.from_unixtime(
                        adjusted_time_key_field - (adjusted_time_key_field % slide_seconds) + slide_seconds
                    )
                )
                + anchor_time_offset_seconds
            )

            window_start = self.func.convert_epoch_seconds_to_feature_store_format_version(
                window_start, self.fdw.get_feature_store_format_version
            )
            window_end = self.func.convert_epoch_seconds_to_feature_store_format_version(
                window_end, self.fdw.get_feature_store_format_version
            )

            select_cols = agg_cols + partition_cols + [window_start.as_(self.window_start_column_name)]
            group_by_cols = [*partition_cols, window_start]
            if self.window_end_column_name:
                select_cols.append(window_end.as_(self.window_end_column_name))
                group_by_cols.append(window_end)
            q = q.groupby(*group_by_cols)
        else:
            # Continuous
            select_cols = (
                agg_cols
                + partition_cols
                + [
                    timestamp_field,
                    self.func.convert_epoch_seconds_to_feature_store_format_version(
                        self.func.to_unixtime(Field(time_aggregation.time_key)),
                        self.fdw.get_feature_store_format_version,
                    ).as_(anchor_time()),
                ]
            )
        res = q.select(*select_cols)
        return res

    def _get_partial_agg_columns_and_names(self) -> List[Tuple[Term, str]]:
        """
        Snowflake overrides this method to use snowflake specific aggregation functions
        """
        time_aggregation = self.fdw.trailing_time_window_aggregation
        agg_cols = []
        output_columns = set()
        for feature in time_aggregation.features:
            aggregation_plan = AGGREGATION_PLANS.get(feature.function)
            if callable(aggregation_plan):
                aggregation_plan = aggregation_plan(
                    Field(time_aggregation.time_key), feature.function_params, time_aggregation.is_continuous
                )

            if not aggregation_plan or not aggregation_plan.is_supported(self.dialect):
                msg = (
                    f"Aggregation {get_aggregation_function_name(feature.function)} is not supported by {self.dialect}"
                )
                raise NotImplementedError(msg)

            if time_aggregation.is_continuous:
                if aggregation_plan.continuous_aggregation_query_terms is None:
                    msg = f"Continuous mode is not supported for aggregation {get_aggregation_function_name(feature.function)} with dialect {self.dialect}"
                    raise NotImplementedError(msg)

                agg_query_terms = aggregation_plan.continuous_aggregation_query_terms(feature.input_feature_name)
            else:
                agg_query_terms = aggregation_plan.partial_aggregation_query_terms(feature.input_feature_name)

            for column_name, aggregated_column in zip(
                aggregation_plan.materialized_column_names(feature.input_feature_name),
                agg_query_terms,
            ):
                if column_name in output_columns:
                    continue
                output_columns.add(column_name)
                agg_cols.append((aggregated_column, column_name))
        return agg_cols


@attrs.frozen
class AddAnchorTimeNode(QueryNode):
    """Augment a dataframe with an anchor time column that represents the batch materialization window.

    This is useful for preparing a dataframe for materialization, as the materialization logic requires an anchor time
    column for BFVs and BWAFVs. The anchor time is the start time of the materialization window, so it is calculated as
    window('timestamp_field', batch_schedule).start. The resulting column will use seconds format for BFVs and
    nanoseconds for BWAFVS. This is controlled via `feature_store_format_version` parameter,
    which is set to NANOS for BWAFVs.

    Attributes:
        input_node: The input node to be transformed.
        feature_store_format_version: The feature store format version for the FV, which determines whether its
            timestamp is in seconds or nanoseconds.
        batch_schedule: The batch materialization schedule for the feature view, with units determined by `feature_store_format_version`.
        timestamp_field: The column name of the feature timestamp field.
    """

    input_node: NodeRef
    feature_store_format_version: int
    batch_schedule: int
    timestamp_field: str

    @staticmethod
    def for_feature_definition(
        dialect: Dialect, compute_mode: ComputeMode, fd: FeatureDefinitionWrapper, input_node: NodeRef
    ) -> NodeRef:
        return AddAnchorTimeNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=input_node,
            feature_store_format_version=fd.get_feature_store_format_version,
            batch_schedule=fd.get_batch_schedule_for_version,
            timestamp_field=fd.timestamp_key,
        ).as_ref()

    @property
    def columns(self) -> Sequence[str]:
        return (*self.input_node.columns, anchor_time())

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        return (
            "Add anchor time column '_anchor_time' to represent the materialization window. "
            f"It is calculated as window('{self.timestamp_field}', batch_schedule).start where batch_schedule = "
            f"{convert_duration_to_seconds(self.batch_schedule, self.feature_store_format_version)} seconds."
        )

    def _to_query(self) -> pypika.queries.QueryBuilder:
        input_query = self.input_node._to_query()
        uid = self.input_node.name
        epoch_field = self.func.to_unixtime(Field(self.timestamp_field))
        epoch_field = self.func.convert_epoch_seconds_to_feature_store_format_version(
            epoch_field, self.feature_store_format_version
        )
        anchor_field = (epoch_field - epoch_field % self.batch_schedule).as_(anchor_time())
        return self.func.query().with_(input_query, uid).from_(AliasedQuery(uid)).select("*", anchor_field)


@attrs.frozen
class AddRetrievalAnchorTimeNode(QueryNode):
    """Augment a dataframe with an anchor time column that represents the most recent features available for retrieval.

    This node should only be used on WAFVs.

    The column will be an epoch column with units determined by `feature_store_format_version`.

    For continuous SWAFV, features are not aggregated, so the anchor time column is simply a copy of the retrieval
    timestamp column.

    For non-continuous WAFV, features are aggregated in tiles, so the anchor time column represents the most recent tile
    available for retrieval. At time t, the most recent tile available for retrieval is equivalent to the most recent
    tile for which any feature row has an effective timestamp that is less than t. Thus for non-continuous WAFV, this
    node is conceptually the opposite of `AddEffectiveTimestampNode`.

    For example, consider feature retrieval for a BWAFV at time t. Let T = t - data_delay. Then the most recent
    materialization job ran at time T - (T % batch_schedule), so the most recent tile available for retrieval is the
    last tile that was materialized by that job, which has anchor time T - (T % batch_schedule) - tile_interval.

    Similarly, consider feature retrieval for a SWAFV at time T. Since there is no data delay, the most recent
    materialization job ran at time T - (T % tile_interval), so the most recent tile available for retrieval is the
    last tile that was materialized by that job, which has anchor time T - (T % tile_interval) - tile_interval.

    Attributes:
        input_node: The input node to be transformed.
        name: The name of the feature view.
        feature_store_format_version: The feature store format version for the FV, which determines whether its
            timestamp is in seconds or nanoseconds.
        batch_schedule: The batch materialization schedule for the feature view, with units determined by `feature_store_format_version`.
            Only used for BWAFVs.
        tile_interval: The tile interval for the feature view, with units determined by `feature_store_format_version`.
        timestamp_field: The column name of the retrieval timestamp field.
        is_stream: If True, the WAFV is a SWAFV.
        data_delay_seconds: The data delay for the feature view, in seconds.
    """

    input_node: NodeRef
    name: str
    feature_store_format_version: int
    batch_schedule: int
    tile_interval: int
    timestamp_field: str
    is_stream: bool
    data_delay_seconds: int = 0

    @property
    def columns(self) -> Sequence[str]:
        return (*list(self.input_node.columns), anchor_time())

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        base = (
            "Add anchor time column '_anchor_time' to represent the most recent feature data available for retrieval. "
            "The time at which feature data becomes available for retrieval depends on two factors: the frequency at "
            "which the feature view is materialized, and the data delay. "
        )

        if self.tile_interval == 0:  # Continuous
            return (
                base
                + f"Since '{self.name}' is a stream feature view with aggregations in continuous mode, the anchor time "
                + f"column is just a copy of the timestamp column '{self.timestamp_field}'."
            )
        elif self.is_stream:
            return (
                base
                + f"Since '{self.name} is a stream feature view with aggregations in time interval mode, feature data "
                + "is stored in tiles. Each tile has size equal to the tile interval, which is "
                + f"{convert_duration_to_seconds(self.tile_interval, self.feature_store_format_version)} seconds. "
                + "The anchor time column contains the start time of the most recent tile available for retrieval. "
                + f"It is calculated as '{self.timestamp_field}' - ('{self.timestamp_field}' % tile_interval) "
                + "- tile_interval."
            )
        else:
            if self.data_delay_seconds > 0:
                data_delay_seconds = f"Let T = '{self.timestamp_field}' - data_delay where data_delay = {self.data_delay_seconds} seconds. "
            else:
                data_delay_seconds = f"Let T be the timestamp column '{self.timestamp_field}'. "

            return (
                base
                + f"Since '{self.name}' is a batch feature view with aggregations, feature data is stored in tiles. "
                + "Each tile has size equal to the tile interval, which is "
                f"{convert_duration_to_seconds(self.tile_interval, self.feature_store_format_version)} seconds. "
                + "The anchor time column contains the start time of the most recent tile available for retrieval. "
                + data_delay_seconds
                + f"The anchor time column is calculated as T - (T % batch_schedule) - tile_interval where batch_schedule = "
                f"{convert_duration_to_seconds(self.batch_schedule, self.feature_store_format_version)} seconds."
            )

    def _to_query(self) -> pypika.queries.QueryBuilder:
        uid = self.input_node.name
        input_query = self.input_node._to_query()
        data_delay_seconds = self.data_delay_seconds or 0
        anchor_time_field = self.func.convert_epoch_seconds_to_feature_store_format_version(
            self.func.to_unixtime(self.func.date_add("second", -data_delay_seconds, Field(self.timestamp_field))),
            self.feature_store_format_version,
        )
        if self.tile_interval == 0:
            return (
                self.func.query()
                .with_(input_query, uid)
                .from_(AliasedQuery(uid))
                .select("*", anchor_time_field.as_(anchor_time()))
            )
        # For stream, we use the tile interval for bucketing since the data is available as soon as
        # the aggregation interval ends.
        # For BAFV, we use the batch schedule to get the last tile written.
        if self.is_stream:
            anchor_time_field = anchor_time_field - anchor_time_field % self.tile_interval - self.tile_interval
        else:
            anchor_time_field = anchor_time_field - anchor_time_field % self.batch_schedule - self.tile_interval
        return (
            self.func.query()
            .with_(input_query, uid)
            .from_(AliasedQuery(uid))
            .select("*", anchor_time_field.as_(anchor_time()))
        )


@attrs.frozen
class ConvertEpochToTimestampNode(QueryNode):
    """Convert epoch columns to timestamp columns.

    Attributes:
        input_node: The input node to be transformed.
        feature_store_formats: A dictionary mapping column names to feature store format versions. Each column in this
            dictionary will be converted from epoch to timestamp. Its feature store format version determines whether
            the timestamp is in seconds or nanoseconds.
    """

    input_node: NodeRef
    feature_store_formats: Dict[str, int]

    @property
    def columns(self) -> Sequence[str]:
        return self.input_node.columns

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        return (
            f"Convert columns {list(self.feature_store_formats.keys())} from epoch (either seconds or ns) to timestamp."
        )

    def _to_query(self) -> pypika.queries.QueryBuilder:
        input_query = self.input_node._to_query()
        uid = self.input_node.name
        fields = []
        for col in self.input_node.columns:
            feature_store_format_version = self.feature_store_formats.get(col)
            field = Field(col)
            if feature_store_format_version:
                epoch_field_in_secs = self.func.convert_epoch_term_in_seconds(field, feature_store_format_version)
                fields.append(self.func.from_unixtime(epoch_field_in_secs).as_(col))
            else:
                fields.append(field)
        return self.func.query().with_(input_query, uid).from_(AliasedQuery(uid)).select(*fields)


@attrs.frozen
class RenameColsNode(QueryNode):
    """
    Rename columns according to `mapping`. No action is taken for columns mapped to `None`. Drop columns in `drop`.
    """

    input_node: NodeRef
    mapping: Optional[Dict[str, str]] = attrs.field(default=None)
    drop: Optional[List[str]] = None

    @mapping.validator  # type: ignore
    def check_non_null_keys(self, _, value):
        if value is None:
            return
        for k in value.keys():
            if k is None:
                msg = f"RenameColsNode mapping should only contain non-null keys. Mapping={value}"
                raise ValueError(msg)

    @property
    def columns(self) -> Sequence[str]:
        cols = self.input_node.columns
        assert cols is not None, self.input_node
        newcols = []
        for col in cols:
            if self.drop and col in self.drop:
                continue
            elif self.mapping and col in self.mapping:
                newcols.append(self.mapping[col])
            else:
                newcols.append(col)
        return tuple(newcols)

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        actions = []
        if self.mapping:
            actions.append(f"Rename columns with map {self.mapping}.")
        if self.drop:
            # NOTE: the order of drop columns is unimportant
            actions.append(f"Drop columns {sorted(self.drop)}.")
        if not actions:
            actions.append("No columns are renamed or dropped.")
        return " ".join(actions)

    def _to_query(self) -> pypika.queries.QueryBuilder:
        input_query = self.input_node._to_query()
        uid = self.input_node.name
        projections = []
        for col in self.input_node.columns:
            if self.drop and col in self.drop:
                continue
            elif self.mapping and col in self.mapping:
                projections.append(Field(col).as_(self.mapping[col]))
            else:
                projections.append(Field(col))
        return self.func.query().with_(input_query, uid).from_(AliasedQuery(uid)).select(*projections)


@attrs.frozen
class ExplodeTimestampByTimeWindowsNode(QueryNode):
    """
    Explodes each anchor time into multiple rows, each with a new anchor time
    that is the sum of the anchor time and the time window.
    """

    input_node: NodeRef
    timestamp_field: str
    fdw: FeatureDefinitionWrapper
    time_filter: pendulum.Period

    @property
    def columns(self) -> Sequence[str]:
        return self.input_node.columns

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        return f"Explode the '{self.timestamp_field}' column for each time window, each with a new timestamp that is the sum of the timestamp and the time window."

    def _time_window_specs(self) -> List[TimeWindowSpec]:
        return [
            create_time_window_spec_from_data_proto(feature.time_window)
            for feature in self.fdw.fv_spec.aggregate_features
        ]

    def _to_query(self) -> pypika.queries.QueryBuilder:
        spine_df = self.input_node._to_query()
        aliased_input = self.input_node.name
        join_keys = [Field(col) for col in self.input_node.columns if col != anchor_time()]

        start_time_ns = convert_timestamp_for_version(self.time_filter.start, self.fdw.get_feature_store_format_version)
        end_time_ns = convert_timestamp_for_version(self.time_filter.end, self.fdw.get_feature_store_format_version)

        time_deltas = set()
        for time_window in self._time_window_specs():
            if isinstance(time_window, LifetimeWindowSpec):
                time_deltas.add(datetime.timedelta(0))
            elif isinstance(time_window, RelativeTimeWindowSpec):
                time_deltas.update((time_window.window_start, time_window.window_end))
            elif isinstance(time_window, TimeWindowSeriesSpec):
                for time_window in time_window.time_windows:
                    time_deltas.update((time_window.window_start, time_window.window_end))
            else:
                msg = f"Invalid time_window type: {type(time_window)}"
                raise ValueError(msg)

        time_deltas_ns = [
            pypika.Tuple(convert_timedelta_for_version(abs(td), self.fdw.get_feature_store_format_version))
            for td in time_deltas
        ]

        time_deltas_cte = (
            self.func.query()
            .from_(Values(values=time_deltas_ns, alias="tecton_time_deltas", columns=["deltas"]))
            .select("*")
        )

        cross_join_sql = (
            self.func.query()
            .with_(spine_df, "_tecton_spine_df")
            .with_(time_deltas_cte, "_tecton_time_deltas")
            .from_(AliasedQuery("_tecton_spine_df"))
            .cross_join(AliasedQuery("_tecton_time_deltas"))
            .cross()
            .select(
                "*",
            )
        )

        updated_anchor_times = (
            self.func.query()
            .with_(cross_join_sql, "_tecton_cross_join")
            .from_(AliasedQuery("_tecton_cross_join"))
            .select(*join_keys, (Field(anchor_time()) + Field("deltas")).as_(anchor_time()))
        )

        filtered_times = (
            self.func.query()
            .with_(updated_anchor_times, "_tecton_updated_times")
            .from_(AliasedQuery("_tecton_updated_times"))
            .select(
                *join_keys,
                Case()
                .when(Field(anchor_time()) <= start_time_ns, start_time_ns)
                .else_(Field(anchor_time()))
                .as_(anchor_time()),
            )
            .distinct()
            .where(Field(anchor_time()) < end_time_ns)
        )

        return filtered_times


@attrs.frozen
class DeriveValidityPeriodNode(QueryNode):
    """
    Derives the `valid_from` and `valid_to` columns from a fully aggregated data frame
    and removes duplicates and rows with default values for all aggregation columns.
    """

    input_node: NodeRef
    fdw: FeatureDefinitionWrapper
    timestamp_field: str

    @property
    def columns(self) -> Sequence[str]:
        cols = self.input_node.columns
        cols = [*cols, valid_to(), valid_from()]
        cols.remove(self.timestamp_field)
        if self.fdw.timestamp_key in cols:
            cols.remove(self.fdw.timestamp_key)
        return tuple(cols)

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        return "Derive the 'valid_from' and 'valid_to' columns for each feature value."

    def _to_query(self) -> pypika.queries.QueryBuilder:
        input_query = self.input_node._to_query()
        aliased_input = self.input_node.name
        join_keys = self.fdw.join_keys

        features = self.fdw.fv_spec.features
        fields = [Field(col) for col in self.input_node.columns]
        timestamp_field = Field(self.timestamp_field)

        derive_validity_query = (
            self.func.query()
            .with_(input_query, "_tecton_input_query")
            .from_(AliasedQuery("_tecton_input_query"))
            .select(
                input_query.star,
                Lead(timestamp_field).over(*join_keys).orderby(timestamp_field).as_(valid_to()),
                timestamp_field.as_(valid_from()),
            )
        )

        row_change_condition = None
        if self.fdw.serving_ttl is not None:
            derive_validity_query = self._expire_ttl(derive_validity_query)

            # if `valid_from` is not equal to the previous `valid_to` (in the case of TTL expiry),
            # we should not merge the rows even though the feature values are equal
            row_change_condition = Field(valid_from()) != Lag(Field(valid_to())).over(*join_keys).orderby(
                timestamp_field
            )

        track_changes_cols = list(features)
        for column in track_changes_cols:
            field = Field(column)
            prev_field = Lag(Field(column)).over(*join_keys).orderby(timestamp_field)
            column_has_changed = (
                (field != prev_field)
                | (field.isnull() & prev_field.isnotnull())
                | (prev_field.isnull() & field.isnotnull())
            )
            if row_change_condition is None:
                row_change_condition = column_has_changed
            else:
                row_change_condition = row_change_condition.__or__(column_has_changed)

        # Check if any feature column changed in value, set _tecton_is_new=1 for rows with changes
        track_changes_query = (
            self.func.query()
            .with_(derive_validity_query, "_tecton_derive_validity_query")
            .from_(AliasedQuery("_tecton_derive_validity_query"))
            .select(
                derive_validity_query.star,
                Case().when(row_change_condition, 1).else_(0).as_("_tecton_is_new"),
            )
        )

        # Cumulatively sum the `_tecton_is_new` column to create "groups".
        # A group is a set of consecutive rows that has the same aggregated value.
        group_query = (
            self.func.query()
            .with_(track_changes_query, "_tecton_track_changes_query")
            .from_(AliasedQuery("_tecton_track_changes_query"))
            .select(
                derive_validity_query.star,
                an.Sum(Cast(Field("_tecton_is_new"), "INTEGER"))
                .over(*join_keys)
                .orderby(timestamp_field)
                .as_("_tecton_group"),
            )
        )

        min_valid_from = an.Min(Field(valid_from())).over(*join_keys, "_tecton_group").as_("_tecton_group_valid_from")
        max_valid_to = an.Max(Field(valid_to())).over(*join_keys, "_tecton_group")

        # if valid_to for a group is "null", we've reached the last event and the "max_valid_to" should be null
        # since we don't know how long the value is valid
        group_contains_null_valid_to = (
            an.Count(Case().when(Field(valid_to()).isnull(), 1)).over(*join_keys, "_tecton_group") > 0
        )

        merge_query = (
            self.func.query()
            .with_(group_query, "_tecton_group_query")
            .from_(AliasedQuery("_tecton_group_query"))
            .select(
                track_changes_query.star,
                min_valid_from,
                Case().when(group_contains_null_valid_to, None).else_(max_valid_to).as_("_tecton_group_valid_to"),
            )
        )

        full_merge_query = (
            self.func.query()
            .with_(merge_query, "_tecton_merge_query")
            .from_(AliasedQuery("_tecton_merge_query"))
            .select(
                *[
                    Field(col)
                    for col in self.input_node.columns
                    if col not in [self.timestamp_field, self.fdw.timestamp_key]
                ],
                Field("_tecton_group_valid_from").as_(valid_from()),
                Field("_tecton_group_valid_to").as_(valid_to()),
            )
            .groupby(*join_keys, *features, "_tecton_group", "_tecton_group_valid_to", "_tecton_group_valid_from")
        )

        if self.fdw.fv_spec.type == MaterializedFeatureViewType.TEMPORAL_AGGREGATE:
            full_merge_query = self._remove_default_values(full_merge_query)

        return full_merge_query

    def _expire_ttl(self, input_query: pypika.queries.QueryBuilder) -> pypika.queries.QueryBuilder:
        """
        Trims `valid_to` values according to TTL for non-aggregate feature views
        """
        select_fields = [Field(col) for col in self.input_node.columns]
        valid_to_field = Field(valid_to())
        valid_from_field = Field(valid_from())
        select_fields.append(valid_from_field)

        valid_to_timestamp = self.func.to_timestamp(valid_to_field)
        valid_from_timestamp = self.func.to_timestamp(valid_from_field)

        ttl_seconds = self.fdw.serving_ttl.total_seconds()
        adjusted_valid_to = self.func.date_add("second", int(ttl_seconds), valid_from_field)

        expire_ttl_query = (
            self.func.query()
            .with_(input_query, "_tecton_expire_ttl")
            .from_(AliasedQuery("_tecton_expire_ttl"))
            .select(
                *select_fields,
                Case()
                .when(
                    (valid_to_field.isnull())
                    | (valid_to_timestamp - valid_from_timestamp > Interval(seconds=ttl_seconds)),
                    adjusted_valid_to,
                )
                .else_(valid_to_field)
                .as_(valid_to()),
            )
        )

        return expire_ttl_query

    def _is_time_window_series_feature(self, feature: feature_view_pb2.AggregateFeature) -> bool:
        time_window = create_time_window_spec_from_data_proto(feature.time_window)
        return isinstance(time_window, TimeWindowSeriesSpec)

    def _is_count_feature(self, feature: feature_view_pb2.AggregateFeature) -> bool:
        return (
            feature.function == AggregationFunction.AGGREGATION_FUNCTION_COUNT
            or feature.function == AggregationFunction.AGGREGATION_FUNCTION_APPROX_COUNT_DISTINCT
        )

    def _remove_default_values(self, input_query: pypika.queries.QueryBuilder) -> pypika.queries.QueryBuilder:
        """
        Removes rows with default values for all aggregation columns.
        """
        aggregate_features = self.fdw.fv_spec.aggregate_features
        not_default_value_conditions = []

        if self.fdw.aggregation_secondary_key:
            # For secondary key aggs, we remove rows that have empty rollup output lists
            column_names = [rollup_output.name for rollup_output in self.fdw.fv_spec.secondary_key_rollup_outputs]
            not_default_value_conditions.extend([Length(Field(column)) > 0 for column in column_names])
        else:
            for feature in aggregate_features:
                column_name = feature.output_feature_name
                if self._is_time_window_series_feature(feature):
                    not_all_counts_empty = pypika.terms.Term.wrap_constant(0) != self.func.any(column_name)
                    not_all_nulls = Length(self.func.list_filter_nulls(column_name)) > 0
                    if self._is_count_feature(feature):
                        not_default_value_conditions.append(not_all_nulls & not_all_counts_empty)
                    else:
                        not_default_value_conditions.append(not_all_nulls)
                else:
                    if self._is_count_feature(feature):
                        not_default_value_conditions.append(
                            (Field(column_name).isnotnull()) & (Field(column_name) != 0)
                        )
                    else:
                        not_default_value_conditions.append(Field(column_name).isnotnull())

        remove_default_values_query = (
            self.func.query()
            .with_(input_query, "_tecton_full_merge_query")
            .from_(AliasedQuery("_tecton_full_merge_query"))
            .select(input_query.star)
            .where(Criterion.any(not_default_value_conditions))
        )

        return remove_default_values_query


@attrs.frozen
class UserSpecifiedDataNode(QueryNode):
    """Arbitrary data container for user-provided data (e.g. spine).

    The executor node will need to typecheck and know how to handle the type of mock data.
    """

    data: DataframeWrapper
    metadata: Optional[Dict[str, Any]] = attrs.field(default=None)

    @property
    def columns(self) -> Sequence[str]:
        return self.data.columns

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return ()

    def as_str(self) -> str:
        return f"User provided data with columns {'|'.join(self.columns)}"

    def _to_query(self) -> pypika.queries.QueryBuilder:
        t = self.data._temp_table_name
        return self.func.query().from_(Table(t)).select(*self.columns)


@attrs.frozen
class DataNode(QueryNode):
    """Arbitrary data container.

    The executor node will need to typecheck and know how to handle the type of mock data.

    Only supports Spark.
    """

    data: DataframeWrapper
    metadata: Optional[Dict[str, Any]] = attrs.field(default=None)

    @property
    def columns(self) -> Sequence[str]:
        return self.data.columns

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return ()

    def as_str(self) -> str:
        return f"Data with columns {'|'.join(self.columns)}"

    def _to_query(self) -> pypika.queries.QueryBuilder:
        raise NotImplementedError


@attrs.frozen
class MockDataSourceScanNode(QueryNode):
    """Provides mock data for a data source and applies the given time range filter.

    Attributes:
        data: The mock data, in the form of a NodeRef.
        ds: The data source being mocked.
        columns: The columns of the data.
        start_time: The start time to be applied.
        end_time: The end time to be applied.
    """

    data: NodeRef
    ds: specs.DataSourceSpec
    columns: Tuple[str]
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.data,)

    def as_str(self) -> str:
        s = f"Read mock data source '{self.ds.name}'"
        if self.start_time:
            s += f" and filter by start time {self.start_time}"
        if self.end_time:
            s += f" and filter by end time {self.end_time}"
        return s

    def _to_query(self) -> pypika.queries.QueryBuilder:
        uid = self.data.name
        input_query = self.data._to_query()
        q = self.func.query().with_(input_query, uid).from_(AliasedQuery(uid)).select("*")
        if self.start_time or self.end_time:
            timestamp_field = Field(self.ds.batch_source.timestamp_field)
            if self.start_time:
                q.where(timestamp_field >= self.func.to_timestamp(self.start_time))
            if self.end_time:
                q.where(timestamp_field < self.func.to_timestamp(self.end_time))
        return q


@attrs.frozen
class RespectFeatureStartTimeNode(QueryNode):
    """
    Null out all features outside of feature start time

    NOTE: the feature start time is assumed to already be in appropriate units
    for the column: nanoseconds/seconds for anchor time filter, or timestamp
    for timestamp filter
    """

    input_node: NodeRef
    retrieval_time_col: str
    feature_start_time: Union[pendulum.datetime, int]
    features: List[str]
    feature_store_format_version: int

    @classmethod
    def for_anchor_time_column(
        cls,
        dialect: Dialect,
        compute_mode: ComputeMode,
        input_node: NodeRef,
        anchor_time_col: str,
        fdw: FeatureDefinitionWrapper,
    ) -> "RespectFeatureStartTimeNode":
        """
        This factory method is aimed at consolidating logic for
        scenarios where we want to apply this logic to 'anchor
        time' columns.
        """
        start_time_anchor_units = time_utils.convert_timestamp_for_version(
            fdw.feature_start_timestamp, fdw.get_feature_store_format_version
        )

        tile_interval = fdw.get_tile_interval_seconds_for_offline_store

        # TODO: ideally we could join using 'window end' timestamps rather
        # than 'window start' anchor times and avoid this complexity.
        if tile_interval == 0:
            # No correction needed since the earliest 'anchor time' is the
            # feature start time for continuous.
            ts = start_time_anchor_units
        else:
            # We have to subtract the tile interval from the start time to get
            # the appropriate earliest anchor time.
            ts = start_time_anchor_units - tile_interval

        # NOTE: this filter is extremely important for correctness.
        #   The offline store contains partial aggregates from _before_ the
        #   feature start time (with the goal of having the feature start
        #   time be the first complete aggregate). This filter ensures that
        #   spine timestamps from before the feature start time, but after
        #   we have partial aggregates in the offline store, receive null
        #   feature values.
        return cls(
            dialect, compute_mode, input_node, anchor_time_col, ts, fdw.features, fdw.get_feature_store_format_version
        )

    @property
    def columns(self) -> Sequence[str]:
        return self.input_node.columns

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        feature_start_time = (
            convert_epoch_to_datetime(self.feature_start_time, self.feature_store_format_version)
            if isinstance(self.feature_start_time, int)
            else self.feature_start_time
        )
        return (
            f"Respect the feature start time for all rows where '{self.retrieval_time_col}' < {feature_start_time} "
            f"by setting all feature columns for those rows to NULL"
        )

    def _to_query(self) -> pypika.queries.QueryBuilder:
        input_query = self.input_node._to_query()
        if isinstance(self.feature_start_time, int):
            # retrieval_time_col is _anchor_time
            feature_start_time_term = self.feature_start_time
        else:
            feature_start_time_term = self.func.to_timestamp(self.feature_start_time)

        uid = self.input_node.name
        cond = Field(self.retrieval_time_col) >= feature_start_time_term
        project_list = []
        for c in self.columns:
            if c in self.features:
                newcol = Case().when(cond, Field(c)).else_(NULL).as_(c)
                project_list.append(newcol)
            else:
                project_list.append(Field(c))
        return self.func.query().with_(input_query, uid).from_(AliasedQuery(uid)).select(*project_list)


@attrs.frozen
class RespectTTLNode(QueryNode):
    """
    Null out all features with retrieval time > expiration time.
    """

    input_node: NodeRef
    retrieval_time_col: str
    expiration_time_col: str
    features: List[str]

    @property
    def columns(self) -> Sequence[str]:
        return self.input_node.columns

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        return f"Null out any values where '{self.retrieval_time_col}' > '{self.expiration_time_col}'"

    def _to_query(self) -> pypika.queries.QueryBuilder:
        input_query = self.input_node._to_query()
        cond = Field(self.retrieval_time_col) < Field(self.expiration_time_col)
        project_list = []
        for c in self.input_node.columns:
            if c not in self.features:
                project_list.append(Field(c))
            else:
                newcol = Case().when(cond, Field(c)).else_(NULL).as_(c)
                project_list.append(newcol)
        uid = self.input_node.name
        return self.func.query().with_(input_query, uid).from_(AliasedQuery(uid)).select(*project_list)


@attrs.frozen
class CustomFilterNode(QueryNode):
    input_node: NodeRef
    filter_str: str

    @property
    def columns(self) -> Sequence[str]:
        return self.input_node.columns

    def as_str(self) -> str:
        return f"Apply filter: ({self.filter_str})"

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def _to_query(self) -> pypika.queries.QueryBuilder:
        raise NotImplementedError


@attrs.frozen
class FeatureTimeFilterNode(QueryNode):
    """Filters the data with respect to the given time limits and materialization policy.

    Attributes:
        input_node: The input node to be transformed.
        feature_data_time_limits: The time limits to be applied.
        policy: The materialization policy to be used.
        timestamp_field: The column name of the feature timestamp field.
    """

    input_node: NodeRef
    feature_data_time_limits: pendulum.Period
    policy: feature_view_pb2.MaterializationTimeRangePolicy
    start_timestamp_field: str
    end_timestamp_field: str

    @property
    def columns(self) -> Sequence[str]:
        return self.input_node.columns

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        time_range_str = f"[{self.feature_data_time_limits.start}, {self.feature_data_time_limits.end})"
        if (
            self.policy
            == feature_view_pb2.MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FAIL_IF_OUT_OF_RANGE
        ):
            return f"Assert all rows in column '{self.start_timestamp_field}' are in range {time_range_str}"
        else:
            if self.start_timestamp_field == self.end_timestamp_field:
                return f"Apply time range filter {time_range_str} to column '{self.start_timestamp_field}'"
            else:
                return f"Apply time range filter such that '{self.start_timestamp_field}' < {self.feature_data_time_limits.end} and '{self.end_timestamp_field}' >= {self.feature_data_time_limits.start}"

    def _to_query(self) -> pypika.queries.QueryBuilder:
        if (
            self.policy
            == feature_view_pb2.MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FAIL_IF_OUT_OF_RANGE
        ):
            # snowflake/athena are post-fwv4
            raise NotImplementedError
        input_query = self.input_node._to_query()
        uid = self.input_node.name
        time_field = Field(self.start_timestamp_field)
        where_conds = []
        where_conds.append(time_field >= self.func.to_timestamp(self.feature_data_time_limits.start))
        where_conds.append(time_field < self.func.to_timestamp(self.feature_data_time_limits.end))
        q = self.func.query().with_(input_query, uid).from_(AliasedQuery(uid)).select("*")
        for w in where_conds:
            q = q.where(w)
        return q

    @property
    def output_schema(self) -> Optional[Schema]:
        return self.input_node.output_schema


@attrs.frozen
class TrimValidityPeriodNode(QueryNode):
    """Filters the data with respect to the given limits.

    Remove rows where (`valid_from` >= end or `valid_to` <= start)
    If valid_from < `start`, set it to `start`
    if valid_to is null or valid_to > `end`, set to `end`

    Attributes:
        input_node: The input node to be transformed.
        start: The lower bound value
        end: The lower bound value
    """

    input_node: NodeRef
    start: Any
    end: Any

    @property
    def columns(self) -> Sequence[str]:
        return self.input_node.columns

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        message = f"Filter out rows where '{valid_from()}' >= {self.end} or '{valid_to()}' <= {self.start}. "
        message += f"If '{valid_from()} < {self.start}, set it to {self.start}. "
        message += f"If '{valid_to()} > {self.end} or '{valid_to()}' is null, set it to {self.end}."

        return message

    def _to_query(self) -> pypika.queries.QueryBuilder:
        input_query = self.input_node._to_query()
        aliased_input = self.input_node.name
        fields = [Field(col) for col in self.columns if col not in [valid_to(), valid_from()]]

        valid_to_field = Field(valid_to())
        valid_from_field = Field(valid_from())
        start_time = self.func.to_timestamp(self.start)
        end_time = self.func.to_timestamp(self.end)

        # Trim values to ensure `valid_from` >= `start_time` and `valid_to` <= `end_time`
        update_query = (
            self.func.query()
            .with_(input_query, aliased_input)
            .from_(AliasedQuery(aliased_input))
            .select(
                *fields,
                Case()
                .when((valid_to_field.isnull()) | (valid_to_field > end_time), end_time)
                .else_(valid_to_field)
                .as_(valid_to()),
                Case().when(valid_from_field < start_time, start_time).else_(valid_from_field).as_(valid_from()),
            )
        )

        # Filter values where `valid_from` > `end_time` and `valid_to` < `start_time`
        filter_query = (
            self.func.query()
            .with_(update_query, "_tecton_trim_query")
            .from_("_tecton_trim_query")
            .select("*")
            .where((valid_from_field < end_time) & (valid_to_field > start_time))
        )

        return filter_query

    @property
    def output_schema(self) -> Optional[Schema]:
        return self.input_node.output_schema


@attrs.frozen
class MetricsCollectorNode(QueryNode):
    """
    Collect metrics on features
    """

    input_node: NodeRef

    @property
    def columns(self) -> Sequence[str]:
        return self.input_node.columns

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        return "Collect metrics on features"

    def _to_query(self) -> pypika.queries.QueryBuilder:
        raise NotImplementedError


@attrs.frozen
class AddEffectiveTimestampNode(QueryNode):
    """Augment a dataframe with an effective timestamp.

    The effective timestamp for a given row is the earliest it will be available in the online store for inference.
    For BFVs and BWAFVs, materialization jobs run every `batch_schedule`, so the effective timestamp is calculated as
    window('timestamp_field', batch_schedule).end + data_delay, and is therefore always strictly greater than the
    feature timestamp. For SWAFVs in non-continuous mode, the feature timestamps are aligned to the aggregation window,
    so the effective timestamp is just the feature timestamp. For SFVs, SWAFVs in continuous mode, and feature tables,
    the effective timestamp is also just the feature timestamp.

    Attributes:
        input_node: The input node to be transformed.
        timestamp_field: The column name of the feature timestamp field.
        effective_timestamp_name: The name of the effective timestamp column to be added.
        is_stream: If True, the feature view has a stream data source.
        batch_schedule_seconds: The batch materialization schedule for the feature view, in seconds.
        data_delay_seconds: The data delay for the feature view, in seconds.
        is_temporal_aggregate: If True, the feature view is a WAFV.
    """

    input_node: NodeRef
    timestamp_field: str
    effective_timestamp_name: str
    batch_schedule_seconds: int
    is_stream: bool
    data_delay_seconds: int
    is_temporal_aggregate: bool

    @property
    def columns(self) -> Sequence[str]:
        return [*self.input_node.columns, self.effective_timestamp_name]

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        if self.batch_schedule_seconds == 0 or self.is_stream:
            return f"Add effective timestamp column '{self.effective_timestamp_name}' that is equal to the timestamp column '{self.timestamp_field}'."
        else:
            result = (
                f"Add effective timestamp column '{self.effective_timestamp_name}' that is equal to window('"
                f"{self.timestamp_field}', batch_schedule).end where batch_schedule = "
                f"{self.batch_schedule_seconds} seconds."
            )
            if self.data_delay_seconds > 0:
                result += f" Then add data_delay to the effective timestamp column where data_delay = {self.data_delay_seconds} seconds."
            return result

    def _to_query(self) -> pypika.queries.QueryBuilder:
        input_query = self.input_node._to_query()
        uid = self.input_node.name
        if self.batch_schedule_seconds == 0 or self.is_stream:
            effective_timestamp = Field(self.timestamp_field)
        else:
            timestamp_col = Field(self.timestamp_field)
            # Timestamp of temporal aggregate is end of the anchor time window. Subtract 1 milli
            # to get the correct bucket for batch schedule.
            if self.is_temporal_aggregate:
                timestamp_col = self.func.date_add("millisecond", -1, timestamp_col)
            effective_timestamp = self.func.from_unixtime(
                convert_to_effective_timestamp(
                    self.func.to_unixtime(timestamp_col), self.batch_schedule_seconds, self.data_delay_seconds
                )
            )
        fields = []
        for col in self.columns:
            if col == self.effective_timestamp_name:
                fields.append(effective_timestamp.as_(self.effective_timestamp_name))
            else:
                fields.append(Field(col))
        return self.func.query().with_(input_query, uid).from_(AliasedQuery(uid)).select(*fields)


@attrs.frozen
class AddDurationNode(QueryNode):
    """Adds a duration to a timestamp field"""

    input_node: NodeRef
    timestamp_field: str
    duration: pendulum.Duration
    new_column_name: str

    @property
    def columns(self) -> Sequence[str]:
        return (*list(self.input_node.columns), self.new_column_name)

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        return f"Add {self.duration.in_words()} to '{self.timestamp_field}' as new column '{self.new_column_name}'"

    def _to_query(self) -> pypika.queries.QueryBuilder:
        input_query = self.input_node._to_query()
        uid = self.input_node.name
        return (
            self.func.query()
            .with_(input_query, uid)
            .from_(AliasedQuery(uid))
            .select(
                "*",
                self.func.date_add("second", int(self.duration.total_seconds()), Field(self.timestamp_field)).as_(
                    self.new_column_name
                ),
            )
        )


@attrs.frozen
class StreamWatermarkNode(QueryNode):
    input_node: NodeRef
    time_column: str
    stream_watermark: str

    @property
    def columns(self) -> Sequence[str]:
        return self.input_node.columns

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        return f"Set Stream Watermark {self.stream_watermark} on the DataFrame"

    def _to_query(self) -> pypika.queries.QueryBuilder:
        raise NotImplementedError


@attrs.frozen
class SelectDistinctNode(QueryNode):
    input_node: NodeRef
    columns: List[str]

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        return f"Select distinct with columns {self.columns}."

    def _to_query(self) -> pypika.queries.QueryBuilder:
        input_query = self.input_node._to_query()
        uid = self.input_node.name
        fields = [Field(c) for c in self.columns]
        return self.func.query().with_(input_query, uid).from_(AliasedQuery(uid)).select(*fields).distinct()


@attrs.frozen
class AggregationSecondaryKeyRollupNode(QueryNode):
    """
    Rollup aggregation secondary key and corresponding feature values for each distinct window.

    Attributes:
        full_aggregation_node: The input node, which is always a full aggregation node.
        fdw: The feature definition wrapper that contains the useful metadata.
        group_by_columns: The columns to group by when rolling up the secondary key and its corresponding feature values.
    """

    full_aggregation_node: NodeRef
    fdw: FeatureDefinitionWrapper
    group_by_columns: Iterable[str]

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.full_aggregation_node,)

    def as_str(self) -> str:
        return f"Rollup aggregation secondary key '{self.fdw.aggregation_secondary_key}' and corresponding feature values for each distinct window."

    @property
    def columns(self) -> Sequence[str]:
        return list(self.group_by_columns) + list(self.fdw.features)

    def _to_query(self) -> pypika.queries.QueryBuilder:
        """
        Group features by windows and put them into temp struct col for each distinct window. Rollup temp structs into
        a list. Filter out rows where indicator column is null (indicating no value for that time window and secondary
        key grouping). Sort the rows by secondary key prior to rolling up to array.

        See `AggregationSecondaryKeyRollupSparkNode` for more info.

        Sample resulting query:

        WITH pre_aggregate AS (
        SELECT
            user_id,
            anchor_time,
            LIST(STRUCT_PACK(ad_id, indicator_1d, value_max_1d) ORDER BY ad_id ASC)
                FILTER (WHERE indicator_1d IS NOT NULL) as _struct_1d,
            LIST(STRUCT_PACK(ad_id, indicator_3d, value_max_3d) ORDER BY ad_id ASC)
                FILTER (WHERE indicator_3d IS NOT NULL) as _struct_3d
        FROM my_df
        GROUP BY user_id, anchor_time
        )
        SELECT
            user_id,
            anchor_time,
            LIST_TRANSFORM(_struct_1d, st -> st['ad_id']) as ad_id_1d,
            LIST_TRANSFORM(_struct_1d, st -> st['value_max_1d']) as value_max_1d,
            LIST_TRANSFORM(_struct_3d, st -> st['ad_id']) as ad_id_3d,
            LIST_TRANSFORM(_struct_3d, st -> st['value_max_3d']) as value_max_3d,
        FROM pre_aggregate
        """
        if self.dialect != Dialect.DUCKDB:
            raise NotImplementedError

        input_query = self.full_aggregation_node._to_query()

        # Group columns by windows. Each time window here maps to a list of columns:
        #  time_window -> [secondary_key, secondary_key_indicator, agg_features...]
        window_to_features = self.fdw.window_to_features_map_for_secondary_keys

        group_by_fields = [Field(col) for col in self.group_by_columns]

        pre_agg_query = (
            Query.from_(input_query)
            .select(
                *group_by_fields,
                *[
                    # Creates temporary lists of structs, where each struct contains secondary key column,
                    # indicator column, and feature columns. Sorts the structs by secondary key and filters out
                    # rows where the indicator for that time window is null.
                    # E.g.:
                    # LIST(STRUCT_PACK(sec_agg_key, indicator_1d, feature_1d) ORDER BY ad_id ASC)
                    # FILTER (WHERE indicator_1d IS NOT NULL) as _struct_1d
                    Coalesce(
                        self.func.ordered_filtered_list(
                            from_column=self.func.struct(cols),
                            order_by_column=Field(self.fdw.aggregation_secondary_key),
                            filter_clause=Field(temp_indictor_column_name(window)).isnotnull(),
                            direction=Order.asc,
                        ),
                        LiteralValue("[]"),
                    ).as_(temp_struct_column_name(window))
                    for window, cols in window_to_features.items()
                ],
            )
            .groupby(*group_by_fields)
        )

        """
        # noqa E501
        At this point the pre-aggregate table will look something like this:
        | user_id | anchor_time | _struct_1d                                                        | _struct_3d                                                   |
        |---------|-------------|-------------------------------------------------------------------|--------------------------------------------------------------|
        | a       | 1           | [{'ad_id': 1, 'indicator_1d': 1.0, 'value_max_1d': 1.0}, {...}]   | [{'ad_id': 1, 'indicator_3d': 1, 'value_max_3d': 11}, {...}] |
        | a       | 2           | [{'ad_id': 1, 'indicator_1d': 1.0, 'value_max_1d': 1.0}, {...}]   | [{'ad_id': 1, 'indicator_3d': 1, 'value_max_3d': 21}, {...}] |
        """

        # The following block populates the SELECT clause for the final query to extract feature and secondary key
        # columns from the temporary structs created in the previous step
        # E.g.:
        # LIST_TRANSFORM(_struct_1d, st -> st['ad_id']) as ad_id_1d,
        # LIST_TRANSFORM(_struct_1d, st -> st['value_max_1d']) as value_max_1d,
        list_transforms = []
        for secondary_key_output in self.fdw.materialized_fv_spec.secondary_key_rollup_outputs:
            time_window = secondary_key_output.time_window
            temp_struct_column = temp_struct_column_name(time_window)

            # extract features from the temp structs
            for agg_feature in self.fdw.trailing_time_window_aggregation.features:
                if create_time_window_spec_from_data_proto(agg_feature.time_window) == time_window:
                    list_transforms.append(
                        self.func.list_transform(
                            Field(temp_struct_column), f"st -> st['{agg_feature.output_feature_name}']"
                        ).as_(agg_feature.output_feature_name)
                    )

            # extract secondary key column
            list_transforms.append(
                self.func.list_transform(
                    Field(temp_struct_column), f"st -> st['{self.fdw.aggregation_secondary_key}']"
                ).as_(secondary_key_output.name)
            )

        query = Query.from_(pre_agg_query).select(
            *group_by_fields,
            *list_transforms,
        )

        return query


@attrs.frozen
class AddUniqueIdNode(QueryNode):
    """
    Add a '_tecton_unique_id' column to the input node. This column is used to uniquely identify rows in the input node.

    Warning: The generated unique ID is non-deterministic on Spark, so this column may not be safe to join on.
    """

    input_node: NodeRef
    column_name: Optional[str] = attrs.Factory(tecton_unique_id_col)

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self):
        return f"Add a {self.column_name} column to the input node."

    @property
    def columns(self) -> Sequence[str]:
        return (*self.input_node.columns, self.column_name)

    def _to_query(self) -> pypika.queries.QueryBuilder:
        if self.dialect not in (Dialect.DUCKDB, Dialect.SNOWFLAKE):
            raise NotImplementedError

        input_query = self.input_node._to_query()

        row_number = RowNumber().over(NULL)
        if self.dialect == Dialect.SNOWFLAKE:
            # see example for generating row numbers w/o gaps
            # https://docs.snowflake.com/en/sql-reference/functions/seq1
            row_number = row_number.orderby(Function("seq4"))

        return Query.from_(input_query).select("*", row_number.as_(self.column_name))


@attrs.frozen
class PythonDataNode(QueryNode):
    """Data container for python-native data.

    This data should be relatively small. The executor node is responsible translating this into
    an appropriate dataframe/table representation for the execution engine.
    """

    columns: Tuple[str, ...]
    data: Any
    schema: Optional[Schema] = None

    @classmethod
    def from_schema(
        cls, dialect: Dialect, compute_mode: ComputeMode, schema: Schema, data: Tuple[Tuple[Any, ...]]
    ) -> QueryNode:
        return cls(
            dialect=dialect,
            compute_mode=compute_mode,
            columns=tuple(schema.column_names()),
            data=data,
            schema=schema,
        )

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return ()

    def as_str(self):
        return "Create a dataframe/table from the provided data + columns."

    def _to_query(self) -> pypika.queries.QueryBuilder:
        raise NotImplementedError


@attrs.frozen
class InnerJoinOnRangeNode(QueryNode):
    """Joins the left against the right, using the right columns as the conditional.

    In pseudo-sql it is:
        SELECT
            left.*
            right.*
        FROM
            left INNER JOIN right
            ON (right.right_inclusive_start_column IS null OR left.left_join_condition_column >= right.right_inclusive_start_column)
                AND left.left_join_condition_column < right.right_exclusive_end_column)

    NOTE: the Spark implementation hardcodes a broadcast join since the only usage of this should be on small dataframes that are safe to broadcast.
    """

    left: NodeRef
    right: NodeRef
    left_join_condition_column: str
    right_inclusive_start_column: str
    right_exclusive_end_column: str

    @property
    def columns(self) -> Sequence[str]:
        return (*self.left.columns, *self.right.columns)

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.left, self.right)

    @property
    def input_names(self) -> Optional[List[str]]:
        return ["left", "right"]

    def as_str(self) -> str:
        return f"Inner join on ({self.right_inclusive_start_column} IS null OR {self.right_inclusive_start_column} <= {self.left_join_condition_column}) AND ({self.left_join_condition_column} < {self.right_exclusive_end_column})"

    def _to_query(self) -> pypika.queries.QueryBuilder:
        raise NotImplementedError


@attrs.frozen
class OnlinePartialAggNodeV2(QueryNode):
    """Performs partial aggregations for the new online materialization format (i.e. compaction)."""

    input_node: NodeRef
    fdw: FeatureDefinitionWrapper
    aggregation_groups: Tuple[compaction_utils.AggregationGroup, ...]

    @property
    def columns(self) -> Sequence[str]:
        return (
            *self.fdw.join_keys,
            aggregation_group_id(),
            aggregation_tile_id(),
            *(f"{group.window_index}_{group.tile_index}" for group in self.aggregation_groups),
        )

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    @property
    def input_names(self) -> Optional[List[str]]:
        return ["input_node"]

    def as_str(self) -> str:
        return "Perform partial aggregations for compacted online store format."

    def _to_query(self) -> pypika.queries.QueryBuilder:
        raise NotImplementedError


@attrs.frozen
class OnlineListAggNode(QueryNode):
    """Collects partial aggregations for every sawtooth tile into one list for each aggregation window.

    Used for the online compaction query."""

    input_node: NodeRef
    fdw: FeatureDefinitionWrapper
    aggregation_groups: Tuple[compaction_utils.AggregationGroup, ...]

    @property
    def columns(self) -> Sequence[str]:
        return (
            *self.fdw.join_keys,
            aggregation_group_id(),
            *(str(group.window_index) for group in self.aggregation_groups),
        )

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    @property
    def input_names(self) -> Optional[List[str]]:
        return ["input_node"]

    def as_str(self) -> str:
        return "Collect partial aggregations for each aggregation window into a list for compacted online store format."

    def _to_query(self) -> pypika.queries.QueryBuilder:
        raise NotImplementedError


@attrs.frozen
class ConvertTimestampToUTCNode(QueryNode):
    input_node: NodeRef
    timestamp_key: str

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.input_node.columns

    @property
    def inputs(self) -> Tuple[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        return f"Convert '{self.timestamp_key}' to UTC"

    @property
    def output_schema(self) -> Optional[Schema]:
        return self.input_node.output_schema

    def _to_query(self) -> pypika.Query:
        if self.dialect == Dialect.DUCKDB:
            columns = [c for c in self.columns if c != self.timestamp_key]
            fields = [pypika.Field(c) for c in columns]
            timestamp_utc = self.func.to_utc(pypika.Field(self.timestamp_key)).as_(self.timestamp_key)
            return (
                pypika.Query()
                .from_(self.input_node._to_query())
                .select(
                    *fields,
                    timestamp_utc,
                )
            )
        else:
            return self.input_node._to_query()

    @staticmethod
    def for_feature_definition(
        dialect: Dialect, compute_mode: ComputeMode, fd: FeatureDefinitionWrapper, input_node: NodeRef
    ) -> NodeRef:
        return ConvertTimestampToUTCNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=input_node,
            timestamp_key=fd.timestamp_key,
        ).as_ref()


@attrs.frozen
class TakeLastRowNode(QueryNode):
    """Takes the last row partition by the `partition_by_columns` order by `order_by_column` descending.

    This is different from a 'last' Tecton aggregation since it is row-oriented, rather than column oriented.
    This means that it maintains all the fields of the returned row (including nulls and the timestamp). Tecton
    `last` aggregation ignores nulls.

    Example Input:
        partition_by_columns = ("user_id",)
        order_by_column = "timestamp"

        | user_id | value | timestamp           |
        |---------|-------|---------------------|
        | "user_1"| 10    | 2023-11-07T08:00:00Z|
        | "user_1"| null  | 2023-11-07T08:00:01Z|
        | "user_2"| 35    | 2023-11-07T09:00:00Z|
        | "user_2"| -1    | 2023-11-07T09:00:00Z|
        | "user_3"| 42    | 2023-11-07T10:00:00Z|

    Expected Output:
        | user_id | value | timestamp           |
        |---------|-------|---------------------|
        | "user_1"| null  | 2023-11-07T08:00:01Z|
        | "user_2"| -1    | 2023-11-07T09:10:00Z|
        | "user_3"| 42    | 2023-11-07T10:00:00Z|
    """

    input_node: NodeRef
    partition_by_columns: Tuple[str, ...]
    order_by_column: str

    @staticmethod
    def for_feature_definition(
        dialect: Dialect, compute_mode: ComputeMode, fdw: FeatureDefinitionWrapper, input_node: NodeRef
    ) -> NodeRef:
        batch_table_parts = fdw.fv_spec.online_batch_table_format.online_batch_table_parts
        if len(batch_table_parts) != 1:
            msg = "length of the spec's online_batch_table_format for temporal FV was not 1"
            raise ValueError(msg)

        return TakeLastRowNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=input_node,
            partition_by_columns=fdw.join_keys,
            order_by_column=fdw.timestamp_key,
        ).as_ref()

    @property
    def columns(self) -> Sequence[str]:
        return self.input_node.columns

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        return (
            f"Take last row, partition by ({self.partition_by_columns}), order by ({self.order_by_column}) descending"
        )

    def _to_query(self) -> pypika.queries.QueryBuilder:
        input_query = self.input_node._to_query()
        aliased_input = self.input_node.name
        fields = [Field(col) for col in self.columns]

        row_num = (
            RowNumber().over(*self.partition_by_columns).orderby(input_query[self.order_by_column], order=Order.desc)
        )

        row_num_query = (
            self.func.query()
            .with_(input_query, aliased_input)
            .from_(AliasedQuery(aliased_input))
            .select("*", row_num.as_("_tecton_row_num"))
        )

        query = self.func.query().from_(row_num_query).select(*fields).where(Field("_tecton_row_num") == 1)

        return query


@attrs.frozen
class TemporalBatchTableFormatNode(QueryNode):
    """Constructs temporal feature views in the new online materialization format (i.e. compaction).

    This format is expected to be a single OnlineBatchTablePart since temporal FVs are based around the 'last' row over a time window.
    """

    input_node: NodeRef
    fdw: FeatureDefinitionWrapper
    online_batch_table_part: OnlineBatchTablePart

    @staticmethod
    def for_feature_definition(
        dialect: Dialect, compute_mode: ComputeMode, fdw: FeatureDefinitionWrapper, input_node: NodeRef
    ) -> NodeRef:
        batch_table_parts = fdw.fv_spec.online_batch_table_format.online_batch_table_parts

        if not fdw.is_temporal:
            msg = "TemporalBatchTableFormat is only valid for Temporal FVs"
            raise ValueError(msg)

        if len(batch_table_parts) != 1:
            msg = "length of the spec's online_batch_table_format for Temporal FV was not 1"
            raise ValueError(msg)

        return TemporalBatchTableFormatNode(
            dialect=dialect,
            compute_mode=compute_mode,
            input_node=input_node,
            online_batch_table_part=batch_table_parts[0],
            fdw=fdw,
        ).as_ref()

    @property
    def columns(self) -> Sequence[str]:
        return (*self.fdw.join_keys, aggregation_group_id(), str(self.online_batch_table_part.window_index))

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        return "Convert row to the temporal batch table format"

    def _to_query(self) -> pypika.queries.QueryBuilder:
        raise NotImplementedError


@attrs.frozen
class TextEmbeddingInferenceNode(QueryNode):
    input_node: NodeRef
    inference_configs: Tuple[TextEmbeddingInferenceConfig, ...]

    @property
    def columns(self) -> Sequence[str]:
        output_columns = (c.output_column for c in self.inference_configs)
        return (*self.input_node.columns, *output_columns)

    @property
    def inputs(self) -> Sequence[NodeRef]:
        return (self.input_node,)

    def as_str(self) -> str:
        input_columns = [c.input_column for c in self.inference_configs]
        return f"Compute text embeddings over columns ({input_columns})"
