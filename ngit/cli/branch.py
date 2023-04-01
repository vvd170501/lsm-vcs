import click


@click.command()
@click.argument('branch', required=False)
def branch(**kwargs):
    return _branch(**kwargs)


def _branch(branch: str | None):
    if branch is not None:
        assert branch, 'Empty branch name is not allowed'
        _create_branch(branch)
    else:
        branches = _list_branches()
        print('\n'.join(branches))  # mark current branch?


def _create_branch(branch: str):
    raise NotImplementedError()


def _list_branches() -> list[str]:
    """Returns sorted list of branch names."""
    raise NotImplementedError()
