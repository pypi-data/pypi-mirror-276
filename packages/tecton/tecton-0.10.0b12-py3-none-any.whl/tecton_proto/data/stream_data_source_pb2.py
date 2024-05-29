# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/data/stream_data_source.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tecton_proto.args import data_source_config_pb2 as tecton__proto_dot_args_dot_data__source__config__pb2
from tecton_proto.args import transformation_pb2 as tecton__proto_dot_args_dot_transformation__pb2
from tecton_proto.args import user_defined_function_pb2 as tecton__proto_dot_args_dot_user__defined__function__pb2
from tecton_proto.common import schema_pb2 as tecton__proto_dot_common_dot_schema__pb2
from tecton_proto.common import spark_schema_pb2 as tecton__proto_dot_common_dot_spark__schema__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*tecton_proto/data/stream_data_source.proto\x12\x11tecton_proto.data\x1a*tecton_proto/args/data_source_config.proto\x1a&tecton_proto/args/transformation.proto\x1a-tecton_proto/args/user_defined_function.proto\x1a tecton_proto/common/schema.proto\x1a&tecton_proto/common/spark_schema.proto\"\\\n\x0fKinesisDSConfig\x12\x1f\n\x0bstream_name\x18\x01 \x01(\tR\nstreamName\x12\x16\n\x06region\x18\x02 \x01(\tR\x06regionJ\x04\x08\x03\x10\x04J\x04\x08\x04\x10\x05J\x04\x08\x05\x10\x06\"\xfd\x02\n\rKafkaDSConfig\x12+\n\x11\x62ootstrap_servers\x18\x01 \x01(\tR\x10\x62ootstrapServers\x12\x16\n\x06topics\x18\x02 \x01(\tR\x06topics\x12\x32\n\x15ssl_keystore_location\x18\x07 \x01(\tR\x13sslKeystoreLocation\x12\x44\n\x1fssl_keystore_password_secret_id\x18\x08 \x01(\tR\x1bsslKeystorePasswordSecretId\x12\x36\n\x17ssl_truststore_location\x18\t \x01(\tR\x15sslTruststoreLocation\x12H\n!ssl_truststore_password_secret_id\x18\n \x01(\tR\x1dsslTruststorePasswordSecretId\x12+\n\x11security_protocol\x18\x0b \x01(\tR\x10securityProtocol\"c\n\x1dSparkStreamDataSourceFunction\x12\x42\n\x08\x66unction\x18\x01 \x01(\x0b\x32&.tecton_proto.args.UserDefinedFunctionR\x08\x66unction\"\xd6\x06\n\x10StreamDataSource\x12T\n\x13kinesis_data_source\x18\x01 \x01(\x0b\x32\".tecton_proto.data.KinesisDSConfigH\x00R\x11kinesisDataSource\x12N\n\x11kafka_data_source\x18\x0b \x01(\x0b\x32 .tecton_proto.data.KafkaDSConfigH\x00R\x0fkafkaDataSource\x12o\n\x1aspark_data_source_function\x18\x0c \x01(\x0b\x32\x30.tecton_proto.data.SparkStreamDataSourceFunctionH\x00R\x17sparkDataSourceFunction\x12J\n\x0bpush_source\x18\r \x01(\x0b\x32\'.tecton_proto.data.PushDataSourceConfigH\x00R\npushSource\x12\x43\n\x0cspark_schema\x18\t \x01(\x0b\x32 .tecton_proto.common.SparkSchemaR\x0bsparkSchema\x12Z\n\x15raw_stream_translator\x18\x03 \x01(\x0b\x32&.tecton_proto.args.UserDefinedFunctionR\x13rawStreamTranslator\x12<\n\x1a\x64\x65\x64uplication_column_names\x18\n \x03(\tR\x18\x64\x65\x64uplicationColumnNames\x12\x1f\n\x0btime_column\x18\x06 \x01(\tR\ntimeColumn\x12\x44\n\rstream_config\x18\x07 \x01(\x0b\x32\x1f.tecton_proto.args.StreamConfigR\x0cstreamConfig\x12\x44\n\x07options\x18\x08 \x03(\x0b\x32*.tecton_proto.data.StreamDataSource.OptionR\x07options\x1a\x30\n\x06Option\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05valueB\x0f\n\rstream_sourceJ\x04\x08\x02\x10\x03J\x04\x08\x04\x10\x05J\x04\x08\x05\x10\x06\"\x9d\x02\n\x14PushDataSourceConfig\x12\x1f\n\x0blog_offline\x18\x01 \x01(\x08R\nlogOffline\x12M\n\x0epost_processor\x18\x02 \x01(\x0b\x32&.tecton_proto.args.UserDefinedFunctionR\rpostProcessor\x12>\n\x0cinput_schema\x18\x03 \x01(\x0b\x32\x1b.tecton_proto.common.SchemaR\x0binputSchema\x12U\n\x13post_processor_mode\x18\x04 \x01(\x0e\x32%.tecton_proto.args.TransformationModeR\x11postProcessorModeB\x13\n\x0f\x63om.tecton.dataP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.data.stream_data_source_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017com.tecton.dataP\001'
  _KINESISDSCONFIG._serialized_start=270
  _KINESISDSCONFIG._serialized_end=362
  _KAFKADSCONFIG._serialized_start=365
  _KAFKADSCONFIG._serialized_end=746
  _SPARKSTREAMDATASOURCEFUNCTION._serialized_start=748
  _SPARKSTREAMDATASOURCEFUNCTION._serialized_end=847
  _STREAMDATASOURCE._serialized_start=850
  _STREAMDATASOURCE._serialized_end=1704
  _STREAMDATASOURCE_OPTION._serialized_start=1621
  _STREAMDATASOURCE_OPTION._serialized_end=1669
  _PUSHDATASOURCECONFIG._serialized_start=1707
  _PUSHDATASOURCECONFIG._serialized_end=1992
# @@protoc_insertion_point(module_scope)
