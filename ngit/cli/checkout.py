import click


@click.command()
@click.argument('ref')
def checkout(**kwargs):
    return _checkout(**kwargs)


def _checkout(ref):
    raise NotImplementedError()
