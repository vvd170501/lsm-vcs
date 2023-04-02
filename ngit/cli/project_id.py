from base64 import b64encode

import click

from ..context import get_context
from ..core.nodes import resolve_named_node


@click.command()
def project_id(**kwargs):
    click.echo(_project_id(**kwargs))


def _project_id() -> str:
    if not get_context().fs.is_ngit_repo:
        raise click.ClickException('Not in a ngit repository')
    proj_id = resolve_named_node('root')
    assert proj_id
    # To avoid special chars (e.g. '#' or any control chars)
    return b64encode(proj_id.encode())
