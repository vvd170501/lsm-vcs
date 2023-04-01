import click

from ..core.nodes import create_named_node
from ..core.refs import set_head_ref


@click.command()
def init(**kwargs):
    return _init(**kwargs)


def _init():
    # Branch events: create / update / delete
    create_named_node('', 'branch', exist_ok=True)
    # Commit tree. Each commit contains a reference to its parent and references to related file changes
    create_named_node('', 'commit', exist_ok=True)
    # File changes
    create_named_node('', 'fs', exist_ok=True)
    set_head_ref('')
