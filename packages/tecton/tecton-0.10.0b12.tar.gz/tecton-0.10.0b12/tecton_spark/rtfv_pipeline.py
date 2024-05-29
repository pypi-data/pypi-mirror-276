import re
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas
from pyspark.sql.types import ArrayType
from pyspark.sql.types import MapType
from pyspark.sql.types import StructType

from tecton_core import conf
from tecton_core import specs
from tecton_core.compute_mode import ComputeMode
from tecton_core.errors import UDF_ERROR
from tecton_core.errors import UDF_TYPE_ERROR
from tecton_core.id_helper import IdHelper
from tecton_core.pipeline_common import constant_node_to_value
from tecton_core.pipeline_common import convert_ndarray_to_list
from tecton_core.query_consts import udf_internal
from tecton_proto.args.pipeline_pb2 import Pipeline
from tecton_proto.args.pipeline_pb2 import PipelineNode
from tecton_proto.args.pipeline_pb2 import TransformationNode
from tecton_proto.args.transformation_pb2 import TransformationMode
from tecton_spark import feature_view_spark_utils
from tecton_spark.spark_pipeline import SparkFeaturePipeline
from tecton_spark.type_annotations import PySparkDataFrame


# TODO(TEC-8978): remove \. from namespace regex when FWv3 FVs are no longer supported.
_NAMESPACE_SEPARATOR_REGEX = re.compile(r"__|\.")


def feature_name(namespaced_feature_name: str) -> str:
    """Gets the base feature name from a namespaced_feature_name (e.g. feature_view__feature)

    Supports both `__` (fwv5) and `.` (fwv3) separators. Does two attempts at
    getting the feature name since `__` was allowed in feature view names in
    fwv3.
    """

    spl = _NAMESPACE_SEPARATOR_REGEX.split(namespaced_feature_name)
    if len(spl) == 2:
        return spl[1]

    return namespaced_feature_name.split(".")[1]


# For Pandas-mode:
# A pandas udf takes as inputs (pandas.Series...) and outputs pandas.Series.
# However, the user-defined transforms take as input pandas.DataFrame and output
# pandas.DataFrame. RealtimeFeaturePipeline will construct a UDF Wrapper functions
# that translates the inputs and outputs and performs some type checking.
#
# The general idea is that each Node of the pipeline evaluates to a pandas.DataFrame.
# This is what we want since the user-defined transforms take pandas.DataFrame
# as inputs both from RequestDataSourceNode or FeatureViewNode.
# pandas_udf_wrapper then typechecks and translates the final pandas.DataFrame into a
# jsonized pandas.Series to match what spark expects.
#
# For Python-mode, we can use a simpler wrapper function for the udf because we don't do
# any spark<->pandas type conversions.
class RealtimeFeaturePipeline(SparkFeaturePipeline):
    _VALID_MODES = ["pipeline", "python", "pandas"]

    def __init__(
        self,
        name: str,
        pipeline: Pipeline,
        transformations: List[specs.TransformationSpec],
        # maps input + feature name to arg index that udf function wrapper will be called with.
        # this is needed because we need to know which pandas.Series that are inputs to this
        # function correspond to the desired request context fields or dependent fv features
        # that the customer-defined udf uses.
        udf_arg_idx_map: Dict[str, int],
        output_schema: Optional[StructType],
        # the id of this OnDemandFeatureView; only required to be set when reading from source data
        fv_id: Optional[str] = None,
        data_source_inputs: Optional[Dict[str, Union[Dict[str, Any], pandas.DataFrame]]] = None,
    ) -> None:
        self._pipeline = pipeline
        self._name = name
        self._fv_id = fv_id
        self.udf_arg_idx_map = udf_arg_idx_map
        self._id_to_transformation = {t.id: t for t in transformations}
        self._output_schema = output_schema
        self._data_source_inputs = data_source_inputs
        # In Spark, the UDF cannot reference a proto enum, so instead save mode as a string
        self.mode = (
            "python"
            if self._id_to_transformation[
                IdHelper.to_string(self._pipeline.root.transformation_node.transformation_id)
            ].transformation_mode
            == TransformationMode.TRANSFORMATION_MODE_PYTHON
            else "pandas"
        )
        # Access this conf value outside of the UDF to avoid doing it many times and avoiding any worker/driver state issues.
        self._should_check_output_schema = conf.get_bool("TECTON_PYTHON_ODFV_OUTPUT_SCHEMA_CHECK_ENABLED")

    def get_dataframe(self) -> PySparkDataFrame:
        df = self._node_to_value(self._pipeline.root)
        return df

    def py_wrapper(self, *args):
        assert self.mode == "python"
        self._udf_args: List = args
        res = self._node_to_value(self._pipeline.root)
        if self._should_check_output_schema:
            feature_view_spark_utils.check_python_odfv_output_schema(res, self._output_schema, self._name)
        return res

    def pandas_udf_wrapper(self, *args):
        assert self.mode == "pandas"

        import json

        import pandas

        # self.udf_arg_idx_map tells us which of these pandas.Series correspond to a given
        # RequestDataSource or FeatureView input
        self._udf_args: List[pandas.Series] = args

        output_df = self._node_to_value(self._pipeline.root)

        assert isinstance(
            output_df, pandas.DataFrame
        ), f"Transformer returns {str(output_df)}, but must return a pandas.DataFrame instead."

        for field in self._output_schema:
            assert field.name in output_df.columns, (
                f"Expected output schema field '{field.name}' not found in columns of DataFrame returned by "
                f"'{self._name}': [" + ", ".join(output_df.columns) + "]"
            )
            # Convert numpy.arrays to python lists which are JSON serializable by the default serializer.
            if isinstance(field.dataType, (ArrayType, MapType, StructType)):
                output_df[field.name] = output_df[field.name].apply(convert_ndarray_to_list)

        output_strs = []

        # itertuples() is used instead of iterrows() to preserve type safety.
        # See notes in https://pandas.pydata.org/pandas-docs/version/0.17.1/generated/pandas.DataFrame.iterrows.html.
        for row in output_df.itertuples(index=False):
            output_strs.append(json.dumps(row._asdict()))
        return pandas.Series(output_strs)

    def _node_to_value(
        self, pipeline_node: PipelineNode
    ) -> Union[str, int, float, bool, None, Dict[str, Any], pandas.DataFrame, PySparkDataFrame, pandas.Series]:
        if pipeline_node.HasField("constant_node"):
            return constant_node_to_value(pipeline_node.constant_node)
        elif pipeline_node.HasField("feature_view_node"):
            if self._data_source_inputs is not None:
                return self._data_source_inputs[pipeline_node.feature_view_node.input_name]
            elif self.mode == "python":
                fields_dict = {}
                # The input name of this FeatureViewNode tells us which of the udf_args
                # correspond to the Dict we should generate that the parent TransformationNode
                # expects as an input. It also expects the DataFrame to have its columns named
                # by the feature names.
                for feature in self.udf_arg_idx_map:
                    if not feature.startswith(
                        f"{udf_internal(ComputeMode.SPARK)}_{pipeline_node.feature_view_node.input_name}_{self._fv_id}"
                    ):
                        continue
                    idx = self.udf_arg_idx_map[feature]
                    fields_dict[feature_name(feature)] = self._udf_args[idx]
                return fields_dict
            elif self.mode == "pandas":
                all_series = []
                features = []
                # The input name of this FeatureViewNode tells us which of the udf_args
                # correspond to the pandas.DataFrame we should generate that the parent TransformationNode
                # expects as an input. It also expects the DataFrame to have its columns named
                # by the feature names.
                for feature in self.udf_arg_idx_map:
                    if not feature.startswith(
                        f"{udf_internal(ComputeMode.SPARK)}_{pipeline_node.feature_view_node.input_name}_{self._fv_id}"
                    ):
                        continue
                    idx = self.udf_arg_idx_map[feature]
                    all_series.append(self._udf_args[idx])
                    features.append(feature_name(feature))
                df = pandas.concat(all_series, keys=features, axis=1)
                return df
            else:
                msg = "Transform mode {self.mode} is not yet implemented"
                raise NotImplementedError(msg)
        elif pipeline_node.HasField("request_data_source_node"):
            if self._data_source_inputs is not None:
                return self._data_source_inputs[pipeline_node.request_data_source_node.input_name]
            elif self.mode == "python":
                request_context = pipeline_node.request_data_source_node.request_context
                field_names = [c.name for c in request_context.tecton_schema.columns]
                fields_dict = {}
                for input_col in field_names:
                    idx = self.udf_arg_idx_map[input_col]
                    fields_dict[input_col] = self._udf_args[idx]
                return fields_dict
            elif self.mode == "pandas":
                all_series = []
                request_context = pipeline_node.request_data_source_node.request_context
                field_names = [c.name for c in request_context.tecton_schema.columns]
                for input_col in field_names:
                    idx = self.udf_arg_idx_map[input_col]
                    all_series.append(self._udf_args[idx])
                df = pandas.concat(all_series, keys=field_names, axis=1)
                return df
            else:
                msg = "Transform mode {self.mode} is not yet implemented"
                raise NotImplementedError(msg)
        elif pipeline_node.HasField("transformation_node"):
            return self._transformation_node_to_dataframe(pipeline_node.transformation_node)
        elif pipeline_node.HasField("materialization_context_node"):
            msg = "MaterializationContext is unsupported for pandas pipelines"
            raise ValueError(msg)
        else:
            msg = "This is not yet implemented"
            raise NotImplementedError(msg)

    def _apply_transformation_function(
        self, transformation_node: TransformationNode, args: List[Any], kwargs: Dict[str, Any]
    ) -> Union[Dict[str, Any], pandas.DataFrame, PySparkDataFrame]:
        """For the given transformation node, returns the corresponding DataFrame transformation.

        If needed, resulted function is wrapped with a function that translates mode-specific input/output types to DataFrames.
        """
        transformation = self.get_transformation_by_id(transformation_node.transformation_id)
        mode = transformation.transformation_mode
        user_function = transformation.user_function

        if (
            mode != TransformationMode.TRANSFORMATION_MODE_PANDAS
            and mode != TransformationMode.TRANSFORMATION_MODE_PYTHON
        ):
            msg = f"Unsupported transformation mode({transformation.transformation_mode}) for Realtime Feature Views."
            raise KeyError(msg)

        try:
            return user_function(*args, **kwargs)
        except TypeError as e:
            raise UDF_TYPE_ERROR(e)
        except Exception as e:
            raise UDF_ERROR(e)
