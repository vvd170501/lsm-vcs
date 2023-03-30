import click


@click.command()
@click.argument('ref')
def merge(**kwargs):
    return _merge(**kwargs)


def _merge(ref):
    raise NotImplementedError()
