import click

from ..context import get_context
from ..core.nodes import NodeName, resolve_named_node
from ..core.refs import RefId, get_branch_events, parse_ref, get_head, set_head
from ..db_img import build_image, write_image, load_db
from ..db import KVDB
from .common import require_repo
from .branch import create_branch


@click.command()
@click.argument('target')
@click.option('-b', 'chout', is_flag=True, help='Create branch.')
@require_repo
def checkout(target: str, chout: bool) -> None:
    if not target:
        raise click.ClickException('Ref cannot be empty')
    if chout:
        create_branch(target)
        head, _ = get_head()
        set_head(head, target)
        # No reset, like in git
        click.echo(f'Created branch \'{target}\'')
        return
    if target == 'HEAD':
        reset()
        return
    if try_checkout_branch(target):
        click.echo(f'Switched to branch \'{target}\'')
        return
    try:
        ref = parse_ref(target)
    except Exception:
        raise click.ClickException(f'Unknown target: "{target}" is not a branch name or commit id')
    if try_checkout_ref(ref):
        click.echo(f'HEAD is now at {target} (detached)')
    else:
        raise click.ClickException(f'Unknown target: "{target}" is not a branch name or commit id')


def get_branch_ref(branch_name: str) -> RefId | None:
    target_branch = None
    for branch in get_branch_events():
        if branch.name == branch_name:
            target_branch = branch.ref
            # no break, need to get the latest event. TODO use reverse order?
    return target_branch


def try_checkout_branch(target: str) -> bool:
    target_ref = get_branch_ref(target)
    if target_ref is not None:
        set_head(target_ref, target)
        reset()
        return True
    return False


def try_checkout_ref(ref: RefId) -> bool:
    commit_tree = resolve_named_node(NodeName.COMMIT_TREE)
    for node in get_context().server.get_nodes(commit_tree):
        # TODO use something better. Direct get?
        if node.id == ref:
            set_head(ref, '')
            reset()
            return True
    return False


def reset() -> None:
    fs = get_context().fs
    db = load_db(fs)
    if db is None:
        db = KVDB()  # TODO check correctness. Move default to load_db?
    write_image(fs, build_image(db, get_head()[0]))


# Wrappers for tests
def checkout_branch(branch: str) -> None:
    assert try_checkout_branch(branch), f'Branch {branch} doesn\'t exist'


def checkout_ref(ref: RefId) -> None:
    assert try_checkout_ref(ref), f'Ref {ref} doesn\'t exist'
