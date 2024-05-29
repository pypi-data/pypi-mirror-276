import urllib
from typing import Optional

import ray
from google.protobuf import timestamp_pb2

from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_materialization.common.task_params import feature_definition_from_task_params
from tecton_materialization.ray.delta import DeltaWriter
from tecton_materialization.ray.delta import OfflineStoreParams
from tecton_proto.data.feature_view_pb2 import FeatureView
from tecton_proto.materialization.params_pb2 import MaterializationTaskParams
from tecton_proto.online_store_writer.config_pb2 import OnlineStoreWriterConfiguration
from tecton_proto.online_store_writer.copier_pb2 import LocalFileStage
from tecton_proto.online_store_writer.copier_pb2 import ObjectCopyRequest
from tecton_proto.online_store_writer.copier_pb2 import OnlineStoreCopierRequest
from tecton_proto.online_store_writer.copier_pb2 import S3Stage
from tecton_proto.online_store_writer.copier_pb2 import StatusUpdateRequest
from tecton_proto.online_store_writer.copier_pb2 import TimestampUnit


def run_online_store_copier(request):
    request_bytes = request.SerializeToString()
    runner_function = ray.cross_language.java_function(
        "com.tecton.onlinestorewriter.OnlineStoreCopier", "runFromSerializedRequest"
    )
    job = runner_function.remote(request_bytes, None)
    ray.get(job)


def write_to_online_store(
    online_store_writer_config: OnlineStoreWriterConfiguration,
    feature_view: FeatureView,
    feature_end_timestamp: timestamp_pb2.Timestamp,
    fd: FeatureDefinitionWrapper,
    stage_uri_str: str,
) -> None:
    stage_uri = urllib.parse.urlparse(stage_uri_str)
    if stage_uri.scheme in ("file", ""):
        request = OnlineStoreCopierRequest(
            online_store_writer_configuration=online_store_writer_config,
            feature_view=feature_view,
            object_copy_request=ObjectCopyRequest(
                local_file_stage=LocalFileStage(location=stage_uri.path), timestamp_units=TimestampUnit.MICROS
            ),
        )
    elif stage_uri.scheme == "s3":
        key = stage_uri.path
        if key.startswith("/"):
            key = key[1:]
        request = OnlineStoreCopierRequest(
            online_store_writer_configuration=online_store_writer_config,
            feature_view=feature_view,
            object_copy_request=ObjectCopyRequest(
                s3_stage=S3Stage(
                    bucket=stage_uri.netloc,
                    key=key,
                ),
                timestamp_units=TimestampUnit.MICROS,
            ),
        )
    else:
        msg = f"Unexpected staging uri scheme: {stage_uri.scheme}"
        raise NotImplementedError(msg)
    run_online_store_copier(request)

    # Issue status update
    if fd.is_temporal_aggregate and not fd.is_continuous:
        anchor_time = feature_end_timestamp.ToDatetime() - fd.aggregate_slide_interval.ToTimedelta()
        anchor_time_pb = timestamp_pb2.Timestamp()
        anchor_time_pb.FromDatetime(anchor_time)
        status_update = StatusUpdateRequest(anchor_time=anchor_time_pb)
    else:
        status_update = StatusUpdateRequest(materialized_raw_data_end_time=feature_end_timestamp)

    status_request = OnlineStoreCopierRequest(
        online_store_writer_configuration=online_store_writer_config,
        feature_view=feature_view,
        status_update_request=status_update,
    )
    run_online_store_copier(status_request)


def get_delta_writer(
    params: MaterializationTaskParams,
    store_params_override: Optional[OfflineStoreParams] = None,
    table_uri_override: Optional[str] = None,
) -> DeltaWriter:
    role = params.dynamodb_cross_account_role if params.HasField("dynamodb_cross_account_role") else None
    fd = feature_definition_from_task_params(params)

    return DeltaWriter(
        store_params=store_params_override if store_params_override else OfflineStoreParams.for_feature_definition(fd),
        table_uri=table_uri_override if table_uri_override else params.offline_store_path,
        dynamodb_log_table_name=params.delta_log_table,
        dynamodb_log_table_region=params.dynamodb_table_region,
        dynamodb_cross_account_role=role,
    )
