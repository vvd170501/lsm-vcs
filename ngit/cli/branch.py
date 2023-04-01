import click

from ..context import get_context
from ..core.nodes import resolve_named_node
from ..core.refs import get_branch_events, get_head_ref


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


def _create_branch(new_branch_name: str):
    exists = False
    # TODO optimize.
    # - Use reverse order. If the last event wasn't a deletion, then the branch exists
    # - Store last_id for each branch in .ngit to reduce number of traversed nodes
    # - Use a separate subtree for ech branch
    for branch in get_branch_events():
        if branch.name == new_branch_name:
            exists = bool(branch.ref)
    assert not exists, f'Branch "{new_branch_name}" already exists'
    get_context().server.add_node(resolve_named_node('branch'), f'{new_branch_name}/{get_head_ref()}'.encode())


def _list_branches() -> list[str]:
    """Returns sorted list of branch names."""
    branches = set()
    for branch in get_branch_events():
        if branch.ref == '[del]':  # The branch was deleted
            branches.discard(branch.name)
        else:
            branches.add(branch.name)

    return sorted(branches)
