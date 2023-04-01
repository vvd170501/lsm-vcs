from collections.abc import Iterator

import grpc

from .backend import BaseBackend, Node, NodeId, RemoteId
from .proto.helicopter_pb2 import (
    AddNodeRequest,
    AddNodeResponse,
    GetNodesRequest,
    GetNodesResponse,
)
from .proto.helicopter_pb2_grpc import (
    HelicopterStub
)

__all__ = ['HelicopterBackend']


class HelicopterBackend(BaseBackend):
    def __init__(self, host: str, port: int) -> None:
        self._server_channel = grpc.insecure_channel(f'{host}:{port}')
        self._server_stub = HelicopterStub(self._server_channel)

    def __del__(self):
        self._server_channel.close()

    def add_node(self, parent: NodeId, content: bytes) -> NodeId:
        request = AddNodeRequest(parent=parent, content=content)
        resp: AddNodeResponse = self._server_stub.AddNode(request)
        return resp.node.lseq

    def get_nodes(self, root: NodeId, last: NodeId) -> Iterator[Node]:
        request = GetNodesRequest(root=root, last=last)
        resp: GetNodesResponse = self._server_stub.GetNodes(request)
        return (
            Node(node.lseq, node.parent, node.content)
            for node in resp.nodes
        )

    def sync(self, remote: RemoteId):
        raise NotImplementedError()
