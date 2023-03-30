import click


@click.command()
@click.option('-m', '--message', required=True)  # interactive editor is not supported
def commit(**kwargs):
    return _commit(**kwargs)


def _commit(message):
    raise NotImplementedError()
