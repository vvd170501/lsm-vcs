from abc import ABC, abstractmethod
from dataclasses import dataclass

__all__ = ['BaseBackend']


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
    def get_nodes(self, root: NodeId, last: NodeId) -> list[Node]:
        """Returns all nodes in subtree of `root` with ids greater than `last`."""
        pass

    @abstractmethod
    def sync(self, remote: RemoteId):
        pass
