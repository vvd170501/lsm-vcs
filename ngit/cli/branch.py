import click


@click.command()
@click.argument('branch', required=False)
def branch(**kwargs):
    return _branch(**kwargs)


def _branch(branch):
    raise NotImplementedError()
