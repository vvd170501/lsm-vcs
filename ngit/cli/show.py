import click

from .common import require_repo


@click.command()
@click.argument('ref')
@require_repo
def show(**kwargs):
    return _show(**kwargs)


def _show(ref):
    raise NotImplementedError()
