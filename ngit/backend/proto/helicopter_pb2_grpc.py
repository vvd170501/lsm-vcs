# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from ngit.backend.proto import helicopter_pb2 as ngit_dot_backend_dot_proto_dot_helicopter__pb2


class HelicopterStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetNodes = channel.unary_unary(
                '/Helicopter/GetNodes',
                request_serializer=ngit_dot_backend_dot_proto_dot_helicopter__pb2.GetNodesRequest.SerializeToString,
                response_deserializer=ngit_dot_backend_dot_proto_dot_helicopter__pb2.GetNodesResponse.FromString,
                )
        self.AddNode = channel.unary_unary(
                '/Helicopter/AddNode',
                request_serializer=ngit_dot_backend_dot_proto_dot_helicopter__pb2.AddNodeRequest.SerializeToString,
                response_deserializer=ngit_dot_backend_dot_proto_dot_helicopter__pb2.AddNodeResponse.FromString,
                )


class HelicopterServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetNodes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddNode(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HelicopterServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetNodes': grpc.unary_unary_rpc_method_handler(
                    servicer.GetNodes,
                    request_deserializer=ngit_dot_backend_dot_proto_dot_helicopter__pb2.GetNodesRequest.FromString,
                    response_serializer=ngit_dot_backend_dot_proto_dot_helicopter__pb2.GetNodesResponse.SerializeToString,
            ),
            'AddNode': grpc.unary_unary_rpc_method_handler(
                    servicer.AddNode,
                    request_deserializer=ngit_dot_backend_dot_proto_dot_helicopter__pb2.AddNodeRequest.FromString,
                    response_serializer=ngit_dot_backend_dot_proto_dot_helicopter__pb2.AddNodeResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Helicopter', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Helicopter(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetNodes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Helicopter/GetNodes',
            ngit_dot_backend_dot_proto_dot_helicopter__pb2.GetNodesRequest.SerializeToString,
            ngit_dot_backend_dot_proto_dot_helicopter__pb2.GetNodesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddNode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Helicopter/AddNode',
            ngit_dot_backend_dot_proto_dot_helicopter__pb2.AddNodeRequest.SerializeToString,
            ngit_dot_backend_dot_proto_dot_helicopter__pb2.AddNodeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
