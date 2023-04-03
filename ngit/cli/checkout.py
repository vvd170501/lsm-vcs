import click

from ..context import get_context
from ..core.nodes import NodeName, resolve_named_node
from ..core.refs import RefId, get_branch_events, parse_ref, set_head
from .common import require_repo


@click.command()
@click.argument('target')
@require_repo
def checkout(target: str):
    if not target:
        raise click.ClickException('Ref cannot be empty')
    if try_checkout_branch(target):
        click.echo(f'Switched to branch \'{target}\'')
        return

    try:
        ref = parse_ref(target)
    except Exception:
        raise click.ClickException(f'Unknown target: "{target}" is not a branch name or commit id')
    if try_checkout_ref(ref):
        click.echo(f'HEAD is now at {target} (detached)')
        return

    raise click.ClickException(f'Unknown target: "{target}" is not a branch name or commit id')


def try_checkout_branch(target: str) -> bool:
    target_branch = None
    for branch in get_branch_events():
        if branch.name == target:
            target_branch = branch
            # no break, need to get the latest event. TODO use reverse order?
    if target_branch is not None:
        set_head(target_branch.ref, target_branch.name)
        return True
    return False


def try_checkout_ref(ref: RefId) -> bool:
    commit_tree = resolve_named_node(NodeName.COMMIT_TREE)
    for node in get_context().server.get_nodes(commit_tree):
        # TODO use something better. Direct get?
        if node.id == ref:
            set_head(ref, '')
            return True
    return False


# Wrappers for tests
def checkout_branch(branch: str) -> None:
    assert try_checkout_branch(branch), f'Branch {branch} doesn\'t exist'


def checkout_ref(ref: RefId) -> None:
    assert try_checkout_ref(ref), f'Ref {ref} doesn\'t exist'
