# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/offlinestore/delta/transaction_writer.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from tecton_proto.common import aws_credentials_pb2 as tecton__proto_dot_common_dot_aws__credentials__pb2
from tecton_proto.common import schema_pb2 as tecton__proto_dot_common_dot_schema__pb2
from tecton_proto.offlinestore.delta import metadata_pb2 as tecton__proto_dot_offlinestore_dot_delta_dot_metadata__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n8tecton_proto/offlinestore/delta/transaction_writer.proto\x12\x1ftecton_proto.offlinestore.delta\x1a\x1fgoogle/protobuf/timestamp.proto\x1a)tecton_proto/common/aws_credentials.proto\x1a tecton_proto/common/schema.proto\x1a.tecton_proto/offlinestore/delta/metadata.proto\"\xb4\x03\n\x0eInitializeArgs\x12\x12\n\x04path\x18\x01 \x01(\tR\x04path\x12\x0e\n\x02id\x18\x02 \x01(\tR\x02id\x12\x12\n\x04name\x18\x03 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x04 \x01(\tR\x0b\x64\x65scription\x12\x33\n\x06schema\x18\x05 \x01(\x0b\x32\x1b.tecton_proto.common.SchemaR\x06schema\x12+\n\x11partition_columns\x18\x06 \x03(\tR\x10partitionColumns\x12\x35\n\x17\x64ynamodb_log_table_name\x18\x07 \x01(\tR\x14\x64ynamodbLogTableName\x12\x39\n\x19\x64ynamodb_log_table_region\x18\x08 \x01(\tR\x16\x64ynamodbLogTableRegion\x12t\n\x1a\x63ross_account_role_configs\x18\t \x01(\x0b\x32\x37.tecton_proto.offlinestore.delta.CrossAccountRoleConfigR\x17\x63rossAccountRoleConfigs\"\xc9\x01\n\x07\x41\x64\x64\x46ile\x12\x10\n\x03uri\x18\x01 \x01(\tR\x03uri\x12h\n\x10partition_values\x18\x02 \x03(\x0b\x32=.tecton_proto.offlinestore.delta.AddFile.PartitionValuesEntryR\x0fpartitionValues\x1a\x42\n\x14PartitionValuesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"\xdb\x01\n\nUpdateArgs\x12\x45\n\tadd_files\x18\x02 \x03(\x0b\x32(.tecton_proto.offlinestore.delta.AddFileR\x08\x61\x64\x64\x46iles\x12Y\n\ruser_metadata\x18\x04 \x01(\x0b\x32\x34.tecton_proto.offlinestore.delta.TectonDeltaMetadataR\x0cuserMetadata\x12\x1f\n\x0b\x64\x65lete_uris\x18\x05 \x03(\tR\ndeleteUrisJ\x04\x08\x01\x10\x02J\x04\x08\x03\x10\x04\"\xad\x03\n\x0cUpdateResult\x12+\n\x11\x63ommitted_version\x18\x01 \x01(\x04R\x10\x63ommittedVersion\x12V\n\nerror_type\x18\x02 \x01(\x0e\x32\x37.tecton_proto.offlinestore.delta.UpdateResult.ErrorTypeR\terrorType\x12#\n\rerror_message\x18\x03 \x01(\tR\x0c\x65rrorMessage\"\xf2\x01\n\tErrorType\x12\x15\n\x11\x45RROR_UNSPECIFIED\x10\x00\x12\x11\n\rERROR_UNKNOWN\x10\x01\x12\x1b\n\x17\x43ONCURRENT_APPEND_ERROR\x10\x02\x12 \n\x1c\x43ONCURRENT_DELETE_READ_ERROR\x10\x03\x12\"\n\x1e\x43ONCURRENT_DELETE_DELETE_ERROR\x10\x04\x12\x1a\n\x16METADATA_CHANGED_ERROR\x10\x05\x12 \n\x1c\x43ONCURRENT_TRANSACTION_ERROR\x10\x06\x12\x1a\n\x16PROTOCOL_CHANGED_ERROR\x10\x07\"\xa1\x05\n\nExpression\x12\x35\n\x06\x63olumn\x18\x01 \x01(\x0b\x32\x1b.tecton_proto.common.ColumnH\x00R\x06\x63olumn\x12O\n\x07literal\x18\x02 \x01(\x0b\x32\x33.tecton_proto.offlinestore.delta.Expression.LiteralH\x00R\x07literal\x12L\n\x06\x62inary\x18\x03 \x01(\x0b\x32\x32.tecton_proto.offlinestore.delta.Expression.BinaryH\x00R\x06\x62inary\x1a\x97\x01\n\x07Literal\x12\x12\n\x03str\x18\x01 \x01(\tH\x00R\x03str\x12:\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00R\ttimestamp\x12\x16\n\x05int64\x18\x03 \x01(\x03H\x00R\x05int64\x12\x14\n\x04\x62ool\x18\x04 \x01(\x08H\x00R\x04\x62oolB\x0e\n\x0cliteral_type\x1a\x8f\x02\n\x06\x42inary\x12\x45\n\x02op\x18\x01 \x01(\x0e\x32\x35.tecton_proto.offlinestore.delta.Expression.Binary.OpR\x02op\x12?\n\x04left\x18\x02 \x01(\x0b\x32+.tecton_proto.offlinestore.delta.ExpressionR\x04left\x12\x41\n\x05right\x18\x03 \x01(\x0b\x32+.tecton_proto.offlinestore.delta.ExpressionR\x05right\":\n\x02Op\x12\x12\n\x0eOP_UNSPECIFIED\x10\x00\x12\n\n\x06OP_AND\x10\x01\x12\t\n\x05OP_LT\x10\x02\x12\t\n\x05OP_LE\x10\x03\x42\x11\n\x0f\x65xpression_type\"g\n\x11ReadForUpdateArgs\x12R\n\x0eread_predicate\x18\x01 \x01(\x0b\x32+.tecton_proto.offlinestore.delta.ExpressionR\rreadPredicate\")\n\x13ReadForUpdateResult\x12\x12\n\x04uris\x18\x01 \x03(\tR\x04uris\"\xc8\x01\n\x16\x43rossAccountRoleConfig\x12R\n\x15s3_cross_account_role\x18\x01 \x01(\x0b\x32\x1f.tecton_proto.common.AwsIamRoleR\x12s3CrossAccountRole\x12Z\n\x19\x64ynamo_cross_account_role\x18\x02 \x01(\x0b\x32\x1f.tecton_proto.common.AwsIamRoleR\x16\x64ynamoCrossAccountRoleB9\n\x1d\x63om.tecton.offlinestore.deltaB\x16TransactionWriterProtoP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.offlinestore.delta.transaction_writer_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\035com.tecton.offlinestore.deltaB\026TransactionWriterProtoP\001'
  _ADDFILE_PARTITIONVALUESENTRY._options = None
  _ADDFILE_PARTITIONVALUESENTRY._serialized_options = b'8\001'
  _INITIALIZEARGS._serialized_start=252
  _INITIALIZEARGS._serialized_end=688
  _ADDFILE._serialized_start=691
  _ADDFILE._serialized_end=892
  _ADDFILE_PARTITIONVALUESENTRY._serialized_start=826
  _ADDFILE_PARTITIONVALUESENTRY._serialized_end=892
  _UPDATEARGS._serialized_start=895
  _UPDATEARGS._serialized_end=1114
  _UPDATERESULT._serialized_start=1117
  _UPDATERESULT._serialized_end=1546
  _UPDATERESULT_ERRORTYPE._serialized_start=1304
  _UPDATERESULT_ERRORTYPE._serialized_end=1546
  _EXPRESSION._serialized_start=1549
  _EXPRESSION._serialized_end=2222
  _EXPRESSION_LITERAL._serialized_start=1778
  _EXPRESSION_LITERAL._serialized_end=1929
  _EXPRESSION_BINARY._serialized_start=1932
  _EXPRESSION_BINARY._serialized_end=2203
  _EXPRESSION_BINARY_OP._serialized_start=2145
  _EXPRESSION_BINARY_OP._serialized_end=2203
  _READFORUPDATEARGS._serialized_start=2224
  _READFORUPDATEARGS._serialized_end=2327
  _READFORUPDATERESULT._serialized_start=2329
  _READFORUPDATERESULT._serialized_end=2370
  _CROSSACCOUNTROLECONFIG._serialized_start=2373
  _CROSSACCOUNTROLECONFIG._serialized_end=2573
# @@protoc_insertion_point(module_scope)
