import click

from ..context import get_context
from ..core.refs import Branch, get_head, set_head, update_branch
from .common import require_repo


@click.command()
@click.option('-m', '--message', required=True)  # interactive editor is not supported
@require_repo
def commit(**kwargs):
    _commit(**kwargs)


def _commit(message: str):
    head, current_branch = get_head()
    # TODO save diffs to FS tree, add node ids to commit content.
    # Use some more complex data type (also need to save merges)

    # Currently, empty commits are allowed. Maybe they will be disabled later
    head = get_context().server.add_node(head, message.encode())
    set_head(head)
    if current_branch:
        update_branch(Branch(current_branch, head))
