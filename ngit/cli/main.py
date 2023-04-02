import click


from .branch import branch
from .checkout import checkout
from .commit import commit
from .diff import diff
from .fetch import fetch
from .init import init
from .log import log
from .merge import merge
from .project_id import project_id
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
    init,
    log,
    merge,
    project_id,
    # pull,
    show,
    # remote,
]:
    main.add_command(cmd)
