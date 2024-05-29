# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: algorithm_computation_execution.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from terrascope_api.models import common_models_pb2 as common__models__pb2

from terrascope_api.models.common_models_pb2 import *

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%algorithm_computation_execution.proto\x12\x07oi.papi\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x13\x63ommon_models.proto\"\xb4\x05\n\x1d\x41lgorithmComputationExecution\x12\n\n\x02id\x18\x05 \x01(\t\x12\x16\n\x0e\x63omputation_id\x18\x01 \x01(\t\x12,\n\x08start_ts\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12-\n\tfinish_ts\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x17\n\x0fpartial_results\x18\x04 \x01(\x08\x12Z\n\x06status\x18\x06 \x01(\x0e\x32J.oi.papi.AlgorithmComputationExecution.AlgorithmComputationExecutionStatus\x12.\n\ncreated_on\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x33\n\x12validation_details\x18\x08 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tinput_ids\x18\t \x03(\t\"\xa4\x02\n#AlgorithmComputationExecutionStatus\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x07\n\x03NEW\x10\x01\x12\x17\n\x13PERMISSION_CHECKING\x10\x02\x12\x1e\n\x1aPERMISSION_CHECK_SUCCEEDED\x10\x03\x12\x1b\n\x17PERMISSION_CHECK_FAILED\x10\x04\x12\x0e\n\nVALIDATING\x10\x05\x12\x18\n\x14VALIDATION_SUCCEEDED\x10\x06\x12\x15\n\x11VALIDATION_FAILED\x10\x07\x12\x0b\n\x07RUNNING\x10\x08\x12\r\n\tSUCCEEDED\x10\t\x12\n\n\x06\x46\x41ILED\x10\n\x12\x0b\n\x07STOPPED\x10\x0b\x12\r\n\tCANCELLED\x10\x0c\x12\x0c\n\x08RETRYING\x10\r\"_\n\'AlgorithmComputationExecutionGetRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\x12\'\n\npagination\x18\x02 \x01(\x0b\x32\x13.oi.papi.Pagination\"\xba\x01\n(AlgorithmComputationExecutionGetResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12P\n algorithm_computation_executions\x18\x02 \x03(\x0b\x32&.oi.papi.AlgorithmComputationExecution\x12\'\n\npagination\x18\x03 \x01(\x0b\x32\x13.oi.papi.Pagination2\x8e\x01\n AlgorithmComputationExecutionApi\x12j\n\x03get\x12\x30.oi.papi.AlgorithmComputationExecutionGetRequest\x1a\x31.oi.papi.AlgorithmComputationExecutionGetResponseP\x02\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'algorithm_computation_execution_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ALGORITHMCOMPUTATIONEXECUTION']._serialized_start=135
  _globals['_ALGORITHMCOMPUTATIONEXECUTION']._serialized_end=827
  _globals['_ALGORITHMCOMPUTATIONEXECUTION_ALGORITHMCOMPUTATIONEXECUTIONSTATUS']._serialized_start=535
  _globals['_ALGORITHMCOMPUTATIONEXECUTION_ALGORITHMCOMPUTATIONEXECUTIONSTATUS']._serialized_end=827
  _globals['_ALGORITHMCOMPUTATIONEXECUTIONGETREQUEST']._serialized_start=829
  _globals['_ALGORITHMCOMPUTATIONEXECUTIONGETREQUEST']._serialized_end=924
  _globals['_ALGORITHMCOMPUTATIONEXECUTIONGETRESPONSE']._serialized_start=927
  _globals['_ALGORITHMCOMPUTATIONEXECUTIONGETRESPONSE']._serialized_end=1113
  _globals['_ALGORITHMCOMPUTATIONEXECUTIONAPI']._serialized_start=1116
  _globals['_ALGORITHMCOMPUTATIONEXECUTIONAPI']._serialized_end=1258
# @@protoc_insertion_point(module_scope)
