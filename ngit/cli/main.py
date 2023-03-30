import click


from .branch import branch
from .checkout import checkout
from .commit import commit
from .diff import diff
from .fetch import fetch
from .log import log
from .merge import merge
from .show import show


@click.group
def main():
    """Not Git"""
    pass


for cmd in [
    branch,
    checkout,
    commit,
    diff,
    fetch,
    log,
    merge,
    # pull,
    show,
    # remote,
]:
    main.add_command(cmd)
