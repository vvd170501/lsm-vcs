import click

from .common import require_repo


@click.command()
@click.argument('remote')
@require_repo
def fetch(**kwargs):
    return _fetch(**kwargs)


def _fetch(remote):
    raise NotImplementedError()
