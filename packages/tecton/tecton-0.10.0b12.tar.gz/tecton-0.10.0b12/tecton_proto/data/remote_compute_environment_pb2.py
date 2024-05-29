# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/data/remote_compute_environment.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from tecton_proto.common import container_image_pb2 as tecton__proto_dot_common_dot_container__image__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n2tecton_proto/data/remote_compute_environment.proto\x12\x11tecton_proto.data\x1a\x1fgoogle/protobuf/timestamp.proto\x1a)tecton_proto/common/container_image.proto\"\xb4\x08\n\x18RemoteComputeEnvironment\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12\x38\n\x04type\x18\x03 \x01(\x0e\x32$.tecton_proto.data.RemoteComputeTypeR\x04type\x12\x42\n\x06status\x18\x04 \x01(\x0e\x32*.tecton_proto.data.RemoteEnvironmentStatusR\x06status\x12\x42\n\nimage_info\x18\x05 \x01(\x0b\x32#.tecton_proto.common.ContainerImageR\timageInfo\x12\x39\n\ncreated_at\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAt\x12\x39\n\nupdated_at\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tupdatedAt\x12 \n\x0b\x64\x65scription\x18\t \x01(\tR\x0b\x64\x65scription\x12%\n\x0epython_version\x18\x0b \x01(\tR\rpythonVersion\x12\"\n\x0crequirements\x18\x0c \x01(\tR\x0crequirements\x12\x33\n\x15resolved_requirements\x18\r \x01(\tR\x14resolvedRequirements\x12,\n\x12s3_wheels_location\x18\x0e \x01(\tR\x10s3WheelsLocation\x12U\n\x10\x66\x65\x61ture_services\x18\x0f \x03(\x0b\x32*.tecton_proto.data.DependentFeatureServiceR\x0f\x66\x65\x61tureServices\x12\x30\n\x13remote_function_uri\x18\x06 \x01(\tH\x00R\x11remoteFunctionUri\x12`\n\x18realtime_job_environment\x18\x11 \x01(\x0b\x32&.tecton_proto.data.RealtimeEnvironmentR\x16realtimeJobEnvironment\x12\x64\n\x1arift_batch_job_environment\x18\x12 \x01(\x0b\x32\'.tecton_proto.data.RiftBatchEnvironmentR\x17riftBatchJobEnvironment\x12_\n\x1asupported_job_environments\x18\x13 \x03(\x0e\x32!.tecton_proto.data.JobEnvironmentR\x18supportedJobEnvironments\x12\x1f\n\x0bsdk_version\x18\x14 \x01(\tR\nsdkVersionB\r\n\x0b\x64\x65stinationJ\x04\x08\n\x10\x0bJ\x04\x08\x10\x10\x11\"N\n\x18\x41WSComputeInstanceGroups\x12\x32\n\x15\x61utoscaling_group_arn\x18\x01 \x01(\tR\x13\x61utoscalingGroupArn\"\xdd\x03\n\x13RealtimeEnvironment\x12G\n tecton_transform_runtime_version\x18\x01 \x01(\tR\x1dtectonTransformRuntimeVersion\x12\x42\n\nimage_info\x18\x02 \x01(\x0b\x32#.tecton_proto.common.ContainerImageR\timageInfo\x12\x30\n\x13remote_function_uri\x18\x03 \x01(\tH\x00R\x11remoteFunctionUri\x12l\n\x1b\x61ws_compute_instance_groups\x18\x06 \x01(\x0b\x32+.tecton_proto.data.AWSComputeInstanceGroupsH\x00R\x18\x61wsComputeInstanceGroups\x12U\n\x10\x66\x65\x61ture_services\x18\x05 \x03(\x0b\x32*.tecton_proto.data.DependentFeatureServiceR\x0f\x66\x65\x61tureServices\x12-\n\x12online_provisioned\x18\x07 \x01(\x08R\x11onlineProvisionedB\r\n\x0b\x64\x65stinationJ\x04\x08\x04\x10\x05\"\xf0\x01\n\x14RiftBatchEnvironment\x12S\n&tecton_materialization_runtime_version\x18\x01 \x01(\tR#tectonMaterializationRuntimeVersion\x12\x42\n\nimage_info\x18\x02 \x01(\x0b\x32#.tecton_proto.common.ContainerImageR\timageInfo\x12?\n\x1c\x63luster_environment_build_id\x18\x03 \x01(\tR\x19\x63lusterEnvironmentBuildId\"\x9c\x01\n\x1bRemoteEnvironmentUploadInfo\x12%\n\x0e\x65nvironment_id\x18\x01 \x01(\tR\renvironmentId\x12G\n\x0es3_upload_info\x18\x02 \x01(\x0b\x32\x1f.tecton_proto.data.S3UploadInfoH\x00R\x0cs3UploadInfoB\r\n\x0bupload_info\"o\n\x15ObjectStoreUploadPart\x12G\n\x0es3_upload_part\x18\x01 \x01(\x0b\x32\x1f.tecton_proto.data.S3UploadPartH\x00R\x0cs3UploadPartB\r\n\x0bupload_part\"o\n\x0cS3UploadInfo\x12\x1b\n\tupload_id\x18\x01 \x01(\tR\x08uploadId\x12\x42\n\x0cupload_parts\x18\x02 \x03(\x0b\x32\x1f.tecton_proto.data.S3UploadPartR\x0buploadParts\"\x8d\x01\n\x0cS3UploadPart\x12(\n\x10parent_upload_id\x18\x01 \x01(\tR\x0eparentUploadId\x12\x1f\n\x0bpart_number\x18\x02 \x01(\x05R\npartNumber\x12\x13\n\x05\x65_tag\x18\x03 \x01(\tR\x04\x65Tag\x12\x1d\n\nupload_url\x18\x04 \x01(\tR\tuploadUrl\"r\n\x17\x44\x65pendentFeatureService\x12%\n\x0eworkspace_name\x18\x01 \x01(\tR\rworkspaceName\x12\x30\n\x14\x66\x65\x61ture_service_name\x18\x02 \x01(\tR\x12\x66\x65\x61tureServiceName\"i\n\x14\x44\x65pendentFeatureView\x12%\n\x0eworkspace_name\x18\x01 \x01(\tR\rworkspaceName\x12*\n\x11\x66\x65\x61ture_view_name\x18\x02 \x01(\tR\x0f\x66\x65\x61tureViewName*\x90\x01\n\x0eJobEnvironment\x12\x1f\n\x1bJOB_ENVIRONMENT_UNSPECIFIED\x10\x00\x12\x1c\n\x18JOB_ENVIRONMENT_REALTIME\x10\x01\x12\x1e\n\x1aJOB_ENVIRONMENT_RIFT_BATCH\x10\x02\x12\x1f\n\x1bJOB_ENVIRONMENT_RIFT_STREAM\x10\x03*\xb2\x01\n\x17RemoteEnvironmentStatus\x12%\n!REMOTE_ENVIRONMENT_STATUS_PENDING\x10\x00\x12#\n\x1fREMOTE_ENVIRONMENT_STATUS_READY\x10\x01\x12#\n\x1fREMOTE_ENVIRONMENT_STATUS_ERROR\x10\x02\x12&\n\"REMOTE_ENVIRONMENT_STATUS_DELETING\x10\x03*\xab\x01\n\x11RemoteComputeType\x12\x1c\n\x18REMOTE_COMPUTE_TYPE_CORE\x10\x00\x12 \n\x1cREMOTE_COMPUTE_TYPE_EXTENDED\x10\x01\x12\x36\n2REMOTE_COMPUTE_TYPE_SNOWPARK_DEPRECATED_DO_NOT_USE\x10\x02\x12\x1e\n\x1aREMOTE_COMPUTE_TYPE_CUSTOM\x10\x03\x42\x13\n\x0f\x63om.tecton.dataP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.data.remote_compute_environment_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017com.tecton.dataP\001'
  _JOBENVIRONMENT._serialized_start=2784
  _JOBENVIRONMENT._serialized_end=2928
  _REMOTEENVIRONMENTSTATUS._serialized_start=2931
  _REMOTEENVIRONMENTSTATUS._serialized_end=3109
  _REMOTECOMPUTETYPE._serialized_start=3112
  _REMOTECOMPUTETYPE._serialized_end=3283
  _REMOTECOMPUTEENVIRONMENT._serialized_start=150
  _REMOTECOMPUTEENVIRONMENT._serialized_end=1226
  _AWSCOMPUTEINSTANCEGROUPS._serialized_start=1228
  _AWSCOMPUTEINSTANCEGROUPS._serialized_end=1306
  _REALTIMEENVIRONMENT._serialized_start=1309
  _REALTIMEENVIRONMENT._serialized_end=1786
  _RIFTBATCHENVIRONMENT._serialized_start=1789
  _RIFTBATCHENVIRONMENT._serialized_end=2029
  _REMOTEENVIRONMENTUPLOADINFO._serialized_start=2032
  _REMOTEENVIRONMENTUPLOADINFO._serialized_end=2188
  _OBJECTSTOREUPLOADPART._serialized_start=2190
  _OBJECTSTOREUPLOADPART._serialized_end=2301
  _S3UPLOADINFO._serialized_start=2303
  _S3UPLOADINFO._serialized_end=2414
  _S3UPLOADPART._serialized_start=2417
  _S3UPLOADPART._serialized_end=2558
  _DEPENDENTFEATURESERVICE._serialized_start=2560
  _DEPENDENTFEATURESERVICE._serialized_end=2674
  _DEPENDENTFEATUREVIEW._serialized_start=2676
  _DEPENDENTFEATUREVIEW._serialized_end=2781
# @@protoc_insertion_point(module_scope)
