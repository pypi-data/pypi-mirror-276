# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: analysis_computation.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from terrascope_api.models import common_models_pb2 as common__models__pb2
from terrascope_api.models import analysis_pb2 as analysis__pb2
try:
  common__models__pb2 = analysis__pb2.common__models__pb2
except AttributeError:
  common__models__pb2 = analysis__pb2.common_models_pb2

from terrascope_api.models.common_models_pb2 import *
from terrascope_api.models.analysis_pb2 import *

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1a\x61nalysis_computation.proto\x12\x07oi.papi\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x13\x63ommon_models.proto\x1a\x0e\x61nalysis.proto\"i\n AnalysisComputationCreateRequest\x12\x1a\n\x12\x61nalysis_config_id\x18\x01 \x01(\t\x12\x0e\n\x06toi_id\x18\x02 \x01(\t\x12\x19\n\x11\x61oi_collection_id\x18\x03 \x01(\t\"t\n!AnalysisComputationCreateResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12:\n\x14\x61nalysis_computation\x18\x02 \x01(\x0b\x32\x1c.oi.papi.AnalysisComputation\",\n\x1d\x41nalysisComputationRunRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\"5\n\x1e\x41nalysisComputationRunResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\"U\n\x1d\x41nalysisComputationGetRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\x12\'\n\npagination\x18\x02 \x01(\x0b\x32\x13.oi.papi.Pagination\"f\n\x17\x41nalysisComputationNode\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x16\n\x0e\x63omputation_id\x18\x02 \x01(\t\x12\x10\n\x08\x63hildren\x18\x03 \x03(\t\x12\x13\n\x0bhas_results\x18\x04 \x01(\x08\"\xf0\x03\n\x13\x41nalysisComputation\x12\n\n\x02id\x18\x01 \x01(\t\x12\x13\n\x0b\x61nalysis_id\x18\x02 \x01(\t\x12\x0e\n\x06toi_id\x18\x03 \x01(\t\x12\x19\n\x11\x61oi_collection_id\x18\x04 \x01(\t\x12\x1a\n\x12\x61nalysis_config_id\x18\x05 \x01(\t\x12\x30\n\x0csubmitted_on\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\x05state\x18\x07 \x01(\x0e\x32\".oi.papi.AnalysisComputation.State\x12;\n\x11\x63omputation_nodes\x18\x08 \x03(\x0b\x32 .oi.papi.AnalysisComputationNode\x12\x37\n\x08progress\x18\t \x01(\x0b\x32%.oi.papi.AnalysisComputation.Progress\x1a>\n\x08Progress\x12\x0f\n\x07running\x18\x01 \x01(\x01\x12\x11\n\tsucceeded\x18\x02 \x01(\x01\x12\x0e\n\x06\x66\x61iled\x18\x03 \x01(\x01\"V\n\x05State\x12\x11\n\rUNKNOWN_STATE\x10\x00\x12\x0f\n\x0bNOT_STARTED\x10\x01\x12\x0f\n\x0bIN_PROGRESS\x10\x02\x12\n\n\x06PAUSED\x10\x03\x12\x0c\n\x08\x43OMPLETE\x10\x04\"\x9b\x01\n\x1e\x41nalysisComputationGetResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12;\n\x15\x61nalysis_computations\x18\x02 \x03(\x0b\x32\x1c.oi.papi.AnalysisComputation\x12\'\n\npagination\x18\x03 \x01(\x0b\x32\x13.oi.papi.Pagination\"\xb0\x02\n\x1e\x41nalysisComputationListRequest\x12\r\n\x05state\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x34\n\x10min_submitted_on\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x34\n\x10max_submitted_on\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1a\n\x12\x61nalysis_config_id\x18\x05 \x01(\t\x12\x0e\n\x06toi_id\x18\x06 \x01(\t\x12\x19\n\x11\x61oi_collection_id\x18\x07 \x01(\t\x12\x13\n\x0b\x61nalysis_id\x18\x08 \x01(\t\x12\'\n\npagination\x18\t \x01(\x0b\x32\x13.oi.papi.Pagination\"\x9c\x01\n\x1f\x41nalysisComputationListResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12;\n\x15\x61nalysis_computations\x18\x02 \x03(\x0b\x32\x1c.oi.papi.AnalysisComputation\x12\'\n\npagination\x18\x03 \x01(\x0b\x32\x13.oi.papi.Pagination2\x84\x03\n\x16\x41nalysisComputationApi\x12_\n\x06\x63reate\x12).oi.papi.AnalysisComputationCreateRequest\x1a*.oi.papi.AnalysisComputationCreateResponse\x12V\n\x03run\x12&.oi.papi.AnalysisComputationRunRequest\x1a\'.oi.papi.AnalysisComputationRunResponse\x12V\n\x03get\x12&.oi.papi.AnalysisComputationGetRequest\x1a\'.oi.papi.AnalysisComputationGetResponse\x12Y\n\x04list\x12\'.oi.papi.AnalysisComputationListRequest\x1a(.oi.papi.AnalysisComputationListResponseP\x01P\x02\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'analysis_computation_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ANALYSISCOMPUTATIONCREATEREQUEST']._serialized_start=109
  _globals['_ANALYSISCOMPUTATIONCREATEREQUEST']._serialized_end=214
  _globals['_ANALYSISCOMPUTATIONCREATERESPONSE']._serialized_start=216
  _globals['_ANALYSISCOMPUTATIONCREATERESPONSE']._serialized_end=332
  _globals['_ANALYSISCOMPUTATIONRUNREQUEST']._serialized_start=334
  _globals['_ANALYSISCOMPUTATIONRUNREQUEST']._serialized_end=378
  _globals['_ANALYSISCOMPUTATIONRUNRESPONSE']._serialized_start=380
  _globals['_ANALYSISCOMPUTATIONRUNRESPONSE']._serialized_end=433
  _globals['_ANALYSISCOMPUTATIONGETREQUEST']._serialized_start=435
  _globals['_ANALYSISCOMPUTATIONGETREQUEST']._serialized_end=520
  _globals['_ANALYSISCOMPUTATIONNODE']._serialized_start=522
  _globals['_ANALYSISCOMPUTATIONNODE']._serialized_end=624
  _globals['_ANALYSISCOMPUTATION']._serialized_start=627
  _globals['_ANALYSISCOMPUTATION']._serialized_end=1123
  _globals['_ANALYSISCOMPUTATION_PROGRESS']._serialized_start=973
  _globals['_ANALYSISCOMPUTATION_PROGRESS']._serialized_end=1035
  _globals['_ANALYSISCOMPUTATION_STATE']._serialized_start=1037
  _globals['_ANALYSISCOMPUTATION_STATE']._serialized_end=1123
  _globals['_ANALYSISCOMPUTATIONGETRESPONSE']._serialized_start=1126
  _globals['_ANALYSISCOMPUTATIONGETRESPONSE']._serialized_end=1281
  _globals['_ANALYSISCOMPUTATIONLISTREQUEST']._serialized_start=1284
  _globals['_ANALYSISCOMPUTATIONLISTREQUEST']._serialized_end=1588
  _globals['_ANALYSISCOMPUTATIONLISTRESPONSE']._serialized_start=1591
  _globals['_ANALYSISCOMPUTATIONLISTRESPONSE']._serialized_end=1747
  _globals['_ANALYSISCOMPUTATIONAPI']._serialized_start=1750
  _globals['_ANALYSISCOMPUTATIONAPI']._serialized_end=2138
# @@protoc_insertion_point(module_scope)
