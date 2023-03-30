import click


@click.command()
@click.argument('ref')
def show(**kwargs):
    return _show(**kwargs)


def _show(ref):
    raise NotImplementedError()
