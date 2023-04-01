from collections.abc import Iterator
from typing import NamedTuple

import click

from ..backend import NodeId
from ..context import get_context


@click.command()
@click.argument('branch', required=False)
def branch(**kwargs):
    return _branch(**kwargs)


def _branch(branch: str | None):
    if branch is not None:
        assert branch, 'Empty branch name is not allowed'
        _create_branch(branch)
    else:
        branches = _list_branches()
        print('\n'.join(branches))  # mark current branch?


Branch = NamedTuple('Branch', [('name', str), ('ref', NodeId)])


def _get_head_ref() -> NodeId:
    # TODO move to util module
    return get_context().fs.read_file('.ngit/HEAD').decode()


def _resolve_node_id(name: str) -> NodeId:  # name: bytes?
    # TODO move to util module
    import pickle
    # TODO cache node_ids
    node_ids: dict[str, str] = pickle.loads(get_context().fs.read_file('.ngit/node_ids'))
    return node_ids[name]


def _get_branch_nodes() -> Iterator[Branch]:
    # TODO move to some util module
    # This function may be used to resolve branch to a ref (for checkout)
    ctx = get_context()
    for node in ctx.server.get_nodes(_resolve_node_id('branch'), ''):
        name, ref = node.content.decode().split('/')
        yield Branch(name, ref)


def _create_branch(new_branch_name: str):
    exists = False
    # TODO optimize.
    # - Use reverse order. If the last event wasn't a deletion, then the branch exists
    # - Store last_id for each branch in .ngit to reduce number of traversed nodes
    # - Use a separate subtree for ech branch
    for branch in _get_branch_nodes():
        if branch.name == new_branch_name:
            exists = bool(branch.ref)
    assert not exists, f'Branch "{new_branch_name}" already exists'
    get_context().server.add_node(_resolve_node_id('branch'), f'{new_branch_name}/{_get_head_ref()}'.encode())


def _list_branches() -> list[str]:
    """Returns sorted list of branch names."""
    branches = set()
    for branch in _get_branch_nodes():
        if not branch.ref:  # The branch was deleted
            branches.discard(branch.name)
        else:
            branches.add(branch.name)

    return sorted(branches)
