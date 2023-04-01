from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass

__all__ = ['BaseBackend', 'Node', 'NodeId', 'RemoteId']


RemoteId = str
NodeId = str


@dataclass
class Node:
    id: NodeId
    parent: NodeId
    content: bytes


class BaseBackend(ABC):
    @abstractmethod
    def add_node(self, parent: NodeId, content: bytes) -> NodeId:
        pass

    @abstractmethod
    def get_nodes(self, root: NodeId, last: NodeId) -> Iterator[Node]:  # TODO add reverse order?
        """Returns all nodes in subtree of `root` with ids greater than `last`."""
        pass

    @abstractmethod
    def sync(self, remote: RemoteId):
        pass
