import click

from .common import require_repo


@click.command()
@click.argument('ref')
@require_repo
def checkout(**kwargs):
    return _checkout(**kwargs)


def _checkout(ref):
    raise NotImplementedError()
