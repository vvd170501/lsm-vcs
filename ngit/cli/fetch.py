import click


@click.command()
@click.argument('remote')
def fetch(**kwargs):
    return _fetch(**kwargs)


def _fetch(remote):
    raise NotImplementedError()
