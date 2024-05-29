# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/online_store/feature_value.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-tecton_proto/online_store/feature_value.proto\x12\x19tecton_proto.online_store\x1a\x1fgoogle/protobuf/timestamp.proto\"\xf0\x03\n\x0c\x46\x65\x61tureValue\x12H\n\x0b\x61rray_value\x18\x01 \x01(\x0b\x32%.tecton_proto.online_store.ArrayValueH\x00R\narrayValue\x12%\n\rfloat64_value\x18\x02 \x01(\x01H\x00R\x0c\x66loat64Value\x12%\n\rfloat32_value\x18\x03 \x01(\x02H\x00R\x0c\x66loat32Value\x12!\n\x0bint64_value\x18\x04 \x01(\x03H\x00R\nint64Value\x12\x1f\n\nbool_value\x18\x05 \x01(\x08H\x00R\tboolValue\x12#\n\x0cstring_value\x18\x06 \x01(\tH\x00R\x0bstringValue\x12\x45\n\nnull_value\x18\x07 \x01(\x0b\x32$.tecton_proto.online_store.NullValueH\x00R\tnullValue\x12K\n\x0cstruct_value\x18\x08 \x01(\x0b\x32&.tecton_proto.online_store.StructValueH\x00R\x0bstructValue\x12\x42\n\tmap_value\x18\t \x01(\x0b\x32#.tecton_proto.online_store.MapValueH\x00R\x08mapValueB\x07\n\x05value\"b\n\x10\x46\x65\x61tureValueList\x12N\n\x0e\x66\x65\x61ture_values\x18\x01 \x03(\x0b\x32\'.tecton_proto.online_store.FeatureValueR\rfeatureValues\"k\n\x15\x42\x61tchCompactedDataRow\x12R\n\x0e\x63ompacted_tile\x18\x01 \x01(\x0b\x32+.tecton_proto.online_store.FeatureValueListR\rcompactedTile\"o\n\x17\x42\x61tchCompactedDataRowV2\x12T\n\x0f\x63ompacted_tiles\x18\x01 \x03(\x0b\x32+.tecton_proto.online_store.FeatureValueListR\x0e\x63ompactedTiles\"\xaa\x01\n\rRedisTAFVData\x12\x1f\n\x0b\x61nchor_time\x18\x01 \x01(\x03R\nanchorTime\x12(\n\x10written_by_batch\x18\x02 \x01(\x08R\x0ewrittenByBatch\x12N\n\x0e\x66\x65\x61ture_values\x18\x03 \x03(\x0b\x32\'.tecton_proto.online_store.FeatureValueR\rfeatureValues\"\x0b\n\tNullValue\"\xd1\x03\n\nArrayValue\x12#\n\rstring_values\x18\x01 \x03(\tR\x0cstringValues\x12H\n\x0c\x61rray_values\x18\x02 \x03(\x0b\x32%.tecton_proto.online_store.ArrayValueR\x0b\x61rrayValues\x12K\n\rstruct_values\x18\x03 \x03(\x0b\x32&.tecton_proto.online_store.StructValueR\x0cstructValues\x12\x42\n\nmap_values\x18\x04 \x03(\x0b\x32#.tecton_proto.online_store.MapValueR\tmapValues\x12\x1f\n\x0b\x62ool_values\x18\x05 \x03(\x08R\nboolValues\x12%\n\x0cint64_values\x18\x06 \x03(\x03\x42\x02\x10\x01R\x0bint64Values\x12)\n\x0e\x66loat32_values\x18\x07 \x03(\x02\x42\x02\x10\x01R\rfloat32Values\x12)\n\x0e\x66loat64_values\x18\x08 \x03(\x01\x42\x02\x10\x01R\rfloat64Values\x12%\n\x0cnull_indices\x18\t \x03(\x05\x42\x02\x10\x01R\x0bnullIndices\"N\n\x0bStructValue\x12?\n\x06values\x18\x01 \x03(\x0b\x32\'.tecton_proto.online_store.FeatureValueR\x06values\"\x84\x01\n\x08MapValue\x12\x39\n\x04keys\x18\x01 \x01(\x0b\x32%.tecton_proto.online_store.ArrayValueR\x04keys\x12=\n\x06values\x18\x02 \x01(\x0b\x32%.tecton_proto.online_store.ArrayValueR\x06values\"\xe1\x01\n\x11\x43\x61\x63hedFeatureView\x12N\n\x0e\x66\x65\x61ture_values\x18\x01 \x03(\x0b\x32\'.tecton_proto.online_store.FeatureValueR\rfeatureValues\x12\x41\n\x0e\x65\x66\x66\x65\x63tive_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\reffectiveTime\x12\x39\n\nupdated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tupdatedAtB\x1a\n\x16\x63om.tecton.onlinestoreP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.online_store.feature_value_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\026com.tecton.onlinestoreP\001'
  _ARRAYVALUE.fields_by_name['int64_values']._options = None
  _ARRAYVALUE.fields_by_name['int64_values']._serialized_options = b'\020\001'
  _ARRAYVALUE.fields_by_name['float32_values']._options = None
  _ARRAYVALUE.fields_by_name['float32_values']._serialized_options = b'\020\001'
  _ARRAYVALUE.fields_by_name['float64_values']._options = None
  _ARRAYVALUE.fields_by_name['float64_values']._serialized_options = b'\020\001'
  _ARRAYVALUE.fields_by_name['null_indices']._options = None
  _ARRAYVALUE.fields_by_name['null_indices']._serialized_options = b'\020\001'
  _FEATUREVALUE._serialized_start=110
  _FEATUREVALUE._serialized_end=606
  _FEATUREVALUELIST._serialized_start=608
  _FEATUREVALUELIST._serialized_end=706
  _BATCHCOMPACTEDDATAROW._serialized_start=708
  _BATCHCOMPACTEDDATAROW._serialized_end=815
  _BATCHCOMPACTEDDATAROWV2._serialized_start=817
  _BATCHCOMPACTEDDATAROWV2._serialized_end=928
  _REDISTAFVDATA._serialized_start=931
  _REDISTAFVDATA._serialized_end=1101
  _NULLVALUE._serialized_start=1103
  _NULLVALUE._serialized_end=1114
  _ARRAYVALUE._serialized_start=1117
  _ARRAYVALUE._serialized_end=1582
  _STRUCTVALUE._serialized_start=1584
  _STRUCTVALUE._serialized_end=1662
  _MAPVALUE._serialized_start=1665
  _MAPVALUE._serialized_end=1797
  _CACHEDFEATUREVIEW._serialized_start=1800
  _CACHEDFEATUREVIEW._serialized_end=2025
# @@protoc_insertion_point(module_scope)
