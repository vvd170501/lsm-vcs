from base64 import b64encode

import click

from ..core.nodes import resolve_named_node
from .common import require_repo


@click.command()
@require_repo
def project_id(**kwargs):
    click.echo(get_project_id(**kwargs))


def get_project_id() -> str:
    proj_id = resolve_named_node('root')
    assert proj_id
    # To avoid special chars (e.g. '#' or any control chars)
    return b64encode(proj_id.encode()).decode()
