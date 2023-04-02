from functools import wraps

import click

from ..context import get_context


def require_repo(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not get_context().fs.is_ngit_repo:
            raise click.ClickException('Not in a ngit repository')
        return func(*args, **kwargs)

    return wrapper
