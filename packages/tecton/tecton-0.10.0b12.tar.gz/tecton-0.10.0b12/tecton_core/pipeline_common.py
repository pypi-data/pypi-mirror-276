import functools
import operator
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Union

import numpy
import pandas
import pendulum

from tecton_core import errors
from tecton_core import time_utils
from tecton_core.id_helper import IdHelper
from tecton_proto.args.pipeline_pb2 import ConstantNode
from tecton_proto.args.pipeline_pb2 import DataSourceNode
from tecton_proto.args.pipeline_pb2 import Input as InputProto
from tecton_proto.args.pipeline_pb2 import Pipeline
from tecton_proto.args.pipeline_pb2 import PipelineNode
from tecton_proto.args.pipeline_pb2 import RequestContext as RequestContextProto
from tecton_proto.args.pipeline_pb2 import RequestDataSourceNode
from tecton_proto.args.pipeline_pb2 import TransformationNode


CONSTANT_TYPE = Optional[Union[str, int, float, bool]]
CONSTANT_TYPE_OBJECTS = (str, int, float, bool)


def _make_mode_to_type() -> Dict[str, Any]:
    lookup: Dict[str, Any] = {
        "pandas": pandas.DataFrame,
        "python": Dict,
        "pipeline": PipelineNode,
        "spark_sql": str,
        "snowflake_sql": str,
    }
    try:
        # The `pyspark.sql.connect.*` classes are the default for the Notebooks on Databricks Shared Access Mode
        # Clusters of Version 14.3 or higher. That's why we need to support them.
        from pyspark.sql import DataFrame

        try:
            from pyspark.sql.connect.session import DataFrame as ConnectDataFrame
        except ImportError:
            ConnectDataFrame = DataFrame

        lookup["pyspark"] = (DataFrame, ConnectDataFrame)
    except ImportError:
        pass
    try:
        import snowflake.snowpark

        lookup["snowpark"] = snowflake.snowpark.DataFrame
    except ImportError:
        pass
    return lookup


MODE_TO_TYPE_LOOKUP: Dict[str, Any] = _make_mode_to_type()


def constant_node_to_value(constant_node: ConstantNode) -> CONSTANT_TYPE:
    if constant_node.HasField("string_const"):
        return constant_node.string_const
    elif constant_node.HasField("int_const"):
        return int(constant_node.int_const)
    elif constant_node.HasField("float_const"):
        return float(constant_node.float_const)
    elif constant_node.HasField("bool_const"):
        return constant_node.bool_const
    elif constant_node.HasField("null_const"):
        return None
    msg = f"Unknown ConstantNode type: {constant_node}"
    raise KeyError(msg)


def get_keyword_inputs(transformation_node: TransformationNode) -> Dict[str, InputProto]:
    """Returns the keyword inputs of transformation_node in a dict."""
    return {
        node_input.arg_name: node_input for node_input in transformation_node.inputs if node_input.HasField("arg_name")
    }


def positional_inputs(transformation_node: TransformationNode) -> List[InputProto]:
    """Returns the positional inputs of transformation_node in order."""
    return [node_input for node_input in transformation_node.inputs if node_input.HasField("arg_index")]


def check_transformation_type(
    object_name: str,
    result: Any,  # noqa: ANN401
    mode: str,
    supported_modes: List[str],
) -> None:
    possible_mode = None
    for candidate_mode, candidate_type in MODE_TO_TYPE_LOOKUP.items():
        if isinstance(result, candidate_type):
            possible_mode = candidate_mode
            break
    expected_type = MODE_TO_TYPE_LOOKUP[mode]
    actual_type = type(result)

    if isinstance(result, expected_type):
        return
    elif possible_mode is not None and possible_mode in supported_modes:
        msg = f"Transformation function {object_name} with mode '{mode}' is expected to return result with type {expected_type}, but returns result with type {actual_type} instead. Did you mean to set mode='{possible_mode}'?"
        raise TypeError(msg)
    else:
        msg = f"Transformation function {object_name} with mode {mode} is expected to return result with type {expected_type}, but returns result with type {actual_type} instead."
        raise TypeError(msg)


def get_time_window_from_data_source_node(
    feature_time_limits: Optional[pendulum.Period],
    schedule_interval: Optional[pendulum.Duration],
    data_source_node: DataSourceNode,
) -> Optional[pendulum.Period]:
    if data_source_node.HasField("window") and feature_time_limits:
        new_start = feature_time_limits.start - time_utils.proto_to_duration(data_source_node.window)
        if schedule_interval:
            new_start = new_start + schedule_interval
        raw_data_limits = pendulum.Period(new_start, feature_time_limits.end)
    elif data_source_node.HasField("window_unbounded_preceding") and feature_time_limits:
        raw_data_limits = pendulum.Period(pendulum.datetime(1970, 1, 1), feature_time_limits.end)
    elif data_source_node.HasField("start_time_offset") and feature_time_limits:
        new_start = feature_time_limits.start + time_utils.proto_to_duration(data_source_node.start_time_offset)
        raw_data_limits = pendulum.Period(new_start, feature_time_limits.end)
    elif data_source_node.HasField("window_unbounded"):
        raw_data_limits = None
    else:
        # no data_source_override has been set
        raw_data_limits = feature_time_limits
    return raw_data_limits


# TODO(jiadong): Consolidate this method with `get_request_context_node` as they share similar functionality. Need to migrate off all usages of this method first.
def find_request_context(node: PipelineNode) -> Optional[RequestContextProto]:
    """Returns the request context for the pipeline. Assumes there is at most one RequestContext."""
    if node.HasField("request_data_source_node"):
        return node.request_data_source_node.request_context
    elif node.HasField("transformation_node"):
        for child in node.transformation_node.inputs:
            rc = find_request_context(child.node)
            if rc is not None:
                return rc
    return None


def get_input_name_to_ds_id_map(pipeline: Pipeline) -> Dict[str, str]:
    """Return a map from input name to data source id for the pipeline."""
    data_source_nodes = get_all_data_source_nodes(pipeline)
    return {
        node.data_source_node.input_name: IdHelper.to_string(node.data_source_node.virtual_data_source_id)
        for node in data_source_nodes
    }


def get_request_context_node(pipeline: Pipeline) -> Optional[RequestDataSourceNode]:
    """Returns the request_data_source_node for the pipeline. Assumes there is at most one RequestContext."""
    rc_node = [node for node in get_all_pipeline_nodes(pipeline.root) if node.HasField("request_data_source_node")]

    if len(rc_node) == 0:
        return None
    elif len(rc_node) == 1:
        return rc_node[0].request_data_source_node
    else:
        msg = "ODFV is not supposed to have more than 1 request_data_source_node"
        raise errors.TectonValidationError(msg)


def get_all_feature_view_nodes(pipeline: Pipeline) -> List[PipelineNode]:
    """Returns all feature view nodes from the provided pipeline."""
    return [node for node in get_all_pipeline_nodes(pipeline.root) if node.HasField("feature_view_node")]


def get_all_data_source_nodes(pipeline: Pipeline) -> List[PipelineNode]:
    """Returns all data source nodes from the provided pipeline."""
    return [node for node in get_all_pipeline_nodes(pipeline.root) if node.HasField("data_source_node")]


def get_all_pipeline_nodes(node: PipelineNode) -> List[PipelineNode]:
    """Returns all data source nodes from the provided node."""
    if node.HasField("transformation_node"):
        return functools.reduce(
            operator.iadd, [get_all_pipeline_nodes(input.node) for input in node.transformation_node.inputs], []
        )
    else:
        return [node]


def get_all_input_keys(node: PipelineNode) -> Set[str]:
    names_set = set()
    _get_all_input_keys_helper(node, names_set)
    return names_set


def _get_all_input_keys_helper(node: PipelineNode, names_set: Set[str]) -> Set[str]:
    if node.HasField("request_data_source_node"):
        names_set.add(node.request_data_source_node.input_name)
    elif node.HasField("data_source_node"):
        names_set.add(node.data_source_node.input_name)
    elif node.HasField("feature_view_node"):
        names_set.add(node.feature_view_node.input_name)
    elif node.HasField("transformation_node"):
        for child in node.transformation_node.inputs:
            _get_all_input_keys_helper(child.node, names_set)
    return names_set


def get_fco_ids_to_input_keys(node: PipelineNode) -> Dict[str, str]:
    names_dict = {}
    _get_fco_ids_to_input_keys_helper(node, names_dict)
    return names_dict


def _get_fco_ids_to_input_keys_helper(node: PipelineNode, names_dict: Dict[str, str]) -> Dict[str, str]:
    if node.HasField("request_data_source_node"):
        # request data sources don't have fco ids
        pass
    elif node.HasField("data_source_node"):
        ds_node = node.data_source_node
        names_dict[IdHelper.to_string(ds_node.virtual_data_source_id)] = ds_node.input_name
    elif node.HasField("feature_view_node"):
        fv_node = node.feature_view_node
        names_dict[IdHelper.to_string(fv_node.feature_view_id)] = fv_node.input_name
    elif node.HasField("transformation_node"):
        for child in node.transformation_node.inputs:
            _get_fco_ids_to_input_keys_helper(child.node, names_dict)
    return names_dict


def convert_ndarray_to_list(item):
    if isinstance(item, numpy.ndarray):
        return item.tolist()
    elif isinstance(item, dict):
        return {key: convert_ndarray_to_list(value) for key, value in item.items()}
    elif isinstance(item, list):
        return [convert_ndarray_to_list(value) for value in item]
    else:
        return item
