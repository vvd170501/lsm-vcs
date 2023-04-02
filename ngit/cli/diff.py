import click

from .common import require_repo


@click.command()
@click.argument('ref', default='HEAD')
@require_repo
def diff(**kwargs):
    return _diff(**kwargs)


def _diff(ref='HEAD'):
    if ref != 'HEAD':
        raise NotImplementedError('Only diff with HEAD is supported')
    raise NotImplementedError()
