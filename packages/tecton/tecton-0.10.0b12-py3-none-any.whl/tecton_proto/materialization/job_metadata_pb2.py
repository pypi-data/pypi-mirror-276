# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/materialization/job_metadata.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from tecton_proto.spark_common import clusters_pb2 as tecton__proto_dot_spark__common_dot_clusters__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/tecton_proto/materialization/job_metadata.proto\x12\x1ctecton_proto.materialization\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a(tecton_proto/spark_common/clusters.proto\"\xfb\x03\n\x0bJobMetadata\x12\x8a\x01\n\"online_store_copier_execution_info\x18\x01 \x01(\x0b\x32<.tecton_proto.materialization.OnlineStoreCopierExecutionInfoH\x00R\x1eonlineStoreCopierExecutionInfo\x12g\n\x14spark_execution_info\x18\x03 \x01(\x0b\x32\x33.tecton_proto.materialization.SparkJobExecutionInfoH\x00R\x12sparkExecutionInfo\x12\x61\n\x13tecton_managed_info\x18\x04 \x01(\x0b\x32/.tecton_proto.materialization.TectonManagedInfoH\x00R\x11tectonManagedInfo\x12\x86\x01\n materialization_consumption_info\x18\x02 \x01(\x0b\x32<.tecton_proto.materialization.MaterializationConsumptionInfoR\x1ematerializationConsumptionInfoB\n\n\x08job_info\"?\n\x1eOnlineStoreCopierExecutionInfo\x12\x1d\n\nis_revoked\x18\x01 \x01(\x08R\tisRevoked\"\xdd\x01\n\x15SparkJobExecutionInfo\x12\x15\n\x06run_id\x18\x01 \x01(\tR\x05runId\x12\x1d\n\nis_revoked\x18\x02 \x01(\x08R\tisRevoked\x12\x8d\x01\n#stream_handoff_synchronization_info\x18\x03 \x01(\x0b\x32>.tecton_proto.materialization.StreamHandoffSynchronizationInfoR streamHandoffSynchronizationInfo\"\x91\x02\n StreamHandoffSynchronizationInfo\x12.\n\x13new_cluster_started\x18\x01 \x01(\x08R\x11newClusterStarted\x12;\n\x1astream_query_start_allowed\x18\x02 \x01(\x08R\x17streamQueryStartAllowed\x12@\n\x1cquery_cancellation_requested\x18\x03 \x01(\x08R\x1aqueryCancellationRequested\x12>\n\x1bquery_cancellation_complete\x18\x04 \x01(\x08R\x19queryCancellationComplete\"\xfc\x02\n\x1eMaterializationConsumptionInfo\x12z\n\x19offline_store_consumption\x18\x01 \x01(\x0b\x32>.tecton_proto.materialization.OfflineStoreWriteConsumptionInfoR\x17offlineStoreConsumption\x12w\n\x18online_store_consumption\x18\x02 \x01(\x0b\x32=.tecton_proto.materialization.OnlineStoreWriteConsumptionInfoR\x16onlineStoreConsumption\x12\x65\n\x13\x63ompute_consumption\x18\x03 \x01(\x0b\x32\x34.tecton_proto.materialization.ComputeConsumptionInfoR\x12\x63omputeConsumption\"\xfc\x02\n OfflineStoreWriteConsumptionInfo\x12~\n\x10\x63onsumption_info\x18\x01 \x03(\x0b\x32S.tecton_proto.materialization.OfflineStoreWriteConsumptionInfo.ConsumptionInfoEntryR\x0f\x63onsumptionInfo\x12\\\n\x12offline_store_type\x18\x02 \x01(\x0e\x32..tecton_proto.materialization.OfflineStoreTypeR\x10offlineStoreType\x1az\n\x14\x43onsumptionInfoEntry\x12\x10\n\x03key\x18\x01 \x01(\x03R\x03key\x12L\n\x05value\x18\x02 \x01(\x0b\x32\x36.tecton_proto.materialization.OfflineConsumptionBucketR\x05value:\x02\x38\x01\"h\n\x18OfflineConsumptionBucket\x12!\n\x0crows_written\x18\x01 \x01(\x03R\x0browsWritten\x12)\n\x10\x66\x65\x61tures_written\x18\x02 \x01(\x03R\x0f\x66\x65\x61turesWritten\"\xf6\x02\n\x1fOnlineStoreWriteConsumptionInfo\x12}\n\x10\x63onsumption_info\x18\x01 \x03(\x0b\x32R.tecton_proto.materialization.OnlineStoreWriteConsumptionInfo.ConsumptionInfoEntryR\x0f\x63onsumptionInfo\x12Y\n\x11online_store_type\x18\x02 \x01(\x0e\x32-.tecton_proto.materialization.OnlineStoreTypeR\x0fonlineStoreType\x1ay\n\x14\x43onsumptionInfoEntry\x12\x10\n\x03key\x18\x01 \x01(\x03R\x03key\x12K\n\x05value\x18\x02 \x01(\x0b\x32\x35.tecton_proto.materialization.OnlineConsumptionBucketR\x05value:\x02\x38\x01\"m\n\x17OnlineConsumptionBucket\x12!\n\x0crows_written\x18\x01 \x01(\x03R\x0browsWritten\x12)\n\x10\x66\x65\x61tures_written\x18\x02 \x01(\x03R\x0f\x66\x65\x61turesWrittenJ\x04\x08\x03\x10\x04\"\xa0\x01\n\x16\x43omputeConsumptionInfo\x12\x35\n\x08\x64uration\x18\x01 \x01(\x0b\x32\x19.google.protobuf.DurationR\x08\x64uration\x12O\n\rcompute_usage\x18\x02 \x03(\x0b\x32*.tecton_proto.materialization.ComputeUsageR\x0c\x63omputeUsage\"\xbb\x01\n\x0c\x43omputeUsage\x12_\n\x15instance_availability\x18\x01 \x01(\x0e\x32*.tecton_proto.spark_common.AwsAvailabilityR\x14instanceAvailability\x12#\n\rinstance_type\x18\x02 \x01(\tR\x0cinstanceType\x12%\n\x0einstance_count\x18\x03 \x01(\x03R\rinstanceCount\"\xca\x06\n\x12TectonManagedStage\x12Y\n\nstage_type\x18\x01 \x01(\x0e\x32:.tecton_proto.materialization.TectonManagedStage.StageTypeR\tstageType\x12L\n\x05state\x18\x02 \x01(\x0e\x32\x36.tecton_proto.materialization.TectonManagedStage.StateR\x05state\x12#\n\rexternal_link\x18\x03 \x01(\tR\x0c\x65xternalLink\x12\x1a\n\x08progress\x18\x04 \x01(\x02R\x08progress\x12 \n\x0b\x64\x65scription\x18\x05 \x01(\tR\x0b\x64\x65scription\x12Y\n\nerror_type\x18\x06 \x01(\x0e\x32:.tecton_proto.materialization.TectonManagedStage.ErrorTypeR\terrorType\x12!\n\x0c\x65rror_detail\x18\x07 \x01(\tR\x0b\x65rrorDetail\x12,\n\x12\x63ompiled_sql_query\x18\x08 \x01(\tR\x10\x63ompiledSqlQuery\x12\x35\n\x08\x64uration\x18\t \x01(\x0b\x32\x19.google.protobuf.DurationR\x08\x64uration\x12\x39\n\nstart_time\x18\n \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tstartTime\"Z\n\tStageType\x12\r\n\tSNOWFLAKE\x10\x01\x12\n\n\x06PYTHON\x10\x02\x12\r\n\tAGGREGATE\x10\x03\x12\x11\n\rOFFLINE_STORE\x10\x04\x12\x10\n\x0cONLINE_STORE\x10\x05\"_\n\x05State\x12\x15\n\x11STATE_UNSPECIFIED\x10\x00\x12\x0b\n\x07PENDING\x10\x01\x12\x0b\n\x07RUNNING\x10\x02\x12\x0b\n\x07SUCCESS\x10\x03\x12\t\n\x05\x45RROR\x10\x04\x12\r\n\tCANCELLED\x10\x05\"M\n\tErrorType\x12\x1a\n\x16\x45RROR_TYPE_UNSPECIFIED\x10\x00\x12\x14\n\x10UNEXPECTED_ERROR\x10\x01\x12\x0e\n\nUSER_ERROR\x10\x03\"\xab\x01\n\x11TectonManagedInfo\x12H\n\x06stages\x18\x01 \x03(\x0b\x32\x30.tecton_proto.materialization.TectonManagedStageR\x06stages\x12L\n\x05state\x18\x02 \x01(\x0e\x32\x36.tecton_proto.materialization.TectonManagedStage.StateR\x05state*\x8f\x01\n\x0fOnlineStoreType\x12!\n\x1dONLINE_STORE_TYPE_UNSPECIFIED\x10\x00\x12\x1c\n\x18ONLINE_STORE_TYPE_DYNAMO\x10\x01\x12\x1b\n\x17ONLINE_STORE_TYPE_REDIS\x10\x02\x12\x1e\n\x1aONLINE_STORE_TYPE_BIGTABLE\x10\x03*\x8a\x01\n\x10OfflineStoreType\x12\"\n\x1eOFFLINE_STORE_TYPE_UNSPECIFIED\x10\x00\x12\x19\n\x15OFFLINE_STORE_TYPE_S3\x10\x01\x12\x1b\n\x17OFFLINE_STORE_TYPE_DBFS\x10\x02\x12\x1a\n\x16OFFLINE_STORE_TYPE_GCS\x10\x03*\x84\x01\n\x14JobMetadataTableType\x12\'\n#JOB_METADATA_TABLE_TYPE_UNSPECIFIED\x10\x00\x12\"\n\x1eJOB_METADATA_TABLE_TYPE_DYNAMO\x10\x01\x12\x1f\n\x1bJOB_METADATA_TABLE_TYPE_GCS\x10\x02\x42\x1e\n\x1a\x63om.tecton.materializationP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.materialization.job_metadata_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\032com.tecton.materializationP\001'
  _OFFLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._options = None
  _OFFLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._serialized_options = b'8\001'
  _ONLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._options = None
  _ONLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._serialized_options = b'8\001'
  _ONLINESTORETYPE._serialized_start=3996
  _ONLINESTORETYPE._serialized_end=4139
  _OFFLINESTORETYPE._serialized_start=4142
  _OFFLINESTORETYPE._serialized_end=4280
  _JOBMETADATATABLETYPE._serialized_start=4283
  _JOBMETADATATABLETYPE._serialized_end=4415
  _JOBMETADATA._serialized_start=189
  _JOBMETADATA._serialized_end=696
  _ONLINESTORECOPIEREXECUTIONINFO._serialized_start=698
  _ONLINESTORECOPIEREXECUTIONINFO._serialized_end=761
  _SPARKJOBEXECUTIONINFO._serialized_start=764
  _SPARKJOBEXECUTIONINFO._serialized_end=985
  _STREAMHANDOFFSYNCHRONIZATIONINFO._serialized_start=988
  _STREAMHANDOFFSYNCHRONIZATIONINFO._serialized_end=1261
  _MATERIALIZATIONCONSUMPTIONINFO._serialized_start=1264
  _MATERIALIZATIONCONSUMPTIONINFO._serialized_end=1644
  _OFFLINESTOREWRITECONSUMPTIONINFO._serialized_start=1647
  _OFFLINESTOREWRITECONSUMPTIONINFO._serialized_end=2027
  _OFFLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._serialized_start=1905
  _OFFLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._serialized_end=2027
  _OFFLINECONSUMPTIONBUCKET._serialized_start=2029
  _OFFLINECONSUMPTIONBUCKET._serialized_end=2133
  _ONLINESTOREWRITECONSUMPTIONINFO._serialized_start=2136
  _ONLINESTOREWRITECONSUMPTIONINFO._serialized_end=2510
  _ONLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._serialized_start=2389
  _ONLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._serialized_end=2510
  _ONLINECONSUMPTIONBUCKET._serialized_start=2512
  _ONLINECONSUMPTIONBUCKET._serialized_end=2621
  _COMPUTECONSUMPTIONINFO._serialized_start=2624
  _COMPUTECONSUMPTIONINFO._serialized_end=2784
  _COMPUTEUSAGE._serialized_start=2787
  _COMPUTEUSAGE._serialized_end=2974
  _TECTONMANAGEDSTAGE._serialized_start=2977
  _TECTONMANAGEDSTAGE._serialized_end=3819
  _TECTONMANAGEDSTAGE_STAGETYPE._serialized_start=3553
  _TECTONMANAGEDSTAGE_STAGETYPE._serialized_end=3643
  _TECTONMANAGEDSTAGE_STATE._serialized_start=3645
  _TECTONMANAGEDSTAGE_STATE._serialized_end=3740
  _TECTONMANAGEDSTAGE_ERRORTYPE._serialized_start=3742
  _TECTONMANAGEDSTAGE_ERRORTYPE._serialized_end=3819
  _TECTONMANAGEDINFO._serialized_start=3822
  _TECTONMANAGEDINFO._serialized_end=3993
# @@protoc_insertion_point(module_scope)
