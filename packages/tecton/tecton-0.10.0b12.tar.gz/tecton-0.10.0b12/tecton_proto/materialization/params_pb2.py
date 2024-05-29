# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/materialization/params.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tecton_proto.common import aws_credentials_pb2 as tecton__proto_dot_common_dot_aws__credentials__pb2
from tecton_proto.common import id_pb2 as tecton__proto_dot_common_dot_id__pb2
from tecton_proto.data import entity_pb2 as tecton__proto_dot_data_dot_entity__pb2
from tecton_proto.data import feature_service_pb2 as tecton__proto_dot_data_dot_feature__service__pb2
from tecton_proto.data import feature_view_pb2 as tecton__proto_dot_data_dot_feature__view__pb2
from tecton_proto.data import transformation_pb2 as tecton__proto_dot_data_dot_transformation__pb2
from tecton_proto.data import virtual_data_source_pb2 as tecton__proto_dot_data_dot_virtual__data__source__pb2
from tecton_proto.dataobs import config_pb2 as tecton__proto_dot_dataobs_dot_config__pb2
from tecton_proto.materialization import job_metadata_pb2 as tecton__proto_dot_materialization_dot_job__metadata__pb2
from tecton_proto.materialization import materialization_task_pb2 as tecton__proto_dot_materialization_dot_materialization__task__pb2
from tecton_proto.online_store_writer import config_pb2 as tecton__proto_dot_online__store__writer_dot_config__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)tecton_proto/materialization/params.proto\x12\x1ctecton_proto.materialization\x1a)tecton_proto/common/aws_credentials.proto\x1a\x1ctecton_proto/common/id.proto\x1a\x1etecton_proto/data/entity.proto\x1a\'tecton_proto/data/feature_service.proto\x1a$tecton_proto/data/feature_view.proto\x1a&tecton_proto/data/transformation.proto\x1a+tecton_proto/data/virtual_data_source.proto\x1a!tecton_proto/dataobs/config.proto\x1a/tecton_proto/materialization/job_metadata.proto\x1a\x37tecton_proto/materialization/materialization_task.proto\x1a-tecton_proto/online_store_writer/config.proto\"\xb2\x14\n\x19MaterializationTaskParams\x12\x41\n\x0c\x66\x65\x61ture_view\x18\x16 \x01(\x0b\x32\x1e.tecton_proto.data.FeatureViewR\x0b\x66\x65\x61tureView\x12V\n\x14virtual_data_sources\x18\x11 \x03(\x0b\x32$.tecton_proto.data.VirtualDataSourceR\x12virtualDataSources\x12K\n\x0ftransformations\x18\x17 \x03(\x0b\x32!.tecton_proto.data.TransformationR\x0ftransformations\x12\x35\n\x08\x65ntities\x18\x34 \x03(\x0b\x32\x19.tecton_proto.data.EntityR\x08\x65ntities\x12)\n\x10\x66\x65\x61ture_services\x18& \x03(\tR\x0f\x66\x65\x61tureServices\x12\x43\n\rfeature_views\x18\x38 \x03(\x0b\x32\x1e.tecton_proto.data.FeatureViewR\x0c\x66\x65\x61tureViews\x12J\n\x0f\x66\x65\x61ture_service\x18\x39 \x01(\x0b\x32!.tecton_proto.data.FeatureServiceR\x0e\x66\x65\x61tureService\x12\x36\n\x17materialization_task_id\x18# \x01(\tR\x15materializationTaskId\x12\'\n\x0fidempotence_key\x18\x12 \x01(\tR\x0eidempotenceKey\x12\x36\n\nattempt_id\x18) \x01(\x0b\x32\x17.tecton_proto.common.IdR\tattemptId\x12\x39\n\x19spark_job_execution_table\x18\x13 \x01(\tR\x16sparkJobExecutionTable\x12,\n\x12job_metadata_table\x18( \x01(\tR\x10jobMetadataTable\x12&\n\x0f\x64\x65lta_log_table\x18\x32 \x01(\tR\rdeltaLogTable\x12i\n\x17job_metadata_table_type\x18, \x01(\x0e\x32\x32.tecton_proto.materialization.JobMetadataTableTypeR\x14jobMetadataTableType\x12\x32\n\x15\x64ynamodb_table_region\x18\x14 \x01(\tR\x13\x64ynamodbTableRegion\x12}\n\x1aonline_store_writer_config\x18\x18 \x01(\x0b\x32@.tecton_proto.online_store_writer.OnlineStoreWriterConfigurationR\x17onlineStoreWriterConfig\x12^\n\x1b\x64ynamodb_cross_account_role\x18\x35 \x01(\x0b\x32\x1f.tecton_proto.common.AwsIamRoleR\x18\x64ynamodbCrossAccountRole\x12\x44\n\x1f\x64ynamodb_cross_account_role_arn\x18\r \x01(\tR\x1b\x64ynamodbCrossAccountRoleArn\x12J\n\"dynamodb_cross_account_external_id\x18\x1e \x01(\tR\x1e\x64ynamodbCrossAccountExternalId\x12\x32\n\x15\x64\x62\x66s_credentials_path\x18! \x01(\tR\x13\x64\x62\x66sCredentialsPath\x12,\n\x12offline_store_path\x18\x03 \x01(\tR\x10offlineStorePath\x12=\n\x1buse_new_consumption_metrics\x18* \x01(\x08R\x18useNewConsumptionMetrics\x12\x1b\n\tcanary_id\x18\x15 \x01(\tR\x08\x63\x61naryId\x12x\n\x19\x64\x61ta_observability_config\x18% \x01(\x0b\x32<.tecton_proto.dataobs.DataObservabilityMaterializationConfigR\x17\x64\x61taObservabilityConfig\x12U\n\x0f\x62\x61tch_task_info\x18- \x01(\x0b\x32+.tecton_proto.materialization.BatchTaskInfoH\x00R\rbatchTaskInfo\x12X\n\x10stream_task_info\x18. \x01(\x0b\x32,.tecton_proto.materialization.StreamTaskInfoH\x00R\x0estreamTaskInfo\x12X\n\x10ingest_task_info\x18/ \x01(\x0b\x32,.tecton_proto.materialization.IngestTaskInfoH\x00R\x0eingestTaskInfo\x12^\n\x12\x64\x65letion_task_info\x18\x30 \x01(\x0b\x32..tecton_proto.materialization.DeletionTaskInfoH\x00R\x10\x64\x65letionTaskInfo\x12w\n\x1b\x64\x65lta_maintenance_task_info\x18\x31 \x01(\x0b\x32\x36.tecton_proto.materialization.DeltaMaintenanceTaskInfoH\x00R\x18\x64\x65ltaMaintenanceTaskInfo\x12\x61\n\x13\x66\x65\x61ture_export_info\x18\x33 \x01(\x0b\x32/.tecton_proto.materialization.FeatureExportInfoH\x00R\x11\x66\x65\x61tureExportInfo\x12z\n\x1c\x64\x61taset_generation_task_info\x18: \x01(\x0b\x32\x37.tecton_proto.materialization.DatasetGenerationTaskInfoH\x00R\x19\x64\x61tasetGenerationTaskInfo\x12\x35\n\x17secrets_api_service_url\x18\x36 \x01(\tR\x14secretsApiServiceUrl\x12\x31\n\x15secret_access_api_key\x18\x37 \x01(\tR\x12secretAccessApiKeyB\x0b\n\ttask_infoJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03J\x04\x08\x04\x10\x05J\x04\x08\x05\x10\x06J\x04\x08\x06\x10\x07J\x04\x08\x07\x10\x08J\x04\x08\x08\x10\tJ\x04\x08\t\x10\nJ\x04\x08\n\x10\x0bJ\x04\x08\x0b\x10\x0cJ\x04\x08\x0c\x10\rJ\x04\x08\x0e\x10\x0fJ\x04\x08\x0f\x10\x10J\x04\x08\x19\x10\x1aJ\x04\x08\x1a\x10\x1bJ\x04\x08\x1b\x10\x1cJ\x04\x08\x1c\x10\x1dJ\x04\x08\x1d\x10\x1eJ\x04\x08\x1f\x10 J\x04\x08 \x10!J\x04\x08\"\x10#J\x04\x08$\x10%J\x04\x08\'\x10(J\x04\x08+\x10,\"\xb1\x02\n\rBatchTaskInfo\x12g\n\x10\x62\x61tch_parameters\x18\x01 \x01(\x0b\x32<.tecton_proto.materialization.BatchMaterializationParametersR\x0f\x62\x61tchParameters\x12\x39\n\x19\x64ynamodb_json_output_path\x18\x02 \x01(\tR\x16\x64ynamodbJsonOutputPath\x12H\n!should_dedupe_online_store_writes\x18\x03 \x01(\x08R\x1dshouldDedupeOnlineStoreWrites\x12\x32\n\x15should_avoid_coalesce\x18\x04 \x01(\x08R\x13shouldAvoidCoalesce\"\x87\x02\n\x0eStreamTaskInfo\x12j\n\x11stream_parameters\x18\x01 \x01(\x0b\x32=.tecton_proto.materialization.StreamMaterializationParametersR\x10streamParameters\x12:\n\x19streaming_checkpoint_path\x18\x02 \x01(\tR\x17streamingCheckpointPath\x12M\n#streaming_trigger_interval_override\x18\x03 \x01(\tR streamingTriggerIntervalOverride\"|\n\x0eIngestTaskInfo\x12j\n\x11ingest_parameters\x18\x01 \x01(\x0b\x32=.tecton_proto.materialization.IngestMaterializationParametersR\x10ingestParameters\"u\n\x10\x44\x65letionTaskInfo\x12\x61\n\x13\x64\x65letion_parameters\x18\x01 \x01(\x0b\x32\x30.tecton_proto.materialization.DeletionParametersR\x12\x64\x65letionParameters\"\x96\x01\n\x18\x44\x65ltaMaintenanceTaskInfo\x12z\n\x1c\x64\x65lta_maintenance_parameters\x18\x01 \x01(\x0b\x32\x38.tecton_proto.materialization.DeltaMaintenanceParametersR\x1a\x64\x65ltaMaintenanceParameters\"\x86\x01\n\x11\x46\x65\x61tureExportInfo\x12q\n\x19\x66\x65\x61ture_export_parameters\x18\x01 \x01(\x0b\x32\x35.tecton_proto.materialization.FeatureExportParametersR\x17\x66\x65\x61tureExportParameters\"\x9a\x01\n\x19\x44\x61tasetGenerationTaskInfo\x12}\n\x1d\x64\x61taset_generation_parameters\x18\x01 \x01(\x0b\x32\x39.tecton_proto.materialization.DatasetGenerationParametersR\x1b\x64\x61tasetGenerationParametersB\x1e\n\x1a\x63om.tecton.materializationP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.materialization.params_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\032com.tecton.materializationP\001'
  _MATERIALIZATIONTASKPARAMS._serialized_start=533
  _MATERIALIZATIONTASKPARAMS._serialized_end=3143
  _BATCHTASKINFO._serialized_start=3146
  _BATCHTASKINFO._serialized_end=3451
  _STREAMTASKINFO._serialized_start=3454
  _STREAMTASKINFO._serialized_end=3717
  _INGESTTASKINFO._serialized_start=3719
  _INGESTTASKINFO._serialized_end=3843
  _DELETIONTASKINFO._serialized_start=3845
  _DELETIONTASKINFO._serialized_end=3962
  _DELTAMAINTENANCETASKINFO._serialized_start=3965
  _DELTAMAINTENANCETASKINFO._serialized_end=4115
  _FEATUREEXPORTINFO._serialized_start=4118
  _FEATUREEXPORTINFO._serialized_end=4252
  _DATASETGENERATIONTASKINFO._serialized_start=4255
  _DATASETGENERATIONTASKINFO._serialized_end=4409
# @@protoc_insertion_point(module_scope)
