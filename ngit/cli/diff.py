import click


@click.command()
@click.argument('ref', default='HEAD')
def diff(**kwargs):
    return _diff(**kwargs)


def _diff(ref='HEAD'):
    if ref != 'HEAD':
        raise NotImplementedError('Only diff with HEAD is supported')
    raise NotImplementedError()
