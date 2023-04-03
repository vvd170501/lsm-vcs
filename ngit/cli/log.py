import click

from ..core.refs import get_head, iterate_history, ref_to_str
from .common import require_repo


@click.command()
@require_repo
def log():
    head, _ = get_head()
    for commit in iterate_history(head):
        # TODO use hash-based commit ids?
        # TODO add info about branches
        click.echo(f'{ref_to_str(commit.id)} {commit.content.decode()}')
