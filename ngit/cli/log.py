import click


@click.command()
def log(**kwargs):
    return _log(**kwargs)


def _log():
    raise NotImplementedError()
