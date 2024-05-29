# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/data/serving_status.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from tecton_proto.common import id_pb2 as tecton__proto_dot_common_dot_id__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&tecton_proto/data/serving_status.proto\x12\x11tecton_proto.data\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1ctecton_proto/common/id.proto\"m\n\rServingStatus\x12\x44\n\rserving_state\x18\x01 \x01(\x0e\x32\x1f.tecton_proto.data.ServingStateR\x0cservingState\x12\x16\n\x06\x65rrors\x18\x02 \x03(\tR\x06\x65rrors\"\xcd\x01\n\x0bStatusRange\x12\x43\n\x0f\x62\x65gin_inclusive\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0e\x62\x65ginInclusive\x12?\n\rend_exclusive\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0c\x65ndExclusive\x12\x38\n\x06status\x18\x03 \x01(\x0b\x32 .tecton_proto.data.ServingStatusR\x06status\"\xc5\x01\n FeatureViewMaterializationRanges\x12?\n\x0f\x66\x65\x61ture_view_id\x18\x01 \x01(\x0b\x32\x17.tecton_proto.common.IdR\rfeatureViewId\x12`\n\x1c\x62\x61tch_materialization_ranges\x18\x02 \x03(\x0b\x32\x1e.tecton_proto.data.StatusRangeR\x1a\x62\x61tchMaterializationRanges\"\xa0\x05\n\x14ServingStatusSummary\x12X\n\x18offline_readiness_ranges\x18\x01 \x03(\x0b\x32\x1e.tecton_proto.data.StatusRangeR\x16offlineReadinessRanges\x12V\n\x17online_readiness_ranges\x18\x07 \x03(\x0b\x32\x1e.tecton_proto.data.StatusRangeR\x15onlineReadinessRanges\x12u\n\x1c\x62\x61tch_materialization_ranges\x18\x04 \x03(\x0b\x32\x33.tecton_proto.data.FeatureViewMaterializationRangesR\x1a\x62\x61tchMaterializationRanges\x12L\n\x14streaming_start_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x12streamingStartTime\x12Z\n\x18streaming_serving_status\x18\x02 \x01(\x0b\x32 .tecton_proto.data.ServingStatusR\x16streamingServingStatus\x12O\n\x16most_recent_ready_time\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x13mostRecentReadyTime\x12\x64\n!most_recent_batch_processing_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x1dmostRecentBatchProcessingTime\"\xc7\x01\n\x1f\x46\x65\x61tureViewServingStatusSummary\x12?\n\x0f\x66\x65\x61ture_view_id\x18\x03 \x01(\x0b\x32\x17.tecton_proto.common.IdR\rfeatureViewId\x12]\n\x16serving_status_summary\x18\x02 \x01(\x0b\x32\'.tecton_proto.data.ServingStatusSummaryR\x14servingStatusSummaryJ\x04\x08\x01\x10\x02\"\xa6\x02\n FullFeatureServiceServingSummary\x12{\n&feature_service_serving_status_summary\x18\x02 \x01(\x0b\x32\'.tecton_proto.data.ServingStatusSummaryR\"featureServiceServingStatusSummary\x12\x84\x01\n%feature_view_serving_status_summaries\x18\x03 \x03(\x0b\x32\x32.tecton_proto.data.FeatureViewServingStatusSummaryR!featureViewServingStatusSummaries*\xd1\x01\n\x0cServingState\x12\x1d\n\x19SERVING_STATE_UNSPECIFIED\x10\x00\x12\x1a\n\x16SERVING_STATE_DISABLED\x10\x01\x12!\n\x1dSERVING_STATE_NOT_ENOUGH_DATA\x10\x02\x12\x19\n\x15SERVING_STATE_PENDING\x10\x03\x12\x14\n\x10SERVING_STATE_OK\x10\x04\x12\x17\n\x13SERVING_STATE_ERROR\x10\x05\x12\x19\n\x15SERVING_STATE_RUNNING\x10\x06\x42\x13\n\x0f\x63om.tecton.dataP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.data.serving_status_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017com.tecton.dataP\001'
  _SERVINGSTATE._serialized_start=1818
  _SERVINGSTATE._serialized_end=2027
  _SERVINGSTATUS._serialized_start=124
  _SERVINGSTATUS._serialized_end=233
  _STATUSRANGE._serialized_start=236
  _STATUSRANGE._serialized_end=441
  _FEATUREVIEWMATERIALIZATIONRANGES._serialized_start=444
  _FEATUREVIEWMATERIALIZATIONRANGES._serialized_end=641
  _SERVINGSTATUSSUMMARY._serialized_start=644
  _SERVINGSTATUSSUMMARY._serialized_end=1316
  _FEATUREVIEWSERVINGSTATUSSUMMARY._serialized_start=1319
  _FEATUREVIEWSERVINGSTATUSSUMMARY._serialized_end=1518
  _FULLFEATURESERVICESERVINGSUMMARY._serialized_start=1521
  _FULLFEATURESERVICESERVINGSUMMARY._serialized_end=1815
# @@protoc_insertion_point(module_scope)
