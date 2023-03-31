# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import lseqdb_pb2 as lseqdb__pb2


class LSeqDatabaseStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetValue = channel.unary_unary(
                '/lseqdb.LSeqDatabase/GetValue',
                request_serializer=lseqdb__pb2.ReplicaKey.SerializeToString,
                response_deserializer=lseqdb__pb2.Value.FromString,
                )
        self.Put = channel.unary_unary(
                '/lseqdb.LSeqDatabase/Put',
                request_serializer=lseqdb__pb2.PutRequest.SerializeToString,
                response_deserializer=lseqdb__pb2.LSeq.FromString,
                )
        self.SeekGet = channel.unary_unary(
                '/lseqdb.LSeqDatabase/SeekGet',
                request_serializer=lseqdb__pb2.SeekGetRequest.SerializeToString,
                response_deserializer=lseqdb__pb2.DBItems.FromString,
                )
        self.GetReplicaEvents = channel.unary_unary(
                '/lseqdb.LSeqDatabase/GetReplicaEvents',
                request_serializer=lseqdb__pb2.EventsRequest.SerializeToString,
                response_deserializer=lseqdb__pb2.DBItems.FromString,
                )
        self.SyncGet_ = channel.unary_unary(
                '/lseqdb.LSeqDatabase/SyncGet_',
                request_serializer=lseqdb__pb2.SyncGetRequest.SerializeToString,
                response_deserializer=lseqdb__pb2.LSeq.FromString,
                )
        self.SyncPut_ = channel.unary_unary(
                '/lseqdb.LSeqDatabase/SyncPut_',
                request_serializer=lseqdb__pb2.DBItems.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class LSeqDatabaseServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetValue(self, request, context):
        """Database API
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Put(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SeekGet(self, request, context):
        """Supports search only within one replica
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetReplicaEvents(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SyncGet_(self, request, context):
        """System calls for synchronization
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SyncPut_(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LSeqDatabaseServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetValue': grpc.unary_unary_rpc_method_handler(
                    servicer.GetValue,
                    request_deserializer=lseqdb__pb2.ReplicaKey.FromString,
                    response_serializer=lseqdb__pb2.Value.SerializeToString,
            ),
            'Put': grpc.unary_unary_rpc_method_handler(
                    servicer.Put,
                    request_deserializer=lseqdb__pb2.PutRequest.FromString,
                    response_serializer=lseqdb__pb2.LSeq.SerializeToString,
            ),
            'SeekGet': grpc.unary_unary_rpc_method_handler(
                    servicer.SeekGet,
                    request_deserializer=lseqdb__pb2.SeekGetRequest.FromString,
                    response_serializer=lseqdb__pb2.DBItems.SerializeToString,
            ),
            'GetReplicaEvents': grpc.unary_unary_rpc_method_handler(
                    servicer.GetReplicaEvents,
                    request_deserializer=lseqdb__pb2.EventsRequest.FromString,
                    response_serializer=lseqdb__pb2.DBItems.SerializeToString,
            ),
            'SyncGet_': grpc.unary_unary_rpc_method_handler(
                    servicer.SyncGet_,
                    request_deserializer=lseqdb__pb2.SyncGetRequest.FromString,
                    response_serializer=lseqdb__pb2.LSeq.SerializeToString,
            ),
            'SyncPut_': grpc.unary_unary_rpc_method_handler(
                    servicer.SyncPut_,
                    request_deserializer=lseqdb__pb2.DBItems.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'lseqdb.LSeqDatabase', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LSeqDatabase(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lseqdb.LSeqDatabase/GetValue',
            lseqdb__pb2.ReplicaKey.SerializeToString,
            lseqdb__pb2.Value.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Put(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lseqdb.LSeqDatabase/Put',
            lseqdb__pb2.PutRequest.SerializeToString,
            lseqdb__pb2.LSeq.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SeekGet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lseqdb.LSeqDatabase/SeekGet',
            lseqdb__pb2.SeekGetRequest.SerializeToString,
            lseqdb__pb2.DBItems.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetReplicaEvents(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lseqdb.LSeqDatabase/GetReplicaEvents',
            lseqdb__pb2.EventsRequest.SerializeToString,
            lseqdb__pb2.DBItems.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SyncGet_(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lseqdb.LSeqDatabase/SyncGet_',
            lseqdb__pb2.SyncGetRequest.SerializeToString,
            lseqdb__pb2.LSeq.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SyncPut_(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lseqdb.LSeqDatabase/SyncPut_',
            lseqdb__pb2.DBItems.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
