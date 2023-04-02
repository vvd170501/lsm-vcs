import click

from .common import require_repo


@click.command()
@click.argument('ref')
@require_repo
def merge(**kwargs):
    return _merge(**kwargs)


def _merge(ref):
    raise NotImplementedError()
