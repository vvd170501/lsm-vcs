import click

from .common import require_repo


@click.command()
@click.option('-m', '--message', required=True)  # interactive editor is not supported
@require_repo
def commit(**kwargs):
    return _commit(**kwargs)


def _commit(message):
    raise NotImplementedError()
