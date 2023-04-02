import click

from .common import require_repo


@click.command()
@require_repo
def log(**kwargs):
    return _log(**kwargs)


def _log():
    raise NotImplementedError()
