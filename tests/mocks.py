from __future__ import annotations

from collections.abc import Iterator
from os import PathLike
from pathlib import Path
from tempfile import TemporaryDirectory

from ngit.backend import BaseBackend, Node, NodeId, RemoteId
from ngit.fs import BaseFS


class MockFS(BaseFS):
    def __init__(self) -> None:
        self._dir = TemporaryDirectory()
        self._root = Path(self._dir.name)

    def read_file(self, path: str | PathLike) -> bytes | None:
        file = self._root / path
        if not file.exists():
            return None
        assert file.is_file
        return file.read_bytes()

    def write_file(self, path: str | PathLike, content: bytes) -> int:
        file = self._root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        return file.write_bytes(content)

    def iter_dir(self, path: str | PathLike) -> Iterator[Path]:
        return (self._root / path).iterdir()

    def is_dir(self, path: str | PathLike) -> bool:
        return (self._root / path).is_dir()

    @property
    def is_ngit_repo(self) -> bool:
        return True

    @property
    def root(self) -> str | PathLike:
        return self._root

    def __del__(self):
        self._dir.cleanup()


class Tree:
    def __init__(self, id: int, content: bytes = b'') -> None:
        self.id = id
        self.content = content
        self.children: list[Tree] = []

    def add(self, subtree: Tree):
        self.children.append(subtree)


class MockBackend(BaseBackend):
    def __init__(self) -> None:
        self._root = Tree(-1)
        self._nodes: dict[int, Tree] = {
            self._root.id: self._root
        }

    def add_node(self, parent: NodeId, content: bytes) -> NodeId:
        parent_id = self._parse_node_id(parent)
        new_node = Tree(
            len(self._nodes),  # ids start with 1
            content
        )
        self._nodes[parent_id].add(new_node)
        self._nodes[new_node.id] = new_node
        return NodeId(new_node.id)

    def get_nodes(self, root: NodeId, last: NodeId = '') -> Iterator[Node]:
        """Returns all nodes in subtree of `root` with ids greater than `last` (root is always excluded)."""
        root_id = self._parse_node_id(root, must_exist=False)
        last_id = self._parse_node_id(last, must_exist=False)
        if root_id not in self._nodes:
            return
        subtree = self._nodes[root_id]
        yield from self._collect_nodes(subtree, last_id)

    def sync(self, remote: RemoteId):
        raise NotImplementedError()

    def _parse_node_id(self, node: NodeId, must_exist=True) -> int:
        if node:
            node_id = int(node)
        else:
            node_id = -1
        if must_exist:
            assert node_id in self._nodes, f'Unknown node id "{node_id}"'
        return node_id

    def _collect_nodes(self, subtree: Tree, last_id: int) -> Iterator[Node]:
        for child in subtree.children:
            if child.id > last_id:
                yield Node(
                    id=NodeId(child.id),
                    parent=subtree.id,
                    content=child.content
                )
            yield from self._collect_nodes(child, last_id)
