# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from terrascope_api.models import aoi_version_pb2 as aoi__version__pb2

GRPC_GENERATED_VERSION = '1.64.0'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in aoi_version_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class AOIVersionApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/oi.papi.AOIVersionApi/create',
                request_serializer=aoi__version__pb2.AOIVersionCreateRequest.SerializeToString,
                response_deserializer=aoi__version__pb2.AOIVersionCreateResponse.FromString,
                _registered_method=True)
        self.get = channel.unary_unary(
                '/oi.papi.AOIVersionApi/get',
                request_serializer=aoi__version__pb2.AOIVersionGetRequest.SerializeToString,
                response_deserializer=aoi__version__pb2.AOIVersionGetResponse.FromString,
                _registered_method=True)
        self.list = channel.unary_unary(
                '/oi.papi.AOIVersionApi/list',
                request_serializer=aoi__version__pb2.AOIVersionListRequest.SerializeToString,
                response_deserializer=aoi__version__pb2.AOIVersionListResponse.FromString,
                _registered_method=True)


class AOIVersionApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """
        Create a new AOIVersion that is tied to the original AOI by reference of the aoi_id.
        After specifying the aoi modifications, the original is copied and modified. Further, AOIVersions are immutable.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """
        Get the actual AOI details specified by the provided version. Additionally, choose which metadata fields should be returned.
        A list of AOICollections that the AOIVersion is a part of is also returned.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """
        List the available AOIVersions, including on the latest versions by default that match the specific filters.
        Additional options include the ability to list out all fields of the AOIVersion by setting the verbose flag to True.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AOIVersionApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=aoi__version__pb2.AOIVersionCreateRequest.FromString,
                    response_serializer=aoi__version__pb2.AOIVersionCreateResponse.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=aoi__version__pb2.AOIVersionGetRequest.FromString,
                    response_serializer=aoi__version__pb2.AOIVersionGetResponse.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=aoi__version__pb2.AOIVersionListRequest.FromString,
                    response_serializer=aoi__version__pb2.AOIVersionListResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'oi.papi.AOIVersionApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('oi.papi.AOIVersionApi', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class AOIVersionApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/oi.papi.AOIVersionApi/create',
            aoi__version__pb2.AOIVersionCreateRequest.SerializeToString,
            aoi__version__pb2.AOIVersionCreateResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/oi.papi.AOIVersionApi/get',
            aoi__version__pb2.AOIVersionGetRequest.SerializeToString,
            aoi__version__pb2.AOIVersionGetResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def list(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/oi.papi.AOIVersionApi/list',
            aoi__version__pb2.AOIVersionListRequest.SerializeToString,
            aoi__version__pb2.AOIVersionListResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
