import click

from ..backend import NodeId
from ..context import get_context
from ..core.nodes import NodeName, resolve_named_node
from ..core.refs import get_branch_events, parse_ref, ref_to_str, set_head
from .common import require_repo


@click.command()
@click.argument('target')
@require_repo
def checkout(**kwargs):
    ref, branch = _checkout(**kwargs)
    if branch:
        click.echo(f'Switched to branch \'{branch}\'')
    else:
        click.echo(f'HEAD is now at {ref_to_str(ref)} (detached)')


def _checkout(target: str) -> tuple[NodeId, str]:
    target_branch = None
    for branch in get_branch_events():
        if branch.name == target:
            target_branch = branch
            # no break, need to get the latest event. TODO use reverse order?
    if target_branch is not None:
        set_head(target_branch.ref, target_branch.name)
        return target_branch.ref, target_branch.name

    try:
        ref = parse_ref(target)
    except Exception:
        raise click.ClickException(f'Unknown target: "{target}" is not a branch name or commit id')

    commit_tree = resolve_named_node(NodeName.COMMIT_TREE)
    for node in get_context().server.get_nodes(commit_tree):
        # TODO use something better. Direct get?
        if node.id == ref:
            set_head(ref)
            return ref, ''

    raise click.ClickException(f'Unknown target: "{target}" is not a branch name or commit id')
